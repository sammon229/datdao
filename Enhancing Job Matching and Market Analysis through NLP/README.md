# Enhancing Job Matching and Market Analysis through NLP

An NLP project that turns unstructured job descriptions into analyzable categories and matching signals.

## Portfolio snapshot

| Item | Detail |
| --- | --- |
| Business question | How can text features improve job-posting classification and market analysis? |
| Data | Job descriptions with requirements, benefits, and category fields from a Kaggle source |
| Representation | TF-IDF text vectors |
| Baseline model | Multinomial Naive Bayes with hyperparameter tuning |
| Evaluation | Category-level precision, recall, F1-score, and classification reports |

## Workflow

1. Clean and combine the text fields used for analysis.
2. Vectorize job-posting text with TF-IDF.
3. Train and tune a Multinomial Naive Bayes classifier.
4. Compare category performance and inspect where the model is weaker.
5. Translate model output into potential matching and market-insight use cases.

## Files

- [Analysis notebook](Job%20Description%20NLP.ipynb)
- [Job description data](job_description.csv)
- [Project proposal](NLP%20Project%20Proposal%20-%20Enhancing%20Job%20Matching%20and%20Market%20Analysis.docx)
- [Presentation](Enhancing_Job_Matching_and_Market_Analysis_through_NLP.pptx)
- [Portfolio image](../images/Jobmatching.jpg)

## Interpretation and limits

Performance varies by category, so aggregate accuracy alone is not enough for a responsible matching workflow. The dataset may contain sampling, labeling, temporal, and geographic bias. A production system would need calibrated scores, human review, freshness monitoring, explainable match reasons, and bias testing before influencing employment decisions.

## Next steps

- Compare linear models and transformer embeddings against the TF-IDF baseline.
- Add temporal validation to measure drift in job-market language.
- Evaluate ranking quality with human-judged relevance, not only classification metrics.

[← Back to the portfolio](../README.md)

