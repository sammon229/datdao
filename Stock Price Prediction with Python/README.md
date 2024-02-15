# Stock Price Prediction with Python

### Author: Dat Dao

## Introduction
This project explores the application of ARIMA and LSTM models to predict stock prices using historical data from Yahoo Finance. The goal is to leverage a hybrid approach that combines traditional statistical models with advanced machine learning techniques to provide accurate stock price forecasts.

## Data
The dataset includes historical stock price data for selected ETFs (`VOO`, `VTI`, `VGT`, `VFH`, `VHT`, `VIS`, `VAW`, `VNQ`) from Yahoo Finance, featuring daily open, high, low, close prices, and trading volumes.

## Methodology
- Data Preprocessing: Data cleaning and normalization to prepare for modeling.
- Exploratory Data Analysis (EDA): Trend, volume, and correlation analysis to understand data patterns.
- Modeling: Implementation of ARIMA for linear trends and LSTM for capturing non-linear patterns.
- Evaluation: Model performance assessed using Mean Squared Error (MSE).

## Results
The LSTM model consistently outperformed the ARIMA model across all ETFs, demonstrating lower MSE values, indicating more accurate predictions. However, it's noted that LSTM's predictions were on a different scale due to the differencing technique used in data preprocessing.

## Conclusion
The study illustrates the effectiveness of combining statistical and machine learning models for stock price prediction. Despite the promising results, the inherent unpredictability of the stock market necessitates cautious interpretation and application of the model outputs.

## Setup
Ensure you have Python installed and then install the required libraries:
```bash
pip install numpy pandas matplotlib seaborn yfinance statsmodels keras scikit-learn
