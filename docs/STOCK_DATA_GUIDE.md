# 종목 데이터 가이드

## 현재 서비스에서 종목 데이터가 쓰이는 방식

현재 서비스는 CSV 업로드를 핵심 흐름으로 사용하지 않습니다.

현재 운영 방식:

1. 관리자가 `/admin`에서 자산군별 후보 종목을 입력
2. 유니버스 버전을 Postgres에 저장
3. `yfinance`로 가격 이력을 적재
4. 가격 이력으로 수익률을 계산
5. 자산군 역할에 따라 포트폴리오 컴포넌트 생성
6. 그 컴포넌트 유니버스로 Efficient Frontier 계산

즉 현재는 **종목 메타데이터는 관리자 입력**, **가격 데이터는 백엔드 수집** 구조입니다.

## 종목 데이터에 필요한 필드

현재 시스템이 종목 후보군에서 실제로 쓰는 필드는 아래입니다.

- `ticker`
- `name`
- `sector_code`
- `sector_name`
- `market`
- `currency`
- `base_weight` (선택)

### 필드 의미

- `ticker`: 가격 조회와 계산의 기준 키
- `name`: UI 표시용
- `sector_code`: 자산군 그룹핑 기준
- `sector_name`: UI 표시용 한글 이름
- `market`: 거래 시장 메타데이터
- `currency`: 통화 정보
- `base_weight`: 현재는 핵심 제약은 아니지만 확장 대비용 필드

## 자산군과 역할

현재 시스템은 자산군과 역할을 구분합니다.

- 자산군 목록: `app/data/asset_universe.json`
- 역할 템플릿: `app/data/asset_role_templates.json`

현재 지원하는 역할:

- `single_representative`
- `dividend_representative`
- `equal_weight_basket`

즉 같은 자산군 후보군이라도, 역할에 따라:

- 대표 종목 1개가 포트폴리오에 들어가거나
- 대표 종목 1개 + 기대수익률 보정이 적용되거나
- 여러 종목이 동일비중 바스켓으로 함께 들어갈 수 있습니다

현재 기본 카탈로그 기준:

- `short_term_bond`는 `dividend_representative`
- `new_growth`는 `equal_weight_basket`
- 나머지 자산군은 `single_representative`

## 가격 데이터 요구사항

현재 시스템은 내부적으로 아래 형태의 가격 이력이 필요합니다.

- `date`
- `ticker`
- `adjusted_close`

이 데이터는 현재 주로 `yfinance`에서 수집합니다.

중요:

- `adjusted_close`가 필요합니다.
- 최소 `252` 영업일 이상의 이력이 필요합니다.
- 실제 계산은 유니버스에서 가장 늦게 시작한 종목 기준의 **공통 가격 구간**만 사용합니다.

## 관리자 입력 시 주의점

- `ticker`는 정확해야 합니다.
- `sector_code`는 현재 자산군 카탈로그 코드와 일치해야 합니다.
- 계산에 참여시키고 싶은 자산군에는 최소 1개 이상 후보 종목이 있어야 합니다.
- 자산군 역할에 따라 최종 포트폴리오에 들어가는 방식이 달라집니다.

## 데모 데이터

저장소에는 포맷 검증과 내부 테스트용 더미 데이터도 있습니다.

- `app/data/demo/demo_stock_universe.csv`
- `app/data/demo/demo_stock_prices.csv`

이 더미 데이터는 관리자 유니버스가 없을 때 fallback 경로 또는 개발 테스트에 사용합니다.

## CSV는 언제 필요하나

현재 운영 경로는 CSV 입력이 아니지만, 아래 경우엔 여전히 CSV가 유용합니다.

- 초기 데이터 검증
- 오프라인 실험
- 데모용 더미 데이터 재생성
- 외부 팀이 후보 종목 목록을 정리해 전달할 때

즉 CSV는 현재 **운영 기본 경로**라기보다 **보조 입력/실험 도구**에 가깝습니다.
