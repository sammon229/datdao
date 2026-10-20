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
    gap = 24
    box_w = min(142, (760 - gap * max(0, len(steps) - 1)) / max(1, len(steps)))
    box_h = 92
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


def scatter_chart(
    title: str,
    subtitle: str,
    xs: list[float],
    ys: list[float],
    x_label: str,
    y_label: str,
    formatter=short_number,
) -> str:
    """Create an accessible, dependency-free scatter plot with direct labels."""
    pairs = [(x, y) for x, y in zip(xs, ys) if math.isfinite(x) and math.isfinite(y)]
    if not pairs:
        return svg_shell(title, subtitle, '<text x="56" y="160" fill="#5f6e84" font-family="Arial, sans-serif" font-size="14">No numeric observations available.</text>')
    step = max(1, len(pairs) // 260)
    pairs = pairs[::step]
    x_values, y_values = zip(*pairs)
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    x_span = x_max - x_min or 1
    y_span = y_max - y_min or 1
    chart_x, chart_y, chart_w, chart_h = 76, 112, 680, 238
    body = [
        f'<line x1="{chart_x}" y1="{chart_y + chart_h}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h}" stroke="#94a3b8"/>',
        f'<line x1="{chart_x}" y1="{chart_y}" x2="{chart_x}" y2="{chart_y + chart_h}" stroke="#94a3b8"/>',
        f'<text x="{chart_x + chart_w / 2}" y="390" text-anchor="middle" fill="#5f6e84" font-family="Arial, sans-serif" font-size="12">{esc(x_label)}</text>',
        f'<text x="20" y="{chart_y + chart_h / 2}" transform="rotate(-90 20 {chart_y + chart_h / 2})" text-anchor="middle" fill="#5f6e84" font-family="Arial, sans-serif" font-size="12">{esc(y_label)}</text>',
        f'<text x="{chart_x}" y="{chart_y + chart_h + 22}" fill="#5f6e84" font-family="Arial, sans-serif" font-size="11">{esc(formatter(x_min))}</text>',
        f'<text x="{chart_x + chart_w}" y="{chart_y + chart_h + 22}" text-anchor="end" fill="#5f6e84" font-family="Arial, sans-serif" font-size="11">{esc(formatter(x_max))}</text>',
        f'<text x="{chart_x - 10}" y="{chart_y + 5}" text-anchor="end" fill="#5f6e84" font-family="Arial, sans-serif" font-size="11">{esc(formatter(y_max))}</text>',
        f'<text x="{chart_x - 10}" y="{chart_y + chart_h}" text-anchor="end" fill="#5f6e84" font-family="Arial, sans-serif" font-size="11">{esc(formatter(y_min))}</text>',
    ]
    for x_value, y_value in pairs:
        x = chart_x + (x_value - x_min) / x_span * chart_w
        y = chart_y + chart_h - (y_value - y_min) / y_span * chart_h
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#2165d6" opacity=".45"/>')
    return svg_shell(title, subtitle, "\n  ".join(body))


def histogram_chart(
    title: str,
    subtitle: str,
    values: list[float],
    value_label: str,
    bins: int = 8,
) -> str:
    """Create a compact histogram from numeric repository values."""
    values = [value for value in values if math.isfinite(value)]
    if not values:
        return svg_shell(title, subtitle, '<text x="56" y="160" fill="#5f6e84" font-family="Arial, sans-serif" font-size="14">No numeric observations available.</text>')
    low, high = min(values), max(values)
    width = (high - low) / bins or 1
    counts = [0] * bins
    for value in values:
        index = min(bins - 1, int((value - low) / width))
        counts[index] += 1
    labels = [f"{short_number(low + index * width)}–{short_number(low + (index + 1) * width)}" for index in range(bins)]
    return bar_chart(title, subtitle, labels, counts, value_label, lambda value: f"{value:,.0f}")


def visual(image: str, title: str, alt: str, caption: str) -> dict[str, str]:
    return {"image": image, "title": title, "alt": alt, "caption": caption}


def evidence_entry(kind: str, caption: str, visuals: list[dict[str, str]]) -> dict[str, object]:
    return {
        "kind": kind,
        "caption": caption,
        "images": visuals,
        # Keep the first image as a compatibility fallback for older pages.
        "image": visuals[0]["image"],
        "alt": visuals[0]["alt"],
    }


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
    fraud_workflow = write("fraud-workflow.svg", process_diagram(
        "Fraud decision workflow",
        "A transparent review loop connects model output to investigator action.",
        [("Transactions", "anonymized"), ("Features", "scale safely"), ("Classifier", "rank risk"), ("Review", "set threshold"), ("Feedback", "monitor drift")],
        "The visual is a method artifact because the source transaction rows are not redistributed.",
    ))
    evidence["fraud"] = evidence_entry(
        "Evaluation framework",
        "Generated from the project's documented evaluation design; no fraud rows are redistributed in this repository.",
        [
            visual(fraud_image, "Evaluation lenses", "Evaluation map showing precision, recall, F1, accuracy, and cross-validation for fraud detection.", "Five measures keep missed fraud, false alarms, balance, overall performance, and validation stability visible."),
            visual(fraud_workflow, "Decision workflow", "Workflow showing anonymized transactions flowing through features, a classifier, review, and feedback.", "A second visual makes the operational review loop explicit without inventing unavailable model scores."),
        ],
    )

    churn = read_csv(r"Tele Customer Churn Rate  Prediction Using Python/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    contract_totals: Counter[str] = Counter(row["Contract"] for row in churn)
    contract_churn: Counter[str] = Counter(row["Contract"] for row in churn if row["Churn"] == "Yes")
    contracts = ["Month-to-month", "One year", "Two year"]
    churn_rates = [100 * contract_churn[label] / contract_totals[label] for label in contracts]
    churn_image = write("churn-contract-rate.svg", bar_chart("Churn rate by contract", "Computed from 7,043 repository rows; percent of customers marked Churn = Yes.", ["Monthly", "One year", "Two year"], churn_rates, "CHURN RATE (%)", lambda value: f"{value:.1f}%"))
    tenure_buckets = [("0–12", 0, 12), ("13–24", 13, 24), ("25–48", 25, 48), ("49–60", 49, 60), ("61–72", 61, 72)]
    tenure_rates = []
    for _, lower, upper in tenure_buckets:
        rows = [row for row in churn if number(row.get("tenure")) is not None and lower <= number(row.get("tenure")) <= upper]
        tenure_rates.append(100 * sum(row["Churn"] == "Yes" for row in rows) / len(rows) if rows else 0)
    churn_tenure_image = write("churn-tenure-rate.svg", bar_chart("Churn rate by tenure", "Shorter tenure bands carry the clearest early-retention signal.", [label for label, _, _ in tenure_buckets], tenure_rates, "CHURN RATE (%)", lambda value: f"{value:.1f}%"))
    charge_means = []
    for label in ["No", "Yes"]:
        charge_means.append(mean([number(row["MonthlyCharges"]) for row in churn if row["Churn"] == label and number(row.get("MonthlyCharges")) is not None]))
    churn_charge_image = write("churn-monthly-charges.svg", bar_chart("Monthly charges by churn label", "Mean monthly charge in the repository data; a context signal, not a causal claim.", ["Stayed", "Churned"], charge_means, "MEAN MONTHLY CHARGE", lambda value: f"${value:.0f}"))
    evidence["churn"] = evidence_entry(
        "Computed from repository data",
        f"Computed from {len(churn):,} rows in the Telco Customer Churn CSV; the visual set connects contract, tenure, and charge patterns to the retention thesis.",
        [
            visual(churn_image, "Contract comparison", "Bar chart comparing churn rate for month-to-month, one-year, and two-year contracts.", "Contract length is the clearest segmentation view in the dataset."),
            visual(churn_tenure_image, "Tenure comparison", "Bar chart comparing churn rate across five tenure bands.", "The tenure view adds an early-life-cycle lens to the contract comparison."),
            visual(churn_charge_image, "Charge context", "Bar chart comparing mean monthly charges for customers who stayed versus churned.", "Charge levels provide context for outreach prioritization; they do not establish causation."),
        ],
    )

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
    housing_histogram = write("housing-r-price-distribution.svg", histogram_chart("Ames sale-price distribution", "Training split from the R project; distribution of SalePrice values.", [number(row.get("SalePrice")) for row in housing if number(row.get("SalePrice")) is not None], "NUMBER OF SALES"))
    housing_counts = [len(quality_values[key]) for key in quality_keys]
    housing_count_image = write("housing-r-quality-count.svg", bar_chart("Sales by quality level", "The distribution of quality levels matters when interpreting the mean-price pattern.", [f"Q{key}" for key in quality_keys], housing_counts, "NUMBER OF SALES", lambda value: f"{value:,.0f}"))
    evidence["housing-r"] = evidence_entry(
        "Computed from repository data",
        f"Computed from the {len(housing):,}-row R training file; the visual set shows price distribution, quality relationship, and sample coverage.",
        [
            visual(housing_image, "Quality and price", "Bar chart showing mean Ames sale price increasing across OverallQual levels four through nine.", "Overall quality has a strong monotonic relationship with mean sale price."),
            visual(housing_histogram, "Price distribution", "Histogram showing the distribution of Ames sale prices in the R training file.", "The distribution adds scale and skew context to the quality comparison."),
            visual(housing_count_image, "Sample coverage", "Bar chart showing the number of Ames sales in each quality level.", "The count view makes it easier to judge where the quality comparison is well supported."),
        ],
    )

    stocks_image = write("stocks-method-map.svg", process_diagram(
        "ETF forecasting method map",
        "The notebook compares two model families against historical Yahoo Finance OHLCV data.",
        [("OHLCV", "Yahoo Finance"), ("ARIMA", "classical"), ("LSTM", "recurrent"), ("MSE", "compare")],
        "External data required: the repository does not include a static price-history file.",
    ))
    stocks_boundary = write("stocks-evaluation-boundary.svg", process_diagram(
        "Forecast evaluation boundary",
        "The repaired notebook evaluates ARIMA and LSTM forecasts in the same raw-price units.",
        [("Chronological", "last 5 days"), ("ARIMA", "price forecast"), ("LSTM", "inverse diff"), ("MSE", "same units"), ("Caution", "not advice")],
        "External Yahoo Finance history is required before these model outputs can be regenerated.",
    ))
    evidence["stocks"] = evidence_entry(
        "Reproducible method map",
        "Generated from the notebook's documented pipeline; rerunning the notebook retrieves the external Yahoo Finance history.",
        [
            visual(stocks_image, "Model method map", "Method map showing OHLCV data flowing into ARIMA and LSTM before MSE comparison.", "The original model families and data source are visible at a glance."),
            visual(stocks_boundary, "Evaluation boundary", "Workflow showing chronological holdout, ARIMA, LSTM inverse differencing, same-unit MSE, and a caution label.", "The second visual documents the repaired evaluation contract rather than showing an unverified live-market score."),
        ],
    )

    king = read_csv(r"Real Estate Valuation Optimization in King County/kc_house_data.csv")
    grade_values: dict[str, list[float]] = defaultdict(list)
    for row in king:
        grade, price = row.get("grade"), number(row.get("price"))
        if grade and price is not None:
            grade_values[grade].append(price)
    grade_keys = sorted(grade_values, key=lambda item: int(item))
    grade_keys = [key for key in grade_keys if len(grade_values[key]) >= 100]
    king_image = write("king-county-grade.svg", bar_chart("Price by property grade", "Computed from 21,613 King County sales; median price for grades with at least 100 sales.", [f"G{key}" for key in grade_keys], [median(grade_values[key]) for key in grade_keys], "MEDIAN PRICE", lambda value: f"${value / 1000:.0f}K"))
    king_bedrooms: dict[str, list[float]] = defaultdict(list)
    king_xs, king_ys = [], []
    for row in king:
        price = number(row.get("price"))
        bedrooms = number(row.get("bedrooms"))
        living = number(row.get("sqft_living"))
        if price is not None and bedrooms is not None:
            king_bedrooms[str(int(bedrooms))].append(price)
        if price is not None and living is not None:
            king_xs.append(living)
            king_ys.append(price)
    bedroom_keys = sorted([key for key, values in king_bedrooms.items() if len(values) >= 100], key=int)
    king_bedroom_image = write("king-county-bedrooms.svg", bar_chart("Price by bedroom count", "Median price for bedroom groups with at least 100 King County sales.", [f"{key} BR" for key in bedroom_keys], [median(king_bedrooms[key]) for key in bedroom_keys], "MEDIAN PRICE", lambda value: f"${value / 1000:.0f}K"))
    king_scatter_image = write("king-county-living-area.svg", scatter_chart("Living area and sale price", "A sampled view of the repository's sqft_living and price relationship.", king_xs, king_ys, "LIVING AREA (SQ FT)", "SALE PRICE", lambda value: short_number(value)))
    evidence["king-county"] = evidence_entry(
        "Computed from repository data",
        f"Computed from {len(king):,} King County rows; the visual set connects grade, bedroom count, and living area to the valuation thesis.",
        [
            visual(king_image, "Grade comparison", "Bar chart comparing median King County sale price across property grade levels.", "Grade is the clearest categorical valuation comparison in the dataset."),
            visual(king_bedroom_image, "Bedroom comparison", "Bar chart comparing median King County sale price across bedroom counts.", "Bedroom count adds a familiar property-level segmentation view."),
            visual(king_scatter_image, "Size relationship", "Scatter plot showing sampled living area and King County sale price observations.", "The scatter view shows spread and outliers that a single average can hide."),
        ],
    )

    ames = read_csv(r"Data exploration and analysis using Python for residential properties in Ames, Iowa/cleaned_data.csv")
    ames_quality: dict[str, list[float]] = defaultdict(list)
    for row in ames:
        quality, price = row.get("OverallQual"), number(row.get("SalePrice"))
        if quality and price is not None:
            ames_quality[quality].append(price)
    ames_keys = sorted(ames_quality, key=lambda item: int(item))
    ames_keys = [key for key in ames_keys if 4 <= int(key) <= 9]
    ames_image = write("ames-quality.svg", bar_chart("SalePrice by overall quality", "Computed from the cleaned Ames file; mean SalePrice by OverallQual.", [f"Q{key}" for key in ames_keys], [mean(ames_quality[key]) for key in ames_keys], "MEAN SALE PRICE", lambda value: f"${value / 1000:.0f}K"))
    ames_xs, ames_ys = [], []
    price_by_decade: dict[str, list[float]] = defaultdict(list)
    for row in ames:
        price = number(row.get("SalePrice"))
        area = number(row.get("GrLivArea"))
        year = number(row.get("YearBuilt"))
        if price is not None and area is not None:
            ames_xs.append(area)
            ames_ys.append(price)
        if price is not None and year is not None:
            decade = f"{int(year // 10) * 10}s"
            price_by_decade[decade].append(price)
    ames_area_image = write("ames-area-price.svg", scatter_chart("Living area and SalePrice", "Sampled view of cleaned Ames observations; living area versus sale price.", ames_xs, ames_ys, "LIVING AREA (SQ FT)", "SALE PRICE", lambda value: short_number(value)))
    decade_keys = sorted(price_by_decade, key=lambda item: int(item.rstrip("s")))
    ames_decade_image = write("ames-decade-price.svg", bar_chart("SalePrice by build decade", "Mean SalePrice grouped by the home's build decade.", decade_keys, [mean(price_by_decade[key]) for key in decade_keys], "MEAN SALE PRICE", lambda value: f"${value / 1000:.0f}K"))
    evidence["ames"] = evidence_entry(
        "Computed from repository data",
        f"Computed from {len(ames):,} cleaned Ames rows; the visual set covers quality, area, and time context for exploratory analysis.",
        [
            visual(ames_image, "Quality comparison", "Bar chart showing mean Ames SalePrice increasing across overall quality levels.", "Overall quality provides the strongest direct comparison in the cleaned file."),
            visual(ames_area_image, "Area relationship", "Scatter plot showing sampled Ames living area and SalePrice observations.", "The scatter view shows the relationship's spread and outliers."),
            visual(ames_decade_image, "Age context", "Bar chart showing mean Ames SalePrice by build decade.", "Build decade adds age and historical context to the exploratory thesis."),
        ],
    )

    nlp = read_csv(r"Enhancing Job Matching and Market Analysis through NLP/job_description.csv")
    category_counts = Counter(row.get("Category", "Unspecified") or "Unspecified" for row in nlp)
    top_categories = category_counts.most_common(8)
    nlp_image = write("nlp-category.svg", horizontal_chart("Job records by category", "Computed from 325 repository records; top categories by row count.", [label for label, _ in top_categories], [value for _, value in top_categories], "RECORD COUNT"))
    text_lengths: dict[str, list[float]] = defaultdict(list)
    for row in nlp:
        category = row.get("Category", "Unspecified") or "Unspecified"
        text = f"{row.get('Description', '') or ''} {row.get('Requirement', '') or ''}".strip()
        text_lengths[category].append(float(len(text.split())))
    length_categories = [label for label, _ in top_categories]
    nlp_length_image = write("nlp-text-length.svg", horizontal_chart("Average text length by category", "Mean combined description and requirement word count for the most common categories.", length_categories, [mean(text_lengths[label]) for label in length_categories], "MEAN WORD COUNT"))
    evidence["nlp"] = evidence_entry(
        "Computed from repository data",
        f"Computed from {len(nlp):,} job-description rows; the visual set makes the category mix and text-shape differences visible before model evaluation.",
        [
            visual(nlp_image, "Category coverage", "Horizontal bar chart showing the most frequent job categories in the NLP dataset.", "Category imbalance explains why macro-level evaluation matters."),
            visual(nlp_length_image, "Text shape", "Horizontal bar chart comparing average combined text length across the most common job categories.", "Text length is a descriptive signal, not a claim that longer postings are better matches."),
        ],
    )

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
    country_revenue: dict[str, float] = defaultdict(float)
    invoice_status = Counter()
    for row in ecommerce:
        invoice = row.get("InvoiceNo", "")
        quantity = number(row.get("Quantity")) or 0
        unit_price = number(row.get("UnitPrice")) or 0
        country_revenue[row.get("Country", "Unknown") or "Unknown"] += quantity * unit_price
        invoice_status["Cancelled" if invoice.startswith("C") else "Completed"] += 1
    countries = [label for label, _ in sorted(country_revenue.items(), key=lambda item: item[1], reverse=True)[:8]]
    ecommerce_country_image = write("ecommerce-country-revenue.svg", horizontal_chart("Revenue by country", "Approximate line revenue from Quantity × UnitPrice for the eight largest countries.", countries, [country_revenue[label] for label in countries], "LINE REVENUE"))
    ecommerce_status_image = write("ecommerce-order-status.svg", bar_chart("Invoice status mix", "Cancelled invoices are identified by the source InvoiceNo prefix C.", ["Completed", "Cancelled"], [invoice_status["Completed"], invoice_status["Cancelled"]], "ROW COUNT", lambda value: f"{value:,.0f}"))
    evidence["ecommerce"] = evidence_entry(
        "Computed from repository data",
        f"Computed from {len(ecommerce):,} e-commerce rows; the visual set covers volume, geographic value, and cancellation handling.",
        [
            visual(ecommerce_image, "Monthly volume", "Bar chart showing distinct monthly invoice counts across the e-commerce dataset.", "Monthly volume gives the ingestion and replay story a time dimension."),
            visual(ecommerce_country_image, "Country revenue", "Horizontal bar chart showing approximate line revenue for the eight largest countries.", "Country aggregation shows how the same raw rows can support an analytical view."),
            visual(ecommerce_status_image, "Invoice status", "Bar chart comparing completed and cancelled invoice rows.", "Cancellation handling is a concrete data-quality and pipeline concern."),
        ],
    )

    DATA_JS.write_text("window.evidenceData = " + json.dumps(evidence, indent=2) + ";\n", encoding="utf-8")
    print(f"Generated {len(evidence)} evidence visuals in {OUT}")
    for key, item in evidence.items():
        print(f"{key}: {item['kind']} -> {len(item['images'])} visuals")


if __name__ == "__main__":
    main()
