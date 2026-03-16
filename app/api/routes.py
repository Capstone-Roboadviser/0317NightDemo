from fastapi import APIRouter, HTTPException

from app.schemas import (
    AssetUniverseResponse,
    HealthResponse,
    PortfolioRequest,
    PortfolioResponse,
)
from app.services.engine import AllocationEngine
from app.services.universe import ASSET_UNIVERSE
from app.web import render_homepage


router = APIRouter()
engine = AllocationEngine()


@router.get("/", tags=["web"])
def homepage():
    return render_homepage()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/v1/assets", response_model=AssetUniverseResponse, tags=["portfolio"])
def list_assets() -> AssetUniverseResponse:
    return AssetUniverseResponse(assets=ASSET_UNIVERSE)


@router.post("/v1/portfolio/recommend", response_model=PortfolioResponse, tags=["portfolio"])
def recommend_portfolio(payload: PortfolioRequest) -> PortfolioResponse:
    try:
        return engine.recommend(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
