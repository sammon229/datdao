# Telecom Customer Churn Prediction

### Author: Dat Dao

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
The findings indicate that factors like tenure, contract type, and monthly charges are pivotal in predicting churn. The Logistic Regression model, in particular, demonstrated high accuracy, making it a valuable tool for telecom companies in their efforts to reduce churn and enhance customer loyalty.

For a comprehensive analysis and detailed findings, refer to the accompanying documentation and analysis scripts.

### Requirements:
- Python 3.8+
- Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn

### Setup:
```bash
# Clone this repository
git clone https://github.com/sammon229/datdao/
# Navigate to the project directory
cd Tele Customer Churn Rate  Prediction Using Python
# Install required Python packages
pip install -r requirements.txt

# Running the analysis script
python Customer Churn Rate Prediction using Python.ipynb
