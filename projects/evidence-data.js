window.evidenceData = {
  "fraud": {
    "kind": "Evaluation framework",
    "caption": "Generated from the project's documented evaluation design; no fraud rows are redistributed in this repository.",
    "images": [
      {
        "image": "../images/evidence/fraud-evaluation.svg",
        "title": "Evaluation lenses",
        "alt": "Evaluation map showing precision, recall, F1, accuracy, and cross-validation for fraud detection.",
        "caption": "Five measures keep missed fraud, false alarms, balance, overall performance, and validation stability visible."
      },
      {
        "image": "../images/evidence/fraud-workflow.svg",
        "title": "Decision workflow",
        "alt": "Workflow showing anonymized transactions flowing through features, a classifier, review, and feedback.",
        "caption": "A second visual makes the operational review loop explicit without inventing unavailable model scores."
      }
    ],
    "image": "../images/evidence/fraud-evaluation.svg",
    "alt": "Evaluation map showing precision, recall, F1, accuracy, and cross-validation for fraud detection."
  },
  "churn": {
    "kind": "Computed from repository data",
    "caption": "Computed from 7,043 rows in the Telco Customer Churn CSV; the visual set connects contract, tenure, and charge patterns to the retention thesis.",
    "images": [
      {
        "image": "../images/evidence/churn-contract-rate.svg",
        "title": "Contract comparison",
        "alt": "Bar chart comparing churn rate for month-to-month, one-year, and two-year contracts.",
        "caption": "Contract length is the clearest segmentation view in the dataset."
      },
      {
        "image": "../images/evidence/churn-tenure-rate.svg",
        "title": "Tenure comparison",
        "alt": "Bar chart comparing churn rate across five tenure bands.",
        "caption": "The tenure view adds an early-life-cycle lens to the contract comparison."
      },
      {
        "image": "../images/evidence/churn-monthly-charges.svg",
        "title": "Charge context",
        "alt": "Bar chart comparing mean monthly charges for customers who stayed versus churned.",
        "caption": "Charge levels provide context for outreach prioritization; they do not establish causation."
      }
    ],
    "image": "../images/evidence/churn-contract-rate.svg",
    "alt": "Bar chart comparing churn rate for month-to-month, one-year, and two-year contracts."
  },
  "housing-r": {
    "kind": "Computed from repository data",
    "caption": "Computed from the 1,460-row R training file; the visual set shows price distribution, quality relationship, and sample coverage.",
    "images": [
      {
        "image": "../images/evidence/housing-r-quality.svg",
        "title": "Quality and price",
        "alt": "Bar chart showing mean Ames sale price increasing across OverallQual levels four through nine.",
        "caption": "Overall quality has a strong monotonic relationship with mean sale price."
      },
      {
        "image": "../images/evidence/housing-r-price-distribution.svg",
        "title": "Price distribution",
        "alt": "Histogram showing the distribution of Ames sale prices in the R training file.",
        "caption": "The distribution adds scale and skew context to the quality comparison."
      },
      {
        "image": "../images/evidence/housing-r-quality-count.svg",
        "title": "Sample coverage",
        "alt": "Bar chart showing the number of Ames sales in each quality level.",
        "caption": "The count view makes it easier to judge where the quality comparison is well supported."
      }
    ],
    "image": "../images/evidence/housing-r-quality.svg",
    "alt": "Bar chart showing mean Ames sale price increasing across OverallQual levels four through nine."
  },
  "stocks": {
    "kind": "Reproducible method map",
    "caption": "Generated from the notebook's documented pipeline; rerunning the notebook retrieves the external Yahoo Finance history.",
    "images": [
      {
        "image": "../images/evidence/stocks-method-map.svg",
        "title": "Model method map",
        "alt": "Method map showing OHLCV data flowing into ARIMA and LSTM before MSE comparison.",
        "caption": "The original model families and data source are visible at a glance."
      },
      {
        "image": "../images/evidence/stocks-evaluation-boundary.svg",
        "title": "Evaluation boundary",
        "alt": "Workflow showing chronological holdout, ARIMA, LSTM inverse differencing, same-unit MSE, and a caution label.",
        "caption": "The second visual documents the repaired evaluation contract rather than showing an unverified live-market score."
      }
    ],
    "image": "../images/evidence/stocks-method-map.svg",
    "alt": "Method map showing OHLCV data flowing into ARIMA and LSTM before MSE comparison."
  },
  "king-county": {
    "kind": "Computed from repository data",
    "caption": "Computed from 21,613 King County rows; the visual set connects grade, bedroom count, and living area to the valuation thesis.",
    "images": [
      {
        "image": "../images/evidence/king-county-grade.svg",
        "title": "Grade comparison",
        "alt": "Bar chart comparing median King County sale price across property grade levels.",
        "caption": "Grade is the clearest categorical valuation comparison in the dataset."
      },
      {
        "image": "../images/evidence/king-county-bedrooms.svg",
        "title": "Bedroom comparison",
        "alt": "Bar chart comparing median King County sale price across bedroom counts.",
        "caption": "Bedroom count adds a familiar property-level segmentation view."
      },
      {
        "image": "../images/evidence/king-county-living-area.svg",
        "title": "Size relationship",
        "alt": "Scatter plot showing sampled living area and King County sale price observations.",
        "caption": "The scatter view shows spread and outliers that a single average can hide."
      }
    ],
    "image": "../images/evidence/king-county-grade.svg",
    "alt": "Bar chart comparing median King County sale price across property grade levels."
  },
  "ames": {
    "kind": "Computed from repository data",
    "caption": "Computed from 2,920 cleaned Ames rows; the visual set covers quality, area, and time context for exploratory analysis.",
    "images": [
      {
        "image": "../images/evidence/ames-quality.svg",
        "title": "Quality comparison",
        "alt": "Bar chart showing mean Ames SalePrice increasing across overall quality levels.",
        "caption": "Overall quality provides the strongest direct comparison in the cleaned file."
      },
      {
        "image": "../images/evidence/ames-area-price.svg",
        "title": "Area relationship",
        "alt": "Scatter plot showing sampled Ames living area and SalePrice observations.",
        "caption": "The scatter view shows the relationship's spread and outliers."
      },
      {
        "image": "../images/evidence/ames-decade-price.svg",
        "title": "Age context",
        "alt": "Bar chart showing mean Ames SalePrice by build decade.",
        "caption": "Build decade adds age and historical context to the exploratory thesis."
      }
    ],
    "image": "../images/evidence/ames-quality.svg",
    "alt": "Bar chart showing mean Ames SalePrice increasing across overall quality levels."
  },
  "nlp": {
    "kind": "Computed from repository data",
    "caption": "Computed from 325 job-description rows; the visual set makes the category mix and text-shape differences visible before model evaluation.",
    "images": [
      {
        "image": "../images/evidence/nlp-category.svg",
        "title": "Category coverage",
        "alt": "Horizontal bar chart showing the most frequent job categories in the NLP dataset.",
        "caption": "Category imbalance explains why macro-level evaluation matters."
      },
      {
        "image": "../images/evidence/nlp-text-length.svg",
        "title": "Text shape",
        "alt": "Horizontal bar chart comparing average combined text length across the most common job categories.",
        "caption": "Text length is a descriptive signal, not a claim that longer postings are better matches."
      }
    ],
    "image": "../images/evidence/nlp-category.svg",
    "alt": "Horizontal bar chart showing the most frequent job categories in the NLP dataset."
  },
  "ecommerce": {
    "kind": "Computed from repository data",
    "caption": "Computed from 541,909 e-commerce rows; the visual set covers volume, geographic value, and cancellation handling.",
    "images": [
      {
        "image": "../images/evidence/ecommerce-monthly.svg",
        "title": "Monthly volume",
        "alt": "Bar chart showing distinct monthly invoice counts across the e-commerce dataset.",
        "caption": "Monthly volume gives the ingestion and replay story a time dimension."
      },
      {
        "image": "../images/evidence/ecommerce-country-revenue.svg",
        "title": "Country revenue",
        "alt": "Horizontal bar chart showing approximate line revenue for the eight largest countries.",
        "caption": "Country aggregation shows how the same raw rows can support an analytical view."
      },
      {
        "image": "../images/evidence/ecommerce-order-status.svg",
        "title": "Invoice status",
        "alt": "Bar chart comparing completed and cancelled invoice rows.",
        "caption": "Cancellation handling is a concrete data-quality and pipeline concern."
      }
    ],
    "image": "../images/evidence/ecommerce-monthly.svg",
    "alt": "Bar chart showing distinct monthly invoice counts across the e-commerce dataset."
  }
};
