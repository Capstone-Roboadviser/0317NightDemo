from __future__ import annotations

from dataclasses import dataclass

from app.domain.enums import InvestmentHorizon, RiskProfile


@dataclass(frozen=True)
class AssetClass:
    code: str
    name: str
    category: str
    description: str
    color: str
    min_weight: float
    max_weight: float


@dataclass(frozen=True)
class UserProfile:
    risk_profile: RiskProfile
    investment_horizon: InvestmentHorizon
    target_volatility: float | None = None


@dataclass(frozen=True)
class MarketAssumptions:
    seed: int
    years: int
    annual_returns: dict[str, float]
    annual_volatilities: dict[str, float]
    correlations: dict[str, dict[str, float]]


@dataclass(frozen=True)
class PortfolioMetrics:
    expected_return: float
    volatility: float
    sharpe_ratio: float


@dataclass(frozen=True)
class FrontierPoint:
    volatility: float
    expected_return: float
    weights: dict[str, float]


@dataclass(frozen=True)
class AllocationView:
    asset_code: str
    asset_name: str
    weight: float
    risk_contribution: float


@dataclass(frozen=True)
class PortfolioSimulationResult:
    portfolio_id: str
    disclaimer: str
    summary: str
    explanation_title: str
    explanation_body: str
    target_volatility: float
    metrics: PortfolioMetrics
    weights: dict[str, float]
    allocations: list[AllocationView]
    frontier_points: list[FrontierPoint]
    frontier_options: list[tuple[str, FrontierPoint]]
    selected_point_index: int
    random_portfolios: list[tuple[float, float]]
    used_fallback: bool
