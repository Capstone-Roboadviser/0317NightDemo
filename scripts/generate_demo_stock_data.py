from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SECTORS = [
    {
        "code": "bond",
        "name": "채권",
        "ticker_prefix": "BND",
        "stock_prefix": "Bond Core",
        "annual_return": 0.038,
        "annual_volatility": 0.065,
    },
    {
        "code": "real_assets",
        "name": "실물",
        "ticker_prefix": "RAS",
        "stock_prefix": "Real Asset",
        "annual_return": 0.055,
        "annual_volatility": 0.125,
    },
    {
        "code": "etf",
        "name": "ETF",
        "ticker_prefix": "ETF",
        "stock_prefix": "Index ETF",
        "annual_return": 0.072,
        "annual_volatility": 0.145,
    },
    {
        "code": "tech_healthcare",
        "name": "기술주 및 헬스케어",
        "ticker_prefix": "THC",
        "stock_prefix": "Tech Health",
        "annual_return": 0.094,
        "annual_volatility": 0.205,
    },
    {
        "code": "ai_semiconductor_social",
        "name": "AI반도체 및 소셜미디어",
        "ticker_prefix": "AIS",
        "stock_prefix": "AI Social",
        "annual_return": 0.108,
        "annual_volatility": 0.235,
    },
    {
        "code": "financials",
        "name": "금융",
        "ticker_prefix": "FIN",
        "stock_prefix": "Financial",
        "annual_return": 0.068,
        "annual_volatility": 0.175,
    },
    {
        "code": "energy",
        "name": "에너지",
        "ticker_prefix": "ENG",
        "stock_prefix": "Energy",
        "annual_return": 0.062,
        "annual_volatility": 0.195,
    },
    {
        "code": "consumer_other",
        "name": "소비재 및 기타",
        "ticker_prefix": "CNS",
        "stock_prefix": "Consumer",
        "annual_return": 0.058,
        "annual_volatility": 0.135,
    },
]


def build_universe(stocks_per_sector: int) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for sector in SECTORS:
        weight = round(1.0 / stocks_per_sector, 4)
        for index in range(1, stocks_per_sector + 1):
            rows.append(
                {
                    "ticker": f"{sector['ticker_prefix']}{index}",
                    "name": f"{sector['stock_prefix']} {index}",
                    "sector_code": sector["code"],
                    "sector_name": sector["name"],
                    "market": "USA",
                    "currency": "USD",
                    "base_weight": weight,
                }
            )
    return pd.DataFrame(rows)


def build_prices(universe: pd.DataFrame, years: int, seed: int, end_date: str) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end=pd.Timestamp(end_date), periods=252 * years)
    market_factor = rng.normal(0.00018, 0.0058, size=len(dates))

    price_rows: list[dict[str, object]] = []
    for sector in SECTORS:
        sector_members = universe[universe["sector_code"] == sector["code"]]["ticker"].tolist()
        sector_daily_mean = sector["annual_return"] / 252
        sector_daily_vol = sector["annual_volatility"] / np.sqrt(252)
        sector_factor = rng.normal(0.0, sector_daily_vol * 0.55, size=len(dates))

        for member_index, ticker in enumerate(sector_members, start=1):
            idio_vol = max(sector_daily_vol * (0.35 + 0.05 * member_index), 0.0015)
            idiosyncratic = rng.normal(0.0, idio_vol, size=len(dates))
            drift_adjustment = rng.normal(0.0, 0.00004)
            daily_returns = sector_daily_mean + drift_adjustment + 0.35 * market_factor + 0.45 * sector_factor + idiosyncratic
            daily_returns = np.clip(daily_returns, -0.12, 0.12)

            start_price = float(rng.uniform(35, 220))
            prices = start_price * np.cumprod(1 + daily_returns)

            for date, price in zip(dates, prices):
                price_rows.append(
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "ticker": ticker,
                        "adjusted_close": round(float(price), 4),
                    }
                )

    return pd.DataFrame(price_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate demo stock-level dataset for combination search.")
    parser.add_argument("--output-dir", default="app/data/demo", help="Directory where CSV files will be written.")
    parser.add_argument("--years", type=int, default=2, help="Number of years of business-day prices to generate.")
    parser.add_argument("--stocks-per-sector", type=int, default=4, help="Number of demo stocks to create per sector.")
    parser.add_argument("--seed", type=int, default=31, help="Random seed for deterministic output.")
    parser.add_argument("--end-date", default="2026-03-17", help="Inclusive end date in YYYY-MM-DD format.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    universe = build_universe(args.stocks_per_sector)
    prices = build_prices(universe, years=args.years, seed=args.seed, end_date=args.end_date)

    universe_path = output_dir / "demo_stock_universe.csv"
    prices_path = output_dir / "demo_stock_prices.csv"

    universe.to_csv(universe_path, index=False)
    prices.to_csv(prices_path, index=False)

    print(universe_path)
    print(prices_path)
    print(f"universe_rows={len(universe)}")
    print(f"price_rows={len(prices)}")


if __name__ == "__main__":
    main()
