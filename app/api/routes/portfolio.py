from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.request import PortfolioSimulationRequest
from app.api.schemas.response import (
    AssetClassResponse,
    AssetUniverseResponse,
    FrontierPreviewResponse,
    FrontierPointResponse,
    PortfolioSimulationResponse,
    RandomPortfolioResponse,
    StockInstrumentResponse,
    StocksBySectorResponse,
)
from app.core.config import DATA_DIR
from app.data.stock_repository import StockDataRepository
from app.domain.enums import InvestmentHorizon, RiskProfile
from app.domain.models import PortfolioSimulationResult, UserProfile
from app.services.portfolio_service import PortfolioSimulationService


router = APIRouter(prefix="/portfolio", tags=["portfolio"])
portfolio_service = PortfolioSimulationService()


@router.get("/assets", response_model=AssetUniverseResponse)
def list_assets() -> AssetUniverseResponse:
    assets = portfolio_service.list_assets()
    return AssetUniverseResponse(
        assets=[
            AssetClassResponse(
                code=asset.code,
                name=asset.name,
                category=asset.category,
                description=asset.description,
                color=asset.color,
                min_weight=asset.min_weight,
                max_weight=asset.max_weight,
            )
            for asset in assets
        ]
    )


@router.get("/stocks", response_model=StocksBySectorResponse)
def list_stocks() -> StocksBySectorResponse:
    stock_repo = StockDataRepository()
    universe_path = DATA_DIR / "demo" / "demo_stock_universe.csv"
    instruments = stock_repo.load_stock_universe(universe_path)
    sectors: dict[str, list[StockInstrumentResponse]] = {}
    for inst in instruments:
        item = StockInstrumentResponse(
            ticker=inst.ticker,
            name=inst.name,
            sector_code=inst.sector_code,
            sector_name=inst.sector_name,
        )
        sectors.setdefault(inst.sector_code, []).append(item)
    return StocksBySectorResponse(sectors=sectors)


@router.get("/frontier", response_model=FrontierPreviewResponse)
def get_frontier(
    risk_profile: RiskProfile = Query(default=RiskProfile.BALANCED),
    investment_horizon: InvestmentHorizon = Query(default=InvestmentHorizon.MEDIUM),
    target_volatility: float | None = Query(default=None, ge=0.03, le=0.25),
) -> FrontierPreviewResponse:
    result = _simulate(UserProfile(risk_profile=risk_profile, investment_horizon=investment_horizon, target_volatility=target_volatility))
    return FrontierPreviewResponse(
        portfolio_id=result.portfolio_id,
        target_volatility=round(result.target_volatility, 4),
        frontier_points=[_frontier_point_response(point) for point in result.frontier_points],
        frontier_options=[_frontier_point_response(point, label=label) for label, point in result.frontier_options],
        selected_point_index=result.selected_point_index,
        selected_point=_frontier_point_response(result.frontier_points[result.selected_point_index], label="현재 포트폴리오"),
        random_portfolios=[
            RandomPortfolioResponse(volatility=round(point[0], 4), expected_return=round(point[1], 4), weights={k: round(v, 4) for k, v in point[2].items()})
            for point in result.random_portfolios
        ],
    )


@router.post("/simulate", response_model=PortfolioSimulationResponse)
def simulate_portfolio(payload: PortfolioSimulationRequest) -> PortfolioSimulationResponse:
    result = _simulate(payload.to_domain())
    selected_point = result.frontier_points[result.selected_point_index]
    return PortfolioSimulationResponse(
        portfolio_id=result.portfolio_id,
        disclaimer=result.disclaimer,
        summary=result.summary,
        explanation_title=result.explanation_title,
        explanation=result.explanation_body,
        target_volatility=round(result.target_volatility, 4),
        expected_return=round(result.metrics.expected_return, 4),
        volatility=round(result.metrics.volatility, 4),
        sharpe_ratio=round(result.metrics.sharpe_ratio, 4),
        weights={code: round(weight, 4) for code, weight in result.weights.items()},
        allocations=[
            {
                "asset_code": item.asset_code,
                "asset_name": item.asset_name,
                "weight": round(item.weight, 4),
                "risk_contribution": round(item.risk_contribution, 4),
            }
            for item in result.allocations
        ],
        frontier_points=[_frontier_point_response(point) for point in result.frontier_points],
        frontier_options=[_frontier_point_response(point, label=label) for label, point in result.frontier_options],
        selected_point_index=result.selected_point_index,
        selected_point=_frontier_point_response(selected_point, label="현재 포트폴리오"),
        random_portfolios=[
            RandomPortfolioResponse(volatility=round(point[0], 4), expected_return=round(point[1], 4), weights={k: round(v, 4) for k, v in point[2].items()})
            for point in result.random_portfolios
        ],
        used_fallback=result.used_fallback,
    )


def _simulate(user_profile: UserProfile) -> PortfolioSimulationResult:
    try:
        return portfolio_service.simulate(user_profile)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def _frontier_point_response(point, label: str | None = None) -> FrontierPointResponse:
    return FrontierPointResponse(
        label=label,
        volatility=round(point.volatility, 4),
        expected_return=round(point.expected_return, 4),
    )
