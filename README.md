# RoboAdviser Demo API

이 프로젝트는 노트북 기반 Efficient Frontier 실험 코드를, 데모용 FastAPI 서비스 구조로 재정리한 예시입니다.

중요한 점:

- 이 서비스는 시장을 예측하는 AI가 아닙니다.
- 이 서비스는 자산배분 시뮬레이션 데모입니다.
- 실시간 시세 대신 재현 가능한 샘플 데이터를 사용합니다.
- 결과는 교육용/연구용/데모용 예시이며 투자 자문이 아닙니다.

## 1. 프로젝트 목적

사용자가 `위험성향`, `투자기간`, `목표 변동성`을 입력하면:

- 고정된 5개 자산군을 기준으로
- 기대수익률과 공분산을 계산하고
- Efficient Frontier 위에서
- 데모용 포트폴리오 비중을 반환합니다.

자산군은 서버에서 고정합니다.

- `us_equity`
- `global_bond`
- `reit`
- `gold`
- `cash`

## 2. 폴더 구조

```text
app/
  api/
    routes.py
  services/
    data_service.py
    risk_model.py
    optimizer.py
    explainer.py
    engine.py
    universe.py
  main.py
  schemas.py
README.md
requirements.txt
```

## 3. 설치

```bash
cd "/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. 실행

```bash
uvicorn app.main:app --reload
```

브라우저에서 아래 주소를 열면 됩니다.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 5. 주요 API

### `GET /health`

서버 상태 확인용입니다.

### `GET /v1/assets`

고정 자산군 목록을 반환합니다.

### `POST /v1/portfolio/recommend`

포트폴리오 계산 요청입니다.

예시 요청:

```json
{
  "risk_profile": "balanced",
  "investment_horizon": "medium",
  "target_volatility": 0.11
}
```

예시 응답:

```json
{
  "disclaimer": "Demo only. This API simulates asset allocation using sample data and does not predict markets or provide investment advice.",
  "summary": "This demo allocation targets about 11.0% annual volatility and lands at 10.8% expected volatility with 5.7% expected return.",
  "target_volatility": 0.11,
  "metrics": {
    "expected_return": 0.057,
    "volatility": 0.108,
    "sharpe_ratio": 0.343
  },
  "allocations": [
    {
      "asset_code": "us_equity",
      "asset_name": "US Equity",
      "weight": 0.34
    }
  ],
  "frontier": [
    {
      "volatility": 0.07,
      "expected_return": 0.04
    }
  ]
}
```

## 6. 설계 원칙

- 노트북 셀 순서 의존성을 제거했습니다.
- 전역변수 대신 명시적 입력과 반환값을 사용합니다.
- 외부 시세 API를 호출하지 않습니다.
- 같은 입력에는 같은 결과가 나오도록 결정론적으로 구성했습니다.
- 최적화 실패 시 설명 가능한 fallback 결과를 반환합니다.

## 7. 데모에서 보여주기 좋은 포인트

- `risk_profile`만 바꿔도 비중이 달라집니다.
- `target_volatility`를 주면 프론티어 위 다른 점을 선택할 수 있습니다.
- 응답이 단순해서 프론트엔드 카드/차트 연결이 쉽습니다.

## 8. 다음 확장 아이디어

- 샘플 데이터 대신 캐시된 ETF 가격 데이터 사용
- 프론트엔드 대시보드 연결
- 사용자별 세션 저장
- 간단한 백테스트 API 추가

추가 설명은 [docs/DEMO_GUIDE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/DEMO_GUIDE.md)에 정리했습니다.
