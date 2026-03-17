# API 명세

## 1. 헬스체크

### `GET /health`

서버 상태 확인용입니다.

응답 예시:

```json
{
  "status": "ok"
}
```

## 2. 자산군 목록

### `GET /portfolio/assets`

현재 데모에서 사용하는 고정 자산군 목록을 반환합니다.

응답 예시:

```json
{
  "assets": [
    {
      "code": "bond",
      "name": "채권",
      "category": "bond",
      "description": "변동성을 낮추고 포트폴리오의 방어 역할을 담당하는 금리 민감 자산군입니다.",
      "color": "#5B7C99",
      "min_weight": 0.05,
      "max_weight": 0.50
    }
  ]
}
```

## 3. 포트폴리오 시뮬레이션

### `POST /portfolio/simulate`

위험 성향, 투자기간, 목표 변동성을 입력받아 포트폴리오 예시를 계산합니다.
추가로 `data_source`를 통해 `관리자 유니버스`, `자산군 가정값`, `개별주식 조합 데모` 중 하나를 선택할 수 있습니다.

요청 예시:

```json
{
  "risk_profile": "growth",
  "investment_horizon": "long",
  "data_source": "managed_universe",
  "target_volatility": 0.15
}
```

응답 예시:

```json
{
  "portfolio_id": "growth-long-150",
  "disclaimer": "본 결과는 샘플 데이터 기반의 데모용 자산배분 시뮬레이션이며, 시장 예측이나 투자 자문을 제공하지 않습니다.",
  "summary": "이 시뮬레이션은 연 15.0% 수준의 목표 변동성을 기준으로 포트폴리오를 선택했고, 예상 변동성은 15.1%, 예상 수익률은 11.2%입니다.",
  "explanation_title": "왜 이런 포트폴리오가 나왔을까?",
  "explanation": "이 포트폴리오는 효율적 투자선 위의 한 점으로...",
  "data_source": "managed_universe",
  "data_source_label": "관리자 종목 유니버스 (research-package-20260318-010101)",
  "target_volatility": 0.15,
  "expected_return": 0.112,
  "volatility": 0.151,
  "sharpe_ratio": 0.61,
  "weights": {
    "bond": 0.10,
    "real_assets": 0.10,
    "etf": 0.18,
    "tech_healthcare": 0.17,
    "ai_semiconductor_social": 0.18,
    "financials": 0.10,
    "energy": 0.08,
    "consumer_other": 0.09
  },
  "allocations": [
    {
      "asset_code": "ai_semiconductor_social",
      "asset_name": "AI반도체 및 소셜미디어",
      "weight": 0.18,
      "risk_contribution": 0.24
    }
  ],
  "frontier_points": [
    {
      "label": null,
      "volatility": 0.071,
      "expected_return": 0.044,
      "weights": {
        "bond": 0.2
      }
    },
    {
      "label": null,
      "volatility": 0.086,
      "expected_return": 0.058,
      "weights": {
        "bond": 0.15
      }
    }
  ],
  "selected_point_index": 8,
  "selected_point": {
    "label": "현재 포트폴리오",
    "volatility": 0.151,
    "expected_return": 0.112,
    "weights": {
      "bond": 0.10
    }
  },
  "random_portfolios": [
    {
      "volatility": 0.104,
      "expected_return": 0.073,
      "weights": {
        "bond": 0.12
      }
    }
  ],
  "used_fallback": false,
  "selected_combination": {
    "combination_id": "bond:BND2-BND3|etf:ETF1-ETF2",
    "members_by_sector": {
      "bond": ["BND2", "BND3"],
      "etf": ["ETF1", "ETF2"]
    },
    "total_combinations_tested": 40,
    "successful_combinations": 40,
    "discard_reasons": {}
  }
}
```

## 4. Efficient Frontier 미리보기

### `GET /portfolio/frontier`

현재 데모 기준 frontier 전체 점과 선택 지점을 반환합니다.

쿼리 파라미터:

- `risk_profile`: `conservative` | `balanced` | `growth`
- `investment_horizon`: `short` | `medium` | `long`
- `data_source`: `managed_universe` | `asset_assumptions` | `stock_combination_demo`
- `target_volatility`: 선택 입력

예시:

```text
GET /portfolio/frontier?risk_profile=balanced&investment_horizon=medium&data_source=managed_universe&target_volatility=0.11
```

응답에는 아래 정보가 포함됩니다.

- `portfolio_id`
- `data_source`
- `data_source_label`
- `target_volatility`
- `frontier_points`
- `frontier_options`
- `selected_point_index`
- `selected_point`
- `random_portfolios`
- `selected_combination` (관리자 유니버스 / 개별주식 조합 데모 모드일 때)

## 5. 관리자 유니버스 관리

### `GET /admin/universe/status`

현재 Postgres 연결 여부, 활성 버전, 가격 이력 범위를 반환합니다.

### `GET /admin/universe/versions`

저장된 유니버스 버전 목록을 반환합니다.

### `GET /admin/universe/versions/active`

현재 활성화된 유니버스 버전을 반환합니다.

### `POST /admin/universe/versions`

로그인 없이 관리자 입력용 유니버스 버전을 직접 생성합니다.

요청 예시:

```json
{
  "version_name": "manual-20260318-v1",
  "notes": "관리자 수기 입력 버전",
  "activate": true,
  "instruments": [
    {
      "ticker": "SPY",
      "name": "SPDR S&P 500 ETF Trust",
      "sector_code": "etf",
      "sector_name": "ETF",
      "market": "USA",
      "currency": "USD",
      "base_weight": 0.4
    }
  ]
}
```

### `POST /admin/universe/versions/{version_id}/activate`

저장된 버전 중 하나를 활성 유니버스로 전환합니다.

### `GET /admin/tickers/search`

Yahoo Finance 기준 티커 또는 종목명 검색 결과를 반환합니다. `/admin` 화면의 섹터 검색창에서 사용합니다.

예시:

```text
GET /admin/tickers/search?query=nvda&max_results=8
```

### `GET /admin/tickers/lookup`

티커 1개를 검증하고 `name`, `market`, `currency`를 자동채움용으로 반환합니다.

예시:

```text
GET /admin/tickers/lookup?ticker=NVDA
```

### `POST /admin/prices/refresh`

활성 유니버스 또는 특정 버전의 티커 목록을 기준으로 yfinance에서 가격 데이터를 수집해 Postgres에 저장합니다.

요청 예시:

```json
{
  "refresh_mode": "incremental",
  "full_lookback_years": 5
}
```

응답 예시:

```json
{
  "job": {
    "job_id": 12,
    "version_id": 3,
    "version_name": "manual-20260318-v1",
    "refresh_mode": "incremental",
    "status": "partial_success",
    "ticker_count": 24,
    "success_count": 22,
    "failure_count": 2,
    "message": "22개 종목 갱신 성공, 2개 실패",
    "created_at": "2026-03-18T03:00:00Z",
    "started_at": "2026-03-18T03:00:00Z",
    "finished_at": "2026-03-18T03:01:15Z"
  },
  "price_stats": {
    "total_rows": 12096,
    "ticker_count": 24,
    "min_date": "2021-03-18",
    "max_date": "2026-03-17"
  }
}
```

### `GET /admin/prices/status`

현재 활성 유니버스의 가격 데이터 범위와 최근 갱신 잡 상태를 반환합니다.

## 오류 응답

### 400

입력 검증 실패 예시:

```json
{
  "detail": "안정형 성향은 목표 변동성을 12% 초과로 설정할 수 없습니다."
}
```

### 422

계산 실패 예시:

```json
{
  "detail": "효율적 투자선 계산에 실패했습니다."
}
```
