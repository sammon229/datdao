# Ames Iowa Residential Property Analysis

Exploratory analysis of residential properties in Ames, Iowa, with a focus on the features associated with sale price.

## Portfolio snapshot

| Item | Detail |
| --- | --- |
| Question | Which property characteristics are most associated with SalePrice? |
| Data | Ames residential sales with property, quality, location, and sale fields |
| Tools | Python, pandas, NumPy, seaborn, matplotlib, statsmodels |
| Approach | Cleaning, exploratory analysis, correlation review, and regression diagnostics |
| Reported result | The original analysis reports an R-squared of approximately 45.2% for its regression specification |

## What to look for

- Overall quality and living area show the clearest positive relationship with sale price.
- Neighborhood, condition, garage capacity, and age provide useful context beyond square footage.
- The notebook demonstrates how visual exploration and statistical diagnostics shape a modeling decision.

## Files

- [Analysis notebook](Data%20Exploreation%20and%20Analysis%20Ames%2CIowa.ipynb)
- [Cleaned dataset](cleaned_data.csv)
- [Project presentation](Data%20Exploration%20and%20Analysis%20Project.pptx)
- [Written report](Ames%20Iowa%20Residential%20Properties%20Analysis.docx)

## Reproduce locally

```powershell
git clone https://github.com/sammon229/datdao.git
Set-Location "datdao/Data exploration and analysis using Python for residential properties in Ames, Iowa"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install numpy pandas matplotlib seaborn statsmodels jupyter
jupyter notebook "Data Exploreation and Analysis Ames,Iowa.ipynb"
```

## Limitations

This is an Ames-specific educational analysis, not a production valuation service. The reported fit depends on the original feature selection, preprocessing, and train/test design; it should not be treated as a current market estimate.

[← Back to the portfolio](../README.md)

