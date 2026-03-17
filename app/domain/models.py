from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from app.domain.enums import InvestmentHorizon, PriceRefreshMode, RiskProfile, SimulationDataSource


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
    data_source: SimulationDataSource = SimulationDataSource.MANAGED_UNIVERSE


@dataclass(frozen=True)
class MarketAssumptions:
    seed: int
    years: int
    annual_returns: dict[str, float]
    annual_volatilities: dict[str, float]
    correlations: dict[str, dict[str, float]]


@dataclass(frozen=True)
class ExpectedReturnModelInput:
    asset_codes: list[str]
    returns: pd.DataFrame | None = None
    annual_returns: dict[str, float] | None = None


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
class StockInstrument:
    ticker: str
    name: str
    sector_code: str
    sector_name: str
    market: str
    currency: str
    base_weight: float | None = None


@dataclass(frozen=True)
class ManagedUniverseVersion:
    version_id: int
    version_name: str
    source_type: str
    notes: str | None
    is_active: bool
    created_at: str
    instrument_count: int


@dataclass(frozen=True)
class ManagedPriceStats:
    total_rows: int
    ticker_count: int
    min_date: str | None
    max_date: str | None


@dataclass(frozen=True)
class ManagedPriceRefreshJob:
    job_id: int
    version_id: int
    version_name: str
    refresh_mode: PriceRefreshMode
    status: str
    ticker_count: int
    success_count: int
    failure_count: int
    message: str | None
    created_at: str
    started_at: str | None
    finished_at: str | None


@dataclass(frozen=True)
class ManagedPriceRefreshJobItem:
    job_id: int
    ticker: str
    status: str
    rows_upserted: int
    error_message: str | None
    started_at: str | None
    finished_at: str | None


@dataclass(frozen=True)
class ManagedPriceRefreshResult:
    job: ManagedPriceRefreshJob
    price_stats: ManagedPriceStats


@dataclass(frozen=True)
class ManagedUniverseSectorReadiness:
    sector_code: str
    sector_name: str
    required_count: int
    actual_count: int
    ready: bool


@dataclass(frozen=True)
class CombinationEvaluation:
    combination_id: str
    members_by_sector: dict[str, list[str]]
    sector_returns_shape: tuple[int, int]
    best_point: FrontierPoint
    metrics: PortfolioMetrics


@dataclass(frozen=True)
class CombinationSearchResult:
    total_combinations_tested: int
    successful_combinations: int
    discard_reasons: dict[str, int]
    best_evaluation: CombinationEvaluation
    top_evaluations: list[CombinationEvaluation]


@dataclass(frozen=True)
class CombinationSelectionView:
    combination_id: str
    members_by_sector: dict[str, list[str]]
    total_combinations_tested: int
    successful_combinations: int
    discard_reasons: dict[str, int]


@dataclass(frozen=True)
class ManagedUniverseReadiness:
    ready: bool
    summary: str
    issues: list[str]
    active_version_name: str | None
    instrument_count: int
    priced_ticker_count: int
    stock_return_rows: int
    effective_history_rows: int | None
    minimum_history_rows: int
    sector_checks: list[ManagedUniverseSectorReadiness]
    selected_combination: CombinationSelectionView | None = None


@dataclass(frozen=True)
class PortfolioSimulationResult:
    portfolio_id: str
    disclaimer: str
    summary: str
    explanation_title: str
    explanation_body: str
    data_source: SimulationDataSource
    data_source_label: str
    target_volatility: float
    metrics: PortfolioMetrics
    weights: dict[str, float]
    allocations: list[AllocationView]
    frontier_points: list[FrontierPoint]
    frontier_options: list[tuple[str, FrontierPoint]]
    selected_point_index: int
    random_portfolios: list[tuple[float, float, dict[str, float]]]
    used_fallback: bool
    selected_combination: CombinationSelectionView | None = None
