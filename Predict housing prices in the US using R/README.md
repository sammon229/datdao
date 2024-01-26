# Real Estate Price Prediction using R

### Author: Dat Dao
### Date: February 12, 2023

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

For more information or to delve into the study's detailed analysis, please refer to the full research documentation&#8203;``【oaicite:0】``&#8203;.


### Requirements:
- R (version 4.2.3)
- R libraries: dplyr,forecast,randomForest,caret,psych,caTools,tidyr,xlsx,ggplot2,mice,lmtest,car

### Setup:
```bash
# Clone this repository
git clone https://github.com/sammon229/datdao.github.io/tree/main
# Navigate to the project directory
cd datdao.github.io/Predict housing prices in the US using R/
# Install R packages
Rscript -e "install.packages(c('[dplyr,forecast,randomForest,caret,psych,caTools,tidyr,xlsx,ggplot2,mice,lmtest,car]'))"

# Running the script
Rscript FinalCode.R


