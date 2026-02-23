"""Flask web application for the Gold Junior Mining Analyzer."""

from flask import Flask, render_template, request
from analyzer import rank_companies, score_company, compute_valuation, GOLD_PRICE_USD
from sample_data import SAMPLE_COMPANIES
from models import Stage

app = Flask(__name__)


def _format_number(value, decimals=1):
    """Format a number with comma separators."""
    if value is None:
        return "N/A"
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.{decimals}f}M"
    elif value >= 1_000:
        return f"{value / 1_000:,.{decimals}f}K"
    return f"{value:,.{decimals}f}"


def _format_currency(value, decimals=0):
    if value is None:
        return "N/A"
    return f"${value:,.{decimals}f}"


def _format_oz(value):
    if value is None or value == 0:
        return "N/A"
    return f"{value:,.0f} oz"


app.jinja_env.globals.update(
    format_number=_format_number,
    format_currency=_format_currency,
    format_oz=_format_oz,
    gold_price=GOLD_PRICE_USD,
)


@app.route("/")
def dashboard():
    stage_filter = request.args.get("stage", "all")
    sort_by = request.args.get("sort", "overall")

    companies = SAMPLE_COMPANIES
    if stage_filter != "all":
        companies = [c for c in companies if c.stage.value == stage_filter]

    ranked = rank_companies(companies)

    if sort_by == "ev_per_oz":
        ranked.sort(key=lambda x: x[1].ev_per_total_resource_oz or float("inf"))
    elif sort_by == "market_cap":
        ranked.sort(key=lambda x: x[0].financials.market_cap_m, reverse=True)
    elif sort_by == "resource":
        ranked.sort(key=lambda x: x[0].resource.total_oz, reverse=True)
    elif sort_by == "grade":
        ranked.sort(key=lambda x: x[0].resource.grade_g_per_t, reverse=True)
    # default: overall score (already sorted)

    return render_template(
        "dashboard.html",
        ranked=ranked,
        stage_filter=stage_filter,
        sort_by=sort_by,
        total_companies=len(SAMPLE_COMPANIES),
        stages=[s.value for s in Stage],
    )


@app.route("/company/<ticker>")
def company_detail(ticker):
    company = next((c for c in SAMPLE_COMPANIES if c.ticker == ticker), None)
    if company is None:
        return "Company not found", 404

    metrics, scores = score_company(company)
    return render_template(
        "company.html",
        company=company,
        metrics=metrics,
        scores=scores,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
