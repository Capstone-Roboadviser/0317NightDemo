# 데모 가이드

## 이 데모가 보여주는 것

이 서비스는 투자 예측을 보여주는 데모가 아니라, 자산배분 구조를 설명하는 데모입니다.

사용자는:

1. 위험 성향을 고릅니다.
2. 투자기간을 고릅니다.
3. 필요하면 목표 변동성을 직접 입력합니다.
4. 시스템은 효율적 투자선 위의 포트폴리오 예시를 계산합니다.
5. 화면은 현재 포트폴리오 포인트, 비중, 리스크 기여도, 설명 문장을 보여줍니다.

## 발표할 때 강조하면 좋은 메시지

- "이 서비스는 실시간 투자 추천이 아니라 자산배분 시뮬레이션입니다."
- "관리자 유니버스가 있으면 그 버전 기준으로, 없으면 내장 데모 데이터 기준으로 계산합니다."
- "결과는 버전 관리된 입력 데이터를 기준으로 계산되므로 시연 중에도 재현성이 유지됩니다."
- "핵심은 숫자 자체보다, 현재 포트폴리오가 효율적 투자선 위의 어떤 지점에 있는지 보여주는 것입니다."

## 화면에서 꼭 보여줘야 할 순서

1. 위험 선택
2. Efficient Frontier 그래프
3. 현재 포트폴리오 포인트
4. 자산군별 비중
5. 리스크 기여도
6. 설명 문장

## 추천 입력값

### 안정형

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

## 시연 전 체크리스트

- `/health`가 `{"status":"ok"}` 를 반환하는지 확인
- `DATABASE_URL`이 있으면 `/admin/universe/status`에서 활성 버전이 보이는지 확인
- `/admin`에서 수기 유니버스를 만들 수 있는지 확인
- 필요하면 `/admin/prices/refresh`로 가격 갱신 후 `/admin/prices/status`에서 최근 잡 상태 확인
- `/portfolio/assets`에서 8개 자산군이 정상적으로 보이는지 확인
- 메인 페이지에서 차트와 카드가 정상 렌더링되는지 확인
- 위험 슬라이더를 움직였을 때 포트폴리오 포인트가 바뀌는지 확인

## 실행 방법

```bash
cd "/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo"
source .venv/bin/activate
uvicorn app.main:app --reload
```

접속:

- 웹 화면: `http://127.0.0.1:8000/`
- API 문서: `http://127.0.0.1:8000/docs`
