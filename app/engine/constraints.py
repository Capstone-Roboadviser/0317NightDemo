from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from app.domain.models import AssetClass


@dataclass(frozen=True)
class ConstraintSet:
    asset_codes: list[str]
    bounds: tuple[tuple[float, float], ...]
    scipy_constraints: tuple[dict[str, Any], ...]
    initial_weights: np.ndarray


class ConstraintEngine:
    def build(self, assets: list[AssetClass]) -> ConstraintSet:
        asset_codes = [asset.code for asset in assets]
        lower_bounds = np.array([asset.min_weight for asset in assets], dtype=float)
        upper_bounds = np.array([asset.max_weight for asset in assets], dtype=float)

        if lower_bounds.sum() > 1 + 1e-9:
            raise RuntimeError("최소 비중 합이 1을 초과해 제약조건이 성립하지 않습니다.")

        headroom = upper_bounds - lower_bounds
        remaining = 1 - lower_bounds.sum()
        if remaining > headroom.sum() + 1e-9:
            raise RuntimeError("최대 비중 제약으로 인해 전체 비중 합을 1로 맞출 수 없습니다.")

        initial_weights = lower_bounds.copy()
        if remaining > 0 and headroom.sum() > 0:
            initial_weights += (headroom / headroom.sum()) * remaining

        bounds = tuple((asset.min_weight, asset.max_weight) for asset in assets)
        scipy_constraints = ({"type": "eq", "fun": lambda weights: np.sum(weights) - 1.0},)
        return ConstraintSet(
            asset_codes=asset_codes,
            bounds=bounds,
            scipy_constraints=scipy_constraints,
            initial_weights=initial_weights,
        )
