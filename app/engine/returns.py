from __future__ import annotations

import pandas as pd


class HistoricalMeanReturnModel:
    def __init__(self, shrinkage: float = 0.20) -> None:
        self.shrinkage = shrinkage

    def calculate(self, returns: pd.DataFrame) -> pd.Series:
        mean_returns = returns.mean() * 252
        grand_mean = float(mean_returns.mean())
        stabilized = (1 - self.shrinkage) * mean_returns + self.shrinkage * grand_mean
        return stabilized.astype(float)
