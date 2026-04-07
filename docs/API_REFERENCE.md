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

## 2. 자산군 카탈로그

### `GET /portfolio/assets`

현재 시스템이 사용하는 자산군 카탈로그를 반환합니다.

중요:

- 자산군 목록은 `app/data/asset_universe.json`에서 로드됩니다.
- 각 자산군은 `role_key`, `selection_mode`, `weighting_mode`, `return_mode`를 함께 반환합니다.
- 현재 자산군은 최적화 대상이 아니라 **후보 종목을 그룹핑하고 역할을 정의하는 기준**입니다.

응답 주요 필드:

- `code`
- `name`
- `description`
- `color`
- `role_key`
- `role_name`
- `role_description`
- `selection_mode`
- `weighting_mode`
- `return_mode`

## 3. 종목 목록

### `GET /portfolio/stocks`

현재 선택된 데이터 소스 기준 종목 후보군을 자산군별로 반환합니다.

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

참고:

- 메인 웹 UI는 슬라이더 중심으로 동작하지만, API 호환성을 위해 기존 파라미터를 유지합니다.

응답 주요 필드:

- `data_source_label`
- `frontier_points`
- `frontier_options`
- `selected_point`
- `random_portfolios`
- `individual_assets`
- `selected_combination`

중요:

- `frontier_points[*].weights`와 `selected_point.weights`는 **현재 선택된 포트폴리오 컴포넌트의 실제 종목 가중치**입니다.
- `individual_assets`도 같은 frontier 계산에 사용한 기대수익률/공분산 기준으로 계산됩니다.
- 프론트에서 따로 자산군 기준으로 다시 합산합니다.

## 5. 포트폴리오 시뮬레이션

### `POST /portfolio/simulate`

현재 active 유니버스와 사용자 입력을 기준으로 포트폴리오 예시를 계산합니다.

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
- `individual_assets`
- `selected_combination`

### 응답 해석에서 중요한 점

#### `weights`

`weights`는 **화면 표시용 자산군 합산 비중**입니다.

#### `selected_combination`

`selected_combination`은 자산군별로 어떤 종목 멤버가 현재 포트폴리오 컴포넌트에 사용됐는지 보여줍니다.

예시:

```json
{
  "combination_id": "manual-20260330-v1|short_term_bond:SHY|new_growth:QQQ-NVDA|gold:GLD",
  "members_by_sector": {
    "short_term_bond": ["SHY"],
    "new_growth": ["QQQ", "NVDA"],
    "gold": ["GLD"]
  }
}
```

즉 현재 구조는:

- 자산군별 후보군은 여러 개 있을 수 있음
- 역할에 따라 실제 포트폴리오에는 단일 대표 종목 또는 동일비중 바스켓이 들어감

입니다.

## 6. 포트폴리오 히스토리 차트

### `POST /portfolio/volatility-history`

현재 포트폴리오 가중치 기준으로 과거 롤링 변동성 시계열을 계산합니다.

### `POST /portfolio/return-history`

현재 포트폴리오 가중치 기준으로 과거 롤링 수익률 시계열을 계산합니다.

중요:

- 두 엔드포인트는 공통 포트폴리오 수익률 생성 경로를 사용합니다.
- managed universe일 때는 active 유니버스의 **공통 가격 구간**만 사용합니다.

## 6-1. 포트폴리오 비교 백테스트

### `POST /portfolio/comparison-backtest`

최신 갱신 데이터 전체 구간을 `90% train / 10% test`로 자동 분할한 뒤,
train 종료 시점에 추천된 `안정형 / 균형형 / 성장형` 포트폴리오를
test 구간부터 현재까지 비교합니다.

중요:

- 현재 시점에서 계산한 포트폴리오를 과거 전체 구간에 그대로 적용하지 않습니다.
- 기대수익률과 공분산, 대표 종목 조합 선택은 모두 train 구간 기준입니다.
- 실제 성과 비교 곡선은 test 구간에서만 그립니다.

응답 주요 필드:

- `train_start_date`
- `train_end_date`
- `test_start_date`
- `start_date`
- `end_date`
- `split_ratio`
- `lines`

## 7. 관리자 유니버스 관리

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
- `price_window`
- `selected_combination`

## 8. 가격 데이터 갱신

### `POST /admin/prices/refresh`

active 유니버스 티커를 기준으로 가격 이력을 적재합니다.

요청 예시:

```json
{
  "refresh_mode": "full",
  "full_lookback_years": 10
}
```

중요:

- raw 가격은 길게 적재하더라도, 실제 계산은 유니버스의 **가장 늦게 시작한 종목 기준 공통 구간**만 사용합니다.
- 관리자 상태 카드에서도 `공통 사용 구간`을 확인할 수 있습니다.

### `GET /admin/prices/status`

최근 가격 적재 상태를 반환합니다.

### `GET /admin/prices/jobs/{job_id}/items`

가격 적재 잡의 종목별 성공/실패 상세를 반환합니다.

## 9. 티커 검색 / 자동채움

### `GET /admin/tickers/search`

검색어 기준으로 티커 후보를 조회합니다.

### `GET /admin/tickers/lookup`

단일 티커의 이름/시장/통화를 조회합니다.
