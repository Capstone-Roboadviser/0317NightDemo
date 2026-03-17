from __future__ import annotations

from app.core.config import DEFAULT_TARGET_VOLATILITY, HORIZON_VOLATILITY_ADJUSTMENT
from app.domain.models import UserProfile


class ProfileMappingService:
    def resolve_target_volatility(self, user_profile: UserProfile) -> float:
        if user_profile.target_volatility is not None:
            return float(user_profile.target_volatility)

        base = DEFAULT_TARGET_VOLATILITY[user_profile.risk_profile]
        adjustment = HORIZON_VOLATILITY_ADJUSTMENT[user_profile.investment_horizon]
        return float(min(max(base + adjustment, 0.04), 0.22))

    def build_portfolio_id(self, user_profile: UserProfile, target_volatility: float) -> str:
        compact_target = f"{int(round(target_volatility * 1000)):03d}"
        return f"{user_profile.risk_profile.value}-{user_profile.investment_horizon.value}-{compact_target}"
