from pathlib import Path

from app.domain.enums import InvestmentHorizon, RiskProfile


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
ASSET_UNIVERSE_PATH = DATA_DIR / "asset_universe.json"
SAMPLE_MARKET_ASSUMPTIONS_PATH = DATA_DIR / "sample_market_assumptions.json"

APP_NAME = "자산배분 시뮬레이터 데모 API"
APP_DESCRIPTION = (
    "고정된 5개 자산군을 기준으로, 사용자의 위험 성향과 투자기간에 따라 "
    "효율적 투자선 상의 포트폴리오 예시를 계산하고 설명해주는 시뮬레이션 서비스"
)
APP_VERSION = "0.2.0"

RISK_FREE_RATE = 0.02
FRONTIER_POINT_COUNT = 24
RANDOM_PORTFOLIO_COUNT = 160
MINIMUM_HISTORY_ROWS = 252

DEFAULT_TARGET_VOLATILITY = {
    RiskProfile.CONSERVATIVE: 0.07,
    RiskProfile.BALANCED: 0.11,
    RiskProfile.GROWTH: 0.16,
}

HORIZON_VOLATILITY_ADJUSTMENT = {
    InvestmentHorizon.SHORT: -0.01,
    InvestmentHorizon.MEDIUM: 0.00,
    InvestmentHorizon.LONG: 0.01,
}

FALLBACK_WEIGHTS = {
    RiskProfile.CONSERVATIVE: {
        "us_equity": 0.18,
        "global_bond": 0.42,
        "reits": 0.08,
        "gold": 0.12,
        "cash": 0.20,
    },
    RiskProfile.BALANCED: {
        "us_equity": 0.36,
        "global_bond": 0.28,
        "reits": 0.14,
        "gold": 0.10,
        "cash": 0.12,
    },
    RiskProfile.GROWTH: {
        "us_equity": 0.52,
        "global_bond": 0.18,
        "reits": 0.15,
        "gold": 0.08,
        "cash": 0.07,
    },
}

DISCLAIMER_TEXT = (
    "본 결과는 샘플 데이터 기반의 데모용 자산배분 시뮬레이션이며, "
    "시장 예측이나 투자 자문을 제공하지 않습니다."
)
