from __future__ import annotations

import numpy as np

from app.schemas import (
    AllocationItem,
    ExplanationCard,
    FrontierPoint,
    PortfolioMetrics,
    PortfolioRequest,
    PortfolioResponse,
    ScatterPoint,
)
from app.services.data_service import SampleDataService
from app.services.explainer import PortfolioExplainer
from app.services.optimizer import EfficientFrontierOptimizer
from app.services.risk_model import RiskModel
from app.services.universe import ASSET_UNIVERSE, RISK_PROFILE_TARGETS, TIME_HORIZON_ADJUSTMENT


class AllocationEngine:
    def __init__(self) -> None:
        self.data_service = SampleDataService()
        self.risk_model = RiskModel()
        self.optimizer = EfficientFrontierOptimizer()
        self.explainer = PortfolioExplainer()

    def recommend(self, payload: PortfolioRequest) -> PortfolioResponse:
        target_volatility = payload.target_volatility or self._default_target_volatility(
            payload.risk_profile,
            payload.investment_horizon,
        )

        returns = self.data_service.load_returns()
        self.risk_model.validate_inputs(returns)
        expected_returns = self.risk_model.expected_returns(returns)
        covariance = self.risk_model.covariance_matrix(returns)
        result = self.optimizer.optimize(
            expected_returns=expected_returns,
            covariance=covariance,
            target_volatility=target_volatility,
            risk_profile=payload.risk_profile,
        )

        asset_labels = {asset.code: asset.name for asset in ASSET_UNIVERSE}
        summary = self.explainer.build_summary(
            result.weights,
            result.expected_return,
            result.volatility,
            target_volatility,
            result.used_fallback,
        )
        risk_contributions = self._risk_contributions(result.weights, covariance)
        frontier_options = self._frontier_options(result.frontier)
        selected_point = FrontierPoint(
            label="Current Portfolio",
            volatility=round(result.volatility, 4),
            expected_return=round(result.expected_return, 4),
        )

        return PortfolioResponse(
            disclaimer=(
                "Demo only. This API simulates asset allocation using sample data and "
                "does not predict markets or provide investment advice."
            ),
            summary=summary,
            explanation=ExplanationCard(
                title="Why this portfolio?",
                body=self.explainer.build_why_this_portfolio(result.volatility, result.expected_return),
            ),
            target_volatility=round(target_volatility, 4),
            metrics=PortfolioMetrics(
                expected_return=round(result.expected_return, 4),
                volatility=round(result.volatility, 4),
                sharpe_ratio=round(result.sharpe_ratio, 4),
            ),
            allocations=[
                AllocationItem(
                    asset_code=code,
                    asset_name=asset_labels[code],
                    weight=round(float(weight), 4),
                    risk_contribution=round(float(risk_contributions[code]), 4),
                )
                for code, weight in result.weights.items()
            ],
            frontier=[
                FrontierPoint(
                    label=point.get("label"),
                    volatility=round(float(volatility), 4),
                    expected_return=round(float(expected_return), 4),
                )
                for point in result.frontier
                for volatility, expected_return in [(point["volatility"], point["expected_return"])]
            ],
            frontier_options=frontier_options,
            selected_point=selected_point,
            random_portfolios=[
                ScatterPoint(
                    volatility=round(float(volatility), 4),
                    expected_return=round(float(expected_return), 4),
                )
                for volatility, expected_return in result.random_portfolios
            ],
        )

    def _default_target_volatility(self, risk_profile: str, investment_horizon: str) -> float:
        base = RISK_PROFILE_TARGETS[risk_profile]
        adjusted = base + TIME_HORIZON_ADJUSTMENT[investment_horizon]
        return min(max(adjusted, 0.04), 0.22)

    def _risk_contributions(self, weights, covariance):
        covariance = covariance.reindex(index=weights.index, columns=weights.index)
        weight_vector = weights.values
        portfolio_vol = float(np.sqrt(weight_vector.T @ covariance.values @ weight_vector))
        if portfolio_vol <= 0:
            return weights * 0
        marginal = covariance.values @ weight_vector / portfolio_vol
        contribution = weight_vector * marginal
        contribution = contribution / contribution.sum()
        return {code: value for code, value in zip(weights.index, contribution)}

    def _frontier_options(self, frontier: list[dict]) -> list[FrontierPoint]:
        labels = ["Conservative", "Balanced", "Growth"]
        if not frontier:
            return []
        indices = np.linspace(0, len(frontier) - 1, num=3).round().astype(int)
        unique_indices = []
        for idx in indices:
            if idx not in unique_indices:
                unique_indices.append(int(idx))
        while len(unique_indices) < 3:
            unique_indices.append(unique_indices[-1])
        options = []
        for label, idx in zip(labels, unique_indices):
            point = frontier[idx]
            options.append(
                FrontierPoint(
                    label=label,
                    volatility=round(float(point["volatility"]), 4),
                    expected_return=round(float(point["expected_return"]), 4),
                )
            )
        return options
