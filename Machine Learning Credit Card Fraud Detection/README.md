# Credit Card Fraud Detection

An imbalanced-classification study for identifying suspicious credit-card transactions while keeping recall, precision, and false-positive cost visible.

## Portfolio snapshot

| Item | Detail |
| --- | --- |
| Problem | Separate fraudulent and legitimate transactions from anonymized transaction data |
| Features | Anonymized transaction variables plus amount and time fields |
| Evaluation | Precision, recall, F1-score, accuracy, and cross-validation |
| Priority | Investigate fraud without treating accuracy as the only success measure |

## Analysis focus

- Inspect class imbalance before modeling.
- Compare false-positive and false-negative trade-offs.
- Review feature relevance rather than presenting the model as an opaque decision-maker.
- Use cross-validation to reduce the risk of a single favorable split driving the conclusion.

## Files

- [Analysis notebook](Credit%20Card%20Fraud.ipynb)
- [Written report](Advanced%20Credit%20Card%20Fraud%20Detection%20System.docx)
- [Portfolio image](../images/MIT-Fraud-Detection-PRESS_0.jpg)

The source transaction dataset is not redistributed in this repository. Download it from the original source and place it beside the notebook as `creditcard_2023.csv`; the notebook now raises a clear instruction instead of relying on a Kaggle-only path.

## Reproduce locally

```powershell
git clone https://github.com/sammon229/datdao.git
Set-Location "datdao/Machine Learning Credit Card Fraud Detection"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pandas numpy scikit-learn matplotlib seaborn jupyter
jupyter notebook "Credit Card Fraud.ipynb"
```

## Limitations

The dataset is anonymized and historical, so the findings should not be treated as a production fraud rule. A deployable system would require threshold governance, drift monitoring, investigator feedback, privacy controls, and cost-sensitive validation on current transactions.

[← Back to the portfolio](../README.md)
