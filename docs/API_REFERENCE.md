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

요청 예시:

```json
{
  "risk_profile": "growth",
  "investment_horizon": "long",
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
      "expected_return": 0.044
    },
    {
      "label": null,
      "volatility": 0.086,
      "expected_return": 0.058
    }
  ],
  "selected_point_index": 8,
  "selected_point": {
    "label": "현재 포트폴리오",
    "volatility": 0.151,
    "expected_return": 0.112
  },
  "random_portfolios": [
    {
      "volatility": 0.104,
      "expected_return": 0.073
    }
  ],
  "used_fallback": false
}
```

## 4. Efficient Frontier 미리보기

### `GET /portfolio/frontier`

현재 데모 기준 frontier 전체 점과 선택 지점을 반환합니다.

쿼리 파라미터:

- `risk_profile`: `conservative` | `balanced` | `growth`
- `investment_horizon`: `short` | `medium` | `long`
- `target_volatility`: 선택 입력

예시:

```text
GET /portfolio/frontier?risk_profile=balanced&investment_horizon=medium&target_volatility=0.11
```

응답에는 아래 정보가 포함됩니다.

- `portfolio_id`
- `target_volatility`
- `frontier_points`
- `frontier_options`
- `selected_point_index`
- `selected_point`
- `random_portfolios`

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
