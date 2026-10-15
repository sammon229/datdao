# Real Estate Valuation Optimization in King County

An applied machine-learning study for estimating residential sale prices in King County, including Seattle.

## Portfolio snapshot

| Item | Detail |
| --- | --- |
| Data | King County sales from May 2014 through May 2015 |
| Features | Bedrooms, bathrooms, square footage, grade, location, and other property fields |
| Model | Random Forest regression with exploratory analysis and feature engineering |
| Use case | Decision support for valuation exploration, not an automated appraisal |

## Dataset
The dataset encompasses property sales in King County from May 2014 to May 2015, featuring details like bedrooms, bathrooms, square footage, and sale price among its 21 columns.

## Objectives
- Develop a robust machine learning model to predict house prices.
- Provide valuable insights to stakeholders for informed real estate decisions.

## Methodology
- **Data Exploration**: Understanding the relationships between house features and prices.
- **Feature Engineering**: Identifying significant predictors for the model.
- **Model Development**: Utilizing Random Forest Regression and evaluating its performance.

## Challenges and Insights
- Addressing outliers and the inherent variability in house prices.
- Importance of features like square footage and property grade on price predictions.

## Results
- The Random Forest model showed promising results but highlighted the need for further refinement.
- Model performance metrics indicated room for improvement in prediction accuracy.

## Future Directions
- Enhanced feature engineering and exploration of advanced modeling techniques.
- Incorporation of additional data sources for a more comprehensive analysis.

## Usage
Run the notebook from the project directory:

```powershell
git clone https://github.com/sammon229/datdao.git
Set-Location "datdao/Real Estate Valuation Optimization in King County"
python -m pip install pandas numpy scikit-learn matplotlib seaborn jupyter
jupyter notebook "Leveraging Machine Learning to Optimize Real Estate Valuation in King County.ipynb"
```

## Files

- [Analysis notebook](Leveraging%20Machine%20Learning%20to%20Optimize%20Real%20Estate%20Valuation%20in%20King%20County.ipynb)
- [King County data](kc_house_data.csv)
- [Written report](Data%20mining%20Leveraging%20Machine%20Learning%20to%20Optimize%20Real%20Estate%20Valuation%20in%20King%20County.docx)
- [Portfolio image](../images/housevalue.jpg)

## Disclaimer
This project is intended for educational purposes and should not be used as the sole basis for real estate investment decisions.

## Acknowledgements
- King County for providing the dataset.
- Contributors to the Python libraries utilized in this analysis.

[← Back to the portfolio](../README.md)
