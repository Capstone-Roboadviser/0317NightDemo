from __future__ import annotations

import pandas as pd

from app.data.managed_universe_repository import ManagedUniverseRepository
from app.data.stock_repository import StockDataRepository
from app.domain.models import ManagedUniverseVersion, StockInstrument


class ManagedUniverseService:
    """Coordinates admin-managed stock universe versions and cumulative price imports."""

    def __init__(
        self,
        repository: ManagedUniverseRepository | None = None,
        stock_repository: StockDataRepository | None = None,
    ) -> None:
        self.repository = repository or ManagedUniverseRepository()
        self.stock_repository = stock_repository or StockDataRepository()

    def initialize_storage(self) -> None:
        self.repository.initialize()

    def is_configured(self) -> bool:
        return self.repository.is_configured()

    def list_versions(self) -> list[ManagedUniverseVersion]:
        return self.repository.list_universe_versions()

    def get_active_version(self) -> ManagedUniverseVersion | None:
        return self.repository.get_active_version()

    def get_active_instruments(self) -> list[StockInstrument]:
        return self.repository.get_active_instruments()

    def load_prices_for_instruments(self, instruments: list[StockInstrument]) -> pd.DataFrame:
        return self.repository.load_prices_for_tickers([instrument.ticker for instrument in instruments])

    def get_price_stats_for_instruments(self, instruments: list[StockInstrument]) -> dict[str, object]:
        stats = self.repository.get_price_stats([instrument.ticker for instrument in instruments])
        return {
            "total_rows": stats.total_rows,
            "ticker_count": stats.ticker_count,
            "min_date": stats.min_date,
            "max_date": stats.max_date,
        }

    def create_version(
        self,
        *,
        version_name: str,
        instruments: list[StockInstrument],
        notes: str | None = None,
        activate: bool = False,
    ) -> ManagedUniverseVersion:
        self.initialize_storage()
        validated = self.stock_repository.parse_stock_universe_frame(
            pd.DataFrame(
                [
                    {
                        "ticker": item.ticker,
                        "name": item.name,
                        "sector_code": item.sector_code,
                        "sector_name": item.sector_name,
                        "market": item.market,
                        "currency": item.currency,
                        "base_weight": item.base_weight,
                    }
                    for item in instruments
                ]
            )
        )
        return self.repository.create_universe_version(
            version_name=version_name,
            source_type="admin_input",
            instruments=validated,
            notes=notes,
            activate=activate,
        )

    def activate_version(self, version_id: int) -> ManagedUniverseVersion:
        self.initialize_storage()
        return self.repository.activate_version(version_id)

    def get_version(self, version_id: int) -> ManagedUniverseVersion | None:
        return self.repository.get_version(version_id)

    def get_version_instruments(self, version_id: int) -> list[StockInstrument]:
        return self.repository.get_instruments_for_version(version_id)

    def update_version(
        self,
        *,
        version_id: int,
        version_name: str,
        instruments: list[StockInstrument],
        notes: str | None = None,
        activate: bool = False,
    ) -> ManagedUniverseVersion:
        self.initialize_storage()
        validated = self.stock_repository.parse_stock_universe_frame(
            pd.DataFrame(
                [
                    {
                        "ticker": item.ticker,
                        "name": item.name,
                        "sector_code": item.sector_code,
                        "sector_name": item.sector_name,
                        "market": item.market,
                        "currency": item.currency,
                        "base_weight": item.base_weight,
                    }
                    for item in instruments
                ]
            )
        )
        return self.repository.update_universe_version(
            version_id=version_id,
            version_name=version_name,
            instruments=validated,
            notes=notes,
            activate=activate,
        )

    def delete_version(self, version_id: int) -> None:
        self.initialize_storage()
        self.repository.delete_universe_version(version_id)
