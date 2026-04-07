# 웹 기능 명세

## 문서 목적

이 문서는 현재 FastAPI 데모의 브라우저 화면이 실제로 어떤 기능을 제공하는지 정리한 **웹 기능 명세**입니다.

대상 화면:

- 메인 시뮬레이터: `/`
- 관리자 콘솔: `/admin`

기준:

- 현재 구현된 동작 기준
- 발표용 소개 문서가 아니라 개발/QA용 기능 계약서 기준
- 모바일 전환 전까지 웹 화면 유지보수에 필요한 흐름, 입력값, API 의존성, 제약사항 포함

## 범위

이 문서에 포함되는 항목:

- 화면별 목적
- 초기 로드 시 동작
- 사용자 입력과 결과 표시 방식
- 화면이 호출하는 API
- 현재 구현상 제약과 주의사항

이 문서에 포함하지 않는 항목:

- 인증/권한
- 멀티 유저 세션
- 주문 실행/실거래
- 모바일 앱 UX
- 서버 내부 계산 로직 상세 수식

## 공통 규칙

- 화면 언어는 한국어 기준입니다.
- 메인 시뮬레이터는 첫 진입 시 즉시 기본 포트폴리오 계산을 시작합니다.
- 관리자 콘솔은 첫 진입 시 상태, 버전 목록, readiness, 최근 가격 갱신 상세를 즉시 조회합니다.
- 메인 시뮬레이터의 에러는 카드 내 상태 텍스트나 빈 상태 메시지로 표시합니다.
- 관리자 콘솔의 에러와 원본 응답은 하단 로그 패널에 표시합니다.
- 메인 시뮬레이터만 다크 모드 토글을 제공합니다. 선택값은 브라우저 `localStorage.theme`에 저장합니다.

## 1. 메인 시뮬레이터 `/`

### 1-1. 화면 목적

메인 화면은 active 유니버스 또는 내장 데모 유니버스를 기준으로:

- 효율적 투자선 위 포트폴리오를 계산하고
- 현재 선택 포인트를 설명하며
- 자산군 비중/리스크 기여도/히스토리 차트/리밸런싱/비교 백테스트를 함께 보여주는

단일 시뮬레이션 화면입니다.

### 1-2. 초기 로드 규칙

첫 진입 시 화면은 아래 순서로 동작합니다.

1. `GET /portfolio/stocks`
   - 선택 종목 툴팁 구성을 위한 자산군별 종목 목록을 미리 로드합니다.
2. `POST /portfolio/simulate`
   - 기본 입력값으로 포트폴리오를 계산합니다.
3. 계산 성공 후 아래 API를 추가 호출합니다.
   - `POST /portfolio/volatility-history`
   - `POST /portfolio/return-history`
   - `POST /portfolio/rebalance-simulation`
   - `POST /portfolio/comparison-backtest`

기본 입력값:

- `risk_profile = balanced`
- `investment_horizon = medium`
- `data_source = managed_universe`

중요:

- 현재 UI는 `investment_horizon`과 `data_source` 선택 UI를 노출하지 않습니다.
- 두 값은 hidden input으로 고정되어 있습니다.
- 실제 fallback 여부는 백엔드 readiness와 데이터 상태에 따라 달라집니다.

### 1-3. 입력과 상태

| 항목 | 현재 UI 노출 | 현재 값/범위 | 동작 |
|---|---|---|---|
| 위험 슬라이더 | 노출 | `0 ~ 100`, 기본 `50` | 포트폴리오의 프론티어 위치를 조정 |
| 투자기간 | 미노출 | `medium` 고정 | 요청 payload에 포함 |
| 데이터 소스 | 미노출 | `managed_universe` 고정 | 요청 payload에 포함 |
| 시작일 | 노출 | 기본 `2024-01-02` | 리밸런싱 시뮬레이션 입력 |
| 투자금액 | 노출 | 기본 `10,000,000원` | 리밸런싱 시뮬레이션 입력 |

### 1-4. 위험 슬라이더 동작 명세

- 슬라이더 위치는 아래 위험 성향으로 매핑됩니다.
  - `0 ~ 33.33%`: `conservative`
  - `33.34 ~ 66.67%`: `balanced`
  - `66.68 ~ 100%`: `growth`
- 슬라이더는 프론티어의 최소/최대 기대수익률 구간을 기준으로 **목표 기대수익률**을 계산합니다.
- 첫 계산 전 슬라이더 조작은 짧은 debounce 후 `POST /portfolio/simulate`를 호출합니다.
- 이미 한 번 계산이 끝난 뒤에는 슬라이더 조작 시 **추가 API 호출 없이** 클라이언트가 현재 `frontier_points` 중 목표 기대수익률에 가장 가까운 점을 선택합니다.

중요:

- 즉, 현재 웹은 슬라이더 이동마다 새 최적화를 서버에 요청하지 않습니다.
- 서버는 프론티어 전체를 한 번 반환하고, 웹은 그 안에서 현재 포인트만 바꿉니다.

### 1-5. 기능별 명세

#### A. 프론티어 차트

목적:

- 가능한 포트폴리오 분포와 효율적 투자선, 현재 선택 포인트를 시각화합니다.

표시 요소:

- 가능한 포트폴리오 산점도
- 효율적 투자선
- 비교 기준선
- 안정형/균형형/성장형 대표 포인트
- 최대 샤프 포인트
- 현재 포트폴리오 포인트
- 개별 자산 포인트

사용 API:

- `POST /portfolio/simulate`

상호작용:

- 옵션 포인트 또는 최대 샤프 포인트 클릭 시 해당 기대수익률로 슬라이더를 이동합니다.
- 이후 서버 재호출 없이 캐시된 프론티어에서 현재 포인트를 다시 선택합니다.
- 툴팁에는 수익률, 변동성, 자산배분 정보가 표시됩니다.

#### B. 요약 지표 카드

표시 항목:

- 예상 수익률
- 변동성
- 샤프 지수

사용 API:

- `POST /portfolio/simulate`

동작:

- 초기 계산 후 숫자 애니메이션으로 갱신합니다.
- 슬라이더 이동 시 선택된 프론티어 포인트 기준으로 즉시 다시 계산해 표시합니다.

#### C. 히스토리 차트

모드:

- 변동성 추이
- 기대수익률 추이

기간 필터:

- `1주`
- `3달`
- `1년`
- `5년`
- `전체`

사용 API:

- `POST /portfolio/volatility-history`
- `POST /portfolio/return-history`

입력:

- 현재 선택 포트폴리오의 `selected_point.weights`
- 현재 데이터 소스

동작:

- 포트폴리오 계산 직후 자동 로드합니다.
- 슬라이더 이동으로 현재 포인트가 바뀌면 새 weights 기준으로 다시 조회합니다.
- 데이터가 부족하면 빈 상태 메시지를 표시합니다.

#### D. 설명 카드

표시 항목:

- 설명 제목
- 설명 본문
- 요약 텍스트
- disclaimer

사용 API:

- `POST /portfolio/simulate`

중요:

- 첫 계산 직후에는 서버 응답의 설명을 사용합니다.
- 이후 슬라이더 이동으로 현재 포인트만 바뀌는 경우, 설명/요약은 현재 선택 포인트에 맞춰 **클라이언트에서 재작성**됩니다.
- 즉 현재 구현은 포인트별 설명을 서버에 다시 요청하지 않습니다.

#### E. 현재 적용된 종목 유니버스 패널

목적:

- 현재 포트폴리오에 사용된 자산군별 종목 멤버 구성을 보여줍니다.

사용 API:

- `POST /portfolio/simulate`

동작:

- `selected_combination`이 있을 때만 표시합니다.
- 패널은 접고 펼칠 수 있습니다.
- 현재는 자산군 표시명 대신 `sector_code` 중심으로 멤버를 표시합니다.

#### F. 효율적 투자선 옵션 비교

목적:

- 안정형/균형형/성장형 대표 포트폴리오를 미니 도넛과 지표로 비교합니다.

사용 API:

- `POST /portfolio/simulate`

동작:

- 현재 선택 포인트와 기대수익률이 가장 가까운 옵션 카드를 강조 표시합니다.

#### G. 자산배분 카드

뷰 모드:

- 차트
- 목록

표시 항목:

- 자산군 비중
- 자산군 리스크 기여도
- 목록 뷰에서 하위 종목 구성

사용 API:

- `POST /portfolio/simulate`
- `GET /portfolio/stocks`

동작:

- 도넛 차트는 자산군 비중과 리스크 기여도를 각각 별도로 보여줍니다.
- 목록 뷰는 자산군 행을 펼치면 현재 선택 포트폴리오에 포함된 하위 종목을 표시합니다.
- 하위 종목 정보는 `selected_point.weights`와 `selected_combination.members_by_sector`를 조합해 구성합니다.

#### H. 분기별 리밸런싱 시뮬레이션

입력:

- 투자 시작일
- 투자 금액

사용 API:

- `POST /portfolio/rebalance-simulation`

동작:

- 현재 선택 포트폴리오의 weights를 기준으로 분기말 리밸런싱 시뮬레이션을 수행합니다.
- 결과로 아래를 표시합니다.
  - 리밸런싱 최종 가치
  - 바이앤홀드 최종 가치
  - 리밸런싱 시계열 차트
  - 리밸런싱 이벤트 툴팁

현재 구현 주의사항:

- 상단 지표에는 바이앤홀드 최종 가치가 표시됩니다.
- 하지만 차트 본문은 **리밸런싱 포트폴리오 시계열 + 리밸런싱 시점 마커**만 표시합니다.
- 바이앤홀드 전체 시계열 라인은 현재 그리지 않습니다.

#### I. 포트폴리오 비교 백테스트

목적:

- train/test 자동 분할 기반으로 추천 포트폴리오와 벤치마크를 비교합니다.

사용 API:

- `POST /portfolio/comparison-backtest`

동작:

- 포트폴리오 첫 계산 후 자동 실행합니다.
- 서버는 안정형/균형형/성장형 전체 비교 결과를 반환합니다.
- 그러나 현재 웹은 그중에서 **현재 슬라이더 구간에 해당하는 1개 포트폴리오 유형**과 벤치마크만 표시합니다.
- 슬라이더가 바뀌면 서버를 다시 호출하지 않고, 이미 받은 백테스트 데이터를 다시 필터링해 렌더링합니다.

표시 항목:

- test 시작일
- 비교 성과 곡선
- 기대수익 점선
- 리밸런싱 기준선
- hover 툴팁

### 1-6. 메인 화면 API 의존성 표

| 화면 기능 | API |
|---|---|
| 종목 메타데이터 초기 로드 | `GET /portfolio/stocks` |
| 포트폴리오 계산 | `POST /portfolio/simulate` |
| 변동성 추이 | `POST /portfolio/volatility-history` |
| 기대수익률 추이 | `POST /portfolio/return-history` |
| 리밸런싱 시뮬레이션 | `POST /portfolio/rebalance-simulation` |
| 비교 백테스트 | `POST /portfolio/comparison-backtest` |

### 1-7. 현재 제약사항

- 사용자는 투자기간을 바꿀 수 없습니다.
- 사용자는 데이터 소스를 바꿀 수 없습니다.
- 포트폴리오 설명은 포인트별 서버 재생성이 아니라 일부 클라이언트 재작성 로직을 사용합니다.
- 자산군 표시명과 종목 조합 표시는 일부 영역에서 `sector_code` 중심으로 노출됩니다.

## 2. 관리자 콘솔 `/admin`

### 2-1. 화면 목적

관리자 화면은 로그인 없이 아래 작업을 수행하는 데모용 운영 화면입니다.

- 유니버스 버전 생성/수정/삭제
- active 버전 전환
- 티커 검색 및 자동채움
- 가격 갱신 실행
- readiness 확인
- 최근 가격 갱신 상세 확인

### 2-2. 초기 로드 규칙

첫 진입 시 `reloadAll()`을 호출해 아래 데이터를 즉시 조회합니다.

1. `GET /admin/universe/status`
2. `GET /admin/universe/versions`
3. `GET /admin/universe/readiness`
4. 최근 가격 갱신 잡이 있으면 `GET /admin/prices/jobs/{job_id}/items`

### 2-3. 기능별 명세

#### A. 현재 상태 카드

목적:

- DB 연결 여부와 active 유니버스 상태를 빠르게 확인합니다.

표시 항목:

- DB 연결
- 활성 버전명
- 가격 행 수
- 공통 시작일
- 최근 가격일
- 상태 pill
- 공통 가격 구간 설명

사용 API:

- `GET /admin/universe/status`

#### B. 가격 데이터 갱신 카드

입력:

- 갱신 모드: `incremental` / `full`
- 백필 연수: `1 ~ 20`

사용 API:

- `POST /admin/prices/refresh`
- `GET /admin/universe/status`
- `GET /admin/prices/jobs/{job_id}/items`

동작:

- 버튼 클릭 시 active 유니버스를 기준으로 가격 갱신을 실행합니다.
- 실행 중 버튼을 비활성화합니다.
- 완료 후 상태, readiness, 최근 잡 상세를 다시 로드합니다.

최근 갱신 상세 표시 규칙:

- 최근 잡이 성공이면 상세 항목 전체를 보여줍니다.
- 최근 잡이 실패 또는 부분 실패면 실패 항목 위주로 상세를 보여줍니다.

#### C. 유니버스 편집기

목적:

- 자산군별 종목 후보군을 작성하고 버전 단위로 저장합니다.

데이터 원천:

- 자산군 탭 구조는 `app/data/asset_universe.json` 기준으로 동적 생성됩니다.

지원 기능:

- 자산군 탭 전환
- 종목 행 추가/삭제
- 티커 직접 입력
- 티커 자동채움
- 티커 검색 결과 추가
- 새 버전 생성
- 기존 버전 수정

행 입력 필드:

- `ticker`
- `name`
- `market`
- `currency`
- `base_weight` 선택 입력

입력 규칙:

- 티커는 대문자로 정규화합니다.
- 중복 티커는 허용하지 않습니다.
- 비어 있는 티커 행이 있으면 저장할 수 없습니다.
- 종목이 1개도 없으면 저장할 수 없습니다.
- `name`이 비어 있으면 저장할 수 없습니다.
- `market`, `currency`는 비어 있으면 각각 `USA`, `USD` 기본값을 사용합니다.

티커 자동채움:

- `GET /admin/tickers/lookup?ticker=...`
- blur 시점 또는 `자동채움` 버튼으로 실행합니다.

티커 검색:

- `GET /admin/tickers/search?query=...&max_results=8`
- 검색 결과에서 바로 행 추가가 가능합니다.

저장:

- 신규 생성: `POST /admin/universe/versions`
- 수정 저장: `PUT /admin/universe/versions/{version_id}`

현재 저장 규칙:

- 신규 생성은 기본적으로 `activate=true`로 저장합니다.
- 수정 저장은 현재 편집 중인 버전의 active 상태를 그대로 유지합니다.

#### D. 유니버스 버전 목록

목적:

- 저장된 버전의 상태를 확인하고 즉시 조작합니다.

사용 API:

- `GET /admin/universe/versions`
- `POST /admin/universe/versions/{version_id}/activate`
- `GET /admin/universe/versions/{version_id}`
- `DELETE /admin/universe/versions/{version_id}`

지원 기능:

- active 전환
- 수정 모드 로드
- 삭제

삭제 규칙:

- 브라우저 기본 `confirm` 확인창 이후 삭제합니다.

#### E. 시뮬레이션 준비 상태

목적:

- 현재 active 유니버스가 실제 계산 가능한 상태인지 사전 점검합니다.

사용 API:

- `GET /admin/universe/readiness`

표시 항목:

- 계산 가능 여부
- active 버전명
- 최적화 티커 수
- 유효 수익률 행 수
- 공통 시작일
- 차단 사유 목록
- 짧은 이력 종목 목록
- 자산군 분포 진단

#### F. 상태 로그 / 원본 응답

목적:

- 운영자가 최근 성공/실패 응답을 바로 확인합니다.

동작:

- 검색, 자동채움, 저장, 삭제, 가격 갱신, readiness 조회 결과를 텍스트 로그로 남깁니다.
- 원본 응답 객체가 있으면 JSON 형태로 함께 보여줍니다.

### 2-4. 관리자 화면 API 의존성 표

| 화면 기능 | API |
|---|---|
| 현재 상태 | `GET /admin/universe/status` |
| 버전 목록 | `GET /admin/universe/versions` |
| 버전 상세 로드 | `GET /admin/universe/versions/{version_id}` |
| 버전 생성 | `POST /admin/universe/versions` |
| 버전 수정 | `PUT /admin/universe/versions/{version_id}` |
| 버전 삭제 | `DELETE /admin/universe/versions/{version_id}` |
| active 전환 | `POST /admin/universe/versions/{version_id}/activate` |
| readiness 확인 | `GET /admin/universe/readiness` |
| 가격 갱신 | `POST /admin/prices/refresh` |
| 가격 잡 상세 | `GET /admin/prices/jobs/{job_id}/items` |
| 티커 조회 | `GET /admin/tickers/lookup` |
| 티커 검색 | `GET /admin/tickers/search` |

### 2-5. 현재 제약사항

- 인증이 없습니다.
- 관리자 화면은 단일 사용자 운영 전제를 갖습니다.
- 대량 편집, CSV 업로드, pagination, 권한 분리 기능은 없습니다.
- 검색/자동채움/가격 갱신은 외부 시세 데이터 상태에 영향을 받습니다.

## 3. 웹 기준 후속 정리 우선순위

현재 웹 기능명세를 바탕으로 정리 우선순위를 잡으면 아래 순서가 적절합니다.

1. 메인 시뮬레이터에서 숨겨진 `investment_horizon`, `data_source` 노출 여부 결정
2. 슬라이더 이동 시 클라이언트 재작성 설명을 유지할지, 포인트별 서버 설명으로 바꿀지 결정
3. 리밸런싱 카드에서 바이앤홀드 시계열도 실제로 그릴지 결정
4. 비교 백테스트 카드에서 3개 프로필을 모두 보여줄지, 현재처럼 1개만 보여줄지 결정
5. 관리자 화면 인증/권한 구조 도입 여부 결정

## 4. 관련 문서

- 아키텍처: `docs/ARCHITECTURE.md`
- API 명세: `docs/API_REFERENCE.md`
- 데모 가이드: `docs/DEMO_GUIDE.md`
