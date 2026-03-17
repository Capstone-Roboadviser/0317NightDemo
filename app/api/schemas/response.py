from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class AssetClassResponse(BaseModel):
    code: str
    name: str
    category: str
    description: str
    color: str
    min_weight: float
    max_weight: float


class AssetUniverseResponse(BaseModel):
    assets: list[AssetClassResponse]


class FrontierPointResponse(BaseModel):
    label: str | None = None
    volatility: float
    expected_return: float
    weights: dict[str, float] | None = None


class RandomPortfolioResponse(BaseModel):
    volatility: float
    expected_return: float
    weights: dict[str, float] = {}


class AllocationResponse(BaseModel):
    asset_code: str
    asset_name: str
    weight: float
    risk_contribution: float


class StockInstrumentResponse(BaseModel):
    ticker: str
    name: str
    sector_code: str
    sector_name: str


class StocksBySectorResponse(BaseModel):
    sectors: dict[str, list[StockInstrumentResponse]]


class CombinationSelectionResponse(BaseModel):
    combination_id: str
    members_by_sector: dict[str, list[str]]
    total_combinations_tested: int
    successful_combinations: int
    discard_reasons: dict[str, int]


class FrontierPreviewResponse(BaseModel):
    portfolio_id: str
    data_source: str
    data_source_label: str
    target_volatility: float
    frontier_points: list[FrontierPointResponse]
    frontier_options: list[FrontierPointResponse]
    selected_point_index: int
    selected_point: FrontierPointResponse
    random_portfolios: list[RandomPortfolioResponse]
    selected_combination: CombinationSelectionResponse | None = None


class PortfolioSimulationResponse(BaseModel):
    portfolio_id: str
    disclaimer: str
    summary: str
    explanation_title: str
    explanation: str
    data_source: str
    data_source_label: str
    target_volatility: float
    expected_return: float
    volatility: float
    sharpe_ratio: float
    weights: dict[str, float]
    allocations: list[AllocationResponse]
    frontier_points: list[FrontierPointResponse]
    frontier_options: list[FrontierPointResponse]
    selected_point_index: int
    selected_point: FrontierPointResponse
    random_portfolios: list[RandomPortfolioResponse]
    used_fallback: bool
    frontier_vol_min: float = 0.0
    frontier_vol_max: float = 0.0
    selected_combination: CombinationSelectionResponse | None = None
