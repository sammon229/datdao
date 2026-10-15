# Portfolio guide

This repository is a curated portfolio, not a single application. The top-level `index.html` is the visual entry point; project folders hold the technical detail.

## Recommended review path

1. Start with the [portfolio homepage](../index.html) for the project-level story.
2. Open [AI Agent System](../projects/bigboymission/showcase.html) for the featured systems case study and architecture diagrams.
3. Read the [AI Agent System project guide](../projects/bigboymission/README.md) for the local interactive demo.
4. Open the individual project READMEs for methods, data, requirements, and limitations.

## Capability map

| Capability | Evidence in this repository |
| --- | --- |
| Analytics engineering | SQL, Python, R, ETL, data exploration, and model-ready datasets |
| Business intelligence | Power BI, Tableau, dashboard-oriented analysis, and decision framing |
| Automation | Workflow and data-pipeline projects, including streaming and distributed processing concepts |
| Machine learning | Fraud detection, churn prediction, housing valuation, stock forecasting, and NLP matching |
| AI systems design | AI Agent System, canonical task state, orchestration boundaries, and operator workflows |
| Communication | Project READMEs, architecture diagrams, limitations, and reproducible local instructions |

## Data and reproducibility notes

- Dataset-heavy projects retain their source materials where they are part of the original analysis story.
- Large files are not treated as a deployment dependency for the portfolio homepage.
- The AI Agent System demo is deterministic and portfolio-safe. It intentionally does not read real Hermes files, Mnemosyne, Obsidian, cron stores, credentials, or host telemetry.
- When a project needs local dependencies, its README is the source of truth for setup and execution.

## Quality bar for future additions

Each new project should include:

- a concise README with the problem, method, result, limitations, and run instructions;
- a representative visual or sample output that renders on GitHub;
- explicit data provenance and privacy boundaries;
- relative links that work from both GitHub Pages and the repository root;
- generated artifacts and local runtime state excluded from version control.
