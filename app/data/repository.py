from __future__ import annotations

import json

import numpy as np
import pandas as pd

from app.core.config import ASSET_UNIVERSE_PATH, SAMPLE_MARKET_ASSUMPTIONS_PATH
from app.domain.models import AssetClass, MarketAssumptions


class StaticDataRepository:
    """Loads fixed demo data from local JSON files."""

    def __init__(self) -> None:
        self._asset_universe: list[AssetClass] | None = None
        self._market_assumptions: MarketAssumptions | None = None
        self._sample_returns: pd.DataFrame | None = None

    def load_asset_universe(self) -> list[AssetClass]:
        if self._asset_universe is None:
            payload = json.loads(ASSET_UNIVERSE_PATH.read_text())
            self._asset_universe = [AssetClass(**item) for item in payload]
        return self._asset_universe

    def load_market_assumptions(self) -> MarketAssumptions:
        if self._market_assumptions is None:
            payload = json.loads(SAMPLE_MARKET_ASSUMPTIONS_PATH.read_text())
            self._market_assumptions = MarketAssumptions(**payload)
        return self._market_assumptions

    def load_sample_returns(self) -> pd.DataFrame:
        if self._sample_returns is None:
            assumptions = self.load_market_assumptions()
            assets = self.load_asset_universe()
            asset_codes = [asset.code for asset in assets]

            annual_returns = pd.Series(assumptions.annual_returns, dtype=float).reindex(asset_codes)
            annual_volatilities = pd.Series(assumptions.annual_volatilities, dtype=float).reindex(asset_codes)
            correlations = pd.DataFrame(assumptions.correlations, dtype=float).reindex(index=asset_codes, columns=asset_codes)

            if annual_returns.isna().any() or annual_volatilities.isna().any() or correlations.isna().any().any():
                raise RuntimeError("샘플 시장 가정 데이터가 자산군 정의와 일치하지 않습니다.")

            trading_days = 252 * assumptions.years
            dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=trading_days)
            daily_means = annual_returns / 252
            daily_vols = annual_volatilities / np.sqrt(252)
            covariance = np.outer(daily_vols, daily_vols) * correlations.values

            rng = np.random.default_rng(assumptions.seed)
            returns = rng.multivariate_normal(mean=daily_means.values, cov=covariance, size=trading_days)
            returns_df = pd.DataFrame(returns, index=dates, columns=asset_codes).clip(lower=-0.08, upper=0.08)
            self._sample_returns = returns_df.astype(float)

        return self._sample_returns.copy()
