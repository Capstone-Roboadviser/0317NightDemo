# 조합 탐색 가이드

## 이 문서의 위치

현재 서비스의 런타임 조합 탐색은 `portfolio_service.py`와 `portfolio_component_service.py`가 함께 담당합니다.

이 문서는 그 배경 개념을 정리한 참고 문서입니다.

## 현재 조합 탐색 문제 정의

현재 시스템은 아래 문제를 풉니다.

1. 각 자산군의 후보 종목군을 읽는다.
2. 자산군의 역할(`role_key`)에 따라 포트폴리오 컴포넌트 후보를 만든다.
3. 컴포넌트 조합마다 최대 Sharpe 포트폴리오를 계산한다.
4. 가장 좋은 Sharpe를 만든 조합을 선택한다.
5. 선택된 조합으로 Efficient Frontier 전체를 계산한다.

즉 이것은 아래 두 단계가 결합된 구조입니다.

- 상위 문제: 자산군 역할 기반 컴포넌트 선택
- 하위 문제: 선택된 컴포넌트 유니버스에 대한 포트폴리오 최적화

## 현재 역할별 동작

### `single_representative`

- 후보 종목 중 1개가 선택 후보가 됩니다.
- 후보가 3개면 조합 후보도 3개입니다.

### `equal_weight_basket`

- 후보 종목 전체를 하나의 동일비중 바스켓으로 묶습니다.
- 따라서 이 자산군은 조합 수를 늘리지 않고, 하나의 고정 컴포넌트를 제공합니다.
- 현재 저장소 기준 기본 카탈로그는 이 역할을 아직 사용하지 않지만, 런타임은 해당 역할을 지원합니다.

중요:

- 현재 저장소 기준 기본 카탈로그의 7개 자산군은 모두 `single_representative`를 사용합니다.
- 따라서 현재 조합 탐색은 실질적으로 "자산군별 대표 종목 1개 선택" 문제로 동작합니다.
- `equal_weight_basket`은 향후 특정 자산군의 `role_key`를 바꾸면 즉시 사용할 수 있는 확장 포인트입니다.

## 현재 규칙

- 최소 유효 이력: `252` 영업일
- 전수 탐색 임계치: `5000`
- 샘플링 개수: `1000`
- 샘플링 seed: 고정
- 종목 최소 비중: `1%`
- 종목 최대 비중: `30%`
- 평균 종목 상관관계 상한: `0.25`

## 현재 평가 기준

각 조합은 아래 기준으로 평가됩니다.

- 기대수익률은 Black-Litterman market-implied prior 사용
  - `Pi = delta * Sigma * w_prior`
  - `delta = 2.5` 고정
  - `w_prior`는 컴포넌트 시가총액 비중, 실패 시 equal-weight fallback
- long-only
- Sharpe Ratio 최대화
- 평균 종목 상관관계 상한 제약 적용

즉 상관관계는 별도 목표가 아니라, Sharpe를 최적화하는 과정에서 함께 제약으로 작동합니다.

## 현재 코드 위치

- 런타임 orchestration: `app/services/portfolio_service.py`
- 역할 해석/컴포넌트 생성: `app/services/portfolio_component_service.py`
- 과거 조합 탐색 스캐폴드: `app/services/combination_search_service.py`

역할 필드 책임과 확장 방식은 `docs/ASSET_ROLE_DESIGN.md`를 참고하세요.

## 이후 확장 방향

나중에 조합 탐색을 더 고도화하려면 아래 방향이 가능합니다.

1. 역할별 개별 전략 클래스로 분리
2. soft-penalty 기반 상관관계 제약
3. 역할별 최소/최대 자산군 비중 제약
4. Black-Litterman views(P/Q) 도입
5. 배치 기반 장시간 탐색
