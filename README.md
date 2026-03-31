# 자산배분 시뮬레이터 데모

이 프로젝트는 **관리자 유니버스에 등록된 자산군별 후보 종목군**과 **자산군 역할(role)** 을 바탕으로 포트폴리오 컴포넌트를 구성하고, 그 컴포넌트 유니버스로 Efficient Frontier를 계산해 보여주는 FastAPI 데모입니다.

핵심은 두 단계입니다.

1. 자산군 카탈로그와 역할 정의를 기준으로 포트폴리오 컴포넌트를 만든다.
2. 그렇게 만들어진 컴포넌트 유니버스로 Efficient Frontier를 계산한다.

즉 현재 서비스는:

- 관리자는 `/admin`에서 자산군별 후보 종목을 관리합니다.
- 유니버스는 Postgres에 버전 단위로 저장되고 `active` 버전이 계산 기준이 됩니다.
- 가격 데이터는 `yfinance`로 적재합니다.
- 시뮬레이터는 active 유니버스의 **자산군 역할 정의**를 먼저 해석한 뒤, 그 결과 컴포넌트들로 최적화를 수행합니다.
- 화면은 계산 결과를 자산군 기준으로 다시 합산해서 보여줍니다.
- 현재 메인 화면 입력은 `목표 기대수익률 슬라이더` 중심으로 단순화되어 있습니다.

## 현재 시스템 한 줄 요약

`자산군 카탈로그/역할 정의 -> 후보 종목 관리 -> 가격 적재 -> 역할 기반 컴포넌트 구성 -> Efficient Frontier 계산 -> 자산군 기준 UI 표시`

## 현재 상태

현재 기준으로 이 프로젝트는 아래 단계까지 반영돼 있습니다.

- FastAPI 기반 API + 웹 UI 구성
- `/admin` 관리자 콘솔
- Postgres 기반 유니버스 버전 저장/활성화
- `yfinance` 기반 가격 적재
- 가격 적재 실패 상세 확인
- 시뮬레이션 준비 상태 점검
- 역할 기반 포트폴리오 컴포넌트 생성 로직
- 종목 단위 Efficient Frontier 계산
- 자산군 카탈로그/역할 메타데이터 로딩
- 관리자 유니버스 CRUD

## 자산군 카탈로그와 역할 템플릿

현재 구조는 자산군과 역할을 분리합니다.

- 자산군 카탈로그: `app/data/asset_universe.json`
- 역할 템플릿: `app/data/asset_role_templates.json`
- 역할 해석 계층: `app/services/portfolio_component_service.py`

현재 지원하는 역할은 아래와 같습니다.

- `single_representative`
  - 후보 종목 중 대표 종목 1개를 선택합니다.
- `dividend_representative`
  - 후보 종목 중 대표 종목 1개를 선택하고, Black-Litterman prior 기대수익률 위에 배당 보정치를 더합니다.
- `equal_weight_basket`
  - 후보 종목 전체를 동일비중 바스켓으로 묶어 하나의 컴포넌트로 사용합니다.

중요한 점:

- 현재 기본 카탈로그는 역할을 혼합해서 사용합니다.
- `short_term_bond`는 `dividend_representative`로 두고 `BND`의 최근 1년 배당수익률을 우선 참조합니다. 조회가 실패하면 기본 보정치 `2%p`를 fallback으로 사용합니다.
- `cash_equivalents`도 `dividend_representative`로 두고 `BIL`의 최근 1년 배당수익률을 우선 참조합니다. 조회가 실패하면 기본 보정치 `1%p`를 fallback으로 사용합니다.
- `new_growth`는 표시명 `신성장주`로 노출되며 `equal_weight_basket`으로 동작합니다.
- 현재 기본 자산군 카탈로그는 `미국 가치주 / 미국 성장주 / 신성장주 / 단기 채권 / 현금성자산 / 금 / 인프라 채권` 7개입니다.
- 나머지 자산군은 기본적으로 `single_representative`를 사용합니다.
- 구조상 역할 수와 자산군 수는 늘릴 수 있습니다.
- 관리자 콘솔의 자산군 목록도 이 카탈로그를 읽어 동적으로 렌더링됩니다.

## 현재 계산 로직

현재 런타임의 실제 계산 흐름은 아래와 같습니다.

1. `/admin`에서 자산군별 후보 종목을 등록합니다.
2. 저장된 유니버스 버전 중 하나를 `active`로 설정합니다.
3. active 유니버스 종목의 가격 이력을 `yfinance`로 적재합니다.
4. 가격 이력으로 종목별 수익률 행렬을 만듭니다.
   이때 실제 최적화와 히스토리 차트는 유니버스 내에서 가장 늦게 시작한 종목 기준의 **공통 가격 구간**만 사용합니다.
5. 각 자산군의 `role_key`에 따라 포트폴리오 컴포넌트 후보를 만듭니다.
6. `single_representative`면 후보 종목별 후보를 만들고, `equal_weight_basket`이면 전체 종목을 하나의 바스켓으로 묶습니다.
   `dividend_representative`는 대표 종목 1개를 선택하되, 설정된 배당 보정치를 기대수익률에 더합니다.
7. 선택된 컴포넌트 수익률로 연환산 공분산을 계산하고, 시가총액 기반 prior weight를 구합니다.
8. 기대수익률은 Black-Litterman prior `Pi = delta * Sigma * w_prior`로 계산합니다.
   - 현재 `delta`는 `2.5` 고정값을 사용합니다.
   - subjective views(`P`, `Q`)는 아직 적용하지 않으므로 posterior는 prior와 같습니다.
   - 시가총액을 구하지 못하면 equal-weight prior로 fallback 합니다.
9. 조합 수가 작으면 전수 탐색하고, 크면 고정 seed 기반 샘플링을 수행합니다.
10. 각 조합에 대해 최대 Sharpe 포트폴리오를 계산합니다.
11. 가장 좋은 Sharpe를 만든 컴포넌트 조합을 선택합니다.
12. 선택된 조합으로 Efficient Frontier 전체를 계산합니다.
13. 최종 결과를 자산군 비중과 자산군 리스크 기여도로 다시 합산해 화면에 보여줍니다.

## 현재 기대수익률 모델

현재 서비스는 경로에 따라 기대수익률 모델이 다릅니다.

- `asset_assumptions` 모드
  - `sample_market_assumptions.json`의 기대수익률을 그대로 사용합니다.
- `managed_universe` / `stock_combination_demo` 모드
  - 역할 기반 컴포넌트 수익률을 입력으로 받아 **Black-Litterman market-implied prior**를 계산합니다.
  - prior weight는 각 컴포넌트의 시가총액 비중입니다.
  - `equal_weight_basket`은 바스켓 구성 종목들의 시가총액을 합산해 prior weight를 만듭니다.
  - `dividend_representative`는 BL prior 기대수익률에 배당 보정치를 추가로 더합니다.

## 현재 제약조건

현재 서비스는 아래 제약을 사용합니다.

- long-only
- 종목 최소 비중 `1%`
- 종목 최대 비중 `40%`
- 평균 종목 상관관계 상한 `0.25`
- 최소 수익률 이력 `252` 영업일

여기서 중요한 점은:

- **자산군 cap은 별도로 두지 않습니다.**
- 대신 자산군 역할이 포트폴리오 구성 방식을 결정합니다.
- `single_representative`는 대표 종목 1개를 고르고, `equal_weight_basket`은 여러 종목을 동일비중으로 묶습니다.

## 계층 구조

큰 경계는 아래처럼 나뉩니다.

### 1. Presentation Layer

- 메인 시뮬레이터 UI: `app/web.py`
- 관리자 콘솔 UI: `app/admin_web.py`

역할:

- 사용자 입력 수집
- 차트/카드 렌더링
- 관리자 유니버스 관리
- 가격 갱신 실행과 상태 확인
- 자산군 카탈로그/역할 정보 표시

### 2. API Layer

- 라우터: `app/api/router.py`
- 포트폴리오 API: `app/api/routes/portfolio.py`
- 관리자 API: `app/api/routes/admin.py`
- 헬스체크: `app/api/routes/health.py`
- 요청/응답 스키마: `app/api/schemas/*`

역할:

- 입력 검증
- 응답 직렬화
- 관리자/시뮬레이터 엔드포인트 노출

### 3. Service Layer

- 포트폴리오 orchestration: `app/services/portfolio_service.py`
- 역할 기반 컴포넌트 생성: `app/services/portfolio_component_service.py`
- 관리자 유니버스: `app/services/managed_universe_service.py`
- 가격 적재: `app/services/price_refresh_service.py`
- 티커 검색/자동채움: `app/services/ticker_discovery_service.py`
- 설명 문구: `app/services/explanation_service.py`
- 위험성향 매핑: `app/services/mapping_service.py`

역할:

- active 유니버스 불러오기
- 준비 상태 점검
- 역할 기반 컴포넌트 조합 탐색
- 최종 Efficient Frontier 계산 연결
- 프론트용 응답 조립

### 4. Engine Layer

- 제약조건: `app/engine/constraints.py`
- 공분산: `app/engine/covariance.py`
- 기대수익률: `app/engine/returns.py`
- 최적화: `app/engine/optimizer.py`
- 포트폴리오 수학: `app/engine/math.py`
- frontier 옵션: `app/engine/frontier.py`

역할:

- 기대수익률 계산
- 공분산 계산
- 최대 Sharpe 포트폴리오 계산
- Efficient Frontier 계산
- 리스크 기여도 계산

### 5. Data / Infra Layer

- 관리자 저장소: `app/data/managed_universe_repository.py`
- 종목 데이터 파싱: `app/data/stock_repository.py`
- 자산군 메타데이터: `app/data/asset_universe.json`
- 역할 템플릿 메타데이터: `app/data/asset_role_templates.json`
- 데모 데이터: `app/data/demo/*`
- 환경 설정: `app/core/config.py`
- 배포 설정: `railway.json`

역할:

- 유니버스 버전 저장
- 가격 이력 저장
- 종목 수익률 생성
- 자산군/역할 카탈로그 로딩
- 환경 변수/배포 설정 관리

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
- `GET /admin/universe/versions/{version_id}`
- `POST /admin/universe/versions`
- `PUT /admin/universe/versions/{version_id}`
- `DELETE /admin/universe/versions/{version_id}`
- `POST /admin/universe/versions/{version_id}/activate`
- `GET /admin/universe/readiness`
- `POST /admin/prices/refresh`
- `GET /admin/prices/status`
- `GET /admin/prices/jobs/{job_id}/items`
- `GET /admin/tickers/search`
- `GET /admin/tickers/lookup`

세부 응답 형식은 `docs/API_REFERENCE.md`를 참고하세요.

## 관리자 콘솔에서 가능한 작업

`/admin`에서는 아래 작업을 할 수 있습니다.

- 자산군별 후보 종목 등록/삭제
- 자산군 역할 정보 확인
- 티커 검색
- 티커 자동채움
- 유니버스 버전 생성
- 유니버스 버전 수정/삭제
- active 버전 전환
- 가격 데이터 갱신
- 최근 가격 갱신 상세 확인
- 시뮬레이션 준비 상태 점검

## 실행 방법

### 로컬 실행

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

### 환경 변수

```bash
export DATABASE_URL="postgresql://..."
```

`DATABASE_URL`이 없으면:

- 관리자 유니버스 저장
- 가격 적재
- active 유니버스 기반 시뮬레이션

은 사용할 수 없고, 일부 경로는 내장 데모 유니버스로 fallback 합니다.

## Railway 배포 메모

기본 구성:

- Web Service 1개
- Postgres 1개
- `Root Directory = fastapi-demo`
- `DATABASE_URL` 연결
- `Healthcheck Path = /health`

배포 후 확인 URL:

- `/`
- `/admin`
- `/docs`
- `/health`

## 방향성

현재 구조는 “자산군 카탈로그/역할 정의 + 후보 종목 관리 + 역할 기반 컴포넌트 선택 + Sharpe 기반 최적화” 단계입니다.

다음 단계는 보통 아래 순서가 자연스럽습니다.

1. 자산군 카탈로그 자체 CRUD
2. 역할 템플릿 편집 UI
3. 가격 갱신 배치 자동화
4. 역할별 계산 전략 고도화
5. Black-Litterman subjective views(P/Q) 도입

## 관련 문서

- 아키텍처: `docs/ARCHITECTURE.md`
- API 명세: `docs/API_REFERENCE.md`
- 데모 가이드: `docs/DEMO_GUIDE.md`
- 종목 데이터 가이드: `docs/STOCK_DATA_GUIDE.md`
- 조합 탐색 가이드: `docs/COMBINATION_SEARCH_GUIDE.md`
- 리서치 데이터 요청서: `docs/RESEARCH_DATA_REQUEST.txt`
