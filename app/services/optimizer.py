from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from app.services.universe import (
    ASSET_CODES,
    FALLBACK_WEIGHTS,
    MAX_WEIGHT_BY_ASSET,
    MIN_WEIGHT_BY_ASSET,
)


@dataclass
class OptimizationResult:
    weights: pd.Series
    expected_return: float
    volatility: float
    sharpe_ratio: float
    frontier: list[dict]
    random_portfolios: list[tuple[float, float]]
    used_fallback: bool = False


class EfficientFrontierOptimizer:
    def __init__(self, risk_free_rate: float = 0.02, random_seed: int = 11) -> None:
        self.risk_free_rate = risk_free_rate
        self.random_seed = random_seed

    def optimize(
        self,
        expected_returns: pd.Series,
        covariance: pd.DataFrame,
        target_volatility: float,
        risk_profile: str,
    ) -> OptimizationResult:
        expected_returns = expected_returns.reindex(ASSET_CODES)
        covariance = covariance.reindex(index=ASSET_CODES, columns=ASSET_CODES)
        self._validate_matrix(covariance)

        initial = np.repeat(1 / len(ASSET_CODES), len(ASSET_CODES))
        bounds = tuple((MIN_WEIGHT_BY_ASSET[code], MAX_WEIGHT_BY_ASSET[code]) for code in ASSET_CODES)
        constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0},)

        frontier = self._build_frontier(expected_returns, covariance, initial, bounds, constraints)
        selected = self._select_by_target_volatility(frontier, target_volatility)
        random_portfolios = self._sample_random_portfolios(expected_returns, covariance, bounds)
        if selected is None:
            return self._fallback_result(
                expected_returns,
                covariance,
                risk_profile,
                frontier,
                random_portfolios,
            )

        weights = pd.Series(selected["weights"], index=ASSET_CODES, dtype=float)
        portfolio_return, portfolio_vol = self._performance(weights.values, expected_returns, covariance)
        sharpe = (portfolio_return - self.risk_free_rate) / portfolio_vol if portfolio_vol > 0 else 0.0
        return OptimizationResult(
            weights=weights,
            expected_return=portfolio_return,
            volatility=portfolio_vol,
            sharpe_ratio=sharpe,
            frontier=frontier,
            random_portfolios=random_portfolios,
        )

    def _build_frontier(
        self,
        expected_returns: pd.Series,
        covariance: pd.DataFrame,
        initial: np.ndarray,
        bounds: tuple[tuple[float, float], ...],
        constraints: tuple[dict, ...],
        points: int = 20,
    ) -> list[dict]:
        min_return_result = minimize(
            lambda w: self._performance(w, expected_returns, covariance)[0],
            initial,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        max_return_result = minimize(
            lambda w: -self._performance(w, expected_returns, covariance)[0],
            initial,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        if not min_return_result.success or not max_return_result.success:
            raise RuntimeError("Unable to calculate efficient frontier for the demo inputs.")

        min_return = self._performance(min_return_result.x, expected_returns, covariance)[0]
        max_return = self._performance(max_return_result.x, expected_returns, covariance)[0]

        frontier: list[dict] = []
        for target_return in np.linspace(min_return, max_return, points):
            result = minimize(
                lambda w: self._performance(w, expected_returns, covariance)[1],
                initial,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints
                + (
                    {
                        "type": "eq",
                        "fun": lambda w, target_return=target_return: self._performance(
                            w, expected_returns, covariance
                        )[0]
                        - target_return,
                    },
                ),
            )
            if not result.success:
                continue
            portfolio_return, portfolio_vol = self._performance(result.x, expected_returns, covariance)
            frontier.append(
                {
                    "weights": result.x,
                    "expected_return": float(portfolio_return),
                    "volatility": float(portfolio_vol),
                }
            )

        if not frontier:
            raise RuntimeError("No efficient frontier points were produced.")
        return frontier

    def _select_by_target_volatility(self, frontier: list[dict], target_volatility: float) -> dict | None:
        candidates = sorted(
            frontier,
            key=lambda point: (abs(point["volatility"] - target_volatility), -point["expected_return"]),
        )
        return candidates[0] if candidates else None

    def _fallback_result(
        self,
        expected_returns: pd.Series,
        covariance: pd.DataFrame,
        risk_profile: str,
        frontier: list[dict],
        random_portfolios: list[tuple[float, float]],
    ) -> OptimizationResult:
        weights = pd.Series(FALLBACK_WEIGHTS[risk_profile], dtype=float).reindex(ASSET_CODES)
        portfolio_return, portfolio_vol = self._performance(weights.values, expected_returns, covariance)
        sharpe = (portfolio_return - self.risk_free_rate) / portfolio_vol if portfolio_vol > 0 else 0.0
        return OptimizationResult(
            weights=weights,
            expected_return=portfolio_return,
            volatility=portfolio_vol,
            sharpe_ratio=sharpe,
            frontier=frontier,
            random_portfolios=random_portfolios,
            used_fallback=True,
        )

    def _performance(
        self,
        weights: np.ndarray,
        expected_returns: pd.Series,
        covariance: pd.DataFrame,
    ) -> tuple[float, float]:
        portfolio_return = float(np.dot(expected_returns.values, weights))
        portfolio_vol = float(np.sqrt(weights.T @ covariance.values @ weights))
        return portfolio_return, portfolio_vol

    def _validate_matrix(self, covariance: pd.DataFrame) -> None:
        if covariance.isna().any().any():
            raise RuntimeError("Covariance matrix contains missing values.")
        if np.linalg.det(covariance.values) == 0:
            covariance += np.eye(len(covariance)) * 1e-6

    def _sample_random_portfolios(
        self,
        expected_returns: pd.Series,
        covariance: pd.DataFrame,
        bounds: tuple[tuple[float, float], ...],
        samples: int = 160,
    ) -> list[tuple[float, float]]:
        rng = np.random.default_rng(self.random_seed)
        lower = np.array([bound[0] for bound in bounds], dtype=float)
        upper = np.array([bound[1] for bound in bounds], dtype=float)
        remaining = 1 - lower.sum()
        portfolios: list[tuple[float, float]] = []
        attempts = 0

        while len(portfolios) < samples and attempts < samples * 20:
            attempts += 1
            weights = lower + rng.dirichlet(np.ones(len(bounds))) * remaining
            if np.any(weights > upper + 1e-9):
                continue
            weights = weights / weights.sum()
            portfolio_return, portfolio_vol = self._performance(weights, expected_returns, covariance)
            portfolios.append((float(portfolio_vol), float(portfolio_return)))

        return portfolios
