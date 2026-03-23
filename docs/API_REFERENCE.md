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

현재 시스템이 사용하는 8개 자산군 메타데이터를 반환합니다.

중요:

- 현재 자산군은 최적화 대상이 아니라 **후보 종목을 그룹핑하는 기준**입니다.
- 화면에서는 이 자산군 기준으로 결과를 다시 합산해 보여줍니다.

## 3. 종목 목록

### `GET /portfolio/stocks`

현재 선택된 데이터 소스 기준 종목 후보군을 섹터별로 반환합니다.

쿼리 파라미터:

- `data_source`: `managed_universe` | `asset_assumptions` | `stock_combination_demo`

기본값:

- `managed_universe`

## 4. Efficient Frontier 미리보기

### `GET /portfolio/frontier`

현재 입력 조건에서 frontier 전체 점, 현재 선택 포인트, 랜덤 포트폴리오 점 구름을 반환합니다.

쿼리 파라미터:

- `risk_profile`: `conservative` | `balanced` | `growth`
- `investment_horizon`: `short` | `medium` | `long`
- `data_source`: `managed_universe` | `asset_assumptions` | `stock_combination_demo`
- `target_volatility`: 선택 입력

예시:

```text
GET /portfolio/frontier?risk_profile=balanced&investment_horizon=medium&data_source=managed_universe&target_volatility=0.11
```

응답 주요 필드:

- `data_source_label`
- `frontier_points`
- `selected_point`
- `random_portfolios`
- `selected_combination`

중요:

- `frontier_points[*].weights`와 `selected_point.weights`는 **대표 종목 유니버스 기준 종목 가중치**입니다.
- 프론트에서 따로 섹터 기준으로 다시 합산합니다.

## 5. 포트폴리오 시뮬레이션

### `POST /portfolio/simulate`

위험 성향, 투자기간, 목표 변동성을 입력받아 포트폴리오 예시를 계산합니다.

요청 예시:

```json
{
  "risk_profile": "balanced",
  "investment_horizon": "medium",
  "data_source": "managed_universe"
}
```

응답 주요 필드:

- `portfolio_id`
- `summary`
- `explanation_title`
- `explanation`
- `data_source`
- `data_source_label`
- `expected_return`
- `volatility`
- `sharpe_ratio`
- `weights`
- `allocations`
- `frontier_points`
- `selected_point`
- `random_portfolios`
- `selected_combination`

### 응답 해석에서 중요한 점

#### `weights`

`weights`는 **화면 표시용 섹터 합산 비중**입니다.

예시:

```json
{
  "bond": 0.18,
  "etf": 0.21,
  "financials": 0.16
}
```

#### `selected_combination`

`selected_combination`은 섹터별 대표 종목이 어떻게 선택됐는지 보여줍니다.

예시:

```json
{
  "combination_id": "manual-20260323-v1|bond:BIL|etf:QQQ|financials:JPM",
  "members_by_sector": {
    "bond": ["BIL"],
    "etf": ["QQQ"],
    "financials": ["JPM"]
  },
  "total_combinations_tested": 1000,
  "successful_combinations": 1000,
  "discard_reasons": {}
}
```

즉 현재 구조는:

- 섹터별 후보군은 여러 개 있을 수 있음
- 실제 포트폴리오에는 섹터당 대표 종목 1개만 들어감

입니다.

## 6. 관리자 유니버스 관리

### `GET /admin/universe/status`

현재 Postgres 연결 여부, active 버전, 가격 적재 범위, 최근 가격 갱신 잡 상태를 반환합니다.

### `GET /admin/universe/versions`

저장된 유니버스 버전 목록을 반환합니다.

### `GET /admin/universe/versions/active`

현재 활성 버전을 반환합니다.

### `GET /admin/universe/versions/{version_id}`

특정 버전 상세와 등록된 종목 목록을 반환합니다.

### `POST /admin/universe/versions`

신규 유니버스 버전을 생성합니다.

요청 예시:

```json
{
  "version_name": "manual-20260323-v1",
  "notes": "운영 데모 버전",
  "activate": true,
  "instruments": [
    {
      "ticker": "BIL",
      "name": "SPDR Bloomberg 1-3 Month T-Bill ETF",
      "sector_code": "bond",
      "sector_name": "채권",
      "market": "USA",
      "currency": "USD"
    }
  ]
}
```

### `PUT /admin/universe/versions/{version_id}`

기존 유니버스 버전을 수정합니다.

### `DELETE /admin/universe/versions/{version_id}`

기존 유니버스 버전을 삭제합니다.

### `POST /admin/universe/versions/{version_id}/activate`

저장된 버전 중 하나를 active 상태로 전환합니다.

### `GET /admin/universe/readiness`

현재 active 유니버스가 실제 시뮬레이션 계산까지 가능한지 점검합니다.

주요 필드:

- `ready`
- `summary`
- `issues`
- `priced_ticker_count`
- `stock_return_rows`
- `effective_history_rows`
- `sector_checks`
- `selected_combination`

현재 readiness는 아래를 확인합니다.

- active 버전 존재 여부
- 종목 등록 여부
- 가격 적재 여부
- 최소 이력 충족 여부
- 섹터별 후보 종목 존재 여부

## 7. 가격 데이터 갱신

### `POST /admin/prices/refresh`

active 유니버스 또는 특정 버전의 티커를 기준으로 `yfinance`에서 가격 데이터를 수집해 Postgres에 저장합니다.

요청 예시:

```json
{
  "refresh_mode": "incremental",
  "full_lookback_years": 5
}
```

### `GET /admin/prices/status`

가격 적재 상태 요약을 반환합니다.

### `GET /admin/prices/jobs/{job_id}/items`

가격 갱신 잡의 티커별 상세 결과를 반환합니다.

쿼리 파라미터:

- `failed_only`: 실패한 항목만 조회할지 여부
- `limit`: 최대 반환 개수

예시:

```text
GET /admin/prices/jobs/12/items?failed_only=true&limit=40
```

## 8. 티커 자동채움 / 검색

### `GET /admin/tickers/lookup`

티커 1개를 검증하고, `name`, `market`, `currency` 자동채움 정보를 반환합니다.

예시:

```text
GET /admin/tickers/lookup?ticker=NVDA
```

### `GET /admin/tickers/search`

Yahoo Finance 기준 티커 또는 회사명 검색 결과를 반환합니다.

예시:

```text
GET /admin/tickers/search?query=bank&max_results=8
```

제약:

- `max_results`는 `1 ~ 20`

## 9. 참고

이 API는 현재 아래 운영 구조를 전제로 합니다.

- 관리자 유니버스는 Postgres에 저장
- 가격 데이터는 `yfinance`에서 적재
- 시뮬레이터는 active 유니버스 기준
- 각 섹터에서 대표 종목 1개씩을 고른 조합 중 최고 Sharpe 구조를 선택
