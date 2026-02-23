"""Sample junior gold mining company data for demonstration.

These are fictional companies inspired by real junior mining archetypes.
All data is illustrative and should not be used for investment decisions.
"""

from models import (
    MiningCompany, Stage, GoldResource, GoldReserve,
    Financials, ProductionMetrics,
)

SAMPLE_COMPANIES: list[MiningCompany] = [
    MiningCompany(
        name="Maple Gold Mines",
        ticker="MGM.V",
        exchange="TSXV",
        stage=Stage.EXPLORATION,
        jurisdiction="Canada",
        description="Exploring a large land package in the Abitibi greenstone belt, Quebec. "
                    "Multiple high-grade zones identified with ongoing drill programs.",
        flagship_project="Douay-Joutel Gold Project",
        resource=GoldResource(
            measured_oz=0,
            indicated_oz=850_000,
            inferred_oz=1_200_000,
            grade_g_per_t=1.4,
        ),
        financials=Financials(
            market_cap_m=45,
            share_price=0.12,
            shares_outstanding_m=375,
            cash_m=8,
            debt_m=0,
            burn_rate_m_per_q=1.5,
        ),
        catalysts=[
            "Upcoming drill results from Zone 531",
            "Potential JV with major miner",
            "Updated resource estimate expected Q3",
        ],
        risks=[
            "Early-stage exploration risk",
            "Dilution risk from future financings",
        ],
    ),

    MiningCompany(
        name="Andean Gold Corp",
        ticker="AGC.TO",
        exchange="TSX",
        stage=Stage.DEVELOPMENT,
        jurisdiction="Peru",
        description="Advancing a permitted open-pit gold project in southern Peru. "
                    "Feasibility study completed with strong economics.",
        flagship_project="Cerro Dorado Project",
        resource=GoldResource(
            measured_oz=500_000,
            indicated_oz=1_800_000,
            inferred_oz=900_000,
            grade_g_per_t=1.1,
        ),
        reserve=GoldReserve(
            proven_oz=400_000,
            probable_oz=1_500_000,
        ),
        financials=Financials(
            market_cap_m=180,
            share_price=1.45,
            shares_outstanding_m=124,
            cash_m=35,
            debt_m=20,
            burn_rate_m_per_q=4.0,
        ),
        catalysts=[
            "Construction decision expected H1",
            "Potential offtake agreement with gold streamer",
            "Environmental permit renewal (low risk)",
        ],
        risks=[
            "Construction financing still needed (~$200M)",
            "Peru political uncertainty",
            "Water access challenges in arid region",
        ],
    ),

    MiningCompany(
        name="Sahel Resources",
        ticker="SHR.AX",
        exchange="ASX",
        stage=Stage.EXPLORATION,
        jurisdiction="Burkina Faso",
        description="Exploring a highly prospective gold belt in West Africa with "
                    "multiple drill-ready targets across a 400 km² land package.",
        flagship_project="Banfora Gold Project",
        resource=GoldResource(
            measured_oz=0,
            indicated_oz=400_000,
            inferred_oz=2_500_000,
            grade_g_per_t=2.3,
        ),
        financials=Financials(
            market_cap_m=28,
            share_price=0.08,
            shares_outstanding_m=350,
            cash_m=5,
            debt_m=0,
            burn_rate_m_per_q=1.2,
        ),
        catalysts=[
            "Phase 2 drilling underway",
            "First resource estimate expected",
            "Regional consolidation target",
        ],
        risks=[
            "Political instability in Burkina Faso",
            "Limited infrastructure",
            "Security concerns in Sahel region",
        ],
    ),

    MiningCompany(
        name="Pacific Rim Gold",
        ticker="PRG.V",
        exchange="TSXV",
        stage=Stage.PRODUCTION,
        jurisdiction="Australia",
        description="Small-scale gold producer operating a high-grade underground mine "
                    "in Western Australia with exploration upside.",
        flagship_project="Kalgoorlie East Mine",
        resource=GoldResource(
            measured_oz=300_000,
            indicated_oz=700_000,
            inferred_oz=500_000,
            grade_g_per_t=5.8,
        ),
        reserve=GoldReserve(
            proven_oz=250_000,
            probable_oz=550_000,
        ),
        financials=Financials(
            market_cap_m=120,
            share_price=0.85,
            shares_outstanding_m=141,
            cash_m=22,
            debt_m=15,
            burn_rate_m_per_q=0,
            revenue_m=65,
        ),
        production=ProductionMetrics(
            annual_production_oz=35_000,
            aisc_per_oz=1_280,
            recovery_rate_pct=93.5,
        ),
        catalysts=[
            "Mine life extension from new ore zones",
            "Near-mine exploration drilling",
            "Cash flow growth at current gold prices",
        ],
        risks=[
            "Single-asset concentration risk",
            "Grade variability in underground mining",
            "Labor cost inflation in WA",
        ],
    ),

    MiningCompany(
        name="Nevada Goldstrike",
        ticker="NGS",
        exchange="NYSE-A",
        stage=Stage.DEVELOPMENT,
        jurisdiction="USA",
        description="Advancing a large-scale oxide gold heap-leach project in Nevada. "
                    "Low capex relative to resource size.",
        flagship_project="Railroad Valley Gold Project",
        resource=GoldResource(
            measured_oz=800_000,
            indicated_oz=2_500_000,
            inferred_oz=1_500_000,
            grade_g_per_t=0.65,
        ),
        reserve=GoldReserve(
            proven_oz=600_000,
            probable_oz=2_000_000,
        ),
        financials=Financials(
            market_cap_m=350,
            share_price=3.20,
            shares_outstanding_m=109,
            cash_m=80,
            debt_m=0,
            burn_rate_m_per_q=5.0,
        ),
        catalysts=[
            "Permitting milestone expected Q2",
            "Takeout target for mid-tier producers",
            "Updated PFS with improved economics",
        ],
        risks=[
            "Low grade means sensitivity to gold price",
            "Heap leach recovery rate risk",
            "Federal permitting timeline uncertainty",
        ],
    ),

    MiningCompany(
        name="Cordillera Mining",
        ticker="CMI.V",
        exchange="TSXV",
        stage=Stage.EXPLORATION,
        jurisdiction="Colombia",
        description="High-grade vein exploration project in the Mid-Cauca gold belt, "
                    "one of the world's most prolific gold districts.",
        flagship_project="Buritica North Project",
        resource=GoldResource(
            measured_oz=0,
            indicated_oz=200_000,
            inferred_oz=600_000,
            grade_g_per_t=8.5,
        ),
        financials=Financials(
            market_cap_m=22,
            share_price=0.18,
            shares_outstanding_m=122,
            cash_m=3.5,
            debt_m=0,
            burn_rate_m_per_q=0.8,
        ),
        catalysts=[
            "High-grade intercepts from current drill program",
            "Proximity to Zijin's Buritica mine",
            "Vein extensions open at depth",
        ],
        risks=[
            "Early-stage with small resource",
            "Colombia permitting complexity",
            "Community relations challenges",
        ],
    ),

    MiningCompany(
        name="Boreal Gold",
        ticker="BGL.V",
        exchange="TSXV",
        stage=Stage.DEVELOPMENT,
        jurisdiction="Finland",
        description="Developing a gold project in the Central Lapland Greenstone Belt, "
                    "Finland's premier gold district. Low political risk jurisdiction.",
        flagship_project="Soretiapulkka Gold Project",
        resource=GoldResource(
            measured_oz=200_000,
            indicated_oz=1_100_000,
            inferred_oz=700_000,
            grade_g_per_t=2.8,
        ),
        reserve=GoldReserve(
            proven_oz=150_000,
            probable_oz=800_000,
        ),
        financials=Financials(
            market_cap_m=95,
            share_price=0.62,
            shares_outstanding_m=153,
            cash_m=18,
            debt_m=5,
            burn_rate_m_per_q=2.5,
        ),
        catalysts=[
            "Construction permit application submitted",
            "EU critical minerals funding potential",
            "Proximity to Agnico Eagle's Kittila mine",
        ],
        risks=[
            "Finnish environmental permitting timeline",
            "Seasonal drilling limitations",
            "Small scale may limit economics",
        ],
    ),

    MiningCompany(
        name="Outback Minerals",
        ticker="OBM.AX",
        exchange="ASX",
        stage=Stage.EXPLORATION,
        jurisdiction="Australia",
        description="Grass-roots explorer with a large tenement package in the "
                    "Tanami region of the Northern Territory.",
        flagship_project="Tanami West Project",
        resource=GoldResource(
            measured_oz=0,
            indicated_oz=150_000,
            inferred_oz=350_000,
            grade_g_per_t=3.2,
        ),
        financials=Financials(
            market_cap_m=12,
            share_price=0.04,
            shares_outstanding_m=300,
            cash_m=2.5,
            debt_m=0,
            burn_rate_m_per_q=0.6,
        ),
        catalysts=[
            "Geophysical survey results pending",
            "Near Newmont's Tanami operations",
            "NT government exploration grants",
        ],
        risks=[
            "Very early stage",
            "Remote location with limited infrastructure",
            "Small resource base",
        ],
    ),
]
