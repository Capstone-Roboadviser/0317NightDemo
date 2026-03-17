# 개별 주식 데이터 준비 가이드

## 목적

이 문서는 섹터 내부의 개별 주식 조합을 샘플링하고, 조합별 Efficient Frontier와 최대 Sharpe Ratio를 비교하려는 경우 어떤 데이터를 준비해야 하는지 설명합니다.

핵심 흐름은 아래와 같습니다.

1. 개별 주식 가격 데이터를 준비한다.
2. 개별 주식 수익률 시계열을 계산한다.
3. 섹터별로 선택된 종목을 묶어 섹터 수익률 시계열을 만든다.
4. 그 섹터 수익률들로 기대수익률, 공분산, Efficient Frontier를 계산한다.
5. 각 조합의 최대 Sharpe 포인트를 비교한다.

## 필수 파일 1: 종목 유니버스 CSV

권장 파일: [stock_universe_template.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/templates/stock_universe_template.csv)

필수 컬럼:

- `ticker`: 종목 식별자
- `name`: 종목명
- `sector_code`: 시스템 내부 자산군 코드
- `sector_name`: 표시용 자산군 이름
- `market`: 거래 시장
- `currency`: 통화

선택 컬럼:

- `base_weight`: 섹터 내부 기본가중치

예시:

```csv
ticker,name,sector_code,sector_name,market,currency,base_weight
IEF,iShares 7-10 Year Treasury Bond ETF,bond,채권,USA,USD,0.34
TLT,iShares 20+ Year Treasury Bond ETF,bond,채권,USA,USD,0.33
SPY,SPDR S&P 500 ETF Trust,etf,ETF,USA,USD,0.50
```

## 필수 파일 2: 가격 시계열 CSV

권장 파일: [stock_prices_template.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/templates/stock_prices_template.csv)

필수 컬럼:

- `date`
- `ticker`
- `adjusted_close`

`adjusted_close`를 쓰는 이유:

- 배당과 분할을 반영한 값이기 때문
- 단순 종가보다 총수익률에 가깝기 때문

예시:

```csv
date,ticker,adjusted_close
2025-01-02,IEF,94.10
2025-01-03,IEF,94.22
2025-01-02,SPY,589.12
2025-01-03,SPY,592.08
```

## 데이터 준비 원칙

### 1. 자산군 코드는 현재 시스템과 맞춰야 합니다

현재 데모의 8개 자산군 코드는 아래와 같습니다.

- `bond`
- `real_assets`
- `etf`
- `tech_healthcare`
- `ai_semiconductor_social`
- `financials`
- `energy`
- `consumer_other`

### 2. 가능한 한 동일한 날짜 범위를 맞추는 것이 좋습니다

종목마다 상장일이 다르면 결측치가 많아집니다.

권장:

- 공통 시작일 이후 데이터만 사용
- 최근 2~5년 정도로 기간을 통일

### 3. 통화가 섞이면 환율 처리 기준을 정해야 합니다

지금 템플릿은 단순화를 위해 `USD` 기준을 가정합니다.

나중에 한국 주식, 미국 주식, 원자재 ETF를 섞는다면:

- 모두 KRW로 환산
또는
- 모두 USD 기준으로 통일

중 하나를 먼저 정해야 합니다.

### 4. 생존편향을 주의해야 합니다

현재 상장된 종목만 보면 과거 성과가 과대평가될 수 있습니다.

데모 단계에서는 일단 현재 종목군으로 시작해도 되지만, 실제 연구로 가면 주의가 필요합니다.

## 권장 최소 데이터 양

- 최소 252 영업일 이상
- 권장 2년 이상
- 섹터별 후보 종목은 최소 3개 이상

## 지금 코드에서 이 데이터를 어디에 쓰나

로더와 탐색 스캐폴드는 아래 파일에 있습니다.

- [stock_repository.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/stock_repository.py)
- [combination_search_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/combination_search_service.py)

## 바로 써볼 수 있는 더미 데이터

현재 저장소에는 포맷 검증과 조합 탐색 테스트용 더미 데이터셋도 포함되어 있습니다.

- [demo_stock_universe.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_universe.csv)
- [demo_stock_prices.csv](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/demo/demo_stock_prices.csv)

구성:

- 8개 자산군
- 자산군당 4개 종목
- 약 2년치 영업일 가격 데이터
- 총 종목 수 32개

재생성 스크립트:

- [generate_demo_stock_data.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/scripts/generate_demo_stock_data.py)

예시 실행:

```bash
cd "/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo"
../.venv/bin/python scripts/generate_demo_stock_data.py
```

## 다음 단계 추천

1. 섹터별 후보 종목 리스트를 CSV로 만든다.
2. 각 종목의 adjusted close 시계열을 붙인다.
3. 섹터별 몇 개 종목을 뽑을지 규칙을 정한다.
4. 샘플링 횟수와 섹터 내부 가중 방식을 정한다.
5. 조합 탐색을 실행해서 최대 Sharpe 후보를 비교한다.
