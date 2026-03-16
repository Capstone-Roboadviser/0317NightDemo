from __future__ import annotations

import numpy as np
import pandas as pd

from app.services.universe import ASSET_CODES


class SampleDataService:
    """Provides deterministic sample price history for demos."""

    def __init__(self, seed: int = 7, years: int = 4) -> None:
        self.seed = seed
        self.years = years

    def load_prices(self) -> pd.DataFrame:
        trading_days = 252 * self.years
        dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=trading_days)

        annual_returns = np.array([0.088, 0.038, 0.061, 0.034, 0.020], dtype=float)
        annual_vols = np.array([0.19, 0.07, 0.16, 0.12, 0.01], dtype=float)
        correlations = np.array(
            [
                [1.00, 0.20, 0.65, 0.05, 0.05],
                [0.20, 1.00, 0.15, 0.10, 0.55],
                [0.65, 0.15, 1.00, 0.10, 0.05],
                [0.05, 0.10, 0.10, 1.00, 0.10],
                [0.05, 0.55, 0.05, 0.10, 1.00],
            ],
            dtype=float,
        )

        daily_means = annual_returns / 252
        daily_vols = annual_vols / np.sqrt(252)
        covariance = np.outer(daily_vols, daily_vols) * correlations

        rng = np.random.default_rng(self.seed)
        returns = rng.multivariate_normal(mean=daily_means, cov=covariance, size=trading_days)
        returns_df = pd.DataFrame(returns, index=dates, columns=ASSET_CODES)
        returns_df = returns_df.clip(lower=-0.08, upper=0.08)

        prices = 100 * (1 + returns_df).cumprod()
        return prices.round(4)

    def load_returns(self) -> pd.DataFrame:
        prices = self.load_prices()
        returns = prices.pct_change(fill_method=None).dropna(how="any")
        if len(returns) < 252:
            raise RuntimeError("Not enough sample history to run the demo.")
        return returns
