# Stock Price Prediction with Python

An experiment comparing classical time-series forecasting with recurrent neural networks on historical ETF prices.

### Author: Dat Dao

## Portfolio snapshot

| Item | Detail |
| --- | --- |
| Instruments | VOO, VTI, VGT, VFH, VHT, VIS, VAW, and VNQ |
| Data | Historical daily OHLCV data collected through Yahoo Finance |
| Models | ARIMA and LSTM |
| Metric | Mean Squared Error (MSE) with visual forecast comparison |

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
The original analysis reports lower MSE for LSTM than ARIMA across the selected ETFs. The notebook also notes that differencing and scaling put some predictions on a different scale, so the metric comparison requires careful interpretation.

## Conclusion
The study illustrates the effectiveness of combining statistical and machine learning models for stock price prediction. Despite the promising results, the inherent unpredictability of the stock market necessitates cautious interpretation and application of the model outputs.

## Setup
Ensure you have Python installed and then install the required libraries:
```bash
pip install numpy pandas matplotlib seaborn yfinance statsmodels keras scikit-learn
```

Open the notebook after installation:

```powershell
jupyter notebook "Stock Price Prediction with Python.ipynb"
```

## Files

- [Analysis notebook](Stock%20Price%20Prediction%20with%20Python.ipynb)
- [Written report](Stock%20Price%20Prediction%20with%20Python.docx)
- [Portfolio image](../images/stock-prices.jpg)

## Limitations

Historical price patterns do not guarantee future performance. This is a research and learning artifact, not financial advice or a trading system. A stronger evaluation would use walk-forward validation, realistic transaction costs, leakage checks, and out-of-sample monitoring.

[← Back to the portfolio](../README.md)
