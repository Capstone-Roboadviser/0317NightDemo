from typing import Literal

from pydantic import BaseModel, Field, model_validator


RiskProfile = Literal["conservative", "balanced", "growth"]
TimeHorizon = Literal["short", "medium", "long"]


class HealthResponse(BaseModel):
    status: str


class AssetInfo(BaseModel):
    code: str
    name: str
    color: str
    description: str


class AssetUniverseResponse(BaseModel):
    assets: list[AssetInfo]


class PortfolioRequest(BaseModel):
    risk_profile: RiskProfile = Field(
        ..., description="Risk preference used to pick a target volatility band."
    )
    investment_horizon: TimeHorizon = Field(
        ..., description="Intended holding period for the simulation."
    )
    target_volatility: float | None = Field(
        default=None,
        ge=0.03,
        le=0.25,
        description="Optional annualized volatility target. If omitted, the server chooses one.",
    )

    @model_validator(mode="after")
    def validate_profile_and_target(self) -> "PortfolioRequest":
        if self.risk_profile == "conservative" and self.target_volatility and self.target_volatility > 0.12:
            raise ValueError("Conservative profile cannot target volatility above 12%.")
        return self


class AllocationItem(BaseModel):
    asset_code: str
    asset_name: str
    weight: float
    risk_contribution: float


class FrontierPoint(BaseModel):
    label: str | None = None
    volatility: float
    expected_return: float


class ScatterPoint(BaseModel):
    volatility: float
    expected_return: float


class ExplanationCard(BaseModel):
    title: str
    body: str


class PortfolioMetrics(BaseModel):
    expected_return: float
    volatility: float
    sharpe_ratio: float


class PortfolioResponse(BaseModel):
    disclaimer: str
    summary: str
    explanation: ExplanationCard
    target_volatility: float
    metrics: PortfolioMetrics
    allocations: list[AllocationItem]
    frontier: list[FrontierPoint]
    frontier_options: list[FrontierPoint]
    selected_point: FrontierPoint
    random_portfolios: list[ScatterPoint]
