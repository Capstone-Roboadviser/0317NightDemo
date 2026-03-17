from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.core.config import FALLBACK_WEIGHTS, FRONTIER_POINT_COUNT, MINIMUM_HISTORY_ROWS, RANDOM_PORTFOLIO_COUNT, RISK_FREE_RATE
from app.data.repository import StaticDataRepository
from app.domain.enums import RiskProfile
from app.domain.models import AllocationView, AssetClass, FrontierPoint, PortfolioSimulationResult, UserProfile
from app.engine.constraints import ConstraintEngine
from app.engine.covariance import ShrinkageCovarianceModel
from app.engine.frontier import build_frontier_options, select_frontier_point_index
from app.engine.math import portfolio_metrics_from_weights, risk_contributions
from app.engine.optimizer import EfficientFrontierOptimizer
from app.engine.returns import HistoricalMeanReturnModel
from app.services.explanation_service import ExplanationService
from app.services.mapping_service import ProfileMappingService


@dataclass
class EngineContext:
    assets: list[AssetClass]
    expected_returns: pd.Series
    covariance: pd.DataFrame
    frontier_points: list[FrontierPoint]
    random_portfolios: list[tuple[float, float]]
    used_fallback: bool


class PortfolioSimulationService:
    def __init__(self) -> None:
        self.repository = StaticDataRepository()
        self.mapping_service = ProfileMappingService()
        self.explanation_service = ExplanationService()
        self.return_model = HistoricalMeanReturnModel()
        self.covariance_model = ShrinkageCovarianceModel()
        self.constraint_engine = ConstraintEngine()
        self.optimizer = EfficientFrontierOptimizer()
        self._context: EngineContext | None = None

    def list_assets(self) -> list[AssetClass]:
        return self.repository.load_asset_universe()

    def simulate(self, user_profile: UserProfile) -> PortfolioSimulationResult:
        target_volatility = self.mapping_service.resolve_target_volatility(user_profile)
        portfolio_id = self.mapping_service.build_portfolio_id(user_profile, target_volatility)
        context = self._prepare_context()

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

        return PortfolioSimulationResult(
            portfolio_id=portfolio_id,
            disclaimer=self.explanation_service.disclaimer(),
            summary=summary,
            explanation_title=explanation_title,
            explanation_body=explanation_body,
            target_volatility=target_volatility,
            metrics=metrics,
            weights=selected_point.weights,
            allocations=allocations,
            frontier_points=context.frontier_points,
            frontier_options=build_frontier_options(context.frontier_points),
            selected_point_index=selected_point_index,
            random_portfolios=context.random_portfolios,
            used_fallback=context.used_fallback,
        )

    def _prepare_context(self) -> EngineContext:
        if self._context is not None:
            return self._context

        assets = self.repository.load_asset_universe()
        returns = self.repository.load_sample_returns()
        self._validate_returns(returns)

        expected_returns = self.return_model.calculate(returns)
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

        self._context = EngineContext(
            assets=assets,
            expected_returns=expected_returns.reindex([asset.code for asset in assets]),
            covariance=covariance.reindex(index=[asset.code for asset in assets], columns=[asset.code for asset in assets]),
            frontier_points=sorted(frontier_points, key=lambda point: point.volatility),
            random_portfolios=random_portfolios,
            used_fallback=used_fallback,
        )
        return self._context

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
