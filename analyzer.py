"""Analysis engine for junior gold mining companies.

Computes valuation metrics, scores companies on multiple dimensions,
and ranks them for investment attractiveness.
"""

from dataclasses import dataclass
from models import MiningCompany, Stage, JurisdictionRisk

# Current gold price assumption (USD/oz) - update as needed
GOLD_PRICE_USD = 2350.0


@dataclass
class ValuationMetrics:
    """Computed valuation metrics for a mining company."""
    ev_per_total_resource_oz: float | None = None
    ev_per_mi_resource_oz: float | None = None
    ev_per_reserve_oz: float | None = None
    price_to_nav_ratio: float | None = None
    market_cap_per_resource_oz: float | None = None
    cash_runway_quarters: float | None = None
    aisc_margin_per_oz: float | None = None
    aisc_margin_pct: float | None = None


@dataclass
class ScoreBreakdown:
    """Score breakdown across dimensions (each 0-100)."""
    resource_quality: float = 0.0
    valuation: float = 0.0
    financial_health: float = 0.0
    jurisdiction: float = 0.0
    stage_progress: float = 0.0
    grade: float = 0.0
    overall: float = 0.0
    rank: int = 0
    rating: str = ""


def compute_valuation(company: MiningCompany) -> ValuationMetrics:
    """Compute valuation metrics for a company."""
    m = ValuationMetrics()
    ev = company.financials.enterprise_value_m

    total_res = company.resource.total_oz
    mi_res = company.resource.total_mi_oz
    reserve = company.reserve.total_oz

    if total_res > 0:
        m.ev_per_total_resource_oz = (ev * 1_000_000) / total_res
        m.market_cap_per_resource_oz = (company.financials.market_cap_m * 1_000_000) / total_res

    if mi_res > 0:
        m.ev_per_mi_resource_oz = (ev * 1_000_000) / mi_res

    if reserve > 0:
        m.ev_per_reserve_oz = (ev * 1_000_000) / reserve

    m.cash_runway_quarters = company.financials.cash_runway_quarters

    if company.production and company.production.aisc_per_oz > 0:
        m.aisc_margin_per_oz = GOLD_PRICE_USD - company.production.aisc_per_oz
        m.aisc_margin_pct = (m.aisc_margin_per_oz / GOLD_PRICE_USD) * 100

    return m


def _score_resource_quality(company: MiningCompany) -> float:
    """Score resource size and confidence (0-100)."""
    total = company.resource.total_oz
    mi = company.resource.total_mi_oz

    # Size score: 0-50 based on total resource ounces
    if total >= 10_000_000:
        size_score = 50
    elif total >= 5_000_000:
        size_score = 40
    elif total >= 2_000_000:
        size_score = 30
    elif total >= 1_000_000:
        size_score = 20
    elif total >= 500_000:
        size_score = 10
    else:
        size_score = 5

    # Confidence score: 0-30 based on M+I / total ratio
    if total > 0:
        mi_ratio = mi / total
        confidence_score = mi_ratio * 30
    else:
        confidence_score = 0

    # Reserve bonus: 0-20
    if company.reserve.total_oz > 0:
        reserve_ratio = company.reserve.total_oz / max(total, 1)
        reserve_score = min(reserve_ratio * 40, 20)
    else:
        reserve_score = 0

    return min(size_score + confidence_score + reserve_score, 100)


def _score_valuation(company: MiningCompany, metrics: ValuationMetrics) -> float:
    """Score valuation attractiveness (0-100). Lower EV/oz = better."""
    ev_oz = metrics.ev_per_total_resource_oz
    if ev_oz is None or ev_oz <= 0:
        return 0

    # For junior gold miners, EV/oz benchmarks:
    # <$20/oz = very cheap (exploration), <$50 = cheap, <$100 = fair,
    # <$200 = getting expensive, >$200 = expensive
    if company.stage == Stage.EXPLORATION:
        if ev_oz < 10:
            return 95
        elif ev_oz < 20:
            return 85
        elif ev_oz < 40:
            return 70
        elif ev_oz < 80:
            return 50
        elif ev_oz < 150:
            return 30
        else:
            return 15
    elif company.stage == Stage.DEVELOPMENT:
        if ev_oz < 30:
            return 95
        elif ev_oz < 60:
            return 80
        elif ev_oz < 100:
            return 65
        elif ev_oz < 175:
            return 45
        elif ev_oz < 300:
            return 25
        else:
            return 10
    else:  # Production
        if ev_oz < 80:
            return 90
        elif ev_oz < 150:
            return 75
        elif ev_oz < 250:
            return 55
        elif ev_oz < 400:
            return 35
        else:
            return 15


def _score_financial_health(company: MiningCompany) -> float:
    """Score financial health (0-100)."""
    score = 50.0  # base

    # Cash position relative to market cap
    if company.financials.market_cap_m > 0:
        cash_ratio = company.financials.cash_m / company.financials.market_cap_m
        if cash_ratio > 0.3:
            score += 20
        elif cash_ratio > 0.15:
            score += 10
        elif cash_ratio < 0.05:
            score -= 20

    # Debt load
    if company.financials.debt_m == 0:
        score += 15
    elif company.financials.market_cap_m > 0:
        debt_ratio = company.financials.debt_m / company.financials.market_cap_m
        if debt_ratio > 0.5:
            score -= 25
        elif debt_ratio > 0.3:
            score -= 15
        elif debt_ratio > 0.1:
            score -= 5

    # Cash runway
    runway = company.financials.cash_runway_quarters
    if runway is not None:
        if runway >= 8:
            score += 15
        elif runway >= 4:
            score += 5
        elif runway < 2:
            score -= 20

    return max(0, min(score, 100))


def _score_jurisdiction(company: MiningCompany) -> float:
    """Score jurisdiction risk (0-100). Safe jurisdictions score higher."""
    risk = company.jurisdiction_risk
    return {
        JurisdictionRisk.LOW: 90,
        JurisdictionRisk.MEDIUM: 60,
        JurisdictionRisk.HIGH: 30,
        JurisdictionRisk.VERY_HIGH: 10,
    }[risk]


def _score_stage(company: MiningCompany) -> float:
    """Score stage of progress (0-100). More advanced = higher."""
    base = {
        Stage.EXPLORATION: 25,
        Stage.DEVELOPMENT: 55,
        Stage.PRODUCTION: 80,
    }[company.stage]

    # Bonus if they have reserves (shows economic viability study done)
    if company.reserve.total_oz > 0:
        base += 15

    # Bonus if producing with good margins
    if company.production and company.production.aisc_per_oz > 0:
        margin = GOLD_PRICE_USD - company.production.aisc_per_oz
        if margin > 1000:
            base += 10
        elif margin > 500:
            base += 5

    return min(base, 100)


def _score_grade(company: MiningCompany) -> float:
    """Score ore grade (0-100). Higher grade = better."""
    g = company.resource.grade_g_per_t
    if g <= 0:
        return 0
    # Open pit benchmarks differ from underground, but as a general guide:
    # <0.5 g/t = low, 0.5-1.0 = moderate, 1.0-3.0 = good,
    # 3.0-8.0 = high grade, >8.0 = bonanza
    if g >= 10:
        return 100
    elif g >= 5:
        return 85
    elif g >= 3:
        return 70
    elif g >= 1.5:
        return 55
    elif g >= 1.0:
        return 40
    elif g >= 0.5:
        return 25
    else:
        return 10


# Weights for overall score
WEIGHTS = {
    "resource_quality": 0.20,
    "valuation": 0.25,
    "financial_health": 0.15,
    "jurisdiction": 0.10,
    "stage_progress": 0.15,
    "grade": 0.15,
}


def _rating_label(score: float) -> str:
    if score >= 80:
        return "Strong Buy"
    elif score >= 65:
        return "Buy"
    elif score >= 50:
        return "Hold"
    elif score >= 35:
        return "Weak Hold"
    else:
        return "Avoid"


def score_company(company: MiningCompany) -> tuple[ValuationMetrics, ScoreBreakdown]:
    """Score a company across all dimensions and return metrics + breakdown."""
    metrics = compute_valuation(company)

    breakdown = ScoreBreakdown()
    breakdown.resource_quality = _score_resource_quality(company)
    breakdown.valuation = _score_valuation(company, metrics)
    breakdown.financial_health = _score_financial_health(company)
    breakdown.jurisdiction = _score_jurisdiction(company)
    breakdown.stage_progress = _score_stage(company)
    breakdown.grade = _score_grade(company)

    breakdown.overall = (
        breakdown.resource_quality * WEIGHTS["resource_quality"]
        + breakdown.valuation * WEIGHTS["valuation"]
        + breakdown.financial_health * WEIGHTS["financial_health"]
        + breakdown.jurisdiction * WEIGHTS["jurisdiction"]
        + breakdown.stage_progress * WEIGHTS["stage_progress"]
        + breakdown.grade * WEIGHTS["grade"]
    )

    breakdown.rating = _rating_label(breakdown.overall)

    return metrics, breakdown


def rank_companies(
    companies: list[MiningCompany],
) -> list[tuple[MiningCompany, ValuationMetrics, ScoreBreakdown]]:
    """Score and rank a list of companies. Returns sorted list (best first)."""
    results = []
    for c in companies:
        m, s = score_company(c)
        results.append((c, m, s))

    results.sort(key=lambda x: x[2].overall, reverse=True)

    for i, (_, _, s) in enumerate(results, 1):
        s.rank = i

    return results
