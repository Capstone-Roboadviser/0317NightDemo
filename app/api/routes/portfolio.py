import math

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.request import PortfolioSimulationRequest, VolatilityHistoryRequest
from app.api.schemas.response import (
    AssetClassResponse,
    AssetUniverseResponse,
    CombinationSelectionResponse,
    FrontierPreviewResponse,
    FrontierPointResponse,
    IndividualAssetResponse,
    PortfolioSimulationResponse,
    RandomPortfolioResponse,
    StockInstrumentResponse,
    StocksBySectorResponse,
    ReturnHistoryResponse,
    ReturnPointResponse,
    VolatilityHistoryResponse,
    VolatilityPointResponse,
)
from app.core.config import DEMO_STOCK_PRICES_PATH, TARGET_VOLATILITY_MAX, TARGET_VOLATILITY_MIN, TARGET_VOLATILITY_STEP
from app.data.stock_repository import StockDataRepository
from app.domain.enums import InvestmentHorizon, RiskProfile, SimulationDataSource
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
def list_stocks(
    data_source: SimulationDataSource = Query(default=SimulationDataSource.MANAGED_UNIVERSE),
) -> StocksBySectorResponse:
    instruments = portfolio_service.list_stocks(data_source)
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
    data_source: SimulationDataSource = Query(default=SimulationDataSource.MANAGED_UNIVERSE),
    target_volatility: float | None = Query(default=None, ge=TARGET_VOLATILITY_MIN, le=TARGET_VOLATILITY_MAX),
) -> FrontierPreviewResponse:
    _validate_target_volatility_step(target_volatility)
    result = _simulate(
        UserProfile(
            risk_profile=risk_profile,
            investment_horizon=investment_horizon,
            target_volatility=target_volatility,
            data_source=data_source,
        )
    )
    return FrontierPreviewResponse(
        portfolio_id=result.portfolio_id,
        data_source=result.data_source.value,
        data_source_label=result.data_source_label,
        target_volatility=round(result.target_volatility, 4),
        frontier_points=[_frontier_point_response(point) for point in result.frontier_points],
        frontier_options=[_frontier_point_response(point, label=label) for label, point in result.frontier_options],
        selected_point_index=result.selected_point_index,
        selected_point=_frontier_point_response(result.frontier_points[result.selected_point_index], label="현재 포트폴리오"),
        random_portfolios=[
            RandomPortfolioResponse(volatility=round(point[0], 4), expected_return=round(point[1], 4), weights={k: round(v, 4) for k, v in point[2].items()})
            for point in result.random_portfolios
        ],
        individual_assets=[
            IndividualAssetResponse(
                code=item.code,
                name=item.name,
                volatility=round(item.volatility, 4),
                expected_return=round(item.expected_return, 4),
            )
            for item in result.individual_assets
        ],
        selected_combination=_combination_response(result.selected_combination),
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
        data_source=result.data_source.value,
        data_source_label=result.data_source_label,
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
        individual_assets=[
            IndividualAssetResponse(
                code=item.code,
                name=item.name,
                volatility=round(item.volatility, 4),
                expected_return=round(item.expected_return, 4),
            )
            for item in result.individual_assets
        ],
        used_fallback=result.used_fallback,
        frontier_vol_min=round(min(p.volatility for p in result.frontier_points), 4) if result.frontier_points else 0.0,
        frontier_vol_max=round(max(p.volatility for p in result.frontier_points), 4) if result.frontier_points else 0.0,
        selected_combination=_combination_response(result.selected_combination),
    )


def _simulate(user_profile: UserProfile) -> PortfolioSimulationResult:
    try:
        return portfolio_service.simulate(user_profile)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def _validate_target_volatility_step(target_volatility: float | None) -> None:
    if target_volatility is None:
        return
    snapped = TARGET_VOLATILITY_MIN + round((target_volatility - TARGET_VOLATILITY_MIN) / TARGET_VOLATILITY_STEP) * TARGET_VOLATILITY_STEP
    if abs(target_volatility - snapped) > 1e-9:
        raise HTTPException(status_code=400, detail="목표 변동성은 4%부터 22%까지 2%p 단위로 입력해야 합니다.")


def _frontier_point_response(point, label: str | None = None) -> FrontierPointResponse:
    return FrontierPointResponse(
        label=label,
        volatility=round(point.volatility, 4),
        expected_return=round(point.expected_return, 4),
        weights={code: round(weight, 4) for code, weight in point.weights.items()},
    )


def _load_history_prices(
    *,
    tickers: list[str],
    data_source: SimulationDataSource,
) -> pd.DataFrame:
    normalized_tickers = sorted({str(ticker).strip().upper() for ticker in tickers if ticker})
    if not normalized_tickers:
        raise HTTPException(status_code=400, detail="비중 정보가 비어 있습니다.")

    if data_source == SimulationDataSource.MANAGED_UNIVERSE:
        if not portfolio_service.managed_universe_service.is_configured():
            raise HTTPException(status_code=400, detail="관리자 유니버스 DB가 설정되지 않았습니다.")
        prices = portfolio_service.managed_universe_service.load_prices_for_active_version_tickers(normalized_tickers)
    elif data_source == SimulationDataSource.STOCK_COMBINATION_DEMO:
        repo = StockDataRepository()
        prices = repo.load_stock_prices(str(DEMO_STOCK_PRICES_PATH))
        prices["ticker"] = prices["ticker"].astype(str).str.upper()
    else:
        raise HTTPException(
            status_code=400,
            detail="종목 히스토리 조회는 관리자 유니버스 또는 데모 종목 유니버스에서만 지원합니다.",
        )

    if prices.empty:
        raise HTTPException(status_code=400, detail="요청한 종목의 가격 데이터가 없습니다.")

    prices = prices.copy()
    prices["ticker"] = prices["ticker"].astype(str).str.upper()
    available_tickers = set(prices["ticker"].unique())
    matched = [ticker for ticker in normalized_tickers if ticker in available_tickers]
    if not matched:
        raise HTTPException(status_code=400, detail="요청한 종목의 가격 데이터가 없습니다.")

    filtered = prices[prices["ticker"].isin(matched)].copy()
    if filtered.empty:
        raise HTTPException(status_code=400, detail="요청한 종목의 가격 데이터가 없습니다.")
    return filtered


def _build_portfolio_return_series(payload: VolatilityHistoryRequest) -> tuple[pd.Series, pd.DatetimeIndex]:
    try:
        tickers = [t.upper() for t in payload.weights.keys()]
        weights_upper = {t.upper(): w for t, w in payload.weights.items()}
        prices = _load_history_prices(tickers=tickers, data_source=payload.data_source)
        pivoted = prices.pivot_table(index="date", columns="ticker", values="adjusted_close", aggfunc="last").sort_index()
        if pivoted.empty:
            raise HTTPException(status_code=400, detail="요청한 종목의 가격 데이터가 없습니다.")

        returns = pivoted.pct_change().dropna(how="all")
        if returns.empty:
            raise HTTPException(status_code=400, detail="요청한 종목으로 유효 수익률 시계열을 만들지 못했습니다.")

        weight_series = pd.Series(weights_upper, dtype=float).reindex(returns.columns).fillna(0.0)
        total = float(weight_series.sum())
        if total <= 0:
            raise HTTPException(status_code=400, detail="포트폴리오 비중 합계가 0보다 커야 합니다.")
        weight_series = weight_series / total

        portfolio_returns = returns.fillna(0.0).dot(weight_series)
        if portfolio_returns.empty:
            raise HTTPException(status_code=400, detail="요청한 종목으로 포트폴리오 수익률을 만들지 못했습니다.")
        return portfolio_returns, pivoted.index
    except HTTPException:
        raise
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/volatility-history", response_model=VolatilityHistoryResponse)
def volatility_history(payload: VolatilityHistoryRequest) -> VolatilityHistoryResponse:
    portfolio_returns, all_dates = _build_portfolio_return_series(payload)
    rolling_vol = portfolio_returns.rolling(window=payload.rolling_window, min_periods=payload.rolling_window).std() * math.sqrt(252)
    rolling_vol = rolling_vol.dropna()

    points = [
        VolatilityPointResponse(date=date.strftime("%Y-%m-%d"), volatility=round(float(vol), 6))
        for date, vol in rolling_vol.items()
        if np.isfinite(vol)
    ]

    return VolatilityHistoryResponse(
        points=points,
        earliest_data_date=all_dates.min().strftime("%Y-%m-%d") if len(all_dates) > 0 else "",
        latest_data_date=all_dates.max().strftime("%Y-%m-%d") if len(all_dates) > 0 else "",
    )


@router.post("/return-history", response_model=ReturnHistoryResponse)
def return_history(payload: VolatilityHistoryRequest) -> ReturnHistoryResponse:
    portfolio_returns, all_dates = _build_portfolio_return_series(payload)
    rolling_ret = portfolio_returns.rolling(window=payload.rolling_window, min_periods=payload.rolling_window).mean() * 252
    rolling_ret = rolling_ret.dropna()

    points = [
        ReturnPointResponse(date=date.strftime("%Y-%m-%d"), expected_return=round(float(ret), 6))
        for date, ret in rolling_ret.items()
        if np.isfinite(ret)
    ]

    return ReturnHistoryResponse(
        points=points,
        earliest_data_date=all_dates.min().strftime("%Y-%m-%d") if len(all_dates) > 0 else "",
        latest_data_date=all_dates.max().strftime("%Y-%m-%d") if len(all_dates) > 0 else "",
    )


def _combination_response(selection) -> CombinationSelectionResponse | None:
    if selection is None:
        return None
    return CombinationSelectionResponse(
        combination_id=selection.combination_id,
        members_by_sector=selection.members_by_sector,
        total_combinations_tested=selection.total_combinations_tested,
        successful_combinations=selection.successful_combinations,
        discard_reasons=selection.discard_reasons,
    )
