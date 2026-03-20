from fastapi import APIRouter, HTTPException

from app.api.schemas.request import (
    ManagedUniverseVersionCreateRequest,
    ManagedUniverseVersionUpdateRequest,
    PriceRefreshRequest,
)
from app.api.schemas.response import (
    CombinationSelectionResponse,
    ManagedUniverseItemResponse,
    ManagedPriceRefreshJobResponse,
    ManagedPriceRefreshJobItemResponse,
    ManagedPriceRefreshResponse,
    ManagedUniverseReadinessResponse,
    ManagedUniverseSectorReadinessResponse,
    ManagedPriceStatsResponse,
    ManagedUniverseStatusResponse,
    ManagedUniverseVersionDetailResponse,
    ManagedUniverseVersionResponse,
    TickerLookupResponse,
    TickerSearchResponse,
    TickerSearchResultResponse,
)
from app.domain.models import (
    ManagedPriceRefreshJob,
    ManagedPriceRefreshResult,
    ManagedPriceStats,
    ManagedUniverseVersion,
)
from app.services.managed_universe_service import ManagedUniverseService
from app.services.portfolio_service import PortfolioSimulationService
from app.services.price_refresh_service import PriceRefreshService
from app.services.ticker_discovery_service import TickerDiscoveryService


router = APIRouter(prefix="/admin", tags=["admin"])
managed_universe_service = ManagedUniverseService()
price_refresh_service = PriceRefreshService(managed_universe_service)
ticker_discovery_service = TickerDiscoveryService()
portfolio_simulation_service = PortfolioSimulationService()


@router.get("/universe/status", response_model=ManagedUniverseStatusResponse)
def get_managed_universe_status() -> ManagedUniverseStatusResponse:
    try:
        active_version = managed_universe_service.get_active_version() if managed_universe_service.is_configured() else None
        instruments = managed_universe_service.get_active_instruments() if active_version is not None else []
        price_stats = (
            ManagedPriceStatsResponse(**managed_universe_service.get_price_stats_for_instruments(instruments))
            if instruments
            else None
        )
        latest_refresh_job = price_refresh_service.get_latest_job(active_version.version_id) if active_version is not None else None
        return ManagedUniverseStatusResponse(
            database_configured=managed_universe_service.is_configured(),
            active_version=None if active_version is None else _version_response(active_version),
            price_stats=price_stats,
            latest_refresh_job=None if latest_refresh_job is None else _price_refresh_job_response(latest_refresh_job),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/universe/versions", response_model=list[ManagedUniverseVersionResponse])
def list_managed_universe_versions() -> list[ManagedUniverseVersionResponse]:
    try:
        return [_version_response(item) for item in managed_universe_service.list_versions()]
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/universe/versions/active", response_model=ManagedUniverseVersionResponse)
def get_active_universe_version() -> ManagedUniverseVersionResponse:
    try:
        active = managed_universe_service.get_active_version()
        if active is None:
            raise HTTPException(status_code=404, detail="활성화된 관리자 유니버스 버전이 없습니다.")
        return _version_response(active)
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/universe/versions/{version_id}", response_model=ManagedUniverseVersionDetailResponse)
def get_universe_version_detail(version_id: int) -> ManagedUniverseVersionDetailResponse:
    try:
        version = managed_universe_service.get_version(version_id)
        if version is None:
            raise HTTPException(status_code=404, detail=f"유니버스 버전 {version_id}를 찾을 수 없습니다.")
        instruments = managed_universe_service.get_version_instruments(version_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _version_detail_response(version, instruments)


@router.post("/universe/versions", response_model=ManagedUniverseVersionResponse)
def create_universe_version(payload: ManagedUniverseVersionCreateRequest) -> ManagedUniverseVersionResponse:
    try:
        version = managed_universe_service.create_version(
            version_name=payload.version_name,
            notes=payload.notes,
            activate=payload.activate,
            instruments=payload.to_domain_instruments(),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _version_response(version)


@router.put("/universe/versions/{version_id}", response_model=ManagedUniverseVersionResponse)
def update_universe_version(version_id: int, payload: ManagedUniverseVersionUpdateRequest) -> ManagedUniverseVersionResponse:
    try:
        version = managed_universe_service.update_version(
            version_id=version_id,
            version_name=payload.version_name,
            notes=payload.notes,
            activate=payload.activate,
            instruments=payload.to_domain_instruments(),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _version_response(version)


@router.delete("/universe/versions/{version_id}")
def delete_universe_version(version_id: int) -> dict[str, object]:
    try:
        version = managed_universe_service.get_version(version_id)
        if version is None:
            raise HTTPException(status_code=404, detail=f"유니버스 버전 {version_id}를 찾을 수 없습니다.")
        managed_universe_service.delete_version(version_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "deleted": True,
        "version_id": version_id,
        "version_name": version.version_name,
    }


@router.post("/universe/versions/{version_id}/activate", response_model=ManagedUniverseVersionResponse)
def activate_universe_version(version_id: int) -> ManagedUniverseVersionResponse:
    try:
        version = managed_universe_service.activate_version(version_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _version_response(version)


@router.post("/prices/refresh", response_model=ManagedPriceRefreshResponse)
def refresh_prices(payload: PriceRefreshRequest) -> ManagedPriceRefreshResponse:
    try:
        result = price_refresh_service.refresh_prices(
            version_id=payload.version_id,
            refresh_mode=payload.refresh_mode,
            full_lookback_years=payload.full_lookback_years,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _price_refresh_response(result)


@router.get("/prices/status", response_model=ManagedUniverseStatusResponse)
def get_price_refresh_status() -> ManagedUniverseStatusResponse:
    return get_managed_universe_status()


@router.get("/universe/readiness", response_model=ManagedUniverseReadinessResponse)
def get_managed_universe_readiness() -> ManagedUniverseReadinessResponse:
    try:
        readiness = portfolio_simulation_service.inspect_managed_universe_readiness()
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ManagedUniverseReadinessResponse(
        ready=readiness.ready,
        summary=readiness.summary,
        issues=readiness.issues,
        active_version_name=readiness.active_version_name,
        instrument_count=readiness.instrument_count,
        priced_ticker_count=readiness.priced_ticker_count,
        stock_return_rows=readiness.stock_return_rows,
        effective_history_rows=readiness.effective_history_rows,
        minimum_history_rows=readiness.minimum_history_rows,
        sector_checks=[
            ManagedUniverseSectorReadinessResponse(
                sector_code=item.sector_code,
                sector_name=item.sector_name,
                required_count=item.required_count,
                actual_count=item.actual_count,
                ready=item.ready,
            )
            for item in readiness.sector_checks
        ],
        selected_combination=None
        if readiness.selected_combination is None
        else CombinationSelectionResponse(
            combination_id=readiness.selected_combination.combination_id,
            members_by_sector=readiness.selected_combination.members_by_sector,
            total_combinations_tested=readiness.selected_combination.total_combinations_tested,
            successful_combinations=readiness.selected_combination.successful_combinations,
            discard_reasons=readiness.selected_combination.discard_reasons,
        ),
    )


@router.get("/prices/jobs/{job_id}/items", response_model=list[ManagedPriceRefreshJobItemResponse])
def get_price_refresh_job_items(job_id: int, failed_only: bool = False, limit: int = 100) -> list[ManagedPriceRefreshJobItemResponse]:
    try:
        items = managed_universe_service.repository.get_refresh_job_items(
            job_id,
            failed_only=failed_only,
            limit=limit,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return [
        ManagedPriceRefreshJobItemResponse(
            job_id=item.job_id,
            ticker=item.ticker,
            status=item.status,
            rows_upserted=item.rows_upserted,
            error_message=item.error_message,
            started_at=item.started_at,
            finished_at=item.finished_at,
        )
        for item in items
    ]


@router.get("/tickers/lookup", response_model=TickerLookupResponse)
def lookup_ticker(ticker: str) -> TickerLookupResponse:
    try:
        result = ticker_discovery_service.lookup_ticker(ticker)
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return TickerLookupResponse(
        ticker=result.ticker,
        name=result.name,
        market=result.market,
        currency=result.currency,
        exchange=result.exchange,
        quote_type=result.quote_type,
    )


@router.get("/tickers/search", response_model=TickerSearchResponse)
def search_tickers(query: str, max_results: int = 8) -> TickerSearchResponse:
    if max_results < 1 or max_results > 20:
        raise HTTPException(status_code=422, detail="max_results는 1 이상 20 이하로 입력해주세요.")
    try:
        results = ticker_discovery_service.search_tickers(query=query, max_results=max_results)
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return TickerSearchResponse(
        query=query.strip(),
        results=[
            TickerSearchResultResponse(
                ticker=item.ticker,
                name=item.name,
                exchange=item.exchange,
                quote_type=item.quote_type,
                market=item.market,
                currency=item.currency,
            )
            for item in results
        ],
    )


def _version_response(version: ManagedUniverseVersion) -> ManagedUniverseVersionResponse:
    return ManagedUniverseVersionResponse(
        version_id=version.version_id,
        version_name=version.version_name,
        source_type=version.source_type,
        notes=version.notes,
        is_active=version.is_active,
        created_at=version.created_at,
        instrument_count=version.instrument_count,
    )


def _version_detail_response(version: ManagedUniverseVersion, instruments) -> ManagedUniverseVersionDetailResponse:
    return ManagedUniverseVersionDetailResponse(
        **_version_response(version).model_dump(),
        instruments=[
            ManagedUniverseItemResponse(
                ticker=item.ticker,
                name=item.name,
                sector_code=item.sector_code,
                sector_name=item.sector_name,
                market=item.market,
                currency=item.currency,
                base_weight=item.base_weight,
            )
            for item in instruments
        ],
    )


def _price_stats_response(stats: ManagedPriceStats) -> ManagedPriceStatsResponse:
    return ManagedPriceStatsResponse(
        total_rows=stats.total_rows,
        ticker_count=stats.ticker_count,
        min_date=stats.min_date,
        max_date=stats.max_date,
    )


def _price_refresh_job_response(job: ManagedPriceRefreshJob) -> ManagedPriceRefreshJobResponse:
    return ManagedPriceRefreshJobResponse(
        job_id=job.job_id,
        version_id=job.version_id,
        version_name=job.version_name,
        refresh_mode=job.refresh_mode.value,
        status=job.status,
        ticker_count=job.ticker_count,
        success_count=job.success_count,
        failure_count=job.failure_count,
        message=job.message,
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
    )


def _price_refresh_response(result: ManagedPriceRefreshResult) -> ManagedPriceRefreshResponse:
    return ManagedPriceRefreshResponse(
        job=_price_refresh_job_response(result.job),
        price_stats=_price_stats_response(result.price_stats),
    )
