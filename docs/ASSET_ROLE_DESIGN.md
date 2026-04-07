# 자산군 역할 설계 문서

## 문서 목적

이 문서는 현재 서비스의 핵심 설계인 **자산군(asset class)** 과 **역할(role)** 분리 구조를 설명합니다.

특히 아래 질문에 답하는 문서입니다.

- 자산군별 `role_key`는 어디에 저장되는가
- 역할 템플릿은 어떤 필드를 가지는가
- 런타임은 자산군 카탈로그와 역할 템플릿을 어떻게 합치는가
- 역할이 실제 포트폴리오 계산에 어떤 영향을 주는가
- 새 역할을 추가하려면 어떤 코드를 수정해야 하는가

## 1. 핵심 아이디어

현재 구조는 아래 두 가지를 분리합니다.

- 자산군 목록과 자산군별 비즈니스 메타데이터
- 자산군이 포트폴리오 계산에 편입되는 방식

즉 자산군은 "무슨 자산군인가"를 설명하고, 역할은 "그 자산군을 어떻게 계산 입력으로 바꿀 것인가"를 설명합니다.

한 줄로 요약하면:

`asset_universe.json`의 각 자산군이 `role_key`를 가지고 있고, `asset_role_templates.json`이 그 `role_key`를 실제 계산 규칙으로 해석합니다.

## 2. 관련 파일

| 파일 | 역할 |
|---|---|
| `app/data/asset_universe.json` | 자산군 카탈로그와 자산군별 `role_key` 정의 |
| `app/data/asset_role_templates.json` | 역할 템플릿 정의 |
| `app/data/repository.py` | 자산군 카탈로그와 역할 템플릿을 합쳐 `AssetClass`로 로딩 |
| `app/services/portfolio_component_service.py` | 역할 메타데이터를 optimizer 입력용 컴포넌트 후보로 변환 |
| `app/services/portfolio_service.py` | 자산군별 후보 조합 탐색과 최종 포트폴리오 계산 orchestration |

## 3. 데이터 모델

### 3-1. 자산군 카탈로그

`app/data/asset_universe.json`의 각 row는 자산군 자체의 의미를 정의합니다.

주요 필드:

- `code`
- `name`
- `category`
- `description`
- `color`
- `min_weight`
- `max_weight`
- `role_key`

중요:

- 이 파일은 자산군의 표시명과 제약 메타데이터를 가집니다.
- 실제 선택 방식은 `role_key`를 통해 역할 템플릿에서 가져옵니다.

### 3-2. 역할 템플릿

`app/data/asset_role_templates.json`의 각 row는 역할 규칙을 정의합니다.

주요 필드:

- `key`
- `name`
- `description`
- `selection_mode`
- `weighting_mode`
- `return_mode`

현재 저장소 기준 역할 템플릿은 2개입니다.

1. `single_representative`
2. `equal_weight_basket`

## 4. 로딩 방식

런타임은 `StaticDataRepository.load_asset_universe()`에서 아래 순서로 자산군 정보를 만듭니다.

1. 역할 템플릿 파일을 먼저 읽습니다.
2. 자산군 카탈로그를 읽습니다.
3. 각 자산군의 `role_key`로 역할 템플릿을 찾습니다.
4. 템플릿의 `name`, `description`, `selection_mode`, `weighting_mode`, `return_mode`를 자산군 객체에 주입합니다.
5. 최종적으로 API/UI/서비스가 사용하는 `AssetClass` 객체를 만듭니다.

즉 API나 UI가 받는 자산군 정보는 단순 JSON 원본이 아니라, 역할 템플릿이 합쳐진 결과입니다.

중요:

- `role_key`에 해당하는 템플릿이 없으면 로딩 시점에 `RuntimeError`가 발생합니다.
- 따라서 자산군 카탈로그와 역할 템플릿은 항상 함께 관리되어야 합니다.

## 5. 역할이 계산에 들어가는 방식

역할 메타데이터가 실제 계산으로 연결되는 중심 계층은 `PortfolioComponentService`입니다.

역할 해석 흐름:

1. 자산군별 등록 종목을 모읍니다.
2. 가격 이력이 있는 종목만 남깁니다.
3. 자산군의 `selection_mode`에 따라 컴포넌트 후보를 만듭니다.
4. 선택된 후보를 `component_returns`로 변환합니다.
5. optimizer는 종목이 아니라 컴포넌트 기준으로 최적화를 수행합니다.
6. 최종 결과는 다시 종목 비중으로 explode 합니다.

즉 역할의 본질은:

- 후보 종목군을 몇 개의 컴포넌트 후보로 바꿀지
- 컴포넌트 수익률을 어떻게 만들지
- 최종 컴포넌트 비중을 종목 비중으로 어떻게 되돌릴지

를 정의하는 것입니다.

## 6. 필드별 책임

### 6-1. `role_key`

역할 템플릿을 찾기 위한 키입니다.

예:

- `single_representative`
- `equal_weight_basket`

### 6-2. `selection_mode`

자산군 후보 종목을 어떤 방식으로 후보 컴포넌트로 만들지 결정합니다.

현재 구현:

- `single_representative`
  - 후보 종목이 3개면 컴포넌트 후보도 3개
- `all_members`
  - 후보 종목 전체를 하나의 컴포넌트로 묶음

### 6-3. `weighting_mode`

컴포넌트 내부에서 종목 비중을 어떻게 나눌지 결정합니다.

현재 구현:

- `single`
  - 대표 종목 1개에 100%
- `equal_weight`
  - 구성 종목 수만큼 동일 비중 분할

### 6-4. `return_mode`

현재는 역할 메타데이터로 API/UI에 노출되고 후보 객체에도 실리지만,
`PortfolioComponentService`의 실제 수익률 생성 분기에는 아직 사용되지 않습니다.

즉 현재 코드 기준으로:

- 실제 계산 분기에 직접 영향을 주는 필드: `selection_mode`, `weighting_mode`
- 현재는 메타데이터 성격이 더 강한 필드: `return_mode`

이 점은 앞으로 역할 전략이 늘어날 때 확장 포인트가 됩니다.

## 7. 현재 지원 역할

### 7-1. `single_representative`

의미:

- 자산군 후보 종목 중 대표 종목 1개를 선택 후보로 둡니다.

생성 결과:

- 후보 종목이 `AAPL`, `MSFT`, `GOOGL` 3개면
- 컴포넌트 후보는 아래 3개가 생깁니다.
  - `(AAPL)`
  - `(MSFT)`
  - `(GOOGL)`

계산 특성:

- 조합 탐색 시 조합 수를 늘립니다.
- 선택된 컴포넌트의 종목 비중은 해당 티커 1개에 그대로 귀속됩니다.

### 7-2. `equal_weight_basket`

의미:

- 자산군 후보 종목 전체를 동일비중 바스켓 하나로 묶습니다.

생성 결과:

- 후보 종목이 `AAPL`, `MSFT`, `GOOGL` 3개면
- 컴포넌트 후보는 아래 1개만 생깁니다.
  - `(AAPL, MSFT, GOOGL)`

계산 특성:

- 조합 탐색 수를 늘리지 않습니다.
- 선택된 컴포넌트 비중은 내부 종목 수만큼 균등 분할됩니다.
- 시가총액 prior 계산 시 바스켓 구성 종목의 시가총액 합을 사용합니다.

## 8. 현재 기본 카탈로그 상태

현재 저장소의 `app/data/asset_universe.json` 기준으로는 7개 자산군 모두 `single_representative`를 사용합니다.

현재 기본 매핑:

| 자산군 코드 | 자산군 이름 | 현재 `role_key` |
|---|---|---|
| `us_value` | 미국 가치주 | `single_representative` |
| `us_growth` | 미국 성장주 | `single_representative` |
| `new_growth` | 신성장주 | `single_representative` |
| `short_term_bond` | 단기 채권 | `single_representative` |
| `cash_equivalents` | 현금성자산 | `single_representative` |
| `gold` | 금 | `single_representative` |
| `infra_bond` | 인프라 채권 | `single_representative` |

중요:

- 런타임은 `equal_weight_basket`을 처리할 수 있습니다.
- 하지만 현재 기본 카탈로그는 그 역할을 아직 사용하지 않습니다.
- 즉 "구조는 role 확장을 지원하지만, 현재 저장소 기본 설정은 전부 대표 종목형" 상태입니다.

## 9. 조합 탐색에 미치는 영향

역할은 조합 탐색 수를 직접 바꿉니다.

예시:

- 자산군 A: 후보 3개, `single_representative`
- 자산군 B: 후보 4개, `single_representative`
- 자산군 C: 후보 5개, `equal_weight_basket`

그러면 조합 수는:

- A에서 3개
- B에서 4개
- C에서 1개

즉 총 `3 x 4 x 1 = 12`개입니다.

같은 후보 종목 수라도 어떤 역할을 주느냐에 따라 탐색 비용이 크게 달라집니다.

## 10. 최적화 전후 변환

### 10-1. 최적화 전

역할 해석 후 optimizer는 아래처럼 종목이 아니라 컴포넌트를 받습니다.

- `us_value -> (VTV)`
- `us_growth -> (QQQ)`
- `new_growth -> (NVDA, AMD, PLTR)` 같은 바스켓 가능

### 10-2. 최적화 후

optimizer가 컴포넌트 비중을 반환하면 `explode_component_weights()`가 이를 종목 비중으로 다시 펼칩니다.

예:

- `single` 컴포넌트 `VTV = 20%`
  - 종목 비중: `VTV = 20%`
- `equal_weight` 컴포넌트 `(NVDA, AMD, PLTR) = 15%`
  - 종목 비중:
    - `NVDA = 5%`
    - `AMD = 5%`
    - `PLTR = 5%`

## 11. UI와 API에서의 노출 방식

역할 정보는 현재 아래 경로로 노출됩니다.

- `GET /portfolio/assets`
  - `role_key`, `role_name`, `role_description`, `selection_mode`, `weighting_mode`, `return_mode`
- `/admin`
  - 자산군 탭마다 현재 역할과 선택/비중/수익률 모드를 표시
- `/`
  - 자산 메타데이터를 프론트에 전달하지만, 현재 메인 화면은 역할 설명을 전면적으로 노출하진 않음

즉 역할은 내부 계산 규칙이면서 동시에 운영 화면의 설명 메타데이터이기도 합니다.

## 12. 새 역할을 추가할 때 수정할 곳

새 역할 추가는 JSON만 바꾸는 작업이 아닙니다.

최소 수정 포인트는 아래입니다.

1. `app/data/asset_role_templates.json`
   - 새 `key`, `selection_mode`, `weighting_mode`, `return_mode` 추가
2. `app/services/portfolio_component_service.py`
   - `_build_candidates_for_asset()`에 새 `selection_mode` 처리 추가
   - `build_component_series()`에 새 `weighting_mode` 또는 수익률 생성 방식 추가
   - `explode_component_weights()`에 새 비중 분해 방식 추가
3. 필요하면 `component_prior_weight_series()`도 수정
   - 바스켓/합성 자산의 prior weight 계산 방식이 다르면 여기 반영
4. `app/data/asset_universe.json`
   - 특정 자산군에 새 `role_key` 배정
5. 문서와 UI 확인
   - 관리자 콘솔/README/설계 문서/API 문서 정합성 점검

## 13. 운영상 체크포인트

- `role_key`는 반드시 템플릿 파일에 존재해야 합니다.
- 자산군에 종목이 있어도 역할 해석 결과 후보가 0개면 readiness가 실패할 수 있습니다.
- 역할 수가 늘어나면 조합 수가 폭증할 수 있으므로 조합 탐색 비용을 같이 검토해야 합니다.
- `return_mode`를 확장해 실제 계산 분기로 연결할 계획이라면 문서와 테스트를 함께 업데이트해야 합니다.

## 14. 지금 문서화에서 중요한 결론

현재 저장소 기준으로는:

- 역할 설계 구조는 분리돼 있고
- 런타임은 `single_representative`, `equal_weight_basket` 두 역할을 이해하며
- 기본 자산군 카탈로그는 현재 모두 `single_representative`를 사용하고
- `return_mode`는 아직 계산 전략 분기보다는 메타데이터에 가깝습니다

입니다.

따라서 앞으로 자산군별 역할을 더 적극적으로 쓰려면,
이 문서를 기준으로 **현재 구조**와 **현재 기본 설정값**을 구분해서 관리하는 것이 중요합니다.
