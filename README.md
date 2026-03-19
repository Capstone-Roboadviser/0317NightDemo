# 자산배분 시뮬레이터 데모

관리자 입력 기반의 종목 유니버스를 기준으로, 종목 가격 이력을 적재한 뒤 **종목 단위 Efficient Frontier**를 계산하고, 결과를 **섹터 기준으로 다시 묶어 보여주는** FastAPI 데모입니다.

현재 서비스의 핵심은 다음과 같습니다.

- 관리자는 `/admin`에서 섹터별 종목 후보를 직접 관리합니다.
- 저장된 유니버스는 Postgres에 버전 단위로 보관되고 `active` 버전이 계산 기준이 됩니다.
- 백엔드는 `yfinance`로 가격 이력을 적재합니다.
- 시뮬레이터는 **자산군이 아니라 전체 종목 유니버스**를 직접 최적화합니다.
- 화면에서는 계산 결과를 섹터별 비중과 리스크 기여도로 다시 묶어서 보여줍니다.

## 현재 상태

현재 기준으로 이 프로젝트는 다음 단계를 완료한 상태입니다.

- FastAPI 기반 API + 웹 데모 구성
- `/admin` 관리자 화면 추가
- Postgres 기반 관리자 유니버스 저장
- `yfinance` 기반 가격 데이터 갱신
- 시뮬레이션 준비 상태 진단(`/admin`)
- 종목 단위 Efficient Frontier 최적화
- 섹터는 분류/표시용 메타데이터로만 사용
- 개별 종목 최대 비중 제한
- 평균 종목 상관관계 상한 제약 추가

## 시스템 한 줄 요약

이 서비스는 아래 흐름으로 동작합니다.

1. 관리자가 섹터별로 종목을 등록한다.
2. 활성 유니버스를 기준으로 가격 데이터를 적재한다.
3. 적재된 가격으로 종목 수익률 행렬을 만든다.
4. 종목 전체를 대상으로 Efficient Frontier를 계산한다.
5. 선택된 종목 비중을 섹터별로 다시 합산해 UI에 표시한다.

즉, 현재 계산 단위는 **종목**, 표시 단위는 **섹터**입니다.

## 계층 구조

큰 경계만 보면 현재 구조는 아래처럼 나뉩니다.

### 1. Presentation Layer

- 사용자 메인 화면: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/web.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/web.py)
- 관리자 화면: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/admin_web.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/admin_web.py)

역할:
- 입력 수집
- 차트와 카드 렌더링
- 관리자 유니버스 관리
- 가격 갱신 실행 및 상태 표시

### 2. API Layer

- 메인 라우터: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/router.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/router.py)
- 포트폴리오 API: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/routes/portfolio.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/routes/portfolio.py)
- 관리자 API: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/routes/admin.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/routes/admin.py)

역할:
- 입력 검증
- 응답 직렬화
- 관리자/시뮬레이터 엔드포인트 노출

### 3. Service Layer

- 포트폴리오 서비스: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/portfolio_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/portfolio_service.py)
- 관리자 유니버스 서비스: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/managed_universe_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/managed_universe_service.py)
- 가격 갱신 서비스: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/price_refresh_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/price_refresh_service.py)
- 티커 검색/자동채움: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/ticker_discovery_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/ticker_discovery_service.py)

역할:
- 관리자 유니버스 버전 관리
- 가격 적재
- 준비 상태 진단
- 시뮬레이션 orchestration

### 4. Engine Layer

- 제약조건: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/constraints.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/constraints.py)
- 공분산: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/covariance.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/covariance.py)
- 기대수익률: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/returns.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/returns.py)
- 최적화: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/optimizer.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/optimizer.py)
- 포트폴리오 수학: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/math.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/math.py)

역할:
- 기대수익률 계산
- 공분산 계산
- Efficient Frontier 계산
- Sharpe Ratio 계산
- 리스크 기여도 계산

### 5. Data Layer

- 관리자 유니버스 저장소: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/managed_universe_repository.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/managed_universe_repository.py)
- 종목 데이터 파싱/수익률 생성: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/stock_repository.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/stock_repository.py)
- 정적 자산군 메타데이터: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/asset_universe.json](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/asset_universe.json)
- 데모용 종목/가격 데이터: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_universe.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_universe.csv), [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_prices.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_prices.csv)

역할:
- 유니버스 버전 저장
- 가격 이력 누적 저장
- 종목 수익률 생성
- 데모 fallback 데이터 제공

## 현재 계산 로직

현재 시뮬레이터는 아래 순서로 계산합니다.

1. `active` 관리자 유니버스를 읽습니다.
2. 해당 종목의 가격 이력을 Postgres에서 조회합니다.
3. 가격 이력으로 종목별 일간 수익률을 생성합니다.
4. 최소 이력 조건을 통과한 종목만 최적화에 사용합니다.
5. 기대수익률과 공분산을 계산합니다.
6. 종목 전체를 대상으로 Efficient Frontier를 계산합니다.
7. 사용자 위험 성향/투자기간에 맞는 포인트를 선택합니다.
8. 선택된 종목 비중을 섹터별로 다시 합산해 화면에 보여줍니다.

### 현재 제약조건

현재 기본 제약은 다음과 같습니다.

- long-only
- 개별 종목 최대 비중 `20%`
- 평균 종목 상관관계 상한 `0.25`
- 최소 유효 이력 `252` 영업일

상관관계는 가격 데이터에서 직접 계산한 종목 수익률 공분산을 통해 반영됩니다. 즉, 별도 입력값이 아니라 **실제 가격 이력으로부터 통계적으로 추정**합니다.

## 주요 엔드포인트

### 사용자/시뮬레이터

- `GET /`
- `GET /health`
- `GET /portfolio/assets`
- `GET /portfolio/stocks`
- `GET /portfolio/frontier`
- `POST /portfolio/simulate`

### 관리자

- `GET /admin`
- `GET /admin/universe/status`
- `GET /admin/universe/versions`
- `GET /admin/universe/versions/active`
- `POST /admin/universe/versions`
- `POST /admin/universe/versions/{version_id}/activate`
- `GET /admin/universe/readiness`
- `POST /admin/prices/refresh`
- `GET /admin/prices/status`
- `GET /admin/prices/jobs/{job_id}/items`
- `GET /admin/tickers/search`
- `GET /admin/tickers/lookup`

API 상세는 [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/API_REFERENCE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/API_REFERENCE.md)를 참고하세요.

## 관리자 화면에서 가능한 작업

`/admin`에서는 다음 작업을 할 수 있습니다.

- 섹터별 종목 추가/삭제
- 티커 검색
- 티커 자동채움
- 유니버스 버전 생성 및 활성화
- 가격 데이터 갱신 실행
- 최근 가격 갱신 실패 상세 확인
- 시뮬레이션 준비 상태 점검

중요:
- 현재는 로그인 없이 열리는 데모용 관리자 화면입니다.
- 공개 배포 환경에서는 누구나 `/admin`에 접근할 수 있으므로, 실제 외부 공개 전에는 최소한의 보호장치가 필요합니다.

## 실행 방법

### 1. 로컬 실행

```bash
cd "/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

접속:

- 웹 화면: `http://127.0.0.1:8000/`
- 관리자 화면: `http://127.0.0.1:8000/admin`
- API 문서: `http://127.0.0.1:8000/docs`

### 2. 환경 변수

현재 실사용 경로에는 Postgres 연결이 필요합니다.

```bash
export DATABASE_URL="postgresql://..."
```

`DATABASE_URL`이 없으면:
- 관리자 유니버스 저장
- 가격 적재
- active 유니버스 기반 시뮬레이션

이 동작들은 사용할 수 없고, 일부 경로는 데모 데이터 fallback으로 동작합니다.

## Railway 배포 메모

기본 구성은 아래처럼 맞추면 됩니다.

- Web Service 1개
- Postgres 1개
- `Root Directory = fastapi-demo`
- `DATABASE_URL` 연결
- `Healthcheck Path = /health`

배포 후 주요 확인 URL:

- `/`
- `/admin`
- `/docs`
- `/health`

## 현재 문서

- 아키텍처 개요: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/ARCHITECTURE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/ARCHITECTURE.md)
- API 명세: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/API_REFERENCE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/API_REFERENCE.md)
- 데모 가이드: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/DEMO_GUIDE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/DEMO_GUIDE.md)
- 리서치 데이터 요청서: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/RESEARCH_DATA_REQUEST.txt](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/RESEARCH_DATA_REQUEST.txt)
- 종목 데이터 가이드: [/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/STOCK_DATA_GUIDE.md](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/docs/STOCK_DATA_GUIDE.md)

## 앞으로 남은 일

현재 기준으로 다음 단계는 아래가 핵심입니다.

- 관리자 유니버스 기반 시뮬레이션을 배포 환경에서 완전히 안정화
- 기대수익률 모델 고도화
- 가격 갱신 자동화 배치 도입
- 관리자 보호장치 추가
- 필요 시 상관관계 제약 및 최적화 전략 고도화

한 줄로 요약하면, 지금 이 프로젝트는 **관리자 유니버스와 실제 가격 데이터를 바탕으로 종목 직접 최적화를 수행하는 자산배분 시뮬레이터**까지는 올라온 상태입니다.
