# 아키텍처 문서

## 시스템 목표

현재 시스템 목표는 아래 문장으로 설명하는 것이 가장 정확합니다.

> 관리자 유니버스에 등록된 자산군별 후보 종목군과 자산군 역할 정의를 기준으로, 역할 기반 포트폴리오 컴포넌트를 만들고 Sharpe Ratio가 우수한 구조를 찾아 Efficient Frontier 상의 포트폴리오를 계산하고 설명하는 시뮬레이션 서비스

즉 이 시스템은:

- 실거래 시스템이 아닙니다.
- 투자 추천 AI가 아닙니다.
- 종목 리서치 보고서를 자동 생성하는 시스템이 아닙니다.
- **역할 기반 컴포넌트 구성 + 포트폴리오 최적화**를 설명하는 데모입니다.

## 최상위 구조

현재 구조는 아래 6개 경계로 이해하면 됩니다.

### 1. Presentation Layer

- `app/web.py`
- `app/admin_web.py`

역할:

- 메인 시뮬레이터 UI
- 관리자 콘솔 UI
- 결과 카드/차트 렌더링
- 관리자 입력/가격 갱신 실행
- 자산군 카탈로그와 역할 정보 표시

### 2. API Layer

- `app/api/router.py`
- `app/api/routes/portfolio.py`
- `app/api/routes/admin.py`
- `app/api/routes/health.py`
- `app/api/schemas/request.py`
- `app/api/schemas/response.py`

역할:

- 입력 검증
- 응답 모델 직렬화
- 관리자/시뮬레이터 엔드포인트 분리

### 3. Application / Service Layer

- `app/services/portfolio_service.py`
- `app/services/portfolio_component_service.py`
- `app/services/managed_universe_service.py`
- `app/services/price_refresh_service.py`
- `app/services/ticker_discovery_service.py`
- `app/services/mapping_service.py`
- `app/services/explanation_service.py`

역할:

- active 유니버스 조회
- 가격 적재 orchestration
- 준비 상태 점검
- 역할 기반 컴포넌트 조합 탐색
- 선택된 조합을 기반으로 최종 frontier 계산
- 응답용 설명/요약 생성

### 4. Engine Layer

- `app/engine/constraints.py`
- `app/engine/covariance.py`
- `app/engine/returns.py`
- `app/engine/optimizer.py`
- `app/engine/math.py`
- `app/engine/frontier.py`

역할:

- 기대수익률 계산
- 공분산 계산
- 최대 Sharpe 포인트 계산
- Efficient Frontier 계산
- 리스크 기여도 계산

### 5. Data Layer

- `app/data/managed_universe_repository.py`
- `app/data/stock_repository.py`
- `app/data/asset_universe.json`
- `app/data/asset_role_templates.json`
- `app/data/demo/*`

역할:

- 관리자 유니버스 버전 저장
- 가격 이력 저장
- 종목 수익률 생성
- 자산군/역할 카탈로그 제공
- 데모 fallback 데이터 제공

### 6. Config / Infra Layer

- `app/core/config.py`
- `railway.json`
- `requirements.txt`

역할:

- 환경 변수
- 제약 파라미터
- 배포 설정

## 자산군과 역할을 왜 분리했나

현재 시스템은 아래 두 가지가 따로 변할 수 있다고 봅니다.

- 자산군 목록
- 자산군이 포트폴리오에 들어가는 방식

그래서:

- 자산군은 `asset_universe.json`
- 역할은 `asset_role_templates.json`
- 실제 해석은 `PortfolioComponentService`

로 분리했습니다.

이 구조의 장점:

- 자산군 수가 늘어나도 카탈로그 row 추가로 대응 가능
- 역할 수가 3개에서 4개 이상으로 늘어나도 템플릿/전략 추가로 대응 가능
- 관리자 콘솔과 메인 화면이 같은 카탈로그를 읽으므로 하드코딩 의존이 줄어듭니다

## 현재 지원하는 역할

### `single_representative`

- 후보 종목 중 대표 종목 1개를 선택
- `selection_mode = single_representative`
- `weighting_mode = single`

### `dividend_representative`

- 후보 종목 중 대표 종목 1개를 선택
- 기대수익률 계산 시 `expected_return_adjustment`를 가산
- 배당 성격을 반영하고 싶은 자산군을 위한 역할

### `equal_weight_basket`

- 후보 종목 전체를 하나의 동일비중 바스켓으로 사용
- `selection_mode = all_members`
- `weighting_mode = equal_weight`

중요:

- 현재 기본 자산군 카탈로그는 모두 `single_representative`입니다.
- 하지만 런타임은 이미 세 역할을 모두 이해하도록 구현돼 있습니다.

## 현재 핵심 계산 구조

현재 계산은 “자산군 역할 해석 -> 컴포넌트 조합 탐색 -> Efficient Frontier 계산” 구조입니다.

1. 자산군별 후보 종목군 확보
2. 각 자산군의 역할을 읽음
3. 역할에 따라 포트폴리오 컴포넌트 후보 생성
4. 컴포넌트 조합마다 최대 Sharpe 포인트 계산
5. 가장 좋은 조합 선택
6. 선택된 조합으로 Efficient Frontier 전체 계산
7. 화면에서는 결과를 자산군 비중으로 다시 묶어 표시

즉 계산 단위와 화면 표시 단위는 다릅니다.

- 계산 단위: 역할 기반 컴포넌트
- 화면 표시 단위: 자산군

## 역할 해석 계층

`PortfolioComponentService`가 자산군 메타데이터를 실제 optimizer 입력으로 바꾸는 경계입니다.

이 계층이 하는 일:

1. 자산군별 종목 후보 수집
2. 역할에 따라 후보 생성
3. 단일 대표 종목이면 후보 종목별 후보 생성
4. 동일비중 바스켓이면 하나의 바스켓 후보 생성
5. 최종 선택 결과를 다시 실제 종목 weight로 explode

즉 optimizer는 역할을 직접 모르고, 이미 만들어진 컴포넌트 수익률/weight만 받습니다.

## 관리자 유니버스 흐름

현재 관리자 유니버스는 아래 흐름으로 운용됩니다.

1. `/admin`에서 자산군별 후보 종목 입력
2. 유니버스 버전 저장
3. 특정 버전을 `active`로 전환
4. `yfinance`에서 가격 적재
5. readiness 점검
6. 메인 시뮬레이터에서 active 버전 사용

이때 유니버스는 Postgres에 버전 단위로 저장되므로, 입력값 변경과 계산 기준을 분리할 수 있습니다.

## 공통 가격 구간 정책

유니버스 안 종목들의 가격 이력이 서로 다를 수 있으므로, 실제 계산은 아래 기준을 사용합니다.

- raw 가격은 길게 적재
- 계산과 히스토리 차트는 **가장 늦게 시작한 종목 기준의 공통 구간**만 사용

예를 들어 8종목 중 1종목이 1년치만 있으면, 그 유니버스의 frontier도 1년 공통 구간 기준으로 계산합니다.

## 현재 제약조건

현재 기본 제약은 아래와 같습니다.

- long-only
- 종목 최소 비중 `1%`
- 종목 최대 비중 `50%`
- 평균 종목 상관관계 상한 `0.25`
- 최소 유효 수익률 이력 `252` 영업일

### 왜 평균 상관관계 상한을 두는가

Sharpe Ratio를 기본 목표로 유지하되, 지나치게 비슷하게 움직이는 종목들로만 포트폴리오가 구성되는 것을 줄이기 위해서입니다.

즉 현재 구조는:

- 기본 목표: Sharpe 최대화
- 보조 제약: 평균 상관관계 상한

입니다.

## 상관관계는 어떻게 반영되나

이 서비스는 상관관계를 별도 입력받지 않습니다.

흐름:

1. 가격 이력 적재
2. 가격 -> 일간 수익률
3. 수익률 -> 공분산 / 상관관계 계산
4. `w^T Σ w`로 포트폴리오 변동성 계산

즉 상관관계는 실제 가격 이력에서 통계적으로 추정해 Efficient Frontier 안에 반영됩니다.

## 응답 구조 설계

현재 응답에서 중요한 구분은 아래입니다.

- `weights`: 화면 표시용 자산군 합산 비중
- `allocations`: 자산군별 비중 / 리스크 기여도
- `frontier_points[*].weights`: 선택된 컴포넌트 조합 기준 실제 종목 가중치
- `selected_combination`: 자산군별로 어떤 종목 멤버가 현재 컴포넌트에 사용됐는지

즉 한 응답 안에:

- 계산에 쓰인 종목 레벨 정보
- 화면에 보여줄 자산군 레벨 정보

가 함께 들어 있습니다.

## 현재 설계의 장점

- 자산군 카탈로그와 역할을 분리해 확장성이 높음
- 관리자 입력과 계산 기준이 버전으로 분리됨
- 가격 적재와 시뮬레이션이 분리됨
- 역할 해석 단계와 frontier 계산 단계가 분리됨
- API / 서비스 / 엔진 / 저장소 경계가 비교적 명확함

## 현재 설계의 한계

- 자산군 카탈로그 자체 CRUD는 아직 없음
- 역할 템플릿 편집 UI는 아직 없음
- 현재 기본 카탈로그가 모두 대표 종목 역할이라 혼합 역할 사례는 아직 제한적
- 역할이 늘어나면 `PortfolioComponentService` 전략도 함께 확장해야 함

## 향후 방향

1. 자산군 카탈로그 CRUD
2. 역할 템플릿 관리 UI
3. 역할별 고급 전략 분리
4. 기대수익률 모델 고도화
5. 장시간 배치 탐색/사전 계산 도입
