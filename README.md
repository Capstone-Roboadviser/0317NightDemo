# 자산배분 시뮬레이터 데모

이 프로젝트의 목표는 아래 한 문장으로 정리됩니다.

> 고정된 8개 자산군을 기준으로, 사용자의 위험 성향과 투자기간에 따라 Efficient Frontier 상의 포트폴리오 예시를 계산하고 설명해주는 시뮬레이션 서비스

즉 이 서비스는:

- 실거래 시스템이 아닙니다.
- 투자 예측 AI가 아닙니다.
- 종목 추천 시스템이 아닙니다.
- 자산배분 엔진 데모입니다.

결과는 샘플 데이터 기반의 교육용/연구용/데모용 예시이며, 투자 자문이 아닙니다.

## 빠른 실행

```bash
cd "/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

실행 후 접속 주소:

- 웹 화면: `http://127.0.0.1:8000/`
- Swagger 문서: `http://127.0.0.1:8000/docs`
- 헬스체크: `http://127.0.0.1:8000/health`

## 핵심 기능

- 8개 자산군 기반 시뮬레이션
- 기본 계산 경로: `관리자 종목 유니버스`
- 대체 계산 경로: `개별주식 조합 데모`
- 위험 성향 3단계: `안정형`, `균형형`, `성장형`
- 투자기간 반영: `단기`, `중기`, `장기`
- 목표 변동성 선택 입력 지원
- Efficient Frontier 계산
- 현재 포트폴리오 포인트 선택
- 자산군별 비중과 리스크 기여도 설명
- 데모용 설명 문장 자동 생성

## 현재 자산군

- `bond`: 채권
- `real_assets`: 실물
- `etf`: ETF
- `tech_healthcare`: 기술주 및 헬스케어
- `ai_semiconductor_social`: AI반도체 및 소셜미디어
- `financials`: 금융
- `energy`: 에너지
- `consumer_other`: 소비재 및 기타

## API 개요

### `POST /portfolio/simulate`

사용자의 위험 성향과 투자기간을 받아 포트폴리오 예시를 계산합니다.

### `GET /portfolio/frontier`

현재 데모 기준 Efficient Frontier 포인트와 선택 지점을 반환합니다.

### `GET /portfolio/assets`

고정 자산군 목록을 반환합니다.

### `GET /health`

서버 상태 확인용입니다.

자세한 예시는 [API_REFERENCE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/API_REFERENCE.md)를 참고하세요.

## 구조 요약

이번 버전은 아래 6계층으로 나눠져 있습니다.

1. Presentation Layer
2. API Layer
3. Application Layer
4. Portfolio Engine Layer
5. Data Layer
6. Config / Ops Layer

실제 폴더 구조는 아래와 같습니다.

```text
app/
  api/
    router.py
    routes/
      health.py
      portfolio.py
      web.py
    schemas/
      request.py
      response.py
  core/
    config.py
  data/
    asset_universe.json
    sample_market_assumptions.json
    repository.py
  domain/
    enums.py
    models.py
  engine/
    constraints.py
    covariance.py
    frontier.py
    math.py
    optimizer.py
    returns.py
  services/
    explanation_service.py
    mapping_service.py
    portfolio_service.py
  main.py
  web.py
docs/
  API_REFERENCE.md
  ARCHITECTURE.md
  DEMO_GUIDE.md
```

아키텍처 설명은 [ARCHITECTURE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/ARCHITECTURE.md)에 정리했습니다.

## 데이터 설계

이 프로젝트는 기본적으로 `관리자 유니버스 + 누적 가격 이력` 구조를 사용합니다.

- 종목 유니버스 버전과 가격 이력은 Postgres에 저장
- `DATABASE_URL`이 있으면 관리자 입력 기반으로 계산
- 아직 활성화된 관리자 버전이 없으면, 내장 데모 CSV로 자동 대체

정적 자산군 정의 파일은 계속 사용합니다.

- [asset_universe.json](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/asset_universe.json)
- [sample_market_assumptions.json](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/sample_market_assumptions.json)

## 관리자 유니버스와 개별 주식 조합

현재 API는 두 가지 계산 경로를 지원합니다.

- 기본 경로: Postgres에 저장된 `관리자 종목 유니버스`
- 대체 경로: 내장 `개별주식 조합 데모`

관련 파일:

- [stock_repository.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/stock_repository.py)
- [managed_universe_repository.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/managed_universe_repository.py)
- [combination_search_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/combination_search_service.py)
- [managed_universe_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/managed_universe_service.py)
- [generate_demo_stock_data.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/scripts/generate_demo_stock_data.py)
- [stock_universe_template.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/templates/stock_universe_template.csv)
- [stock_prices_template.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/templates/stock_prices_template.csv)
- [demo_stock_universe.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_universe.csv)
- [demo_stock_prices.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_prices.csv)

운영 흐름은 이렇습니다.

- `/admin/universe/versions`로 관리자 수기 입력 버전 생성
- active 버전이 생기면 `/portfolio/*`가 해당 유니버스를 기준으로 계산
- `/admin/prices/refresh`로 active 유니버스 가격 데이터를 yfinance에서 수집
- active 버전이 없으면 내장 데모 CSV를 대신 사용

필수 환경변수:

```bash
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

가격 갱신은 기본적으로 `incremental` 모드로 돌리는 것을 권장합니다.

- `incremental`: 기존 마지막 저장일 이후만 증분 수집
- `full`: 지정 연수만큼 전체 백필

## Railway 배포

이 프로젝트는 Railway 배포를 위한 설정 파일을 포함합니다.

- [railway.json](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/railway.json)

기본 시작 명령:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

배포 시 권장 확인 항목:

- Public Domain 포트가 실제 앱 포트와 일치하는지 확인
- Healthcheck Path를 `/health`로 설정
- GitHub push 후 Railway redeploy 확인

## 문서 목록

- 아키텍처: [ARCHITECTURE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/ARCHITECTURE.md)
- API 명세: [API_REFERENCE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/API_REFERENCE.md)
- 데모 설명: [DEMO_GUIDE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/DEMO_GUIDE.md)
- 개별 주식 데이터 준비: [STOCK_DATA_GUIDE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/STOCK_DATA_GUIDE.md)
- 조합 탐색 가이드: [COMBINATION_SEARCH_GUIDE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/COMBINATION_SEARCH_GUIDE.md)
