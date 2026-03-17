from __future__ import annotations

from typing import Protocol

import pandas as pd

from app.domain.models import ExpectedReturnModelInput


class ExpectedReturnModel(Protocol):
    def calculate(self, model_input: ExpectedReturnModelInput) -> pd.Series: ...


class AssumptionReturnModel:
    def calculate(self, model_input: ExpectedReturnModelInput) -> pd.Series:
        if model_input.annual_returns is None:
            raise RuntimeError("가정 기반 기대수익률 모델에는 annual_returns 입력이 필요합니다.")
        expected_returns = pd.Series(model_input.annual_returns, dtype=float).reindex(model_input.asset_codes)
        if expected_returns.isna().any():
            raise RuntimeError("샘플 시장 가정의 기대수익률이 자산군 정의와 일치하지 않습니다.")
        return expected_returns.astype(float)


class HistoricalMeanReturnModel:
    def __init__(self, shrinkage: float = 0.20) -> None:
        self.shrinkage = shrinkage

    def calculate(self, model_input: ExpectedReturnModelInput) -> pd.Series:
        if model_input.returns is None:
            raise RuntimeError("과거평균 기대수익률 모델에는 returns 입력이 필요합니다.")
        mean_returns = model_input.returns.mean() * 252
        grand_mean = float(mean_returns.mean())
        stabilized = (1 - self.shrinkage) * mean_returns + self.shrinkage * grand_mean
        return stabilized.reindex(model_input.asset_codes).astype(float)
