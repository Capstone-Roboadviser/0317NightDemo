# Demo Guide

## 이 프로젝트가 하는 일

이 프로젝트는 투자 예측 엔진이 아니라, 자산배분 데모 엔진입니다.

즉:

- 어떤 종목이 오를지 맞히는 모델이 아닙니다.
- 위험과 수익 구조를 바탕으로 포트폴리오 예시를 계산합니다.
- 발표나 시연에서 안정적으로 동작하도록 샘플 데이터를 사용합니다.

## 왜 이런 구조로 만들었나

노트북 코드는 보통 셀 실행 순서와 전역변수에 많이 의존합니다.
서비스로 옮길 때는 이런 구조가 가장 먼저 문제가 됩니다.

그래서 아래처럼 역할을 나눴습니다.

### `data_service.py`

- 데모용 샘플 가격 데이터를 만듭니다.
- 랜덤 시드를 고정해서 결과가 항상 같게 유지됩니다.

### `risk_model.py`

- 일별 수익률로부터 기대수익률과 공분산을 계산합니다.
- 공분산은 약간 shrinkage를 넣어 더 안정적으로 만듭니다.

### `optimizer.py`

- Efficient Frontier를 계산합니다.
- 목표 변동성과 가장 가까운 포트폴리오를 선택합니다.
- 최적화가 실패하면 fallback 비중을 반환합니다.

### `engine.py`

- 요청을 받아 전체 흐름을 조립합니다.
- 프론트엔드에서 쓰기 쉬운 JSON 구조로 변환합니다.

### `routes.py`

- FastAPI 엔드포인트를 제공합니다.

## 데모에서 추천하는 입력값

### 보수형

```json
{
  "risk_profile": "conservative",
  "investment_horizon": "short"
}
```

### 균형형

```json
{
  "risk_profile": "balanced",
  "investment_horizon": "medium"
}
```

### 성장형

```json
{
  "risk_profile": "growth",
  "investment_horizon": "long"
}
```

## 발표할 때 설명 문구 예시

- "이 서비스는 시장 방향을 예측하는 AI가 아니라, 자산군의 위험-수익 구조를 바탕으로 포트폴리오 예시를 계산하는 데모입니다."
- "실시간 시세 대신 재현 가능한 샘플 데이터를 사용해 발표 중 결과가 흔들리지 않도록 했습니다."
- "입력값은 단순하지만 내부적으로는 기대수익률, 공분산, 제약조건, Efficient Frontier 계산을 거칩니다."

## 가장 쉬운 실행 방법

```bash
cd "/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo"
source .venv/bin/activate
uvicorn app.main:app --reload
```

그다음 `http://127.0.0.1:8000/docs` 에서 바로 테스트하면 됩니다.
