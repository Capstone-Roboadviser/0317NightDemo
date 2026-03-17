from pydantic import BaseModel, Field, model_validator

from app.domain.enums import InvestmentHorizon, RiskProfile, SimulationDataSource
from app.domain.models import UserProfile


class PortfolioSimulationRequest(BaseModel):
    risk_profile: RiskProfile = Field(..., description="위험 성향")
    investment_horizon: InvestmentHorizon = Field(..., description="투자 기간")
    data_source: SimulationDataSource = Field(
        default=SimulationDataSource.ASSET_ASSUMPTIONS,
        description="계산에 사용할 데이터 소스. 기본값은 자산군 가정값이며, 데모에서는 개별주식 조합 모드도 선택할 수 있습니다.",
    )
    target_volatility: float | None = Field(
        default=None,
        ge=0.03,
        le=0.25,
        description="선택 입력값. 없으면 위험성향과 투자기간으로 기본 목표 변동성을 계산합니다.",
    )

    @model_validator(mode="after")
    def validate_profile_and_target(self) -> "PortfolioSimulationRequest":
        if self.risk_profile == RiskProfile.CONSERVATIVE and self.target_volatility and self.target_volatility > 0.12:
            raise ValueError("안정형 성향은 목표 변동성을 12% 초과로 설정할 수 없습니다.")
        return self

    def to_domain(self) -> UserProfile:
        return UserProfile(
            risk_profile=self.risk_profile,
            investment_horizon=self.investment_horizon,
            target_volatility=self.target_volatility,
            data_source=self.data_source,
        )
