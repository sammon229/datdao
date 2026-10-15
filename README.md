# Dat Dao · Portfolio

Selected analytics engineering, automation, machine-learning, and AI systems work by Dat Dao.

The repository is intentionally organized in two layers:

- The root portfolio is the public-facing index for browsing projects and opening the visual demos.
- Each project folder contains its own README, source notebooks/scripts, data notes, and reproducibility guidance.

## Featured system: AI Agent System

An interactive local-first command deck for demonstrating multi-agent coordination without exposing a live Hermes installation. The public showcase works directly on GitHub Pages; the full dashboard runs locally with deterministic demo data.

### What it demonstrates

- Executive operations overview with live-worker evidence, blockers, and queued work
- Kanban task control with `[user-input]` promotion to **Ready**
- Agent Fleet hierarchy with assignments, status, cron jobs, skills, and runtime visibility
- Editable cron schedules with simulated Run now feedback
- AI Structure with canonical AI Share lanes: Inbox, Outbox, Status, and Results
- Demo systems telemetry for CPU, RAM, GPU, storage, memory, and sessions
- Portfolio-safe deterministic data with no credentials, private paths, or production integrations

### Architecture

![AI Share Agent Architecture](projects/bigboymission/docs/diagrams/ai-share-agent-architecture.svg)

![Unified AI Systems Backend](projects/bigboymission/docs/diagrams/mission-control-unified-architecture.svg)

➡️ [Open the visual showcase](projects/bigboymission/showcase.html) · [Read the project guide](projects/bigboymission/README.md) · [Run the interactive dashboard locally](projects/bigboymission/README.md#preview-locally)

The project includes the original interactive Archify HTML diagrams under `projects/bigboymission/references/` and extracted SVGs so the architecture is visible directly in GitHub.

## Project map

| Area | Project | Primary focus |
| --- | --- | --- |
| AI systems | [AI Agent System](projects/bigboymission/README.md) | Multi-agent coordination, operator UX, task state, architecture diagrams |
| Fraud analytics | [Credit Card Fraud Detection](Machine%20Learning%20Credit%20Card%20Fraud%20Detection/README.md) | Imbalanced classification and model evaluation |
| Customer analytics | [Telecom Churn Prediction](Tele%20Customer%20Churn%20Rate%20%20Prediction%20Using%20Python/README.md) | Retention signals and customer segmentation |
| NLP | [Job Matching and Market Analysis](Enhancing%20Job%20Matching%20and%20Market%20Analysis%20through%20NLP/README.md) | Text features, matching, and labor-market insights |
| Real estate | [Ames Property Analysis](Data%20exploration%20and%20analysis%20using%20Python%20for%20residential%20properties%20in%20Ames,%20Iowa/README.md) | Exploratory analysis and pricing factors |
| Real estate | [Housing Price Prediction in R](Predict%20housing%20prices%20in%20the%20US%20using%20R/README.md) | Statistical modeling and feature interpretation |
| Real estate | [King County Valuation](Real%20Estate%20Valuation%20Optimization%20in%20King%20County/README.md) | Predictive valuation and optimization |
| Forecasting | [Stock Price Prediction](Stock%20Price%20Prediction%20with%20Python/README.md) | ARIMA/LSTM forecasting experiments |
| Data engineering | [E-commerce Big Data](E-Commerce%20BigData/README.md) | Ingestion, streaming, and distributed processing |

## Portfolio conventions

- Large datasets are retained where they are part of the original project story; generated outputs and local runtime files should stay untracked.
- The AI Agent System demo is explicitly portfolio-safe and does not connect to production Hermes, Mnemosyne, Obsidian, cron stores, credentials, or host telemetry.
- The repository’s GitHub Pages entry point is a presentation layer. Use the local preview instructions when you want to interact with the dashboard controls.
