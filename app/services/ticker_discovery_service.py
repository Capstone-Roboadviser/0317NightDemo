from __future__ import annotations

from dataclasses import dataclass

import yfinance as yf


@dataclass(frozen=True)
class TickerLookupResult:
    ticker: str
    name: str
    market: str
    currency: str
    exchange: str | None = None
    quote_type: str | None = None


@dataclass(frozen=True)
class TickerSearchResult:
    ticker: str
    name: str
    exchange: str | None = None
    quote_type: str | None = None
    market: str | None = None
    currency: str | None = None


class TickerDiscoveryService:
    def search_tickers(self, query: str, max_results: int = 8) -> list[TickerSearchResult]:
        normalized_query = query.strip()
        if not normalized_query:
            raise RuntimeError("검색어를 입력해주세요.")

        try:
            search = yf.Search(
                query=normalized_query,
                max_results=max_results,
                news_count=0,
                lists_count=0,
                include_cb=False,
                include_nav_links=False,
                include_research=False,
                enable_cultural_assets=False,
                recommended=max_results,
                raise_errors=True,
            )
        except Exception as exc:  # pragma: no cover - network dependent
            raise RuntimeError(f"티커 검색에 실패했습니다: {exc}") from exc

        quotes = getattr(search, "quotes", None)
        if quotes is None:
            quotes = getattr(search, "_quotes", [])

        results: list[TickerSearchResult] = []
        seen: set[str] = set()
        for quote in quotes:
            ticker = str(quote.get("symbol") or "").strip().upper()
            if not ticker or ticker in seen:
                continue
            seen.add(ticker)
            results.append(
                TickerSearchResult(
                    ticker=ticker,
                    name=str(
                        quote.get("shortname")
                        or quote.get("longname")
                        or quote.get("displayName")
                        or ticker
                    ).strip(),
                    exchange=self._clean_optional(
                        quote.get("exchange")
                        or quote.get("exchDisp")
                        or quote.get("fullExchangeName")
                    ),
                    quote_type=self._clean_optional(quote.get("quoteType") or quote.get("typeDisp")),
                    market=self._clean_optional(
                        quote.get("exchange")
                        or quote.get("exchDisp")
                        or quote.get("fullExchangeName")
                    ),
                    currency=self._clean_optional(quote.get("currency")),
                )
            )

        return results

    def lookup_ticker(self, ticker: str) -> TickerLookupResult:
        normalized_ticker = ticker.strip().upper()
        if not normalized_ticker:
            raise RuntimeError("티커를 입력해주세요.")

        search_matches = self.search_tickers(normalized_ticker, max_results=8)
        exact_match = next(
            (item for item in search_matches if item.ticker.upper() == normalized_ticker),
            None,
        )
        if exact_match is None:
            raise RuntimeError(f"'{normalized_ticker}' 티커를 찾을 수 없습니다.")

        name = exact_match.name
        market = exact_match.market or exact_match.exchange or "UNKNOWN"
        currency = exact_match.currency
        exchange = exact_match.exchange
        quote_type = exact_match.quote_type

        if not currency or market == "UNKNOWN" or name == normalized_ticker:
            try:
                info = yf.Ticker(normalized_ticker).get_info()
            except Exception:
                info = {}

            name = str(
                info.get("shortName")
                or info.get("longName")
                or info.get("displayName")
                or name
            ).strip()
            market = str(
                info.get("exchange")
                or info.get("fullExchangeName")
                or info.get("market")
                or market
            ).strip()
            currency = str(info.get("currency") or currency or "").strip()
            exchange = str(info.get("exchange") or exchange or "").strip() or exchange
            quote_type = str(info.get("quoteType") or quote_type or "").strip() or quote_type

        if not currency:
            raise RuntimeError(
                f"'{normalized_ticker}' 티커의 통화 정보를 가져오지 못했습니다. 유효한 Yahoo Finance 티커인지 확인해주세요."
            )

        return TickerLookupResult(
            ticker=normalized_ticker,
            name=name or normalized_ticker,
            market=market or "UNKNOWN",
            currency=currency,
            exchange=exchange,
            quote_type=quote_type,
        )

    @staticmethod
    def _clean_optional(value: object) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None
