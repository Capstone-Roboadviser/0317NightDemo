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
            label="현재 포트폴리오",
            volatility=round(result.volatility, 4),
            expected_return=round(result.expected_return, 4),
        )

        return PortfolioResponse(
            disclaimer=(
                "본 결과는 샘플 데이터 기반의 데모용 자산배분 시뮬레이션이며, "
                "시장 예측이나 투자 자문을 제공하지 않습니다."
            ),
            summary=summary,
            explanation=ExplanationCard(
                title="왜 이런 포트폴리오가 나왔을까?",
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
        labels = ["안정형", "균형형", "성장형"]
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
