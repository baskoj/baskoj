#!/usr/bin/env python3
"""
J&T BANKA Portfolio Report Analyzer
Parses monthly PDF reports and generates an HTML dashboard.
"""

import glob
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Missing dependency. Install with: pip3 install pymupdf")
    sys.exit(1)

PDF_DIR = "/Users/jbasko/Documents/jt"
OUTPUT_FILE = os.path.join(PDF_DIR, "portfolio_report.html")


@dataclass
class Holding:
    asset_class: str = ""
    isin: str = ""
    name: str = ""
    currency: str = ""
    quantity: float = 0.0
    purchase_price: float = 0.0
    market_price: float = 0.0
    yield_pct: float = 0.0
    unrealized_pnl: float = 0.0
    total_value: float = 0.0
    weight_pct: float = 0.0


@dataclass
class CashAccount:
    name: str = ""
    currency: str = ""
    amount: float = 0.0
    fx_rate: str = ""
    total_value_czk: float = 0.0
    weight_pct: float = 0.0


@dataclass
class Transaction:
    date: str = ""
    amount: float = 0.0
    description: str = ""


@dataclass
class MonthlyReport:
    file_name: str = ""
    client_name: str = ""
    klid: str = ""
    kid: str = ""
    strategy: str = ""
    ref_currency: str = ""
    valuation_date: str = ""
    portfolio_value: float = 0.0
    cash_balance: float = 0.0
    total_value: float = 0.0
    return_since_inception: float = 0.0
    return_ytd: float = 0.0
    return_monthly: float = 0.0
    deposits_withdrawals: float = 0.0
    prev_date: str = ""
    prev_portfolio_value: float = 0.0
    prev_cash: float = 0.0
    prev_total: float = 0.0
    structure: dict = field(default_factory=dict)
    holdings: list = field(default_factory=list)
    cash_accounts: list = field(default_factory=list)
    transactions: list = field(default_factory=list)


def parse_czech_number(s: str) -> float:
    """Parse Czech-formatted number: 9 200 081,74 -> 9200081.74"""
    s = s.strip().replace("\xa0", " ")
    s = re.sub(r"\s+", "", s)
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def parse_percentage(s: str) -> float:
    """Parse percentage string: -0,08% -> -0.08"""
    s = s.strip().replace("%", "").replace(",", ".").replace("\xa0", "").replace(" ", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def extract_overview(text: str, report: MonthlyReport):
    """Extract data from the 'Základní přehled' page."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i, line in enumerate(lines):
        if line.startswith("KLID"):
            report.klid = line.split(":")[-1].strip()
        elif line.startswith("KID") and ":" in line:
            report.kid = line.split(":")[-1].strip()
        elif "Investiční strategie" in line:
            if i + 1 < len(lines):
                report.strategy = lines[i + 1]
        elif "Referenční měna" in line:
            if i + 1 < len(lines):
                report.ref_currency = lines[i + 1]

    # Extract current valuation block
    current_block = text.split("Aktuální ocenění")[-1]
    if "Předchozí ocenění" in current_block:
        current_block = current_block.split("Předchozí ocenění")[0]

    current_lines = [l.strip() for l in current_block.split("\n") if l.strip()]
    for i, line in enumerate(current_lines):
        if line == "Datum ocenění" and i + 1 < len(current_lines):
            report.valuation_date = current_lines[i + 1]
        elif line == "Hodnota portfolia" and i + 1 < len(current_lines):
            report.portfolio_value = parse_czech_number(current_lines[i + 1])
        elif line == "Stav na účtu" and i + 1 < len(current_lines):
            report.cash_balance = parse_czech_number(current_lines[i + 1])
        elif line == "Celkem" and i + 1 < len(current_lines):
            report.total_value = parse_czech_number(current_lines[i + 1])
        elif "počátku správy" in line and i + 1 < len(current_lines):
            report.return_since_inception = parse_percentage(current_lines[i + 1])
        elif "začátku roku" in line and i + 1 < len(current_lines):
            report.return_ytd = parse_percentage(current_lines[i + 1])
        elif "Uplynulý měsíc" in line and i + 1 < len(current_lines):
            report.return_monthly = parse_percentage(current_lines[i + 1])
        elif "Vklady/výběry" in line and i + 1 < len(current_lines):
            report.deposits_withdrawals = parse_czech_number(current_lines[i + 1])

    # Previous valuation
    if "Předchozí ocenění" in text:
        prev_block = text.split("Předchozí ocenění")[-1]
        prev_block = prev_block.split("Struktura")[0] if "Struktura" in prev_block else prev_block
        prev_lines = [l.strip() for l in prev_block.split("\n") if l.strip()]
        for i, line in enumerate(prev_lines):
            if line == "Datum ocenění" and i + 1 < len(prev_lines):
                report.prev_date = prev_lines[i + 1]
            elif line == "Hodnota portfolia" and i + 1 < len(prev_lines):
                report.prev_portfolio_value = parse_czech_number(prev_lines[i + 1])
            elif line == "Stav na účtu" and i + 1 < len(prev_lines):
                report.prev_cash = parse_czech_number(prev_lines[i + 1])
            elif line == "Celkem" and i + 1 < len(prev_lines):
                report.prev_total = parse_czech_number(prev_lines[i + 1])

    # Portfolio structure percentages
    struct_text = text.split("Struktura")[-1] if "Struktura" in text else ""
    pct_matches = re.findall(r"(\d+)\s*%", struct_text)
    asset_types_found = re.findall(r"(Akcie|Dluhopisy|Peněžní trh)", struct_text)
    if pct_matches and asset_types_found and len(pct_matches) == len(asset_types_found):
        report.structure = {
            asset_types_found[i]: int(pct_matches[i])
            for i in range(len(asset_types_found))
        }


def extract_holdings_from_page(page_text: str, report: MonthlyReport):
    """Extract holdings from 'Složení portfolia' page.

    Text layout per holding (stocks):
        Akcie / ISIN / Name / Currency / Qty / PurchasePrice / MarketPrice /
        Yield% / UnrealizedPnL / TotalValue / Weight%

    Bonds with AÚV have extra lines (accrued interest values).
    Strategy: collect all numeric values between ISINs, pick the LARGEST
    as total_value and the trailing small number as weight%.
    """
    lines = [l.strip() for l in page_text.split("\n") if l.strip()]

    current_class = ""
    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect asset class
        if line in ("Akcie", "Dluhopisy"):
            current_class = line

        # Detect ISIN
        if re.match(r"^[A-Z]{2}[A-Z0-9]{10}$", line):
            h = Holding(asset_class=current_class, isin=line)
            # Name follows ISIN
            i += 1
            if i < len(lines):
                h.name = lines[i]

            # Collect all values until next ISIN or asset class or page footer
            j = i + 1
            raw_values = []  # (line_index, raw_text)
            while j < len(lines) and j < i + 25:
                lj = lines[j]
                # Stop at next holding or footer
                if lj in ("Akcie", "Dluhopisy") or re.match(r"^[A-Z]{2}[A-Z0-9]{10}$", lj):
                    break
                if re.match(r"^\d{2}\.\d{2}\.\d{4}", lj):  # page footer date
                    break
                # Skip known text labels
                if lj in ("AÚV", "CZK", "EUR", "USD"):
                    j += 1
                    continue
                raw_values.append((j, lj))
                j += 1

            # Parse numeric values and percentages
            numbers = []  # (index, value, is_pct)
            for idx, raw in raw_values:
                raw_clean = raw.strip()
                if "%" in raw_clean:
                    pv = parse_percentage(raw_clean)
                    numbers.append((idx, pv, True))
                else:
                    nv = parse_czech_number(raw_clean)
                    if nv != 0 or raw_clean in ("0,00", "0,0000"):
                        numbers.append((idx, nv, False))

            # Weight% is the LAST percentage value
            pct_values = [(idx, v) for idx, v, is_pct in numbers if is_pct]
            non_pct = [(idx, v) for idx, v, is_pct in numbers if not is_pct]

            if pct_values:
                h.weight_pct = pct_values[-1][1]
                # Yield% is the first percentage (for single-pct holdings it's also weight)
                if len(pct_values) >= 2:
                    h.yield_pct = pct_values[0][1]

            # Total value = the LARGEST absolute value among non-pct numbers
            if non_pct:
                h.total_value = max(non_pct, key=lambda x: abs(x[1]))[1]

                # Unrealized PnL: look for signed number that isn't the total
                # It's typically the number just before total_value
                total_idx = max(non_pct, key=lambda x: abs(x[1]))[0]
                pnl_candidates = [(idx, v) for idx, v in non_pct if idx < total_idx and abs(v) > 1]
                if pnl_candidates:
                    h.unrealized_pnl = pnl_candidates[-1][1]

            report.holdings.append(h)
            i = j
            continue
        i += 1


def extract_cash_accounts(text: str, report: MonthlyReport):
    """Extract cash account data from 'Peněžní účty' page."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i, line in enumerate(lines):
        if line.startswith("J&T_"):
            acc = CashAccount(name=line)
            nums = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith("J&T_") and "CELKEM" not in lines[j]:
                if "CZK" in lines[j] and "/" in lines[j]:
                    acc.fx_rate = lines[j]
                elif lines[j] in ("CZK", "EUR", "USD"):
                    acc.currency = lines[j]
                else:
                    val = lines[j].replace("%", "").strip()
                    parsed = parse_czech_number(val)
                    if parsed != 0:
                        nums.append(parsed)
                    elif "%" in lines[j]:
                        nums.append(parse_percentage(lines[j]))
                j += 1

            if nums:
                acc.amount = nums[0] if len(nums) > 0 else 0
                acc.total_value_czk = nums[-2] if len(nums) >= 2 else nums[0]
                acc.weight_pct = nums[-1] if len(nums) >= 2 and nums[-1] < 100 else 0

            report.cash_accounts.append(acc)


def extract_transactions(text: str, report: MonthlyReport):
    """Extract transactions from cash account statement page."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i, line in enumerate(lines):
        m = re.match(r"^(\d{2}\.\d{2}\.\d{4})$", line)
        if m and i + 1 < len(lines):
            tx = Transaction(date=m.group(1))
            j = i + 1
            if j < len(lines):
                tx.amount = parse_czech_number(lines[j])
                j += 1
            if j < len(lines) and not re.match(r"^\d{2}\.\d{2}\.\d{4}$", lines[j]):
                tx.description = lines[j]
            report.transactions.append(tx)


def parse_pdf(filepath: str) -> MonthlyReport:
    """Parse a single PDF report."""
    report = MonthlyReport(file_name=os.path.basename(filepath))
    doc = fitz.open(filepath)

    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())

    # Page 0: cover
    cover_lines = [l.strip() for l in pages_text[0].split("\n") if l.strip()]
    if cover_lines:
        report.client_name = cover_lines[0].split("|")[0].strip()

    # Page 1: overview
    if len(pages_text) > 1:
        extract_overview(pages_text[1], report)

    # Page 2: holdings (may span multiple pages)
    for p in range(2, len(pages_text)):
        txt = pages_text[p]
        if "Složení portfolia" in txt or ("ISIN" in txt and "Název CP" in txt):
            extract_holdings_from_page(txt, report)
        elif "Peněžní účty" in txt:
            extract_cash_accounts(txt, report)
            break

    # Transactions: find cash account statement page
    for p in range(len(pages_text)):
        if "Výpis z klientského účtu" in pages_text[p]:
            extract_transactions(pages_text[p], report)
            break

    doc.close()
    return report


def sort_key(report: MonthlyReport) -> str:
    try:
        return datetime.strptime(report.valuation_date, "%d.%m.%Y").strftime("%Y%m%d")
    except ValueError:
        return report.valuation_date


def fmt_czk(value: float) -> str:
    if value == 0:
        return "0,00"
    sign = "-" if value < 0 else ""
    v = abs(value)
    integer_part = int(v)
    decimal_part = round((v - integer_part) * 100)
    int_str = f"{integer_part:,}".replace(",", " ")
    return f"{sign}{int_str},{decimal_part:02d}"


def fmt_pct(value: float) -> str:
    return f"{value:+.2f}%".replace(".", ",")


def pct_color(value: float) -> str:
    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    return "neutral"


def compute_cash_change(r: MonthlyReport) -> float:
    """Compute month-over-month CZK change in total value."""
    if r.prev_total and r.prev_total > 0:
        return r.total_value - r.prev_total
    return 0.0


def generate_key_points(reports: list) -> list[str]:
    """Auto-generate key insight bullets from the data."""
    points = []
    latest = reports[-1]
    first = reports[0]

    # Allocation shift
    first_struct = first.structure
    latest_struct = latest.structure
    if "Akcie" not in first_struct and "Akcie" in latest_struct:
        points.append(
            f"Equities introduced in portfolio — grew from 0% to {latest_struct.get('Akcie', 0)}% allocation"
        )
    if first_struct.get("Peněžní trh", 0) > 50 and latest_struct.get("Peněžní trh", 0) < 30:
        points.append(
            f"Cash allocation reduced from {first_struct.get('Peněžní trh', 0)}% to "
            f"{latest_struct.get('Peněžní trh', 0)}% — capital actively deployed"
        )
    if latest_struct.get("Dluhopisy", 0) > first_struct.get("Dluhopisy", 0):
        points.append(
            f"Bond allocation grew from {first_struct.get('Dluhopisy', 0)}% to "
            f"{latest_struct.get('Dluhopisy', 0)}%"
        )

    # Deposits
    total_deposits = sum(
        tx.amount for r in reports for tx in r.transactions if tx.amount > 0
        and ("Vklad" in tx.description or "Převod" in tx.description)
    )
    if total_deposits > 0:
        points.append(f"Total cash inflows over period: {fmt_czk(total_deposits)} CZK")

    # Management fees
    total_fees = sum(
        abs(tx.amount) for r in reports for tx in r.transactions
        if "Odměna" in tx.description or "Poplatek" in tx.description or "Náklad" in tx.description
    )
    if total_fees > 0:
        points.append(f"Total management fees charged: {fmt_czk(total_fees)} CZK")

    # Number of holdings
    if latest.holdings:
        n_equities = len([h for h in latest.holdings if h.asset_class == "Akcie"])
        n_bonds = len([h for h in latest.holdings if h.asset_class == "Dluhopisy"])
        points.append(f"Current portfolio holds {n_equities} equity positions and {n_bonds} bond/ETF positions")

    # Diversification
    currencies = set()
    for h in latest.holdings:
        if h.currency:
            currencies.add(h.currency)
    if len(currencies) > 1:
        points.append(f"Multi-currency exposure: {', '.join(sorted(currencies))}")

    return points


def generate_performance_highlights(reports: list) -> list[str]:
    """Auto-generate performance highlight bullets."""
    highlights = []
    latest = reports[-1]

    # Best and worst month
    if len(reports) > 1:
        best = max(reports, key=lambda r: r.return_monthly)
        worst = min(reports, key=lambda r: r.return_monthly)
        best_czk = compute_cash_change(best)
        worst_czk = compute_cash_change(worst)
        highlights.append(
            f"Best month: {best.valuation_date} at {fmt_pct(best.return_monthly)} "
            f"({fmt_czk(best_czk)} CZK)"
        )
        if worst.return_monthly < 0:
            highlights.append(
                f"Worst month: {worst.valuation_date} at {fmt_pct(worst.return_monthly)} "
                f"({fmt_czk(worst_czk)} CZK)"
            )

    # Positive months streak
    positive_months = sum(1 for r in reports if r.return_monthly > 0)
    highlights.append(
        f"{positive_months} out of {len(reports)} months had positive returns"
    )

    # Top and bottom holdings
    if latest.holdings:
        gainers = [h for h in latest.holdings if h.yield_pct > 0]
        losers = [h for h in latest.holdings if h.yield_pct < 0]
        if gainers:
            top = max(gainers, key=lambda h: h.yield_pct)
            highlights.append(
                f"Top performer: {top.name} at {fmt_pct(top.yield_pct)} "
                f"(unrealized {fmt_czk(top.unrealized_pnl)} CZK)"
            )
        if losers:
            bottom = min(losers, key=lambda h: h.yield_pct)
            highlights.append(
                f"Weakest performer: {bottom.name} at {fmt_pct(bottom.yield_pct)} "
                f"(unrealized {fmt_czk(bottom.unrealized_pnl)} CZK)"
            )

    # Overall return in CZK
    first = reports[0]
    total_gain = latest.total_value - first.total_value
    highlights.append(
        f"Total portfolio change: {fmt_czk(total_gain)} CZK ({fmt_pct(latest.return_since_inception)})"
    )

    return highlights


def generate_html(reports: list) -> str:
    reports.sort(key=sort_key)
    client = reports[0].client_name if reports else "Unknown"
    latest = reports[-1]
    first = reports[0]

    totals = [r.total_value for r in reports]
    max_total = max(totals) if totals else 1

    asset_colors = {
        "Akcie": "#2E86AB",
        "Dluhopisy": "#A23B72",
        "Peněžní trh": "#C18C5D",
    }

    key_points = generate_key_points(reports)
    perf_highlights = generate_performance_highlights(reports)

    total_change = latest.total_value - first.total_value
    total_change_pct = (total_change / first.total_value * 100) if first.total_value else 0

    html = f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Report - {client}</title>
<style>
    :root {{
        --bg: #0f1923;
        --card: #172a3a;
        --border: #2a3f50;
        --text: #e0e6ed;
        --text-muted: #8899a6;
        --accent: #c8a951;
        --positive: #4caf50;
        --negative: #ef5350;
        --neutral: #8899a6;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        background: var(--bg);
        color: var(--text);
        padding: 2rem;
        line-height: 1.6;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    header {{
        text-align: center;
        padding: 2rem 0;
        border-bottom: 2px solid var(--accent);
        margin-bottom: 2rem;
    }}
    header h1 {{
        font-size: 1.8rem;
        color: var(--accent);
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    header .subtitle {{
        color: var(--text-muted);
        margin-top: 0.5rem;
        font-size: 0.95rem;
    }}
    .card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    .card h2 {{
        color: var(--accent);
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }}
    .card h3 {{
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 500;
        margin: 1.2rem 0 0.6rem;
    }}
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    .kpi {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }}
    .kpi .label {{
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .kpi .value {{
        font-size: 1.6rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }}
    .kpi .sub {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }}
    .positive {{ color: var(--positive); }}
    .negative {{ color: var(--negative); }}
    .neutral {{ color: var(--neutral); }}
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }}
    th {{
        text-align: left;
        padding: 0.7rem 0.8rem;
        color: var(--text-muted);
        font-weight: 500;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid var(--border);
    }}
    th.right, td.right {{ text-align: right; }}
    td {{
        padding: 0.6rem 0.8rem;
        border-bottom: 1px solid rgba(42, 63, 80, 0.5);
    }}
    tr:hover {{ background: rgba(200, 169, 81, 0.05); }}
    .bar-chart {{
        display: flex;
        align-items: flex-end;
        gap: 1.5rem;
        height: 200px;
        padding: 1rem 0;
    }}
    .bar-col {{
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
        justify-content: flex-end;
    }}
    .bar {{
        width: 60%;
        min-width: 40px;
        background: linear-gradient(180deg, var(--accent), #8a7235);
        border-radius: 6px 6px 0 0;
    }}
    .bar-label {{
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        text-align: center;
    }}
    .bar-value {{
        font-size: 0.75rem;
        color: var(--accent);
        margin-bottom: 0.3rem;
        text-align: center;
        white-space: nowrap;
    }}
    .stacked-bar-chart {{
        display: flex;
        gap: 1.5rem;
        padding: 1rem 0;
    }}
    .stacked-col {{
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .stacked-bar {{
        width: 80%;
        min-width: 50px;
        height: 30px;
        border-radius: 6px;
        overflow: hidden;
        display: flex;
    }}
    .stacked-segment {{
        height: 100%;
    }}
    .legend {{
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin-top: 1rem;
        flex-wrap: wrap;
    }}
    .legend-item {{
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.85rem;
        color: var(--text-muted);
    }}
    .legend-dot {{
        width: 12px;
        height: 12px;
        border-radius: 3px;
    }}
    ul.insights {{
        list-style: none;
        padding: 0;
    }}
    ul.insights li {{
        padding: 0.5rem 0;
        padding-left: 1.2rem;
        position: relative;
        border-bottom: 1px solid rgba(42, 63, 80, 0.3);
        font-size: 0.9rem;
    }}
    ul.insights li:last-child {{ border-bottom: none; }}
    ul.insights li::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0.85rem;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent);
    }}
    .summary-box {{
        background: rgba(200, 169, 81, 0.08);
        border: 1px solid rgba(200, 169, 81, 0.25);
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        line-height: 1.7;
    }}
    .metric-row {{
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0;
        border-bottom: 1px solid rgba(42, 63, 80, 0.3);
    }}
    .metric-row:last-child {{ border-bottom: none; }}
    .metric-label {{ color: var(--text-muted); }}
    .metric-values {{ display: flex; gap: 2rem; text-align: right; }}
    .metric-values .cash {{ min-width: 140px; }}
    .metric-values .pct {{ min-width: 80px; }}
    .meta {{
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
        font-size: 0.85rem;
        color: var(--text-muted);
    }}
    .meta span {{ display: flex; gap: 0.4rem; }}
    .meta .val {{ color: var(--text); }}
    footer {{
        text-align: center;
        padding: 2rem 0 1rem;
        color: var(--text-muted);
        font-size: 0.8rem;
    }}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>Portfolio Analysis</h1>
        <div class="subtitle">{client} &mdash; J&amp;T BANKA &mdash; {first.valuation_date} to {latest.valuation_date}</div>
    </header>
"""

    # ===== SECTION 1: OVERVIEW =====
    html += """    <div class="card">
        <h2>Overview</h2>
"""
    # Overview metric rows for each report
    html += """        <table>
            <tr>
                <th>Metric</th>
"""
    for r in reports:
        html += f"""                <th class="right">{r.valuation_date}</th>
"""
    html += """            </tr>
"""

    # Portfolio Value row
    html += """            <tr>
                <td>Portfolio Value (investments)</td>
"""
    for r in reports:
        pv_pct = (r.portfolio_value / r.total_value * 100) if r.total_value else 0
        html += f"""                <td class="right">{fmt_czk(r.portfolio_value)} <span style="color:var(--text-muted);font-size:0.8rem;">({pv_pct:.0f}%)</span></td>
"""
    html += """            </tr>
"""

    # Cash on Account row
    html += """            <tr>
                <td>Cash on Account</td>
"""
    for r in reports:
        cash_pct = (r.cash_balance / r.total_value * 100) if r.total_value else 0
        html += f"""                <td class="right">{fmt_czk(r.cash_balance)} <span style="color:var(--text-muted);font-size:0.8rem;">({cash_pct:.0f}%)</span></td>
"""
    html += """            </tr>
"""

    # Total row
    html += """            <tr>
                <td><strong>Total</strong></td>
"""
    for r in reports:
        html += f"""                <td class="right"><strong>{fmt_czk(r.total_value)}</strong> <span style="color:var(--text-muted);font-size:0.8rem;">(100%)</span></td>
"""
    html += """            </tr>
"""

    # Return since inception
    html += """            <tr>
                <td>Return Since Inception</td>
"""
    for r in reports:
        czk_gain = r.total_value - first.total_value + (first.deposits_withdrawals - r.deposits_withdrawals if r != first else 0)
        html += f"""                <td class="right {pct_color(r.return_since_inception)}">{fmt_pct(r.return_since_inception)}</td>
"""
    html += """            </tr>
"""

    # YTD Return
    html += """            <tr>
                <td>YTD Return</td>
"""
    for r in reports:
        html += f"""                <td class="right {pct_color(r.return_ytd)}">{fmt_pct(r.return_ytd)}</td>
"""
    html += """            </tr>
"""

    # Monthly Return
    html += """            <tr>
                <td>Monthly Return</td>
"""
    for r in reports:
        monthly_czk = compute_cash_change(r)
        czk_str = f" ({fmt_czk(monthly_czk)})" if monthly_czk != 0 else ""
        html += f"""                <td class="right {pct_color(r.return_monthly)}">{fmt_pct(r.return_monthly)}<span style="color:var(--text-muted);font-size:0.8rem;">{czk_str}</span></td>
"""
    html += """            </tr>
"""

    # Deposits / Withdrawals
    html += """            <tr>
                <td>Net Deposits / Withdrawals</td>
"""
    for r in reports:
        html += f"""                <td class="right">{fmt_czk(r.deposits_withdrawals)}</td>
"""
    html += """            </tr>
        </table>
    </div>
"""

    # ===== SECTION 2: KEY POINTS =====
    html += """    <div class="card">
        <h2>Key Points</h2>
        <ul class="insights">
"""
    for point in key_points:
        html += f"""            <li>{point}</li>
"""
    html += """        </ul>
    </div>
"""

    # ===== SECTION 3: PERFORMANCE HIGHLIGHTS =====
    html += """    <div class="card">
        <h2>Performance Highlights</h2>
        <ul class="insights">
"""
    for hl in perf_highlights:
        html += f"""            <li>{hl}</li>
"""
    html += """        </ul>
    </div>
"""

    # ===== CHARTS =====
    # Portfolio Value Bar Chart
    html += """    <div class="card">
        <h2>Portfolio Value Over Time (CZK)</h2>
        <div class="bar-chart">
"""
    for r in reports:
        bar_h = int((r.total_value / max_total) * 160) if max_total else 0
        html += f"""            <div class="bar-col">
                <div class="bar-value">{fmt_czk(r.total_value)}</div>
                <div class="bar" style="height: {bar_h}px;"></div>
                <div class="bar-label">{r.valuation_date}</div>
            </div>
"""
    html += """        </div>
    </div>
"""

    # Asset Allocation Evolution
    html += """    <div class="card">
        <h2>Asset Allocation Evolution</h2>
        <div class="stacked-bar-chart">
"""
    for r in reports:
        html += f"""            <div class="stacked-col">
                <div class="stacked-bar">
"""
        for at in ["Akcie", "Dluhopisy", "Peněžní trh"]:
            pct = r.structure.get(at, 0)
            color = asset_colors.get(at, "#666")
            if pct > 0:
                html += f"""                    <div class="stacked-segment" style="width:{pct}%; background:{color};" title="{at}: {pct}%"></div>
"""
        html += f"""                </div>
                <div class="bar-label">{r.valuation_date}</div>
            </div>
"""
    html += """        </div>
        <div class="legend">
"""
    for at in ["Akcie", "Dluhopisy", "Peněžní trh"]:
        color = asset_colors.get(at, "#666")
        html += f"""            <div class="legend-item"><div class="legend-dot" style="background:{color};"></div>{at}</div>
"""
    html += """        </div>
    </div>
"""

    # ===== CURRENT HOLDINGS =====
    if latest.holdings:
        holdings_total = sum(h.total_value for h in latest.holdings)
        html += f"""    <div class="card">
        <h2>Current Holdings ({latest.valuation_date})</h2>
        <table>
            <tr>
                <th>Asset Class</th>
                <th>Name</th>
                <th>ISIN</th>
                <th class="right">Value (CZK)</th>
                <th class="right">Weight</th>
                <th class="right">Yield</th>
                <th class="right">Unrealized P&amp;L</th>
            </tr>
"""
        for h in latest.holdings:
            yield_cls = pct_color(h.yield_pct)
            pnl_cls = pct_color(h.unrealized_pnl)
            html += f"""            <tr>
                <td>{h.asset_class}</td>
                <td>{h.name}</td>
                <td style="font-family:monospace;font-size:0.8rem;">{h.isin}</td>
                <td class="right">{fmt_czk(h.total_value)}</td>
                <td class="right">{h.weight_pct:.2f}%</td>
                <td class="right {yield_cls}">{fmt_pct(h.yield_pct) if h.yield_pct else '—'}</td>
                <td class="right {pnl_cls}">{fmt_czk(h.unrealized_pnl) if h.unrealized_pnl else '—'}</td>
            </tr>
"""
        html += f"""            <tr style="border-top:2px solid var(--border);font-weight:600;">
                <td colspan="3">Total Investments</td>
                <td class="right">{fmt_czk(holdings_total)}</td>
                <td colspan="3"></td>
            </tr>
        </table>
    </div>
"""

    # ===== CASH ACCOUNTS =====
    if latest.cash_accounts:
        html += f"""    <div class="card">
        <h2>Cash Accounts ({latest.valuation_date})</h2>
        <table>
            <tr>
                <th>Account</th>
                <th>Currency</th>
                <th class="right">Balance</th>
                <th>FX Rate</th>
                <th class="right">Value (CZK)</th>
                <th class="right">Weight</th>
            </tr>
"""
        for ca in latest.cash_accounts:
            html += f"""            <tr>
                <td>{ca.name}</td>
                <td>{ca.currency}</td>
                <td class="right">{fmt_czk(ca.amount)}</td>
                <td>{ca.fx_rate}</td>
                <td class="right">{fmt_czk(ca.total_value_czk)}</td>
                <td class="right">{ca.weight_pct:.2f}%</td>
            </tr>
"""
        html += """        </table>
    </div>
"""

    # ===== TRANSACTIONS =====
    for r in reports:
        if r.transactions:
            html += f"""    <div class="card">
        <h2>Transactions &mdash; {r.valuation_date}</h2>
        <table>
            <tr><th>Date</th><th class="right">Amount (CZK)</th><th>Description</th></tr>
"""
            for tx in r.transactions:
                css = "positive" if tx.amount > 0 else "negative"
                html += f"""            <tr>
                <td style="color:var(--text-muted);">{tx.date}</td>
                <td class="right {css}">{fmt_czk(tx.amount)}</td>
                <td>{tx.description}</td>
            </tr>
"""
            html += """        </table>
    </div>
"""

    # ===== SUMMARY =====
    html += """    <div class="card">
        <h2>Summary</h2>
        <div class="summary-box">
"""
    html += f"""            <div class="metric-row">
                <span class="metric-label">Period</span>
                <span>{first.valuation_date} &rarr; {latest.valuation_date} ({len(reports)} months)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Starting Value</span>
                <span><strong>{fmt_czk(first.total_value)} CZK</strong></span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Ending Value</span>
                <span><strong>{fmt_czk(latest.total_value)} CZK</strong></span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Total Change</span>
                <span class="{pct_color(total_change)}"><strong>{fmt_czk(total_change)} CZK</strong> ({fmt_pct(total_change_pct)})</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Return Since Inception</span>
                <span class="{pct_color(latest.return_since_inception)}"><strong>{fmt_pct(latest.return_since_inception)}</strong></span>
            </div>
            <div class="metric-row">
                <span class="metric-label">YTD Return (2026)</span>
                <span class="{pct_color(latest.return_ytd)}"><strong>{fmt_pct(latest.return_ytd)}</strong></span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Latest Monthly Return</span>
                <span class="{pct_color(latest.return_monthly)}"><strong>{fmt_pct(latest.return_monthly)}</strong> ({fmt_czk(compute_cash_change(latest))} CZK)</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Investment Strategy</span>
                <span>{latest.strategy}</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Current Allocation</span>
                <span>{' / '.join(f'{k}: {v}%' for k, v in latest.structure.items())}</span>
            </div>
"""
    html += """        </div>
    </div>
"""

    # Metadata
    r0 = reports[0]
    html += f"""    <div class="card">
        <h2>Report Metadata</h2>
        <div class="meta">
            <span>Client: <span class="val">{r0.client_name}</span></span>
            <span>KLID: <span class="val">{r0.klid}</span></span>
            <span>KID: <span class="val">{r0.kid}</span></span>
            <span>Strategy: <span class="val">{r0.strategy}</span></span>
            <span>Currency: <span class="val">{r0.ref_currency}</span></span>
            <span>Reports analyzed: <span class="val">{len(reports)}</span></span>
        </div>
    </div>
"""

    html += f"""    <footer>
        Generated on {datetime.now().strftime("%d.%m.%Y %H:%M")} &mdash; PDF source: {PDF_DIR}
    </footer>
</div>
</body>
</html>"""

    return html


def main():
    pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {PDF_DIR}")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF files:")
    for f in sorted(pdf_files):
        print(f"  - {os.path.basename(f)}")

    reports = []
    for f in sorted(pdf_files):
        print(f"Parsing: {os.path.basename(f)}...")
        try:
            report = parse_pdf(f)
            reports.append(report)
            print(f"  -> {report.valuation_date} | Total: {fmt_czk(report.total_value)} CZK | Monthly: {fmt_pct(report.return_monthly)}")
            if report.holdings:
                print(f"     Holdings: {len(report.holdings)} positions")
                for h in report.holdings:
                    print(f"       {h.name}: {fmt_czk(h.total_value)} CZK ({h.weight_pct:.2f}%)")
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    if not reports:
        print("No reports could be parsed.")
        sys.exit(1)

    html = generate_html(reports)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nHTML report generated: {OUTPUT_FILE}")
    print(f"Open in browser: file://{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
