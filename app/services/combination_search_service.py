from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import islice

import numpy as np
import pandas as pd

from app.core.config import FRONTIER_POINT_COUNT, MINIMUM_HISTORY_ROWS, RANDOM_PORTFOLIO_COUNT, RISK_FREE_RATE
from app.data.repository import StaticDataRepository
from app.data.stock_repository import StockDataRepository
from app.domain.models import AssetClass, CombinationEvaluation, CombinationSearchResult, ExpectedReturnModelInput, FrontierPoint, StockInstrument
from app.engine.constraints import ConstraintEngine
from app.engine.covariance import ShrinkageCovarianceModel
from app.engine.math import portfolio_metrics_from_weights
from app.engine.optimizer import EfficientFrontierOptimizer
from app.engine.returns import ExpectedReturnModel, HistoricalMeanReturnModel


@dataclass(frozen=True)
class CombinationSearchConfig:
    selection_sizes: dict[str, int]
    sample_count: int = 250
    per_sector_weighting: str = "equal"
    random_seed: int = 23
    use_all_instruments_per_sector: bool = False


@dataclass(frozen=True)
class CombinationEngineData:
    assets: list[AssetClass]
    search_result: CombinationSearchResult
    expected_returns: pd.Series
    covariance: pd.DataFrame
    frontier_points: list[FrontierPoint]
    random_portfolios: list[tuple[float, float, dict[str, float]]]


class CombinationSearchService:
    """
    Samples sector-internal stock combinations and keeps the highest-Sharpe result.

    This service is intentionally decoupled from the demo API so we can evolve
    the search process without disturbing the existing presentation flow.
    """

    def __init__(self, return_model: ExpectedReturnModel | None = None) -> None:
        self.return_model = return_model or HistoricalMeanReturnModel(shrinkage=0.25)
        self.covariance_model = ShrinkageCovarianceModel()
        self.constraint_engine = ConstraintEngine()
        self.optimizer = EfficientFrontierOptimizer()

    def search_best_combination(
        self,
        stock_universe_path: str,
        stock_prices_path: str,
        config: CombinationSearchConfig,
    ) -> CombinationSearchResult:
        _, _, _, search_result = self._run_search_from_paths(
            stock_universe_path=stock_universe_path,
            stock_prices_path=stock_prices_path,
            config=config,
        )
        return search_result

    def build_engine_data(
        self,
        stock_universe_path: str,
        stock_prices_path: str,
        config: CombinationSearchConfig,
    ) -> CombinationEngineData:
        stock_repository = StockDataRepository()
        instruments = stock_repository.load_stock_universe(stock_universe_path)
        prices = stock_repository.load_stock_prices(stock_prices_path)
        return self.build_engine_data_from_market_data(
            instruments=instruments,
            prices=prices,
            config=config,
        )

    def search_best_combination_from_market_data(
        self,
        *,
        instruments: list[StockInstrument],
        prices: pd.DataFrame,
        config: CombinationSearchConfig,
    ) -> CombinationSearchResult:
        _, _, _, search_result = self._run_search_from_market_data(
            instruments=instruments,
            prices=prices,
            config=config,
        )
        return search_result

    def build_engine_data_from_market_data(
        self,
        *,
        instruments: list[StockInstrument],
        prices: pd.DataFrame,
        config: CombinationSearchConfig,
    ) -> CombinationEngineData:
        assets, instruments, stock_returns, search_result = self._run_search_from_market_data(
            instruments=instruments,
            prices=prices,
            config=config,
        )

        best_combination = search_result.best_evaluation.members_by_sector
        sector_returns = self._build_sector_returns(
            combination=best_combination,
            instruments=instruments,
            stock_returns=stock_returns,
            weighting=config.per_sector_weighting,
        )
        if sector_returns.empty:
            raise RuntimeError("선택된 최고 조합에서 자산군 수익률 시계열을 만들지 못했습니다.")

        asset_codes = [asset.code for asset in assets]
        sector_returns = sector_returns.reindex(columns=asset_codes).dropna(how="any")
        if len(sector_returns) < MINIMUM_HISTORY_ROWS:
            raise RuntimeError("선택된 최고 조합의 공통 히스토리가 부족합니다.")

        constraints = self.constraint_engine.build(assets)
        expected_returns = self.return_model.calculate(
            ExpectedReturnModelInput(asset_codes=asset_codes, returns=sector_returns)
        )
        covariance = self.covariance_model.calculate(sector_returns)
        frontier_points = self.optimizer.build_frontier(
            expected_returns=expected_returns.reindex(constraints.asset_codes),
            covariance=covariance.reindex(index=constraints.asset_codes, columns=constraints.asset_codes),
            constraints=constraints,
            point_count=FRONTIER_POINT_COUNT,
        )
        random_portfolios = self.optimizer.sample_random_portfolios(
            expected_returns=expected_returns.reindex(constraints.asset_codes),
            covariance=covariance.reindex(index=constraints.asset_codes, columns=constraints.asset_codes),
            constraints=constraints,
            sample_count=RANDOM_PORTFOLIO_COUNT,
        )

        return CombinationEngineData(
            assets=assets,
            search_result=search_result,
            expected_returns=expected_returns.reindex(asset_codes).astype(float),
            covariance=covariance.reindex(index=asset_codes, columns=asset_codes).astype(float),
            frontier_points=sorted(frontier_points, key=lambda point: point.volatility),
            random_portfolios=random_portfolios,
        )

    def _run_search_from_paths(
        self,
        stock_universe_path: str,
        stock_prices_path: str,
        config: CombinationSearchConfig,
    ) -> tuple[list[AssetClass], list[StockInstrument], pd.DataFrame, CombinationSearchResult]:
        stock_repository = StockDataRepository()
        instruments = stock_repository.load_stock_universe(stock_universe_path)
        prices = stock_repository.load_stock_prices(stock_prices_path)
        return self._run_search_from_market_data(
            instruments=instruments,
            prices=prices,
            config=config,
        )

    def _run_search_from_market_data(
        self,
        *,
        instruments: list[StockInstrument],
        prices: pd.DataFrame,
        config: CombinationSearchConfig,
    ) -> tuple[list[AssetClass], list[StockInstrument], pd.DataFrame, CombinationSearchResult]:
        asset_repository = StaticDataRepository()
        stock_repository = StockDataRepository()
        assets = asset_repository.load_asset_universe()
        self._validate_selection_config(assets, config)
        self._validate_instrument_pool(assets, instruments, config)
        stock_returns = stock_repository.build_stock_returns(prices)
        if stock_returns.empty:
            raise RuntimeError("가격 이력으로부터 유효 수익률을 생성하지 못했습니다.")

        combinations = (
            [self._build_all_instruments_combination(assets, instruments)]
            if config.use_all_instruments_per_sector
            else self._sample_combinations(instruments, config)
        )
        evaluations: list[CombinationEvaluation] = []
        discard_reasons: dict[str, int] = defaultdict(int)
        for combination in combinations:
            evaluation, reason = self._evaluate_combination(
                combination=combination,
                instruments=instruments,
                stock_returns=stock_returns,
                assets=assets,
                weighting=config.per_sector_weighting,
            )
            if evaluation is not None:
                evaluations.append(evaluation)
            elif reason is not None:
                discard_reasons[reason] += 1

        if not evaluations:
            reason_text = ", ".join(f"{key}={value}" for key, value in sorted(discard_reasons.items()))
            raise RuntimeError(f"평가 가능한 종목 조합을 찾지 못했습니다. 사유: {reason_text or 'unknown'}")

        top_evaluations = sorted(evaluations, key=lambda item: item.metrics.sharpe_ratio, reverse=True)
        return (
            assets,
            instruments,
            stock_returns,
            CombinationSearchResult(
                total_combinations_tested=len(combinations),
                successful_combinations=len(evaluations),
                discard_reasons=dict(discard_reasons),
                best_evaluation=top_evaluations[0],
                top_evaluations=list(islice(top_evaluations, 10)),
            ),
        )

    def _build_all_instruments_combination(
        self,
        assets: list[AssetClass],
        instruments: list[StockInstrument],
    ) -> dict[str, list[str]]:
        by_sector: dict[str, list[str]] = defaultdict(list)
        for instrument in instruments:
            by_sector[instrument.sector_code].append(instrument.ticker)
        return {
            asset.code: sorted(set(by_sector.get(asset.code, [])))
            for asset in assets
        }

    def _sample_combinations(
        self,
        instruments: list[StockInstrument],
        config: CombinationSearchConfig,
    ) -> list[dict[str, list[str]]]:
        by_sector: dict[str, list[str]] = defaultdict(list)
        for instrument in instruments:
            by_sector[instrument.sector_code].append(instrument.ticker)

        rng = np.random.default_rng(config.random_seed)
        unique_signatures: set[tuple[tuple[str, tuple[str, ...]], ...]] = set()
        combinations: list[dict[str, list[str]]] = []
        attempts = 0
        max_attempts = max(config.sample_count * 20, 200)

        while len(combinations) < config.sample_count and attempts < max_attempts:
            attempts += 1
            combination: dict[str, list[str]] = {}
            valid = True

            for sector_code, selection_size in config.selection_sizes.items():
                available = sorted(set(by_sector.get(sector_code, [])))
                if len(available) < selection_size:
                    raise RuntimeError(
                        f"섹터 '{sector_code}'의 종목 수가 부족합니다. "
                        f"필요 {selection_size}개, 현재 {len(available)}개"
                    )
                picks = sorted(rng.choice(available, size=selection_size, replace=False).tolist())
                combination[sector_code] = picks

            signature = tuple(sorted((sector, tuple(tickers)) for sector, tickers in combination.items()))
            if signature in unique_signatures:
                valid = False
            if valid:
                unique_signatures.add(signature)
                combinations.append(combination)

        return combinations

    def _evaluate_combination(
        self,
        combination: dict[str, list[str]],
        instruments: list[StockInstrument],
        stock_returns: pd.DataFrame,
        assets: list[AssetClass],
        weighting: str,
    ) -> tuple[CombinationEvaluation | None, str | None]:
        sector_returns = self._build_sector_returns(
            combination=combination,
            instruments=instruments,
            stock_returns=stock_returns,
            weighting=weighting,
        )
        if sector_returns.empty:
            return None, "empty_sector_returns"

        asset_codes = [asset.code for asset in assets]
        if set(sector_returns.columns) != set(asset_codes):
            return None, "missing_sector_columns"
        sector_returns = sector_returns.reindex(columns=asset_codes).dropna(how="any")
        if len(sector_returns) < MINIMUM_HISTORY_ROWS:
            return None, "insufficient_common_history"

        constraints = self.constraint_engine.build(assets)
        expected_returns = self.return_model.calculate(
            ExpectedReturnModelInput(asset_codes=asset_codes, returns=sector_returns)
        )
        covariance = self.covariance_model.calculate(sector_returns)
        try:
            frontier = self.optimizer.build_frontier(
                expected_returns=expected_returns.reindex(constraints.asset_codes),
                covariance=covariance.reindex(index=constraints.asset_codes, columns=constraints.asset_codes),
                constraints=constraints,
                point_count=FRONTIER_POINT_COUNT,
            )
        except RuntimeError:
            return None, "optimizer_failure"

        best_point = max(
            frontier,
            key=lambda point: portfolio_metrics_from_weights(
                point.weights,
                expected_returns,
                covariance,
                RISK_FREE_RATE,
            ).sharpe_ratio,
        )
        best_metrics = portfolio_metrics_from_weights(best_point.weights, expected_returns, covariance, RISK_FREE_RATE)
        combination_id = self._build_combination_id(combination)

        return (
            CombinationEvaluation(
                combination_id=combination_id,
                members_by_sector=combination,
                sector_returns_shape=sector_returns.shape,
                best_point=best_point,
                metrics=best_metrics,
            ),
            None,
        )

    def _build_sector_returns(
        self,
        combination: dict[str, list[str]],
        instruments: list[StockInstrument],
        stock_returns: pd.DataFrame,
        weighting: str,
    ) -> pd.DataFrame:
        if weighting not in {"equal", "base_weight"}:
            raise RuntimeError("지원하지 않는 섹터 내부 가중 방식입니다. equal 또는 base_weight를 사용하세요.")

        universe_by_ticker = {instrument.ticker: instrument for instrument in instruments}
        sector_frames: dict[str, pd.Series] = {}

        for sector_code, tickers in combination.items():
            available_tickers = [ticker for ticker in tickers if ticker in stock_returns.columns]
            if not available_tickers:
                continue

            sector_frame = stock_returns[available_tickers].dropna(how="any")
            if sector_frame.empty:
                continue

            if weighting == "base_weight":
                weights = np.array(
                    [universe_by_ticker[ticker].base_weight or 0.0 for ticker in available_tickers],
                    dtype=float,
                )
                if weights.sum() <= 0:
                    weights = np.ones(len(available_tickers), dtype=float)
            else:
                weights = np.ones(len(available_tickers), dtype=float)

            normalized = weights / weights.sum()
            sector_series = sector_frame.mul(normalized, axis=1).sum(axis=1)
            sector_frames[sector_code] = sector_series.astype(float)

        if not sector_frames:
            return pd.DataFrame()

        returns = pd.DataFrame(sector_frames).dropna(how="any")
        return returns.astype(float)

    def _build_combination_id(self, combination: dict[str, list[str]]) -> str:
        chunks = []
        for sector_code, tickers in sorted(combination.items()):
            joined = "-".join(tickers)
            chunks.append(f"{sector_code}:{joined}")
        return "|".join(chunks)

    def _validate_selection_config(self, assets: list[AssetClass], config: CombinationSearchConfig) -> None:
        asset_codes = {asset.code for asset in assets}
        selection_codes = set(config.selection_sizes.keys())
        missing_codes = sorted(asset_codes - selection_codes)
        extra_codes = sorted(selection_codes - asset_codes)

        if missing_codes or extra_codes:
            problems: list[str] = []
            if missing_codes:
                problems.append(f"누락 섹터={', '.join(missing_codes)}")
            if extra_codes:
                problems.append(f"알 수 없는 섹터={', '.join(extra_codes)}")
            raise RuntimeError(f"selection_sizes 구성이 자산군 정의와 일치하지 않습니다. {' / '.join(problems)}")

    def _validate_instrument_pool(
        self,
        assets: list[AssetClass],
        instruments: list[StockInstrument],
        config: CombinationSearchConfig,
    ) -> None:
        counts_by_sector: dict[str, int] = defaultdict(int)
        for instrument in instruments:
            counts_by_sector[instrument.sector_code] += 1

        shortages: list[str] = []
        for asset in assets:
            required = 1 if config.use_all_instruments_per_sector else int(config.selection_sizes.get(asset.code, 0))
            actual = int(counts_by_sector.get(asset.code, 0))
            if actual < required:
                shortages.append(f"{asset.name}({asset.code}) 필요 {required}개 / 현재 {actual}개")

        if shortages:
            raise RuntimeError(
                "관리자 유니버스의 섹터별 종목 수가 부족합니다. "
                + " | ".join(shortages)
            )
