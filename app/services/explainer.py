from __future__ import annotations

import pandas as pd

from app.services.universe import ASSET_UNIVERSE


class PortfolioExplainer:
    def build_summary(
        self,
        weights: pd.Series,
        expected_return: float,
        volatility: float,
        target_volatility: float,
        used_fallback: bool,
    ) -> str:
        labels = {asset.code: asset.name for asset in ASSET_UNIVERSE}
        top_assets = weights.sort_values(ascending=False).head(2)
        top_text = ", ".join(f"{labels[code]} {weight:.0%}" for code, weight in top_assets.items())
        fallback_text = " Fallback weights were used because optimization became unstable." if used_fallback else ""
        return (
            f"This demo allocation targets about {target_volatility:.1%} annual volatility and lands at "
            f"{volatility:.1%} expected volatility with {expected_return:.1%} expected return. "
            f"The largest exposures are {top_text}.{fallback_text}"
        )

    def build_why_this_portfolio(self, volatility: float, expected_return: float) -> str:
        return (
            "This allocation lies on the Efficient Frontier, meaning it aims to deliver the "
            f"highest expected return available near {volatility:.1%} annual risk. "
            f"For this demo, that corresponds to an estimated return of {expected_return:.1%}."
        )
