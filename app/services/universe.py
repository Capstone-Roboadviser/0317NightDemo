from app.schemas import AssetInfo


ASSET_UNIVERSE = [
    AssetInfo(
        code="us_equity",
        name="US Equity",
        color="#0F4C81",
        description="Growth engine with the highest long-run return and largest drawdown risk.",
    ),
    AssetInfo(
        code="global_bond",
        name="Global Bond",
        color="#5B8E7D",
        description="Stability-focused bond sleeve for risk control.",
    ),
    AssetInfo(
        code="reit",
        name="REITs",
        color="#C97C5D",
        description="Income-oriented real asset exposure with equity-like cyclicality.",
    ),
    AssetInfo(
        code="gold",
        name="Gold",
        color="#C6A700",
        description="Diversifier that can cushion equity stress periods.",
    ),
    AssetInfo(
        code="cash",
        name="Cash",
        color="#7A7A7A",
        description="Low-volatility reserve for short-horizon and defensive allocations.",
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
