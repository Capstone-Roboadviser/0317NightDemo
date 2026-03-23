# 아키텍처 문서

## 시스템 목표

현재 시스템 목표는 아래 문장으로 설명하는 것이 가장 정확합니다.

> 관리자 유니버스에 등록된 섹터별 후보 종목군을 기준으로, 각 섹터에서 대표 종목 1개씩을 선택한 조합 중 Sharpe Ratio가 가장 우수한 구조를 찾고, 그 대표 종목 유니버스로 Efficient Frontier 상의 포트폴리오를 계산하고 설명하는 시뮬레이션 서비스

즉 이 시스템은:

- 실거래 시스템이 아닙니다.
- 투자 추천 AI가 아닙니다.
- 종목 리서치 보고서를 자동 생성하는 시스템이 아닙니다.
- **대표 종목 선택 + 포트폴리오 최적화**를 설명하는 데모입니다.

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
- `app/services/managed_universe_service.py`
- `app/services/price_refresh_service.py`
- `app/services/ticker_discovery_service.py`
- `app/services/mapping_service.py`
- `app/services/explanation_service.py`

역할:

- active 유니버스 조회
- 가격 적재 orchestration
- 준비 상태 점검
- 대표 종목 조합 탐색
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
- `app/data/demo/*`

역할:

- 관리자 유니버스 버전 저장
- 가격 이력 저장
- 종목 수익률 생성
- 데모 fallback 데이터 제공

### 6. Config / Infra Layer

- `app/core/config.py`
- `railway.json`
- `requirements.txt`

역할:

- 환경 변수
- 제약 파라미터
- 배포 설정

## 현재 핵심 계산 구조

현재 계산은 “전 종목 직접 최적화”가 아니라 아래 구조입니다.

1. 섹터별 후보 종목군 확보
2. 각 섹터에서 대표 종목 1개 선택
3. 선택된 대표 종목 조합마다 최대 Sharpe 포인트 계산
4. 가장 좋은 조합 선택
5. 선택된 대표 종목 조합으로 Efficient Frontier 전체 계산
6. 화면에서는 결과를 섹터 비중으로 다시 묶어 표시

즉 계산 단위와 화면 표시 단위는 다릅니다.

- 계산 단위: 대표 종목
- 화면 표시 단위: 섹터

## 관리자 유니버스 흐름

현재 관리자 유니버스는 아래 흐름으로 운용됩니다.

1. `/admin`에서 섹터별 후보 종목 입력
2. 유니버스 버전 저장
3. 특정 버전을 `active`로 전환
4. `yfinance`에서 가격 적재
5. readiness 점검
6. 메인 시뮬레이터에서 active 버전 사용

이때 유니버스는 Postgres에 버전 단위로 저장되므로, 입력값 변경과 계산 기준을 분리할 수 있습니다.

## 대표 종목 선택 로직

`portfolio_service.py`가 active 유니버스 기준으로 대표 종목 조합을 탐색합니다.

현재 규칙:

- 각 섹터에서 대표 종목 `1개`
- 섹터별 최소 후보 종목 수 `1개`
- 전수 탐색 가능 조합 수 `<= 5000`이면 전체 조합 탐색
- 그보다 크면 `1000`개 샘플링
- 샘플링은 고정 seed 기반

즉 후보군이 작을 때는 가능한 모든 대표 종목 조합을 보고, 커지면 계산량을 제어하기 위해 샘플링합니다.

## 조합 평가 방식

각 대표 종목 조합은 아래 방식으로 평가합니다.

1. 선택된 종목들의 일간 수익률 시계열 생성
2. 기대수익률 계산
3. 공분산 계산
4. 제약조건 하에서 최대 Sharpe 포인트 계산
5. 최고 Sharpe가 가장 큰 조합을 선택

이 단계는 전체 frontier를 먼저 다 그리지 않고, **조합 비교용으로는 최대 Sharpe 포인트만 먼저 계산**합니다.

선택된 최적 조합이 정해진 뒤에만, 그 조합으로 frontier 전체를 계산합니다.

## 현재 제약조건

현재 기본 제약은 아래와 같습니다.

- long-only
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

- `weights`: 화면 표시용 섹터 합산 비중
- `allocations`: 섹터별 비중 / 리스크 기여도
- `frontier_points[*].weights`: 선택된 대표 종목 유니버스 기준 종목 가중치
- `selected_combination`: 섹터별로 어떤 대표 종목이 선택됐는지

즉 한 응답 안에:

- 계산에 쓰인 종목 레벨 정보
- 화면에 보여줄 섹터 레벨 정보

가 함께 들어 있습니다.

## 현재 설계의 장점

- 관리자 입력과 계산 기준이 버전으로 분리됨
- 가격 적재와 시뮬레이션이 분리됨
- 대표 종목 선택 단계와 frontier 계산 단계가 분리됨
- API / 서비스 / 엔진 / 저장소 경계가 비교적 명확함

## 현재 설계의 한계

- 대표 종목 선택은 아직 heuristic + sampling 중심
- 기대수익률 모델은 단순 historical mean 기반
- 관리자 화면은 로그인 없이 열리는 데모용 UI
- 가격 갱신은 아직 수동 실행 중심

## 방향성

다음 단계에서 가장 자연스러운 확장은 아래입니다.

1. 기대수익률 모델 플러그인화
2. 가격 갱신 배치 자동화
3. 관리자 보호장치 추가
4. 대표 종목 선택 기준 고도화
5. 필요 시 soft-penalty 기반 상관관계 제약 도입

## 현재 문서와의 관계

- `README.md`: 현재 시스템 개요
- `API_REFERENCE.md`: 엔드포인트와 응답 형식
- `DEMO_GUIDE.md`: 시연용 운영 가이드
- `STOCK_DATA_GUIDE.md`: 종목 데이터 요구사항
- `COMBINATION_SEARCH_GUIDE.md`: 대표 종목 조합 탐색의 배경과 참고 설명
