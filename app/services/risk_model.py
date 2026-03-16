from __future__ import annotations

import numpy as np
import pandas as pd


class RiskModel:
    """Computes expected returns and a stabilized covariance matrix."""

    def __init__(self, shrinkage: float = 0.20) -> None:
        self.shrinkage = shrinkage

    def expected_returns(self, returns: pd.DataFrame) -> pd.Series:
        means = returns.mean() * 252
        grand_mean = float(means.mean())
        stabilized = (1 - self.shrinkage) * means + self.shrinkage * grand_mean
        return stabilized.astype(float)

    def covariance_matrix(self, returns: pd.DataFrame) -> pd.DataFrame:
        sample_cov = returns.cov() * 252
        diag_cov = pd.DataFrame(
            np.diag(np.diag(sample_cov.values)),
            index=sample_cov.index,
            columns=sample_cov.columns,
        )
        stabilized = (1 - self.shrinkage) * sample_cov + self.shrinkage * diag_cov
        stabilized += np.eye(len(stabilized)) * 1e-6
        return stabilized.astype(float)

    def validate_inputs(self, returns: pd.DataFrame) -> None:
        if returns.isna().any().any():
            raise RuntimeError("Sample returns contain missing values.")
        if returns.shape[1] < 3:
            raise RuntimeError("At least three assets are required to build a frontier.")
        if returns.shape[0] < 252:
            raise RuntimeError("At least one year of daily history is required.")
