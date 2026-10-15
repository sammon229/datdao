# Telecom Customer Churn Prediction

### Author: Dat Dao

A classification study for identifying customer-retention signals in telecom account and service data.

## Portfolio snapshot

| Item | Detail |
| --- | --- |
| Data | 7,043 customers and 21 account, service, and demographic features |
| Models | Logistic Regression, Random Forest, and Linear Discriminant Analysis |
| Focus | Preprocessing, feature selection, model comparison, and retention interpretation |
| Reported result | The original analysis identifies tenure, contract type, and monthly charges as important signals |

## Introduction
This project investigates the factors leading to customer churn in the telecom industry. By analyzing customer data, including demographics, service subscriptions, and account details, we aim to develop a model that accurately predicts churn, thereby enabling telecom companies to devise effective retention strategies.

## Research Questions
The study addresses key questions regarding customer retention in telecom:
- What factors contribute most significantly to customer churn?
- How can predictive modeling inform retention strategies?
- What role do service features and customer demographics play in churn likelihood?

## Approach
The project employs a data-driven approach, utilizing machine learning models like Logistic Regression, Random Forest, and Linear Discriminant Analysis (LDA) to predict churn. It emphasizes the importance of data preprocessing, model optimization, and performance evaluation in developing a reliable predictive framework.

## Data
The analysis is based on the Telco Customer Churn dataset from Kaggle, covering 7,043 customers with 21 features, including customer account information, service usage, and churn status. The dataset was meticulously cleaned and preprocessed to ensure its suitability for model training and analysis.

## Methodology
- **Data Preprocessing**: Cleaning data, handling missing values, and converting variables to appropriate data types.
- **Feature Selection**: Removing low-correlation features to prevent overfitting and improve model performance.
- **Model Training**: Applying Logistic Regression, Random Forest, and LDA models to the preprocessed data.
- **Performance Evaluation**: Assessing model accuracy and identifying key predictors of churn.

## Implications
The project highlights the criticality of understanding customer behavior and the potential of predictive analytics in crafting targeted retention strategies. It also discusses the ethical considerations in using customer data for predictive purposes.

## Conclusion
The findings indicate that tenure, contract type, and monthly charges are pivotal churn signals. Logistic Regression performed strongly in the original analysis, but retention decisions should use calibrated risk and business cost—not accuracy alone.

For a comprehensive analysis and detailed findings, refer to the accompanying documentation and analysis scripts.

### Requirements:
- Python 3.8+
- Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn, jupyter

### Setup:
```bash
# Clone this repository
git clone https://github.com/sammon229/datdao.git
# Navigate to the project directory
cd "datdao/Tele Customer Churn Rate  Prediction Using Python"
# Install required Python packages
python -m pip install pandas numpy scikit-learn matplotlib seaborn jupyter

# Open the analysis notebook
jupyter notebook "Customer Churn Rate Prediction using Python.ipynb"
```

## Files

- [Analysis notebook](Customer%20Churn%20Rate%20Prediction%20using%20Python.ipynb)
- [Telco dataset](WA_Fn-UseC_-Telco-Customer-Churn.csv)
- [Written report](Enhancing%20Customer%20Retention%20in%20Telecom%20Through%20Predictive%20Analytics.docx)
- [Portfolio image](../images/churn.jpg)

## Limitations

Churn labels, sampling, and contract behavior can change over time. A production retention workflow would need temporal validation, drift monitoring, explainable offers, privacy controls, and fairness review before contacting customers.

[← Back to the portfolio](../README.md)
