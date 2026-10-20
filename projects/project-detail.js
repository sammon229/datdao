const projects = {
  fraud: {
    category: "Machine learning",
    title: "Credit card fraud detection",
    summary: "A cost-aware classification study focused on suspicious transactions, class imbalance, and the trade-off between missed fraud and false alarms.",
    image: "../images/MIT-Fraud-Detection-PRESS_0.jpg",
    alt: "Illustration representing credit card fraud detection",
    metrics: [["5", "evaluation lenses"], ["2", "error costs to balance"], ["CV", "validation included"]],
    question: "Can a classifier identify suspicious transactions without hiding the cost of false positives and false negatives behind accuracy alone?",
    evidence: ["The project evaluates precision, recall, F1-score, accuracy, and cross-validation.", "The workflow starts with class imbalance and reviews feature relevance before treating the model as a decision aid.", "The source transaction dataset is intentionally not redistributed, so the notebook documents how to place it locally before reproduction."],
    methods: ["classification", "precision / recall", "scikit-learn"],
    finding: "The useful contribution is the evaluation frame: fraud detection needs threshold governance and investigator feedback, not a single headline score.",
    limits: "The source data is anonymized and historical. This is an educational analysis, not a production fraud rule.",
    readme: "../Machine%20Learning%20Credit%20Card%20Fraud%20Detection/README.md",
    source: "../Machine%20Learning%20Credit%20Card%20Fraud%20Detection/Credit%20Card%20Fraud.ipynb",
    sourceLabel: "Open notebook"
  },
  churn: {
    category: "Predictive analytics",
    title: "Customer churn signals",
    summary: "A retention-focused workflow that turns account, service, and contract behavior into interpretable signals for customer outreach.",
    image: "../images/churn.jpg",
    alt: "Telecom customer churn analysis visualization",
    metrics: [["7,043", "customers"], ["21", "features"], ["3", "model families"]],
    question: "Which customer and service signals can help a retention team prioritize outreach while keeping the decision interpretable?",
    evidence: ["The repository dataset contains 7,043 customers and 21 account, service, and demographic features.", "The analysis compares Logistic Regression, Random Forest, and Linear Discriminant Analysis.", "Tenure, contract type, and monthly charges are identified as important churn signals in the original analysis."],
    methods: ["logistic regression", "random forest", "LDA"],
    finding: "The project connects model comparison to a practical retention question: who needs attention, and which signals can a team explain?",
    limits: "Churn labels and contract behavior change over time; a production workflow needs drift monitoring, calibrated risk, privacy controls, and fairness review.",
    readme: "../Tele%20Customer%20Churn%20Rate%20%20Prediction%20Using%20Python/README.md",
    source: "../Tele%20Customer%20Churn%20Rate%20%20Prediction%20Using%20Python/Customer%20Churn%20Rate%20Prediction%20using%20Python.ipynb",
    sourceLabel: "Open notebook"
  },
  "housing-r": {
    category: "Statistical modeling",
    title: "Housing price prediction in R",
    summary: "An Ames housing study comparing interpretable regression ideas with a tree-based model for understanding sale-price variation.",
    image: "../images/R%20housing.jpg",
    alt: "Residential housing price prediction visualization",
    metrics: [["2,930", "sales"], ["~85%", "reported variation explained"], ["80+", "regressors explored"]],
    question: "How do property characteristics explain sale price, and what changes when an interpretable regression workflow is compared with Random Forest?",
    evidence: ["The study uses 2,930 Ames residential sales from 2006–2010.", "The methods include OLS, multicollinearity review, maximum-likelihood ideas, and Random Forest.", "The original study reports approximately 85% of sale-price variation explained by the Random Forest approach."],
    methods: ["OLS", "random forest", "R"],
    finding: "The analysis pairs a familiar statistical baseline with a stronger nonlinear model while keeping feature importance and regional scope visible.",
    limits: "The observations are regional and historical. The reported result is not a current valuation service or a guarantee of future accuracy.",
    readme: "../Predict%20housing%20prices%20in%20the%20US%20using%20R/README.md",
    source: "../Predict%20housing%20prices%20in%20the%20US%20using%20R/FinalCode.R",
    sourceLabel: "Open R script"
  },
  stocks: {
    category: "Time series",
    title: "ETF price forecasting",
    summary: "A comparison of classical and recurrent forecasting approaches, with scaling and differencing called out so the result is not over-sold.",
    image: "../images/stock-prices.jpg",
    alt: "Stock price prediction visualization",
    metrics: [["8", "ETFs"], ["2", "model families"], ["MSE", "primary metric"]],
    question: "How do ARIMA and LSTM behave across a small set of ETF price histories, and what does the metric leave out?",
    evidence: ["The experiment covers VOO, VTI, VGT, VFH, VHT, VIS, VAW, and VNQ.", "The workflow compares ARIMA with LSTM using historical daily OHLCV data.", "Mean Squared Error and visual forecast comparison are used together because scaling and differencing affect interpretation."],
    methods: ["ARIMA", "LSTM", "OHLCV"],
    finding: "The original analysis reports lower MSE for LSTM across the selected ETFs, while also documenting why that comparison needs caution.",
    limits: "Historical price patterns do not guarantee future performance. This is a research artifact, not financial advice or a trading system.",
    readme: "../Stock%20Price%20Prediction%20with%20Python/README.md",
    source: "../Stock%20Price%20Prediction%20with%20Python/Stock%20Price%20Prediction%20with%20Python.ipynb",
    sourceLabel: "Open notebook"
  },
  "king-county": {
    category: "Applied machine learning",
    title: "King County valuation",
    summary: "A property-level regression workflow for exploring how size, grade, location, and other fields relate to residential sale price.",
    image: "../images/housevalue.jpg",
    alt: "King County real estate valuation visualization",
    metrics: [["21,613", "sales"], ["21", "dataset columns"], ["1", "RF regression model"]],
    question: "Can property-level features organize a clearer valuation conversation without pretending to replace a professional appraisal?",
    evidence: ["The dataset contains 21,613 King County sales from May 2014 through May 2015.", "The analysis uses bedrooms, bathrooms, square footage, grade, location, and other property fields.", "The project documents exploratory analysis, feature engineering, and Random Forest regression rather than a production appraisal service."],
    methods: ["feature engineering", "random forest", "valuation"],
    finding: "The strongest portfolio lesson is the translation from property fields to decision support, with feature importance and outlier behavior kept in view.",
    limits: "The README does not report a validated performance score. The original results call for further refinement before any operational use.",
    readme: "../Real%20Estate%20Valuation%20Optimization%20in%20King%20County/README.md",
    source: "../Real%20Estate%20Valuation%20Optimization%20in%20King%20County/Leveraging%20Machine%20Learning%20to%20Optimize%20Real%20Estate%20Valuation%20in%20King%20County.ipynb",
    sourceLabel: "Open notebook"
  },
  ames: {
    category: "Exploratory analysis",
    title: "Ames housing exploration",
    summary: "An exploratory and diagnostic workflow showing how quality, living area, neighborhood, and age relate to SalePrice.",
    image: "../images/p1.jpg",
    alt: "Ames residential property analysis visualization",
    metrics: [["2,920", "cleaned rows"], ["20", "dataset columns"], ["45.2%", "reported R²"]],
    question: "Which property characteristics are most associated with SalePrice, and how can visual exploration shape a defensible modeling decision?",
    evidence: ["The cleaned repository file contains 2,920 rows and 20 columns.", "The workflow combines Python, pandas, NumPy, seaborn, matplotlib, and statsmodels.", "The original analysis reports an R-squared of approximately 45.2% for its regression specification."],
    methods: ["EDA", "regression", "Python"],
    finding: "The project shows how quality, living area, neighborhood, garage capacity, and age provide context beyond a single square-footage relationship.",
    limits: "This is an Ames-specific educational analysis. The reported fit depends on the original feature selection, preprocessing, and train/test design.",
    readme: "../Data%20exploration%20and%20analysis%20using%20Python%20for%20residential%20properties%20in%20Ames,%20Iowa/README.md",
    source: "../Data%20exploration%20and%20analysis%20using%20Python%20for%20residential%20properties%20in%20Ames,%20Iowa/Data%20Exploreation%20and%20Analysis%20Ames,Iowa.ipynb",
    sourceLabel: "Open notebook"
  },
  nlp: {
    category: "Natural language processing",
    title: "Job matching with NLP",
    summary: "A text classification baseline that converts job descriptions into category signals while keeping category-level performance and bias visible.",
    image: "../images/Jobmatching.jpg",
    alt: "NLP job matching analysis visualization",
    metrics: [["325", "job records"], ["TF-IDF", "text representation"], ["4", "evaluation views"]],
    question: "Can structured text features improve job-posting classification and create more useful matching and labor-market signals?",
    evidence: ["The repository dataset contains 325 job-description records with requirements, benefits, and category fields.", "The workflow cleans text, creates TF-IDF vectors, and tunes a Multinomial Naive Bayes baseline.", "Evaluation includes category-level precision, recall, F1-score, and classification reports."],
    methods: ["TF-IDF", "Naive Bayes", "classification"],
    finding: "The project demonstrates a transparent NLP baseline and makes the next step clear: compare embeddings, add temporal validation, and evaluate ranking quality with human judgment.",
    limits: "Aggregate accuracy is not enough for employment decisions. Production use would require calibrated scores, human review, freshness monitoring, explainable match reasons, and bias testing.",
    readme: "../Enhancing%20Job%20Matching%20and%20Market%20Analysis%20through%20NLP/README.md",
    source: "../Enhancing%20Job%20Matching%20and%20Market%20Analysis%20through%20NLP/Job%20Description%20NLP.ipynb",
    sourceLabel: "Open notebook"
  },
  ecommerce: {
    category: "Data engineering",
    title: "E-commerce data pipeline",
    summary: "An architecture study that separates ingestion, streaming, storage, and analysis so a high-volume workflow can be inspected and extended.",
    image: "../images/Esri-and-Big-Data.jpg",
    alt: "Big-data ingestion and processing pipeline visualization",
    metrics: [["541,909", "records"], ["8", "source fields"], ["4", "pipeline layers"]],
    question: "How can an e-commerce workflow separate collection, transport, storage, and analysis so each stage can be monitored and replayed?",
    evidence: ["The repository data file contains 541,909 records across 8 source fields.", "The architecture represents Apache NiFi for ingestion, Apache Kafka for streaming, HDFS for storage, and big-data tools for analysis.", "The design keeps raw data available for replay and validation before analytical transformations."],
    methods: ["Apache NiFi", "Kafka", "HDFS"],
    finding: "The project makes data engineering boundaries visible: producers, transport, storage, and downstream analysis can evolve independently.",
    limits: "This is an architecture and learning artifact rather than a packaged multi-node deployment. Production adoption would need schema governance, security, monitoring, retention, and infrastructure as code.",
    readme: "../E-Commerce%20BigData/README.md",
    source: "../E-Commerce%20BigData/Project%20Report%20Ecommerce%20Data%20Ingestion%20and%20Processing%20Pipeline.pdf",
    sourceLabel: "Open report"
  }
};

const key = new URLSearchParams(window.location.search).get("project") || "fraud";
const project = projects[key];
const extra = (window.evidenceData && window.evidenceData[key]) || null;
const root = document.querySelector("#project-root");

if (!project) {
  root.innerHTML = '<section class="error-state"><p class="eyebrow">Project not found</p><h1>Choose a project from the portfolio.</h1><p class="hero-summary">This detail page uses a stable project key from the main portfolio. Return to selected work and choose a project card to open its visual evidence.</p><a class="button button-primary" href="../index.html#work">Back to selected work ↗</a></section>';
} else {
  document.title = `${project.title} | Dat Dao`;
  root.innerHTML = `
    <header class="site-header">
      <a class="brand" href="../index.html" aria-label="Dat Dao home"><span class="brand-mark" aria-hidden="true">DD</span><span>Dat Dao</span></a>
      <a class="back-link" href="../index.html#work">← Back to selected work</a>
    </header>
    <main>
      <section class="project-hero" aria-labelledby="project-title">
        <div>
          <p class="eyebrow"><span class="status-dot" aria-hidden="true"></span>${project.category}</p>
          <h1 id="project-title">${project.title}</h1>
          <p class="hero-summary">${project.summary}</p>
          <div class="hero-actions"><a class="button button-primary" href="${project.readme}">Read source notes ↗</a><a class="button button-secondary" href="${project.source}">${project.sourceLabel} ↗</a></div>
        </div>
        <figure class="hero-visual"><img src="${project.image}" alt="${project.alt}" width="900" height="560"><figcaption>Visual support · project artifact / analysis context</figcaption></figure>
      </section>
      <section class="metric-band" aria-label="Project metrics">${project.metrics.map(([value, label]) => `<div class="metric"><strong>${value}</strong><span>${label}</span></div>`).join("")}</section>
      ${extra ? `<section class="evidence-visual" aria-labelledby="visual-title"><div class="evidence-visual-head"><div><p class="eyebrow">Run output / evidence</p><h2 id="visual-title">Visual support for the thesis</h2></div><span class="evidence-kind">${extra.kind}</span></div><figure class="evidence-chart"><img src="${extra.image}" alt="${extra.alt}" width="840" height="420" loading="lazy"><figcaption>${extra.caption}</figcaption></figure></section>` : ""}
      <section class="detail-grid" aria-label="Project evidence and interpretation">
        <article class="detail-card detail-card-wide"><p class="eyebrow">The question</p><h2>What this project is trying to answer</h2><p>${project.question}</p><div class="method-row">${project.methods.map((method) => `<span class="method">${method}</span>`).join("")}</div><div class="source-note"><strong>Why the visual helps:</strong> the image gives the project a concrete starting point, while the metric band anchors the explanation in the data and evaluation choices.</div></article>
        <article class="detail-card"><p class="eyebrow">Evidence</p><h2>What is in the repository</h2><ul class="evidence-list">${project.evidence.map((item) => `<li>${item}</li>`).join("")}</ul></article>
        <article class="detail-card"><p class="eyebrow">Interpretation</p><h2>What to take away</h2><p>${project.finding}</p><p class="source-note"><strong>Limit:</strong> ${project.limits}</p></article>
      </section>
    </main>
    <footer class="footer-note"><span>© 2026 Dat Dao · Visual project detail</span><span><a class="index-link" href="../index.html#work">More projects ↗</a></span></footer>`;
}
