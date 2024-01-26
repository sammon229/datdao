# Ames Iowa Residential Properties Analysis

### Author: Dat Dao
### Project: Final Project - Data Exploration and Analysis

## Introduction
This project explores a comprehensive dataset containing information about residential properties in Ames, Iowa. The dataset includes various home characteristics such as living area, number of bedrooms and bathrooms, garage size, overall quality and condition, as well as the year built, remodeled, and the final sale price.

## Dataset Overview
- **Columns**: 16 columns including:
  - ID column
  - 13 numerical columns
  - 2 categorical columns (Neighborhood, Condition1, BldgType, and HouseStyle)
- **Target Variable**: SalePrice, representing the property's final sale price in US dollars.
- **Key Features**: Living area (GrLivArea), overall quality and condition (OverallQual and OverallCond), number of bedrooms and bathrooms, garage size, year built and remodeled.

## Objectives
- To build a regression model predicting the sale price based on various characteristics.
- To explore the relationships between different features and the sale price, providing insights into factors affecting property values in the Ames, Iowa area.

## Key Observations
- The condition of the property significantly influences the sale price, with a noticeable trend of higher prices for better conditions.
- A positive correlation exists between the quality of a house and its sale price, with houses of higher quality generally selling at higher prices.
- The living area of the house shows a moderately strong positive linear relationship with the sale price, indicating larger houses tend to be sold at higher prices.

## Statistical Findings
- **Pearson Correlation Coefficient**: Indicates a moderately strong positive linear relationship between living area and sale price.
- **R-squared**: 45.2% variance in sale price is explained by the predictor variables.
- **Adj. R-squared**: Adjusted R-squared value considering the number of predictor variables.
- **F-statistic**: Validates the overall significance of the model.

## Conclusion
This analysis provides valuable insights into the real estate market of Ames, Iowa, helping understand the dynamics between property features and pricing. It emphasizes the importance of considering various home characteristics for accurate property valuation and market understanding.

For more detailed analysis or to use this dataset for further research, please refer to the complete study conducted by Dat Dao

### Requirements:
- Python (version 10)
- Python libraries: numpy, pandas, matplotlib.pyplot, statsmodels.api, seaborn
### Setup:
```bash
# Clone this repository
git clone https://github.com/sammon229/datdao.github.io/new/main
# Navigate to the project directory
cd datdao.github.io/Data exploration and analysis using Python for residential properties in Ames, Iowa/

# Running the script
Pythonscript Data Exploreation and Analysis Ames,Iowa.ipynb

