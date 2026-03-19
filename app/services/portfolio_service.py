from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.core.config import (
    DEMO_STOCK_PRICES_PATH,
    DEMO_STOCK_UNIVERSE_PATH,
    FALLBACK_WEIGHTS,
    FRONTIER_POINT_COUNT,
    MAX_PORTFOLIO_AVERAGE_CORRELATION,
    MINIMUM_HISTORY_ROWS,
    RANDOM_PORTFOLIO_COUNT,
    RISK_FREE_RATE,
    STOCK_MAX_WEIGHT,
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
    ManagedUniverseReadiness,
    ManagedUniverseSectorReadiness,
    PortfolioSimulationResult,
    StockInstrument,
    UserProfile,
)
from app.engine.constraints import (
    ConstraintEngine,
    average_pairwise_correlation,
    build_average_correlation_constraint,
)
from app.engine.covariance import ShrinkageCovarianceModel
from app.engine.frontier import build_frontier_options, select_frontier_point_index
from app.engine.math import portfolio_metrics_from_weights, risk_contributions
from app.engine.optimizer import EfficientFrontierOptimizer
from app.engine.returns import AssumptionReturnModel, ExpectedReturnModel, HistoricalMeanReturnModel
from app.services.explanation_service import ExplanationService
from app.services.managed_universe_service import ManagedUniverseService
from app.services.mapping_service import ProfileMappingService


@dataclass
class EngineContext:
    assets: list[AssetClass]
    instruments: list[StockInstrument]
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
        self.stock_return_model = HistoricalMeanReturnModel(shrinkage=0.25)
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

    def inspect_managed_universe_readiness(self) -> ManagedUniverseReadiness:
        assets = self.list_assets()
        sector_checks = self._build_sector_checks(assets, [])

        if not self.managed_universe_service.is_configured():
            return ManagedUniverseReadiness(
                ready=False,
                summary="DATABASE_URL이 설정되지 않았습니다.",
                issues=["관리자 유니버스는 Postgres 연결 후에만 사용할 수 있습니다."],
                active_version_name=None,
                instrument_count=0,
                priced_ticker_count=0,
                stock_return_rows=0,
                effective_history_rows=None,
                minimum_history_rows=MINIMUM_HISTORY_ROWS,
                sector_checks=sector_checks,
            )

        active_version = self.managed_universe_service.get_active_version()
        if active_version is None:
            return ManagedUniverseReadiness(
                ready=False,
                summary="활성화된 관리자 유니버스 버전이 없습니다.",
                issues=["/admin 에서 유니버스 버전을 생성하고 active 로 전환해주세요."],
                active_version_name=None,
                instrument_count=0,
                priced_ticker_count=0,
                stock_return_rows=0,
                effective_history_rows=None,
                minimum_history_rows=MINIMUM_HISTORY_ROWS,
                sector_checks=sector_checks,
            )

        instruments = self.managed_universe_service.get_active_instruments()
        sector_checks = self._build_sector_checks(assets, instruments)
        issues: list[str] = []

        if not instruments:
            issues.append("활성 관리자 유니버스에 등록된 종목이 없습니다.")
            return ManagedUniverseReadiness(
                ready=False,
                summary="활성 버전은 있지만 종목이 비어 있습니다.",
                issues=issues,
                active_version_name=active_version.version_name,
                instrument_count=0,
                priced_ticker_count=0,
                stock_return_rows=0,
                effective_history_rows=None,
                minimum_history_rows=MINIMUM_HISTORY_ROWS,
                sector_checks=sector_checks,
            )

        shortages = [
            f"{item.sector_name} 필요 {item.required_count}개 / 현재 {item.actual_count}개"
            for item in sector_checks
            if not item.ready
        ]
        issues.extend(shortages)

        prices = self.managed_universe_service.load_prices_for_instruments(instruments)
        if prices.empty:
            issues.append("가격 데이터가 아직 적재되지 않았습니다. /admin 에서 가격 갱신을 먼저 실행해주세요.")
            return ManagedUniverseReadiness(
                ready=False,
                summary="가격 이력이 없어 시뮬레이션을 시작할 수 없습니다.",
                issues=issues,
                active_version_name=active_version.version_name,
                instrument_count=len(instruments),
                priced_ticker_count=0,
                stock_return_rows=0,
                effective_history_rows=None,
                minimum_history_rows=MINIMUM_HISTORY_ROWS,
                sector_checks=sector_checks,
            )

        priced_ticker_count = int(prices["ticker"].astype(str).str.upper().nunique())
        stock_returns = StockDataRepository().build_stock_returns(prices)
        stock_return_rows = int(len(stock_returns))

        if stock_return_rows == 0:
            issues.append("가격 이력으로부터 유효 수익률을 생성하지 못했습니다.")
            return ManagedUniverseReadiness(
                ready=False,
                summary="가격은 적재됐지만 수익률 시계열이 비어 있습니다.",
                issues=issues,
                active_version_name=active_version.version_name,
                instrument_count=len(instruments),
                priced_ticker_count=priced_ticker_count,
                stock_return_rows=stock_return_rows,
                effective_history_rows=None,
                minimum_history_rows=MINIMUM_HISTORY_ROWS,
                sector_checks=sector_checks,
            )

        try:
            optimized_returns = self._prepare_stock_returns_for_optimization(instruments, prices)
        except (RuntimeError, ValueError) as exc:
            issues.append(str(exc))
            return ManagedUniverseReadiness(
                ready=False,
                summary="가격 적재는 완료됐지만 종목 단위 최적화 입력을 만들지 못했습니다.",
                issues=issues,
                active_version_name=active_version.version_name,
                instrument_count=len(instruments),
                priced_ticker_count=priced_ticker_count,
                stock_return_rows=stock_return_rows,
                effective_history_rows=None,
                minimum_history_rows=MINIMUM_HISTORY_ROWS,
                sector_checks=sector_checks,
            )

        effective_history_rows = int(optimized_returns.count().min()) if not optimized_returns.empty else 0
        return ManagedUniverseReadiness(
            ready=True,
            summary=f"시뮬레이션 준비 완료 · 등록된 종목 {optimized_returns.shape[1]}개로 직접 Efficient Frontier를 계산할 수 있습니다.",
            issues=[],
            active_version_name=active_version.version_name,
            instrument_count=len(instruments),
            priced_ticker_count=int(optimized_returns.shape[1]),
            stock_return_rows=stock_return_rows,
            effective_history_rows=effective_history_rows,
            minimum_history_rows=MINIMUM_HISTORY_ROWS,
            sector_checks=sector_checks,
            selected_combination=self._build_universe_selection(
                combination_id=active_version.version_name,
                instruments=instruments,
            ),
        )

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
        allocations = self._build_sector_allocations(
            stock_weights=selected_point.weights,
            stock_risk_contributions=contribution_map,
            assets=context.assets,
            instruments=context.instruments,
        )
        display_selected_point = self._to_sector_frontier_point(selected_point, context.instruments)

        summary = self.explanation_service.build_summary(
            selected_point=display_selected_point,
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
                else "개별 종목 유니버스 모드"
            )
            summary += f" {mode_label}에서는 등록된 전 종목을 직접 최적화 유니버스로 사용했습니다."
            explanation_body += (
                f" 현재 적용된 유니버스 ID는 '{context.selected_combination.combination_id}'이며, "
                "개별 종목 수익률을 직접 사용해 효율적 투자선을 계산한 뒤, 화면에서는 이를 섹터 기준으로 다시 묶어 보여주고 있습니다."
            )
            selected_average_correlation = self._estimate_selected_average_correlation(
                selected_point.weights,
                context.covariance,
            )
            if selected_average_correlation is not None:
                summary += (
                    f" 또한 평균 종목 상관관계가 약 {selected_average_correlation:.2f} 수준이 되도록 "
                    f"상관관계 상한({MAX_PORTFOLIO_AVERAGE_CORRELATION:.2f}) 제약을 함께 적용했습니다."
                )
                explanation_body += (
                    f" 종목 간 평균 상관관계가 {MAX_PORTFOLIO_AVERAGE_CORRELATION:.2f}를 넘지 않도록 제약을 두어, "
                    "Sharpe Ratio를 추구하면서도 지나치게 비슷하게 움직이는 종목 쏠림을 줄였습니다."
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
            weights=display_selected_point.weights,
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
            managed_context = self._prepare_managed_universe_context(allow_fallback=True)
            if managed_context is not None:
                return managed_context
            return self._prepare_demo_stock_universe_context(
                source=SimulationDataSource.STOCK_COMBINATION_DEMO,
                label="관리자 유니버스 미설정 - 데모 종목 사용",
            )
        if user_profile.data_source == SimulationDataSource.STOCK_COMBINATION_DEMO:
            return self._prepare_demo_stock_universe_context()
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
            instruments=[],
            expected_returns=expected_returns.reindex([asset.code for asset in assets]),
            covariance=covariance.reindex(index=[asset.code for asset in assets], columns=[asset.code for asset in assets]),
            frontier_points=sorted(frontier_points, key=lambda point: point.volatility),
            random_portfolios=random_portfolios,
            used_fallback=used_fallback,
            data_source=SimulationDataSource.ASSET_ASSUMPTIONS,
            data_source_label="자산군 가정값",
        )

    def _prepare_managed_universe_context(self, allow_fallback: bool = False) -> EngineContext | None:
        active_version = self.managed_universe_service.get_active_version()
        if active_version is None:
            return None if allow_fallback else None

        instruments = self.managed_universe_service.get_active_instruments()
        if not instruments:
            raise RuntimeError("활성 관리자 유니버스에 등록된 종목이 없습니다. /admin 에서 종목을 추가한 뒤 다시 시도해주세요.")

        prices = self.managed_universe_service.load_prices_for_instruments(instruments)
        if prices.empty:
            raise RuntimeError(
                "활성 관리자 유니버스의 가격 데이터가 없습니다. /admin 에서 가격 갱신을 먼저 실행해주세요."
            )

        selection = self._build_universe_selection(
            combination_id=active_version.version_name,
            instruments=instruments,
        )
        expected_returns, covariance, frontier_points, random_portfolios = self._build_stock_frontier_context(
            instruments=instruments,
            prices=prices,
        )
        return EngineContext(
            assets=self.list_assets(),
            instruments=instruments,
            expected_returns=expected_returns,
            covariance=covariance,
            frontier_points=frontier_points,
            random_portfolios=random_portfolios,
            used_fallback=False,
            data_source=SimulationDataSource.MANAGED_UNIVERSE,
            data_source_label=f"관리자 종목 유니버스 ({active_version.version_name})",
            selected_combination=selection,
        )

    def _prepare_demo_stock_universe_context(
        self,
        *,
        source: SimulationDataSource = SimulationDataSource.STOCK_COMBINATION_DEMO,
        label: str = "개별 종목 데모 유니버스",
    ) -> EngineContext:
        instruments = self._load_demo_instruments()
        prices = StockDataRepository().load_stock_prices(str(DEMO_STOCK_PRICES_PATH))
        selection = self._build_universe_selection(
            combination_id="demo-stock-universe",
            instruments=instruments,
        )
        expected_returns, covariance, frontier_points, random_portfolios = self._build_stock_frontier_context(
            instruments=instruments,
            prices=prices,
        )
        return EngineContext(
            assets=self.list_assets(),
            instruments=instruments,
            expected_returns=expected_returns,
            covariance=covariance,
            frontier_points=frontier_points,
            random_portfolios=random_portfolios,
            used_fallback=False,
            data_source=source,
            data_source_label=label,
            selected_combination=selection,
        )

    def _load_demo_instruments(self):
        return StockDataRepository().load_stock_universe(str(DEMO_STOCK_UNIVERSE_PATH))

    def _build_stock_frontier_context(
        self,
        *,
        instruments: list[StockInstrument],
        prices: pd.DataFrame,
    ) -> tuple[pd.Series, pd.DataFrame, list[FrontierPoint], list[tuple[float, float, dict[str, float]]]]:
        optimized_returns = self._prepare_stock_returns_for_optimization(instruments, prices)
        instrument_codes = list(optimized_returns.columns)
        correlation = optimized_returns.corr().reindex(index=instrument_codes, columns=instrument_codes)
        correlation = correlation.fillna(0.0).astype(float)
        for code in instrument_codes:
            correlation.loc[code, code] = 1.0
        constraints = self.constraint_engine.build_for_codes(
            instrument_codes,
            upper_bounds=pd.Series(STOCK_MAX_WEIGHT, index=instrument_codes, dtype=float).values,
            extra_constraints=(
                build_average_correlation_constraint(
                    correlation.values,
                    MAX_PORTFOLIO_AVERAGE_CORRELATION,
                ),
            ),
        )
        expected_returns = self._build_stock_expected_returns(optimized_returns)
        covariance = self.covariance_model.calculate(optimized_returns)
        frontier_points = self.optimizer.build_frontier(
            expected_returns=expected_returns.reindex(constraints.asset_codes),
            covariance=covariance.reindex(index=constraints.asset_codes, columns=constraints.asset_codes),
            constraints=constraints,
            point_count=FRONTIER_POINT_COUNT,
        )
        random_portfolios = self.optimizer.sample_random_portfolios(
            expected_returns=expected_returns.reindex(constraints.asset_codes),
            covariance=covariance.reindex(index=constraints.asset_codes, columns=constraints.asset_codes),
            constraints=constraints,
            sample_count=RANDOM_PORTFOLIO_COUNT,
        )
        return (
            expected_returns.reindex(instrument_codes).astype(float),
            covariance.reindex(index=instrument_codes, columns=instrument_codes).astype(float),
            sorted(frontier_points, key=lambda point: point.volatility),
            random_portfolios,
        )

    def _prepare_stock_returns_for_optimization(
        self,
        instruments: list[StockInstrument],
        prices: pd.DataFrame,
    ) -> pd.DataFrame:
        stock_returns = StockDataRepository().build_stock_returns(prices)
        if stock_returns.empty:
            raise RuntimeError("가격 이력으로부터 유효 수익률을 생성하지 못했습니다.")

        instrument_codes = [instrument.ticker.upper() for instrument in instruments]
        stock_returns = stock_returns.reindex(columns=instrument_codes)
        non_empty_returns = stock_returns.dropna(axis=1, how="all")
        if non_empty_returns.empty:
            raise RuntimeError("활성 유니버스 종목의 수익률 시계열을 생성하지 못했습니다.")

        valid_counts = non_empty_returns.count()
        eligible_codes = sorted(valid_counts[valid_counts >= MINIMUM_HISTORY_ROWS].index.tolist())
        if len(eligible_codes) < 2:
            available_text = ", ".join(
                f"{code}({int(valid_counts.get(code, 0))}행)"
                for code in valid_counts.sort_values(ascending=False).index[:8]
            )
            raise RuntimeError(
                "최소 252영업일 이상의 수익률 이력이 있는 종목이 2개 이상 필요합니다. "
                f"현재 유효 후보: {available_text or '없음'}"
            )

        eligible_returns = non_empty_returns[eligible_codes].copy()
        if eligible_returns.isna().all(axis=1).all():
            raise RuntimeError("유효 종목들의 공통 수익률 구간을 만들지 못했습니다.")
        return eligible_returns

    def _build_stock_expected_returns(self, stock_returns: pd.DataFrame) -> pd.Series:
        instrument_codes = list(stock_returns.columns)
        return self.stock_return_model.calculate(
            ExpectedReturnModelInput(
                asset_codes=instrument_codes,
                returns=stock_returns,
            )
        )

    def _build_universe_selection(
        self,
        *,
        combination_id: str,
        instruments: list[StockInstrument],
    ) -> CombinationSelectionView:
        members_by_sector: dict[str, list[str]] = {}
        by_sector: dict[str, list[str]] = {}
        for instrument in instruments:
            by_sector.setdefault(instrument.sector_code, []).append(instrument.ticker)
        for sector_code, tickers in by_sector.items():
            members_by_sector[sector_code] = sorted(set(tickers))
        return CombinationSelectionView(
            combination_id=combination_id,
            members_by_sector=members_by_sector,
            total_combinations_tested=1,
            successful_combinations=1,
            discard_reasons={},
        )

    def _aggregate_sector_weights(
        self,
        stock_weights: dict[str, float],
        instruments: list[StockInstrument],
    ) -> dict[str, float]:
        sector_by_ticker = {instrument.ticker.upper(): instrument.sector_code for instrument in instruments}
        aggregated: dict[str, float] = {}
        for ticker, weight in stock_weights.items():
            sector_code = sector_by_ticker.get(str(ticker).upper())
            if sector_code is None:
                continue
            aggregated[sector_code] = aggregated.get(sector_code, 0.0) + float(weight)
        return aggregated

    def _build_sector_allocations(
        self,
        *,
        stock_weights: dict[str, float],
        stock_risk_contributions: dict[str, float],
        assets: list[AssetClass],
        instruments: list[StockInstrument],
    ) -> list[AllocationView]:
        sector_weights = self._aggregate_sector_weights(stock_weights, instruments)
        sector_risk_contributions = self._aggregate_sector_weights(stock_risk_contributions, instruments)
        asset_by_code = {asset.code: asset for asset in assets}
        allocations: list[AllocationView] = []
        for sector_code, weight in sorted(sector_weights.items(), key=lambda item: item[1], reverse=True):
            asset = asset_by_code.get(sector_code)
            if asset is None:
                continue
            allocations.append(
                AllocationView(
                    asset_code=asset.code,
                    asset_name=asset.name,
                    weight=float(weight),
                    risk_contribution=float(sector_risk_contributions.get(sector_code, 0.0)),
                )
            )
        return allocations

    def _to_sector_frontier_point(
        self,
        point: FrontierPoint,
        instruments: list[StockInstrument],
    ) -> FrontierPoint:
        return FrontierPoint(
            volatility=point.volatility,
            expected_return=point.expected_return,
            weights=self._aggregate_sector_weights(point.weights, instruments),
        )

    def _build_sector_checks(
        self,
        assets: list[AssetClass],
        instruments,
    ) -> list[ManagedUniverseSectorReadiness]:
        counts_by_sector: dict[str, int] = {}
        for instrument in instruments:
            counts_by_sector[instrument.sector_code] = counts_by_sector.get(instrument.sector_code, 0) + 1

        return [
            ManagedUniverseSectorReadiness(
                sector_code=asset.code,
                sector_name=asset.name,
                required_count=0,
                actual_count=int(counts_by_sector.get(asset.code, 0)),
                ready=True,
            )
            for asset in assets
        ]

    def _estimate_selected_average_correlation(
        self,
        stock_weights: dict[str, float],
        covariance: pd.DataFrame,
    ) -> float | None:
        if covariance.empty or len(covariance.index) < 2:
            return None

        variances = pd.Series(covariance.values.diagonal(), index=covariance.index, dtype=float)
        standard_deviations = variances.clip(lower=0.0).pow(0.5)
        denominator = standard_deviations.values[:, None] * standard_deviations.values[None, :]
        if (denominator <= 0).all():
            return None

        correlation = covariance.divide(standard_deviations, axis=0).divide(standard_deviations, axis=1)
        correlation = correlation.replace([float("inf"), float("-inf")], 0.0).fillna(0.0)
        for code in correlation.index:
            correlation.loc[code, code] = 1.0

        ordered_weights = pd.Series(stock_weights, dtype=float).reindex(correlation.index).fillna(0.0).values
        return float(average_pairwise_correlation(ordered_weights, correlation.values))

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
