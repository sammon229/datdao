window.evidenceData = {
  "fraud": {
    "image": "../images/evidence/fraud-evaluation.svg",
    "alt": "Evaluation map showing precision, recall, F1, accuracy, and cross-validation for fraud detection.",
    "kind": "Evaluation framework",
    "caption": "Generated from the project's documented evaluation design; no fraud rows are redistributed in this repository."
  },
  "churn": {
    "image": "../images/evidence/churn-contract-rate.svg",
    "alt": "Bar chart comparing churn rate for month-to-month, one-year, and two-year contracts.",
    "kind": "Computed from repository data",
    "caption": "Computed from 7,043 rows in the Telco Customer Churn CSV; the chart supports the thesis that contract structure is a meaningful retention signal."
  },
  "housing-r": {
    "image": "../images/evidence/housing-r-quality.svg",
    "alt": "Bar chart showing mean Ames sale price increasing across OverallQual levels four through nine.",
    "kind": "Computed from repository data",
    "caption": "Computed from the 1,460-row R training file; the pattern supports the thesis that overall quality is a strong sale-price signal."
  },
  "stocks": {
    "image": "../images/evidence/stocks-method-map.svg",
    "alt": "Method map showing OHLCV data flowing into ARIMA and LSTM before MSE comparison.",
    "kind": "Reproducible method map",
    "caption": "Generated from the notebook's documented pipeline; rerunning the notebook retrieves the external Yahoo Finance history."
  },
  "king-county": {
    "image": "../images/evidence/king-county-grade.svg",
    "alt": "Bar chart comparing median King County sale price across property grade levels.",
    "kind": "Computed from repository data",
    "caption": "Computed from 21,613 King County rows; the monotonic grade pattern supports the thesis that property quality is an important valuation feature."
  },
  "ames": {
    "image": "../images/evidence/ames-quality.svg",
    "alt": "Bar chart showing mean Ames SalePrice increasing across overall quality levels.",
    "kind": "Computed from repository data",
    "caption": "Computed from 2,920 cleaned Ames rows; the visual backs the thesis that quality and price move together."
  },
  "nlp": {
    "image": "../images/evidence/nlp-category.svg",
    "alt": "Horizontal bar chart showing the most frequent job categories in the NLP dataset.",
    "kind": "Computed from repository data",
    "caption": "Computed from 325 job-description rows; the category distribution shows why category-level evaluation matters for matching."
  },
  "ecommerce": {
    "image": "../images/evidence/ecommerce-monthly.svg",
    "alt": "Bar chart showing distinct monthly invoice counts across the e-commerce dataset.",
    "kind": "Computed from repository data",
    "caption": "Computed from 541,909 e-commerce rows; the monthly shape supports the thesis for staged ingestion and replayable analysis."
  }
};
