"""Data models for junior gold mining companies."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Stage(Enum):
    EXPLORATION = "Exploration"
    DEVELOPMENT = "Development"
    PRODUCTION = "Production"


class JurisdictionRisk(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"


JURISDICTION_RISK_MAP = {
    # Low risk
    "Canada": JurisdictionRisk.LOW,
    "Australia": JurisdictionRisk.LOW,
    "USA": JurisdictionRisk.LOW,
    "Finland": JurisdictionRisk.LOW,
    "Ireland": JurisdictionRisk.LOW,
    # Medium risk
    "Mexico": JurisdictionRisk.MEDIUM,
    "Brazil": JurisdictionRisk.MEDIUM,
    "Chile": JurisdictionRisk.MEDIUM,
    "Colombia": JurisdictionRisk.MEDIUM,
    "Peru": JurisdictionRisk.MEDIUM,
    "Argentina": JurisdictionRisk.MEDIUM,
    "Senegal": JurisdictionRisk.MEDIUM,
    "Burkina Faso": JurisdictionRisk.MEDIUM,
    "Ghana": JurisdictionRisk.MEDIUM,
    "Cote d'Ivoire": JurisdictionRisk.MEDIUM,
    "Turkey": JurisdictionRisk.MEDIUM,
    "Serbia": JurisdictionRisk.MEDIUM,
    # High risk
    "Tanzania": JurisdictionRisk.HIGH,
    "DRC": JurisdictionRisk.HIGH,
    "Mali": JurisdictionRisk.HIGH,
    "Guinea": JurisdictionRisk.HIGH,
    "Ecuador": JurisdictionRisk.HIGH,
    "Philippines": JurisdictionRisk.HIGH,
    "Indonesia": JurisdictionRisk.HIGH,
    "Papua New Guinea": JurisdictionRisk.HIGH,
    # Very high risk
    "Venezuela": JurisdictionRisk.VERY_HIGH,
    "Russia": JurisdictionRisk.VERY_HIGH,
    "Myanmar": JurisdictionRisk.VERY_HIGH,
    "Zimbabwe": JurisdictionRisk.VERY_HIGH,
}


@dataclass
class GoldResource:
    """Gold resource estimate in ounces, split by NI 43-101 / JORC categories."""
    measured_oz: float = 0.0
    indicated_oz: float = 0.0
    inferred_oz: float = 0.0
    grade_g_per_t: float = 0.0  # average grade in grams per tonne

    @property
    def total_mi_oz(self) -> float:
        """Measured + Indicated (higher confidence)."""
        return self.measured_oz + self.indicated_oz

    @property
    def total_oz(self) -> float:
        return self.measured_oz + self.indicated_oz + self.inferred_oz


@dataclass
class GoldReserve:
    """Proven and probable reserves (subset of resources that are economic)."""
    proven_oz: float = 0.0
    probable_oz: float = 0.0

    @property
    def total_oz(self) -> float:
        return self.proven_oz + self.probable_oz


@dataclass
class Financials:
    """Key financial metrics (all values in USD)."""
    market_cap_m: float = 0.0           # market cap in millions
    share_price: float = 0.0            # current share price
    shares_outstanding_m: float = 0.0   # shares outstanding in millions
    cash_m: float = 0.0                 # cash & equivalents in millions
    debt_m: float = 0.0                 # total debt in millions
    burn_rate_m_per_q: float = 0.0      # quarterly cash burn in millions
    revenue_m: Optional[float] = None   # annual revenue (producers only)

    @property
    def enterprise_value_m(self) -> float:
        return self.market_cap_m + self.debt_m - self.cash_m

    @property
    def net_cash_m(self) -> float:
        return self.cash_m - self.debt_m

    @property
    def cash_runway_quarters(self) -> Optional[float]:
        if self.burn_rate_m_per_q and self.burn_rate_m_per_q > 0:
            return self.cash_m / self.burn_rate_m_per_q
        return None


@dataclass
class ProductionMetrics:
    """For companies that are producing gold."""
    annual_production_oz: float = 0.0
    aisc_per_oz: float = 0.0  # all-in sustaining cost per ounce
    recovery_rate_pct: float = 0.0


@dataclass
class MiningCompany:
    """A junior gold mining company."""
    name: str
    ticker: str
    exchange: str
    stage: Stage
    jurisdiction: str
    description: str
    resource: GoldResource = field(default_factory=GoldResource)
    reserve: GoldReserve = field(default_factory=GoldReserve)
    financials: Financials = field(default_factory=Financials)
    production: Optional[ProductionMetrics] = None
    flagship_project: str = ""
    catalysts: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

    @property
    def jurisdiction_risk(self) -> JurisdictionRisk:
        return JURISDICTION_RISK_MAP.get(self.jurisdiction, JurisdictionRisk.HIGH)
