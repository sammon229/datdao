"""Generate portfolio evidence visuals from the repository's source data.

The script intentionally uses only the Python standard library so the portfolio
can be refreshed without adding a plotting dependency to the repository.
"""

from __future__ import annotations

import csv
import html
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "evidence"
DATA_JS = ROOT / "projects" / "evidence-data.js"


def read_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        return list(csv.DictReader(handle))


def number(value: str | None) -> float | None:
    if value is None or value.strip() in {"", "NA", "N/A", "nan"}:
        return None
    try:
        return float(value.replace(",", ""))
    except ValueError:
        return None


def short_number(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.0f}"


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def svg_shell(title: str, subtitle: str, body: str, height: int = 420) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 {height}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(subtitle)}</desc>
  <rect width="840" height="{height}" rx="20" fill="#f8fafc"/>
  <text x="36" y="42" fill="#172033" font-family="Arial, sans-serif" font-size="22" font-weight="700">{esc(title)}</text>
  <text x="36" y="68" fill="#5f6e84" font-family="Arial, sans-serif" font-size="13">{esc(subtitle)}</text>
  {body}
</svg>
'''


def bar_chart(title: str, subtitle: str, labels: list[str], values: list[float], value_label: str, formatter=short_number) -> str:
    width, height = 840, 420
    chart_x, chart_y, chart_w, chart_h = 56, 112, 728, 238
    maximum = max(values) if values else 1
    gap = chart_w / max(len(values), 1)
    bar_w = min(74, gap * 0.64)
    body = [f'<text x="{chart_x}" y="94" fill="#2165d6" font-family="Arial, sans-serif" font-size="12" font-weight="700">{esc(value_label)}</text>']
    for index, (label, value) in enumerate(zip(labels, values)):
        x = chart_x + index * gap + (gap - bar_w) / 2
        bar_height = max(5, chart_h * value / maximum)
        y = chart_y + chart_h - bar_height
        body.append(f'<line x1="{chart_x}" y1="{chart_y + chart_h}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h}" stroke="#cbd5e1"/>') if index == 0 else None
        body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_height:.1f}" rx="7" fill="#2165d6" opacity=".88"/>')
        body.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 10:.1f}" text-anchor="middle" fill="#172033" font-family="Arial, sans-serif" font-size="12" font-weight="700">{esc(formatter(value))}</text>')
        body.append(f'<text x="{x + bar_w / 2:.1f}" y="{chart_y + chart_h + 24}" text-anchor="middle" fill="#5f6e84" font-family="Arial, sans-serif" font-size="11">{esc(label)}</text>')
    return svg_shell(title, subtitle, "\n  ".join(body), height)


def horizontal_chart(title: str, subtitle: str, labels: list[str], values: list[float], value_label: str) -> str:
    maximum = max(values) if values else 1
    body = [f'<text x="56" y="102" fill="#2165d6" font-family="Arial, sans-serif" font-size="12" font-weight="700">{esc(value_label)}</text>']
    row_h = 32
    for index, (label, value) in enumerate(zip(labels, values)):
        y = 126 + index * row_h
        bar_w = 500 * value / maximum
        body.append(f'<text x="56" y="{y + 16}" fill="#172033" font-family="Arial, sans-serif" font-size="12">{esc(label[:24])}</text>')
        body.append(f'<rect x="250" y="{y}" width="500" height="18" rx="9" fill="#e8eef5"/>')
        body.append(f'<rect x="250" y="{y}" width="{max(8, bar_w):.1f}" height="18" rx="9" fill="#12775b" opacity=".88"/>')
        body.append(f'<text x="770" y="{y + 14}" text-anchor="end" fill="#172033" font-family="Arial, sans-serif" font-size="12" font-weight="700">{esc(short_number(value))}</text>')
    return svg_shell(title, subtitle, "\n  ".join(body), 126 + len(labels) * row_h + 32)


def process_diagram(title: str, subtitle: str, steps: list[tuple[str, str]], note: str) -> str:
    body = []
    box_w, box_h, gap = 142, 92, 34
    start_x = 40
    y = 142
    for index, (label, detail) in enumerate(steps):
        x = start_x + index * (box_w + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="14" fill="#ffffff" stroke="#9db4d0" stroke-width="2"/>')
        body.append(f'<text x="{x + box_w / 2}" y="{y + 35}" text-anchor="middle" fill="#172033" font-family="Arial, sans-serif" font-size="14" font-weight="700">{esc(label)}</text>')
        body.append(f'<text x="{x + box_w / 2}" y="{y + 59}" text-anchor="middle" fill="#5f6e84" font-family="Arial, sans-serif" font-size="11">{esc(detail)}</text>')
        if index < len(steps) - 1:
            body.append(f'<path d="M {x + box_w + 8} {y + box_h / 2} H {x + box_w + gap - 8}" stroke="#2165d6" stroke-width="3" fill="none"/>')
            body.append(f'<path d="M {x + box_w + gap - 8} {y + box_h / 2} l -9 -6 v 12 z" fill="#2165d6"/>')
    body.append(f'<rect x="40" y="286" width="760" height="74" rx="12" fill="#edf7f3"/>')
    body.append(f'<text x="60" y="317" fill="#12775b" font-family="Arial, sans-serif" font-size="13" font-weight="700">{esc(note)}</text>')
    body.append(f'<text x="60" y="341" fill="#5f6e84" font-family="Arial, sans-serif" font-size="12">This visual distinguishes a reproducible method map from a measured model result.</text>')
    return svg_shell(title, subtitle, "\n  ".join(body))


def write(name: str, content: str) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(content, encoding="utf-8")
    return f"../images/evidence/{name}"


def main() -> None:
    evidence: dict[str, dict[str, str]] = {}

    fraud_image = write("fraud-evaluation.svg", process_diagram(
        "Fraud evaluation frame",
        "The project keeps five evaluation lenses visible instead of treating accuracy as the answer.",
        [("Precision", "false alarms"), ("Recall", "missed fraud"), ("F1", "balance"), ("Accuracy", "overall"), ("CV", "stability")],
        "Source dataset not included: the notebook requires creditcard_2023.csv locally.",
    ))
    evidence["fraud"] = {"image": fraud_image, "alt": "Evaluation map showing precision, recall, F1, accuracy, and cross-validation for fraud detection.", "kind": "Evaluation framework", "caption": "Generated from the project's documented evaluation design; no fraud rows are redistributed in this repository."}

    churn = read_csv(r"Tele Customer Churn Rate  Prediction Using Python/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    contract_totals: Counter[str] = Counter(row["Contract"] for row in churn)
    contract_churn: Counter[str] = Counter(row["Contract"] for row in churn if row["Churn"] == "Yes")
    contracts = ["Month-to-month", "One year", "Two year"]
    churn_rates = [100 * contract_churn[label] / contract_totals[label] for label in contracts]
    churn_image = write("churn-contract-rate.svg", bar_chart("Churn rate by contract", "Computed from 7,043 repository rows; percent of customers marked Churn = Yes.", ["Monthly", "One year", "Two year"], churn_rates, "CHURN RATE (%)", lambda value: f"{value:.1f}%"))
    evidence["churn"] = {"image": churn_image, "alt": "Bar chart comparing churn rate for month-to-month, one-year, and two-year contracts.", "kind": "Computed from repository data", "caption": f"Computed from {len(churn):,} rows in the Telco Customer Churn CSV; the chart supports the thesis that contract structure is a meaningful retention signal."}

    housing = read_csv(r"Predict housing prices in the US using R/train.csv")
    quality_values: dict[str, list[float]] = defaultdict(list)
    for row in housing:
        quality, price = row.get("OverallQual"), number(row.get("SalePrice"))
        if quality and price is not None:
            quality_values[quality].append(price)
    quality_keys = sorted(quality_values, key=lambda item: int(item))
    quality_keys = [key for key in quality_keys if 4 <= int(key) <= 9]
    quality_means = [mean(quality_values[key]) for key in quality_keys]
    housing_image = write("housing-r-quality.svg", bar_chart("Sale price rises with quality", "Training split from the Ames data; mean SalePrice by OverallQual.", [f"Q{key}" for key in quality_keys], quality_means, "MEAN SALE PRICE", lambda value: f"${value / 1000:.0f}K"))
    evidence["housing-r"] = {"image": housing_image, "alt": "Bar chart showing mean Ames sale price increasing across OverallQual levels four through nine.", "kind": "Computed from repository data", "caption": f"Computed from the {len(housing):,}-row R training file; the pattern supports the thesis that overall quality is a strong sale-price signal."}

    stocks_image = write("stocks-method-map.svg", process_diagram(
        "ETF forecasting method map",
        "The notebook compares two model families against historical Yahoo Finance OHLCV data.",
        [("OHLCV", "Yahoo Finance"), ("ARIMA", "classical"), ("LSTM", "recurrent"), ("MSE", "compare")],
        "External data required: the repository does not include a static price-history file.",
    ))
    evidence["stocks"] = {"image": stocks_image, "alt": "Method map showing OHLCV data flowing into ARIMA and LSTM before MSE comparison.", "kind": "Reproducible method map", "caption": "Generated from the notebook's documented pipeline; rerunning the notebook retrieves the external Yahoo Finance history."}

    king = read_csv(r"Real Estate Valuation Optimization in King County/kc_house_data.csv")
    grade_values: dict[str, list[float]] = defaultdict(list)
    for row in king:
        grade, price = row.get("grade"), number(row.get("price"))
        if grade and price is not None:
            grade_values[grade].append(price)
    grade_keys = sorted(grade_values, key=lambda item: int(item))
    grade_keys = [key for key in grade_keys if len(grade_values[key]) >= 100]
    king_image = write("king-county-grade.svg", bar_chart("Price by property grade", "Computed from 21,613 King County sales; median price for grades with at least 100 sales.", [f"G{key}" for key in grade_keys], [median(grade_values[key]) for key in grade_keys], "MEDIAN PRICE", lambda value: f"${value / 1000:.0f}K"))
    evidence["king-county"] = {"image": king_image, "alt": "Bar chart comparing median King County sale price across property grade levels.", "kind": "Computed from repository data", "caption": f"Computed from {len(king):,} King County rows; the monotonic grade pattern supports the thesis that property quality is an important valuation feature."}

    ames = read_csv(r"Data exploration and analysis using Python for residential properties in Ames, Iowa/cleaned_data.csv")
    ames_quality: dict[str, list[float]] = defaultdict(list)
    for row in ames:
        quality, price = row.get("OverallQual"), number(row.get("SalePrice"))
        if quality and price is not None:
            ames_quality[quality].append(price)
    ames_keys = sorted(ames_quality, key=lambda item: int(item))
    ames_keys = [key for key in ames_keys if 4 <= int(key) <= 9]
    ames_image = write("ames-quality.svg", bar_chart("SalePrice by overall quality", "Computed from the cleaned Ames file; mean SalePrice by OverallQual.", [f"Q{key}" for key in ames_keys], [mean(ames_quality[key]) for key in ames_keys], "MEAN SALE PRICE", lambda value: f"${value / 1000:.0f}K"))
    evidence["ames"] = {"image": ames_image, "alt": "Bar chart showing mean Ames SalePrice increasing across overall quality levels.", "kind": "Computed from repository data", "caption": f"Computed from {len(ames):,} cleaned Ames rows; the visual backs the thesis that quality and price move together."}

    nlp = read_csv(r"Enhancing Job Matching and Market Analysis through NLP/job_description.csv")
    category_counts = Counter(row.get("Category", "Unspecified") or "Unspecified" for row in nlp)
    top_categories = category_counts.most_common(8)
    nlp_image = write("nlp-category.svg", horizontal_chart("Job records by category", "Computed from 325 repository records; top categories by row count.", [label for label, _ in top_categories], [value for _, value in top_categories], "RECORD COUNT"))
    evidence["nlp"] = {"image": nlp_image, "alt": "Horizontal bar chart showing the most frequent job categories in the NLP dataset.", "kind": "Computed from repository data", "caption": f"Computed from {len(nlp):,} job-description rows; the category distribution shows why category-level evaluation matters for matching."}

    ecommerce = read_csv(r"E-Commerce BigData/data.csv")
    invoices_by_month: dict[str, set[str]] = defaultdict(set)
    for row in ecommerce:
        invoice, date_text = row.get("InvoiceNo", ""), row.get("InvoiceDate", "")
        try:
            month = datetime.strptime(date_text, "%m/%d/%Y %H:%M").strftime("%b '%y")
        except ValueError:
            continue
        invoices_by_month[month].add(invoice)
    month_order = sorted(invoices_by_month, key=lambda item: datetime.strptime(item, "%b '%y"))
    ecommerce_image = write("ecommerce-monthly.svg", bar_chart("Monthly invoice volume", "Computed from the repository data; distinct invoices by month.", month_order, [len(invoices_by_month[key]) for key in month_order], "DISTINCT INVOICES", lambda value: f"{value:,.0f}"))
    evidence["ecommerce"] = {"image": ecommerce_image, "alt": "Bar chart showing distinct monthly invoice counts across the e-commerce dataset.", "kind": "Computed from repository data", "caption": f"Computed from {len(ecommerce):,} e-commerce rows; the monthly shape supports the thesis for staged ingestion and replayable analysis."}

    DATA_JS.write_text("window.evidenceData = " + json.dumps(evidence, indent=2) + ";\n", encoding="utf-8")
    print(f"Generated {len(evidence)} evidence visuals in {OUT}")
    for key, item in evidence.items():
        print(f"{key}: {item['kind']} -> {item['image']}")


if __name__ == "__main__":
    main()
