# 조합 탐색 가이드

## 목표

섹터 내부의 개별 주식 조합이 매우 많을 때, 모든 조합을 전수탐색하기보다 샘플링 기반으로 후보 조합을 만들고, 각 조합의 Efficient Frontier 중 최대 Sharpe Ratio 포인트를 비교합니다.

## 개념 구조

1. 개별 종목 선택
2. 섹터 수익률 시계열 생성
3. 섹터 단위 기대수익률 / 공분산 계산
4. Efficient Frontier 계산
5. 조합별 최대 Sharpe Ratio 비교

즉 이것은 단일 frontier 문제가 아니라 아래 두 단계가 결합된 구조입니다.

- 상위 문제: 섹터 내부 종목 조합 선택
- 하위 문제: 선택된 섹터 조합에 대한 자산배분 최적화

## 현재 추가된 스캐폴드

파일: [combination_search_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/combination_search_service.py)

주요 기능:

- 섹터별 종목 조합 무작위 샘플링
- 선택된 종목으로 섹터 수익률 시계열 생성
- 기존 Efficient Frontier 엔진 재사용
- 조합별 최대 Sharpe Ratio 평가
- 최고 결과와 상위 결과 목록 반환
- 조합 탈락 사유 집계
- 입력 CSV의 중복 / 비정상 값 검증

## 기본 사용 흐름 예시

```python
from app.services.combination_search_service import CombinationSearchConfig, CombinationSearchService

service = CombinationSearchService()
result = service.search_best_combination(
    stock_universe_path="app/data/my_stock_universe.csv",
    stock_prices_path="app/data/my_stock_prices.csv",
    config=CombinationSearchConfig(
        selection_sizes={
            "bond": 2,
            "real_assets": 2,
            "etf": 2,
            "tech_healthcare": 2,
            "ai_semiconductor_social": 2,
            "financials": 2,
            "energy": 2,
            "consumer_other": 2,
        },
        sample_count=500,
        per_sector_weighting="equal",
        random_seed=23,
    ),
)
```

## 반환 결과

`result`에는 아래 핵심 값이 들어 있습니다.

- `total_combinations_tested`: 실제 평가를 시도한 조합 수
- `successful_combinations`: 정상적으로 frontier 계산까지 완료한 조합 수
- `discard_reasons`: 탈락 사유별 집계
- `best_evaluation`: 최고 Sharpe Ratio 조합
- `top_evaluations`: 상위 후보 목록

예를 들어 일부 조합이 데이터 길이 부족이나 최적화 실패로 제외되면 `discard_reasons`에 아래처럼 누적됩니다.

```python
{
    "insufficient_common_history": 12,
    "optimizer_failure": 3,
}
```

## 입력 규칙

### `selection_sizes`

섹터별로 몇 개 종목을 뽑을지 지정합니다.
현재 자산군 정의에 포함된 모든 섹터 코드를 빠짐없이 넣어야 하며, 알 수 없는 섹터 코드를 추가하면 오류가 발생합니다.

예:

```python
{
    "bond": 2,
    "real_assets": 2,
    "etf": 2,
    "tech_healthcare": 3,
    "ai_semiconductor_social": 3,
    "financials": 2,
    "energy": 2,
    "consumer_other": 2,
}
```

### `sample_count`

랜덤 샘플링할 조합 수입니다.

권장 시작값:

- 작은 테스트: `100`
- 데모용 탐색: `300 ~ 1000`
- 더 큰 실험: `2000+`

### `per_sector_weighting`

현재 지원 값:

- `equal`
- `base_weight`

`base_weight`를 쓰려면 종목 유니버스 CSV에 `base_weight` 컬럼이 있어야 합니다.

## 주의사항

- 이 스캐폴드는 아직 API에 연결되어 있지 않습니다.
- 현재는 오프라인 분석/배치 실행용에 가깝습니다.
- 샘플 수가 커지면 계산시간이 급격히 늘 수 있습니다.
- 기대수익률 모델은 지금 `HistoricalMeanReturnModel`을 기본으로 사용합니다.
- 섹터 수익률은 결측치를 `0`으로 채우지 않고, 공통으로 관측된 날짜만 사용합니다.
- `stock_universe.csv`의 중복 ticker, `stock_prices.csv`의 중복 `date+ticker`, 비어 있는 코드, 0 이하 가격은 모두 오류로 처리합니다.

## 다음 리팩토링 포인트

나중에 이 모듈을 본격화하려면 아래가 필요합니다.

1. 기대수익률 모델 주입 구조 명확화
2. 결과 캐시 저장
3. 장시간 탐색용 배치 작업 분리
4. API 엔드포인트 추가
5. 진행률 및 상위 후보 모니터링
