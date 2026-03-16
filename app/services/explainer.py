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
        fallback_text = " 최적화가 불안정해져 사전 정의한 대체 비중을 사용했습니다." if used_fallback else ""
        return (
            f"이 시뮬레이션은 연 {target_volatility:.1%} 수준의 목표 변동성을 기준으로 포트폴리오를 선택했고, "
            f"예상 변동성은 {volatility:.1%}, 예상 수익률은 {expected_return:.1%}로 계산되었습니다. "
            f"가장 큰 비중은 {top_text}입니다.{fallback_text}"
        )

    def build_why_this_portfolio(self, volatility: float, expected_return: float) -> str:
        return (
            "이 포트폴리오는 효율적 투자선 위의 한 점으로, "
            f"연 {volatility:.1%} 수준의 위험에서 기대할 수 있는 수익을 최대화하도록 선택된 예시입니다. "
            f"이번 데모 기준 예상 수익률은 {expected_return:.1%}입니다."
        )
