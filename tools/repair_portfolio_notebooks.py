"""Apply explicit correctness fixes to the portfolio notebooks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def set_cell(path: Path, index: int, source: str) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cell = notebook["cells"][index]
    if cell.get("cell_type") != "code":
        raise ValueError(f"Expected code cell {index}: {path}")
    cell["source"] = source.strip("\n").splitlines(keepends=True)
    cell["execution_count"] = None
    cell["outputs"] = []
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def repair_fraud() -> None:
    path = ROOT / "Machine Learning Credit Card Fraud Detection/Credit Card Fraud.ipynb"
    set_cell(path, 8, """# Keep raw data intact; scale inside the model pipeline to avoid leakage.
df_model = df.drop(columns=['id']).copy()
X = df_model.drop(columns=['Class'])
y = df_model['Class']
""")
    set_cell(path, 9, """# Stratify so the rare fraud class is represented in both partitions.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y
)
""")
    set_cell(path, 10, """from sklearn.pipeline import Pipeline

lr_model = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(
        max_iter=1000, class_weight='balanced', random_state=1
    )),
])
lr_model.fit(X_train, y_train)
""")
    set_cell(path, 14, """# Select features using the training partition, not the held-out test rows.
training_frame = X_train.assign(Class=y_train)
correlation_matrix = training_frame.corr(numeric_only=True).abs()
sorted_correlation = correlation_matrix['Class'].sort_values(ascending=False)
top_15_features = sorted_correlation.drop('Class').head(15).index.tolist()
X = df_model[top_15_features]
y = df_model['Class']
""")
    set_cell(path, 15, """X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y
)
""")
    set_cell(path, 16, """rf = RandomForestClassifier(
    random_state=1, class_weight='balanced', n_jobs=-1
)
""")
    set_cell(path, 17, """# 'auto' was removed from recent scikit-learn versions.
param_grid = {
    'n_estimators': [100, 300],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [4, 10],
    'criterion': ['gini'],
}
""")
    set_cell(path, 18, """random_search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_grid,
    n_iter=10,
    cv=3,
    scoring='average_precision',
    verbose=2,
    random_state=1,
    n_jobs=-1,
)
""")
    set_cell(path, 21, """# Reproducible fallback using parameters supported by current sklearn.
rf_best = RandomForestClassifier(
    n_estimators=100,
    max_features='sqrt',
    max_depth=10,
    criterion='gini',
    class_weight='balanced',
    random_state=1,
    n_jobs=-1,
)
rf_best.fit(X_train, y_train)
rf_y_pred = rf_best.predict(X_test)
""")


def repair_churn() -> None:
    path = ROOT / "Tele Customer Churn Rate  Prediction Using Python/Customer Churn Rate Prediction using Python.ipynb"
    set_cell(path, 4, """data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
data = data.dropna(subset=['TotalCharges']).copy()
print(f"Rows after TotalCharges validation: {len(data):,}")
""")
    set_cell(path, 17, """# F1-macro gives the minority churn class meaningful weight during tuning.
param_grid = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [None, 10, 20],
}
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='f1_macro', n_jobs=-1)
grid_search.fit(X_train, y_train)
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best cross-validation F1-macro: {grid_search.best_score_:.3f}")
""")
    set_cell(path, 16, """from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Build feature lists after optional low-signal columns have been removed.
X = data_reduced.drop(columns=['Churn', 'customerID'], errors='ignore')
y = data_reduced['Churn']
numerical_features = X.select_dtypes(exclude=['object']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
])
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        random_state=1, class_weight='balanced', n_jobs=-1
    )),
])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y
)
""")
    set_cell(path, 18, """from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, classification_report,
    confusion_matrix, f1_score, precision_score, recall_score,
)

y_pred = grid_search.predict(X_test)
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(
    conf_matrix, annot=True, fmt='d', cmap='Blues',
    xticklabels=['Not Churned', 'Churned'],
    yticklabels=['Not Churned', 'Churned'],
)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()
print(classification_report(y_test, y_pred, zero_division=0))
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Balanced accuracy: {balanced_accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.3f}")
print(f"Recall: {recall_score(y_test, y_pred, zero_division=0):.3f}")
print(f"F1: {f1_score(y_test, y_pred, zero_division=0):.3f}")
""")
    set_cell(path, 19, """from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numeric_cols = X.select_dtypes(exclude=['object']).columns.tolist()
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_cols),
])
log_reg_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(
        max_iter=1000, class_weight='balanced', random_state=1
    )),
])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y
)
log_reg_pipeline.fit(X_train, y_train)
y_pred = log_reg_pipeline.predict(X_test)
print(classification_report(y_test, y_pred, zero_division=0))
""")
    set_cell(path, 21, """from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# LDA needs a dense matrix, so use a dense encoder for this comparison.
try:
    dense_encoder = OneHotEncoder(
        drop='first', handle_unknown='ignore', sparse_output=False
    )
except TypeError:  # scikit-learn < 1.2
    dense_encoder = OneHotEncoder(
        drop='first', handle_unknown='ignore', sparse=False
    )
lda_preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
    ('cat', dense_encoder, categorical_cols),
])
lda_pipeline = Pipeline([
    ('preprocessor', lda_preprocessor),
    ('classifier', LinearDiscriminantAnalysis()),
])
lda_pipeline.fit(X_train, y_train)
y_pred = lda_pipeline.predict(X_test)
print("Confusion Matrix:\\n", confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, zero_division=0))
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
""")


def repair_nlp() -> None:
    path = ROOT / "Enhancing Job Matching and Market Analysis through NLP/Job Description NLP.ipynb"
    set_cell(path, 2, """# Keep rows with a target category; text fields are normalized below.
df = df.dropna(subset=['Category']).copy()
""")
    set_cell(path, 4, """# Drop the source index column if it is present.
df = df.drop(columns=[df.columns[0]])
""")
    set_cell(path, 5, """# Combine text fields while treating missing descriptions as empty text.
df['text'] = (
    df['Description'].fillna('') + ' ' + df['Requirement'].fillna('')
).str.replace(r'\\s+', ' ', regex=True).str.strip()
df.head()
""")
    set_cell(path, 7, """# Text preprocessing uses scikit-learn's built-in English stop-word list.
# No network download is required to run this notebook.
""")
    set_cell(path, 8, """# Keep a cleaned text column for inspection; the model pipeline applies TF-IDF.
df['filtered_text'] = df['text'].astype(str).str.replace(
    r'[^A-Za-z0-9 ]+', ' ', regex=True
).str.replace(r'\\s+', ' ', regex=True).str.strip()
df.head()
""")
    set_cell(path, 9, """# Stratify so every category is represented proportionally in the test set.
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['Category'], test_size=0.2, random_state=1,
    stratify=df['Category']
)
""")
    set_cell(path, 13, """y_pred = model.predict(X_test_tfidf)
print(classification_report(y_test, y_pred, zero_division=0))
""")
    set_cell(path, 14, """pipeline = make_pipeline(
    TfidfVectorizer(stop_words='english', max_features=10000),
    MultinomialNB(),
)
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred, zero_division=0))
""")
    set_cell(path, 16, """from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
""")
    set_cell(path, 19, """grid_search = GridSearchCV(
    pipeline, parameter_grid, n_jobs=-1, verbose=1,
    scoring='f1_macro', cv=5,
)
grid_search.fit(X_train, y_train)
""")
    set_cell(path, 21, """tfidf_best_params = {
    'stop_words': 'english',
    'max_df': best_parameters['tfidf__max_df'],
    'ngram_range': best_parameters['tfidf__ngram_range'],
}
nb_best_params = {'alpha': best_parameters['clf__alpha']}

pipeline_best = Pipeline([
    ('tfidf', TfidfVectorizer(**tfidf_best_params)),
    ('clf', MultinomialNB(**nb_best_params)),
])
pipeline_best.fit(X_train, y_train)
y_pred = pipeline_best.predict(X_test)
print(classification_report(y_test, y_pred, zero_division=0))
""")


def repair_king_county() -> None:
    path = ROOT / "Real Estate Valuation Optimization in King County/Leveraging Machine Learning to Optimize Real Estate Valuation in King County.ipynb"
    set_cell(path, 4, """# Remove incomplete rows before descriptive analysis and modeling.
df = df.dropna(axis=0).copy()
df.head()
""")
    set_cell(path, 7, """# Keep dates as datetimes so downstream year/month features are lossless.
df['date'] = pd.to_datetime(df['date'])
df.dtypes
""")
    set_cell(path, 9, """# Create calendar features and remove the raw date column.
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df = df.drop(columns=['date'])
""")
    set_cell(path, 39, """pipe_rf = Pipeline([
    ('scaler', RobustScaler()),
    ('model', RandomForestRegressor(random_state=2, n_jobs=-1)),
])

param_grid_rf = {
    'model__n_estimators': [100, 200, 300],
    'model__max_depth': [None, 5, 10],
    'model__min_samples_split': [2, 5, 10],
}
grid_rf = GridSearchCV(
    pipe_rf, param_grid_rf, cv=5, n_jobs=-1,
    scoring='neg_root_mean_squared_error', refit=True,
)
grid_rf.fit(X_train, y_train)
print("Best parameters: ", grid_rf.best_params_)

y_pred_rf = grid_rf.predict(X_test)
mae = mean_absolute_error(y_test, y_pred_rf)
mse = mean_squared_error(y_test, y_pred_rf)
rmse = sqrt(mse)
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print('Variance Regression Score: ', explained_variance_score(y_test, y_pred_rf))
""")
    set_cell(path, 41, """# The grid-search model above is the canonical reproducible baseline.
# Bayesian search was removed because scikit-optimize is optional and was not
# part of this project's documented environment.
print('Optional Bayesian search omitted; use grid_rf.best_estimator_ for the validated model.')
""")


def repair_ames() -> None:
    path = ROOT / "Data exploration and analysis using Python for residential properties in Ames, Iowa/Data Exploreation and Analysis Ames,Iowa.ipynb"
    set_cell(path, 23, """# Empirical PMFs using pandas, avoiding an undocumented package dependency.
for condition, group in df.groupby('OverallCond'):
    probabilities = group['SalePrice'].value_counts(normalize=True).sort_index()
    plt.step(probabilities.index, probabilities.values, where='mid', label=str(condition))
plt.xlabel('SalePrice')
plt.ylabel('Probability')
plt.title('SalePrice PMF by Overall Condition')
plt.xlim(0, 400000)
plt.ylim(0, 0.05)
plt.legend(title='OverallCond')
plt.show()
""")
    set_cell(path, 53, """# A paired t-test is not appropriate for unrelated area and price variables.
# Use Spearman association to measure the monotonic relationship instead.
from scipy.stats import spearmanr

stat, p_value = spearmanr(df['GrLivArea'], df['SalePrice'])
print(f"Spearman correlation: {stat:.3f}")
print(f"p-value: {p_value:.3g}")
""")


def repair_stock() -> None:
    path = ROOT / "Stock Price Prediction with Python/Stock Price Prediction with Python.ipynb"
    set_cell(path, 1, """symbols = ['VOO', 'VTI', 'VGT', 'VFH', 'VHT', 'VIS', 'VAW', 'VNQ']
all_data = pd.DataFrame()
data_frames = []

# Use a true five-year window and an exclusive end date.
end_date = datetime.today().date()
start_date = end_date - timedelta(days=5 * 365)
today = end_date.strftime('%Y-%m-%d')
five_years_ago = start_date.strftime('%Y-%m-%d')
""")
    set_cell(path, 4, """from pathlib import Path

data_path = Path('stock_data.csv')
if not data_path.exists():
    raise FileNotFoundError(
        'Run the download cell first, or place stock_data.csv in this folder.'
    )
df = pd.read_csv(data_path)
df.head()

symbol_to_name = {
    'VOO': 'Vanguard S&P 500 ETF', 'VTI': 'Vanguard Total Stock Market ETF',
    'VGT': 'Vanguard Information Technology ETF',
    'VFH': 'Vanguard Financials ETF', 'VHT': 'Vanguard Health Care ETF',
    'VIS': 'Vanguard Industrials ETF', 'VAW': 'Vanguard Materials ETF',
    'VNQ': 'Vanguard Real Estate ETF',
}
df['Symbol_Name'] = df['Symbol'].map(symbol_to_name)
""")
    set_cell(path, 10, """# Forecasting must use chronological order within each instrument.
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(['Symbol', 'Date']).reset_index(drop=True)
data_by_symbol = {
    symbol: df.loc[df['Symbol'] == symbol].copy()
    for symbol in symbols
}
""")
    set_cell(path, 13, """def prepare_data_for_lstm(data, look_back=1, test_size=5):
    data_series = data['Close'].astype(float).reset_index(drop=True)
    diff = data_series.diff().dropna()
    scaler = MinMaxScaler(feature_range=(-1, 1))
    diff_scaled = scaler.fit_transform(diff.to_numpy().reshape(-1, 1))

    X, Y = [], []
    for i in range(len(diff_scaled) - look_back):
        X.append(diff_scaled[i:i + look_back, 0])
        Y.append(diff_scaled[i + look_back, 0])
    X, Y = np.asarray(X), np.asarray(Y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    X_train, X_test = X[:-test_size], X[-test_size:]
    y_train, y_test = Y[:-test_size], Y[-test_size:]

    # Make inverse differencing explicit for price-unit evaluation.
    last_train_close = data_series.iloc[-test_size - 1]
    test_close = data_series.iloc[-test_size:].to_numpy()
    return X_train, y_train, X_test, y_test, scaler, last_train_close, test_close
""")
    set_cell(path, 17, """results = {}
for symbol, data in data_by_symbol.items():
    print(f"Processing data for symbol: {symbol}")
    train_data, test_data = split_data(data)

    model_arima = ARIMA(train_data['Close'], order=(5, 1, 0))
    model_arima_fit = model_arima.fit()
    predictions_arima = model_arima_fit.forecast(steps=len(test_data))
    mse_arima = mean_squared_error(test_data['Close'], predictions_arima)

    (
        X_train, y_train, X_test, y_test, scaler,
        last_train_close, test_close,
    ) = prepare_data_for_lstm(data)
    model_lstm = build_and_train_lstm(X_train, y_train)
    predictions_lstm_scaled = model_lstm.predict(X_test, verbose=0)
    predicted_diff = scaler.inverse_transform(predictions_lstm_scaled).ravel()
    predictions_lstm = last_train_close + np.cumsum(predicted_diff)
    mse_lstm = mean_squared_error(test_close, predictions_lstm)

    results[symbol] = {
        'MSE_ARIMA': mse_arima,
        'Predictions_ARIMA': predictions_arima,
        'Real_Values': test_close,
        'MSE_LSTM': mse_lstm,
        'Predictions_LSTM': predictions_lstm,
        'LSTM_Real_Values': test_close,
        'SMA30': test_data['SMA30'],
        'SMA100': test_data['SMA100'],
    }
""")
    set_cell(path, 18, """for symbol, result in results.items():
    print(f"Processing data for symbol: {symbol}")
    result['Predictions_ARIMA'] = result['Predictions_ARIMA'].reset_index(drop=True)
    result['SMA30'] = result['SMA30'].reset_index(drop=True)
    result['SMA100'] = result['SMA100'].reset_index(drop=True)

    print(f"\\nResults for symbol: {symbol}")
    print(f"ARIMA Model MSE (price units): {result['MSE_ARIMA']:.4f}")
    print(f"LSTM Model MSE (price units): {result['MSE_LSTM']:.4f}")

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.plot(result['Real_Values'], label='Real Values', color='blue')
    plt.plot(result['Predictions_ARIMA'], label='ARIMA Predictions', color='red')
    plt.plot(result['SMA30'], label='SMA30', color='purple', alpha=0.6)
    plt.plot(result['SMA100'], label='SMA100', color='orange', alpha=0.6)
    plt.title(f"ARIMA Predictions vs Real Values for {symbol}")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(result['LSTM_Real_Values'], label='Real Values', color='blue')
    plt.plot(result['Predictions_LSTM'], label='LSTM Predictions', color='green')
    plt.title(f"LSTM Predictions vs Real Values for {symbol}")
    plt.legend()
    plt.tight_layout()
    plt.show()
""")


def main() -> None:
    repair_fraud()
    repair_churn()
    repair_nlp()
    repair_king_county()
    repair_ames()
    repair_stock()
    print("Repaired portfolio notebooks and cleared stale outputs.")


if __name__ == "__main__":
    main()
