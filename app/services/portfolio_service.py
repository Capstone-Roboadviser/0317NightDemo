from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.core.config import (
    DEMO_COMBINATION_SAMPLE_COUNT,
    DEMO_COMBINATION_SELECTION_SIZES,
    DEMO_COMBINATION_WEIGHTING,
    DEMO_STOCK_PRICES_PATH,
    DEMO_STOCK_UNIVERSE_PATH,
    FALLBACK_WEIGHTS,
    FRONTIER_POINT_COUNT,
    MINIMUM_HISTORY_ROWS,
    RANDOM_PORTFOLIO_COUNT,
    RISK_FREE_RATE,
)
from app.data.repository import StaticDataRepository
from app.data.stock_repository import StockDataRepository
from app.domain.enums import RiskProfile, SimulationDataSource
from app.domain.models import (
    AllocationView,
    AssetClass,
    CombinationSelectionView,
    ExpectedReturnModelInput,
    FrontierPoint,
    PortfolioSimulationResult,
    UserProfile,
)
from app.engine.constraints import ConstraintEngine
from app.engine.covariance import ShrinkageCovarianceModel
from app.engine.frontier import build_frontier_options, select_frontier_point_index
from app.engine.math import portfolio_metrics_from_weights, risk_contributions
from app.engine.optimizer import EfficientFrontierOptimizer
from app.engine.returns import AssumptionReturnModel, ExpectedReturnModel
from app.services.combination_search_service import CombinationSearchConfig, CombinationSearchService
from app.services.explanation_service import ExplanationService
from app.services.managed_universe_service import ManagedUniverseService
from app.services.mapping_service import ProfileMappingService


@dataclass
class EngineContext:
    assets: list[AssetClass]
    expected_returns: pd.Series
    covariance: pd.DataFrame
    frontier_points: list[FrontierPoint]
    random_portfolios: list[tuple[float, float, dict[str, float]]]
    used_fallback: bool
    data_source: SimulationDataSource
    data_source_label: str
    selected_combination: CombinationSelectionView | None = None


class PortfolioSimulationService:
    def __init__(self, return_model: ExpectedReturnModel | None = None) -> None:
        self.mapping_service = ProfileMappingService()
        self.explanation_service = ExplanationService()
        self.return_model = return_model or AssumptionReturnModel()
        self.combination_service = CombinationSearchService()
        self.managed_universe_service = ManagedUniverseService()
        self.covariance_model = ShrinkageCovarianceModel()
        self.constraint_engine = ConstraintEngine()
        self.optimizer = EfficientFrontierOptimizer()

    def list_assets(self) -> list[AssetClass]:
        return StaticDataRepository().load_asset_universe()

    def list_stocks(self, data_source: SimulationDataSource = SimulationDataSource.MANAGED_UNIVERSE):
        if data_source == SimulationDataSource.MANAGED_UNIVERSE:
            instruments = self.managed_universe_service.get_active_instruments()
            if instruments:
                return instruments
        return self._load_demo_instruments()

    def simulate(self, user_profile: UserProfile) -> PortfolioSimulationResult:
        target_volatility = self.mapping_service.resolve_target_volatility(user_profile)
        portfolio_id = self.mapping_service.build_portfolio_id(user_profile, target_volatility)
        context = self._prepare_context(user_profile)
        if context.selected_combination is not None:
            portfolio_id = f"stocks-{portfolio_id}"

        selected_point_index = select_frontier_point_index(context.frontier_points, target_volatility)
        selected_point = context.frontier_points[selected_point_index]
        metrics = portfolio_metrics_from_weights(
            selected_point.weights,
            context.expected_returns,
            context.covariance,
            RISK_FREE_RATE,
        )
        contribution_map = risk_contributions(selected_point.weights, context.covariance)
        asset_names = {asset.code: asset.name for asset in context.assets}
        allocations = [
            AllocationView(
                asset_code=code,
                asset_name=asset_names[code],
                weight=weight,
                risk_contribution=contribution_map[code],
            )
            for code, weight in selected_point.weights.items()
        ]

        summary = self.explanation_service.build_summary(
            selected_point=selected_point,
            target_volatility=target_volatility,
            assets=context.assets,
            used_fallback=context.used_fallback,
        )
        explanation_title, explanation_body = self.explanation_service.build_explanation(
            selected_point=selected_point,
            target_volatility=target_volatility,
            user_profile=user_profile,
        )
        if context.selected_combination is not None:
            mode_label = (
                "관리자 유니버스 모드"
                if context.data_source == SimulationDataSource.MANAGED_UNIVERSE
                else "개별 종목 조합 모드"
            )
            summary += (
                f" {mode_label}에서는 {context.selected_combination.total_combinations_tested}개 조합 중 "
                f"{context.selected_combination.successful_combinations}개를 평가해 가장 효율적인 조합을 자산군 입력값으로 사용했습니다."
            )
            explanation_body += (
                f" 현재 적용된 조합 ID는 '{context.selected_combination.combination_id}'이며, "
                "섹터별로 선택된 종목 묶음의 수익률 시계열을 집계해 효율적 투자선을 다시 계산했습니다."
            )

        return PortfolioSimulationResult(
            portfolio_id=portfolio_id,
            disclaimer=self.explanation_service.disclaimer(),
            summary=summary,
            explanation_title=explanation_title,
            explanation_body=explanation_body,
            data_source=context.data_source,
            data_source_label=context.data_source_label,
            target_volatility=target_volatility,
            metrics=metrics,
            weights=selected_point.weights,
            allocations=allocations,
            frontier_points=context.frontier_points,
            frontier_options=build_frontier_options(context.frontier_points),
            selected_point_index=selected_point_index,
            random_portfolios=context.random_portfolios,
            used_fallback=context.used_fallback,
            selected_combination=context.selected_combination,
        )

    def _prepare_context(self, user_profile: UserProfile) -> EngineContext:
        if user_profile.data_source == SimulationDataSource.MANAGED_UNIVERSE:
            managed_context = self._prepare_managed_universe_context()
            if managed_context is not None:
                return managed_context
            return self._prepare_stock_combination_context(
                source=SimulationDataSource.STOCK_COMBINATION_DEMO,
                label="관리자 유니버스 미설정 - 데모 조합 사용",
            )
        if user_profile.data_source == SimulationDataSource.STOCK_COMBINATION_DEMO:
            return self._prepare_stock_combination_context()
        return self._prepare_assumption_context()

    def _prepare_assumption_context(self) -> EngineContext:
        repository = StaticDataRepository()
        assets = repository.load_asset_universe()
        market_assumptions = repository.load_market_assumptions()
        returns = repository.load_sample_returns()
        self._validate_returns(returns)

        asset_codes = [asset.code for asset in assets]
        expected_returns = self.return_model.calculate(
            ExpectedReturnModelInput(
                asset_codes=asset_codes,
                annual_returns=market_assumptions.annual_returns,
                returns=returns,
            )
        )
        covariance = self.covariance_model.calculate(returns)
        constraints = self.constraint_engine.build(assets)

        used_fallback = False
        try:
            frontier_points = self.optimizer.build_frontier(
                expected_returns=expected_returns,
                covariance=covariance,
                constraints=constraints,
                point_count=FRONTIER_POINT_COUNT,
            )
            random_portfolios = self.optimizer.sample_random_portfolios(
                expected_returns=expected_returns,
                covariance=covariance,
                constraints=constraints,
                sample_count=RANDOM_PORTFOLIO_COUNT,
            )
        except RuntimeError:
            frontier_points = self._fallback_frontier(expected_returns, covariance)
            random_portfolios = []
            used_fallback = True

        return EngineContext(
            assets=assets,
            expected_returns=expected_returns.reindex([asset.code for asset in assets]),
            covariance=covariance.reindex(index=[asset.code for asset in assets], columns=[asset.code for asset in assets]),
            frontier_points=sorted(frontier_points, key=lambda point: point.volatility),
            random_portfolios=random_portfolios,
            used_fallback=used_fallback,
            data_source=SimulationDataSource.ASSET_ASSUMPTIONS,
            data_source_label="자산군 가정값",
        )

    def _prepare_managed_universe_context(self) -> EngineContext | None:
        instruments = self.managed_universe_service.get_active_instruments()
        if not instruments:
            return None

        prices = self.managed_universe_service.load_prices_for_instruments(instruments)
        if prices.empty:
            return None

        active_version = self.managed_universe_service.get_active_version()
        if active_version is None:
            return None

        engine_data = self.combination_service.build_engine_data_from_market_data(
            instruments=instruments,
            prices=prices,
            config=CombinationSearchConfig(
                selection_sizes=DEMO_COMBINATION_SELECTION_SIZES,
                sample_count=DEMO_COMBINATION_SAMPLE_COUNT,
                per_sector_weighting=DEMO_COMBINATION_WEIGHTING,
            ),
        )
        search_result = engine_data.search_result
        selected_combination = CombinationSelectionView(
            combination_id=search_result.best_evaluation.combination_id,
            members_by_sector=search_result.best_evaluation.members_by_sector,
            total_combinations_tested=search_result.total_combinations_tested,
            successful_combinations=search_result.successful_combinations,
            discard_reasons=search_result.discard_reasons,
        )
        return EngineContext(
            assets=engine_data.assets,
            expected_returns=engine_data.expected_returns,
            covariance=engine_data.covariance,
            frontier_points=engine_data.frontier_points,
            random_portfolios=engine_data.random_portfolios,
            used_fallback=False,
            data_source=SimulationDataSource.MANAGED_UNIVERSE,
            data_source_label=f"관리자 종목 유니버스 ({active_version.version_name})",
            selected_combination=selected_combination,
        )

    def _prepare_stock_combination_context(
        self,
        *,
        source: SimulationDataSource = SimulationDataSource.STOCK_COMBINATION_DEMO,
        label: str = "개별주식 조합 데모",
    ) -> EngineContext:
        engine_data = self.combination_service.build_engine_data(
            stock_universe_path=str(DEMO_STOCK_UNIVERSE_PATH),
            stock_prices_path=str(DEMO_STOCK_PRICES_PATH),
            config=CombinationSearchConfig(
                selection_sizes=DEMO_COMBINATION_SELECTION_SIZES,
                sample_count=DEMO_COMBINATION_SAMPLE_COUNT,
                per_sector_weighting=DEMO_COMBINATION_WEIGHTING,
            ),
        )
        search_result = engine_data.search_result
        selected_combination = CombinationSelectionView(
            combination_id=search_result.best_evaluation.combination_id,
            members_by_sector=search_result.best_evaluation.members_by_sector,
            total_combinations_tested=search_result.total_combinations_tested,
            successful_combinations=search_result.successful_combinations,
            discard_reasons=search_result.discard_reasons,
        )
        return EngineContext(
            assets=engine_data.assets,
            expected_returns=engine_data.expected_returns,
            covariance=engine_data.covariance,
            frontier_points=engine_data.frontier_points,
            random_portfolios=engine_data.random_portfolios,
            used_fallback=False,
            data_source=source,
            data_source_label=label,
            selected_combination=selected_combination,
        )

    def _load_demo_instruments(self):
        return StockDataRepository().load_stock_universe(str(DEMO_STOCK_UNIVERSE_PATH))

    def _fallback_frontier(self, expected_returns: pd.Series, covariance: pd.DataFrame) -> list[FrontierPoint]:
        fallback_points: list[FrontierPoint] = []
        for profile in (RiskProfile.CONSERVATIVE, RiskProfile.BALANCED, RiskProfile.GROWTH):
            weights = FALLBACK_WEIGHTS[profile]
            metrics = portfolio_metrics_from_weights(weights, expected_returns, covariance, RISK_FREE_RATE)
            fallback_points.append(
                FrontierPoint(
                    volatility=metrics.volatility,
                    expected_return=metrics.expected_return,
                    weights=weights,
                )
            )
        return fallback_points

    def _validate_returns(self, returns: pd.DataFrame) -> None:
        if returns.isna().any().any():
            raise RuntimeError("샘플 수익률 데이터에 결측치가 포함되어 있습니다.")
        if returns.shape[0] < MINIMUM_HISTORY_ROWS:
            raise RuntimeError("최소 1년 이상의 샘플 데이터가 필요합니다.")
