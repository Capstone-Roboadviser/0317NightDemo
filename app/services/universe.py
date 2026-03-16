from app.schemas import AssetInfo


ASSET_UNIVERSE = [
    AssetInfo(
        code="us_equity",
        name="미국 주식",
        color="#0F4C81",
        description="장기 기대수익률이 높지만 변동성도 큰 성장 자산군입니다.",
    ),
    AssetInfo(
        code="global_bond",
        name="글로벌 채권",
        color="#5B8E7D",
        description="포트폴리오 변동성을 낮추는 안정형 자산군입니다.",
    ),
    AssetInfo(
        code="reit",
        name="리츠",
        color="#C97C5D",
        description="부동산 기반의 인컴 자산으로 분산 효과를 기대할 수 있습니다.",
    ),
    AssetInfo(
        code="gold",
        name="금",
        color="#C6A700",
        description="시장 불안 시 방어 역할을 기대할 수 있는 대체 자산군입니다.",
    ),
    AssetInfo(
        code="cash",
        name="현금성 자산",
        color="#7A7A7A",
        description="단기 운용과 유동성 확보를 위한 낮은 변동성 자산군입니다.",
    ),
]

ASSET_CODES = [asset.code for asset in ASSET_UNIVERSE]

RISK_PROFILE_TARGETS = {
    "conservative": 0.07,
    "balanced": 0.11,
    "growth": 0.16,
}

TIME_HORIZON_ADJUSTMENT = {
    "short": -0.01,
    "medium": 0.00,
    "long": 0.01,
}

MIN_WEIGHT_BY_ASSET = {
    "us_equity": 0.05,
    "global_bond": 0.10,
    "reit": 0.00,
    "gold": 0.00,
    "cash": 0.00,
}

MAX_WEIGHT_BY_ASSET = {
    "us_equity": 0.65,
    "global_bond": 0.70,
    "reit": 0.25,
    "gold": 0.25,
    "cash": 0.40,
}

FALLBACK_WEIGHTS = {
    "conservative": {
        "us_equity": 0.18,
        "global_bond": 0.42,
        "reit": 0.08,
        "gold": 0.12,
        "cash": 0.20,
    },
    "balanced": {
        "us_equity": 0.36,
        "global_bond": 0.28,
        "reit": 0.14,
        "gold": 0.10,
        "cash": 0.12,
    },
    "growth": {
        "us_equity": 0.52,
        "global_bond": 0.18,
        "reit": 0.15,
        "gold": 0.08,
        "cash": 0.07,
    },
}
