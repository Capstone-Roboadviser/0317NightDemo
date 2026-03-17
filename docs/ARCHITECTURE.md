# 아키텍처 문서

## 시스템 목표

이 데모의 목표는 아래 문장으로 고정합니다.

> 고정된 8개 자산군을 기준으로, 사용자의 위험 성향과 투자기간에 따라 Efficient Frontier 상의 포트폴리오 예시를 계산하고 설명해주는 시뮬레이션 서비스

즉 이 시스템은:

- 실거래 시스템이 아닙니다.
- 투자 예측 AI가 아닙니다.
- 종목 추천 시스템이 아닙니다.
- 자산배분 엔진 데모입니다.

## 최상위 계층

시스템은 6계층으로 나뉩니다.

### 1. Presentation Layer

사용자가 직접 보는 화면입니다.

- 메인 소개 문구
- 입력 폼
- Efficient Frontier 그래프
- 결과 카드
- 자산배분 비중
- 설명 문장
- 디스클레이머

관련 파일:

- [web.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/web.py)

### 2. API Layer

FastAPI 엔드포인트와 요청/응답 검증을 담당합니다.

관련 파일:

- [router.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/router.py)
- [portfolio.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/routes/portfolio.py)
- [health.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/routes/health.py)
- [request.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/schemas/request.py)
- [response.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/api/schemas/response.py)

### 3. Application Layer

비즈니스 흐름을 담당합니다.

- 위험 성향과 투자기간을 내부 목표 변동성으로 매핑
- 포트폴리오 ID 생성
- 계산 결과를 설명 문장과 함께 조합
- 프론트에서 바로 쓰기 쉬운 구조로 결과 정리

관련 파일:

- [portfolio_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/portfolio_service.py)
- [mapping_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/mapping_service.py)
- [explanation_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/explanation_service.py)
- [combination_search_service.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/services/combination_search_service.py)

### 4. Portfolio Engine Layer

핵심 계산 엔진입니다.

- 기대수익률 계산
- 공분산 계산
- 포트폴리오 수학
- 제약조건 구성
- Efficient Frontier 계산
- 현재 선택 포인트 선정

관련 파일:

- [returns.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/returns.py)
- [covariance.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/covariance.py)
- [math.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/math.py)
- [constraints.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/constraints.py)
- [optimizer.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/optimizer.py)
- [frontier.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/engine/frontier.py)

### 5. Data Layer

데모용 정적 데이터와 로딩 책임을 담당합니다.

- 자산군 정의
- 샘플 시장 가정
- 고정 시드 기반 샘플 수익률 생성

관련 파일:

- [asset_universe.json](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/asset_universe.json)
- [sample_market_assumptions.json](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/sample_market_assumptions.json)
- [repository.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/repository.py)
- [stock_repository.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/data/stock_repository.py)

### 6. Config / Ops Layer

배포와 설정을 담당합니다.

- 앱 이름/설명
- 기본 목표 변동성
- fallback 비중
- Railway 설정

관련 파일:

- [config.py](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/app/core/config.py)
- [railway.json](/Users/yoonseungjae/Documents/code/RoboAdviser/fastapi-demo/railway.json)

## 도메인 객체

핵심 도메인 모델은 아래와 같습니다.

### `AssetClass`

- 자산군 코드
- 표시 이름
- 카테고리
- 설명
- 최소/최대 비중

### `UserProfile`

- 위험 성향
- 투자기간
- 목표 변동성

### `FrontierPoint`

- 변동성
- 기대수익률
- 비중 벡터

### `PortfolioSimulationResult`

- 포트폴리오 ID
- 기대수익률
- 변동성
- 샤프 지수
- 자산 비중
- frontier 포인트
- 설명 문장

## 요청 흐름

전체 흐름은 아래와 같습니다.

사용자 입력
→ FastAPI Request Schema 검증
→ Application Service에서 내부 파라미터 변환
→ Portfolio Engine에서 frontier 계산
→ 목표 변동성에 맞는 포인트 선택
→ explanation 생성
→ Response Schema 직렬화
→ 프론트 렌더링

## 데이터 전략

이 프로젝트는 실시간 외부 시세를 직접 읽지 않습니다.

이유:

- 데모에서는 재현성이 더 중요함
- 발표 중 결과가 흔들리면 설명이 어려워짐
- 네트워크 실패가 UX를 해칠 수 있음

따라서 현재는 JSON 기반의 정적 데이터와 고정 시드 샘플 수익률을 사용합니다.

## 설계 원칙

- 노트북 셀 실행 순서 의존성을 제거합니다.
- 전역변수보다 명시적 입력/출력을 우선합니다.
- 계산 실패 시 fallback 전략을 제공합니다.
- NumPy/Pandas 객체는 API 응답 전에 JSON 직렬화 가능한 형태로 변환합니다.
- "예측", "추천", "수익 보장" 표현은 피하고 "시뮬레이션", "예시", "샘플 데이터 기반" 표현을 사용합니다.
