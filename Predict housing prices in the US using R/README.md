# Real Estate Price Prediction using R

An R-based housing-price study using Ames, Iowa sales data to compare interpretable regression with tree-based modeling.

### Author: Dat Dao

## Portfolio snapshot

| Item | Detail |
| --- | --- |
| Data | 2,930 Ames residential sales from 2006–2010 |
| Target | SalePrice |
| Methods | OLS, multicollinearity review, maximum-likelihood ideas, and Random Forest |
| Reported result | The original study reports that the Random Forest approach explains approximately 85% of sale-price variation |
## Introduction
This study delves into the impact of various house characteristics on the final sale price. Using a detailed dataset from Ames, Iowa, the project aims to create a reliable model for predicting house prices, helping buyers, sellers, real estate agents, appraisers, and investors make informed decisions.

## Research Questions
The study explores critical aspects influencing home pricing, which is a complex task especially for potential buyers or real estate agents looking to estimate prices accurately. With the goal to provide a more accurate prediction, the study utilizes around 80 regressors to identify influential characteristics on home prices.

## Approach
The methodology involves evaluating the housing stock using ordinary least squares (OLS) and improving predictions with maximum likelihood (ML) techniques considering spatial correlations. The study also delves into macroeconomic and microeconomic factors affecting housing values and employs Random Forest for precise regression modeling.

## Data
Utilizing a dataset from the Ames Housing Authority, this study encompasses residential property sales in Ames, Iowa, from 2006 to 2010. It includes 2930 observations with a wide range of quantitative and categorical variables detailing various home features. The aim is to predict the home's SalePrice, with the dataset offering a rich set of explanatory variables.

## Methodology
- **Multiple Linear Regression:** A full model analysis with all variables, focusing on identifying and removing any irrelevant variables to improve the model's fit.
- **Multicollinearity Test:** Addressing issues where independent variables are highly correlated, affecting the model's output.
- **Random Forest:** Utilizing this technique for its robustness in handling classification and regression problems, mitigating overfitting risks, and identifying critical features.

## Implications
The study acknowledges potential drawbacks like selection bias due to regional data limitation and emphasizes the need for incorporating macroeconomic factors into the model. It proposes employing a hybrid model integrating both micro and macro elements for effectively forecasting housing values.

## Conclusion
The study proposes an alternative approach using the Random Forest model, which outperforms multiple linear regression or decision trees by identifying variable importance and avoiding overfitting. The model can explain about 85% of the house sale price variation, highlighting the importance of both micro and macro factors in housing price prediction. The study's outcomes are envisioned to assist real estate brokers in enhancing their service and marketing strategies.

The accompanying data files and `FinalCode.R` preserve the original analysis materials for review.


### Requirements:
- R (version 4.2.3 or newer)
- R libraries: dplyr, forecast, randomForest, caret, psych, caTools, tidyr, xlsx, ggplot2, mice, lmtest, car

### Setup:
```bash
# Clone this repository
git clone https://github.com/sammon229/datdao.git
# Navigate to the project directory
cd "datdao/Predict housing prices in the US using R"
# Install R packages
Rscript -e "install.packages(c('dplyr','forecast','randomForest','caret','psych','caTools','tidyr','xlsx','ggplot2','mice','lmtest','car'), repos='https://cloud.r-project.org')"

# Running the script
Rscript FinalCode.R
```

## Limitations

The observations are regional and historical. The model is an educational portfolio artifact, not a current valuation service; any real deployment would need temporal validation, market refreshes, leakage review, uncertainty estimates, and fairness checks.

[← Back to the portfolio](../README.md)


