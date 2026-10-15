# BigBoyMission Portfolio Demo

An interactive, local-preview mission-control dashboard for showcasing multi-agent coordination patterns in a GitHub portfolio. It is not a hosted service and does not require a live Hermes installation.

## What this demo shows

- Executive overview with service health, blockers, queued work, and live worker evidence
- Kanban work control with task drawers, run history, event evidence, and `[user-input]` promotion to **Ready**
- Agent Fleet ordered by hierarchy: BigBoy, MiuMiu, managers, and specialists
- Cron and schedule cards with editable demo fields, enable/disable behavior, and simulated run-now feedback
- Memory search using seeded sample records
- Systems view with simulated CPU, RAM, GPU, and storage telemetry
- AI Structure with the canonical AI Share lanes: Inbox, Outbox, Status, and Results
- Embedded architecture diagrams with no connection to private files or production services

## Architecture gallery

The portfolio includes the actual Archify diagrams as SVG assets so GitHub renders the system visually in the repository. The original interactive Archify HTML is preserved beside each visual asset for local exploration.

### AI Share Agent Architecture

![AI Share Agent Architecture](docs/diagrams/ai-share-agent-architecture.svg)

- [Open the interactive Archify source](references/ai-share-agent-architecture.html)

### Unified AI Systems Backend

![Unified AI Systems Backend](docs/diagrams/mission-control-unified-architecture.svg)

- [Open the interactive Archify source](references/mission-control-unified-architecture.html)

The diagrams communicate the portfolio story at a glance: Dat Dao is the final authority, BigBoy is the Hermes executive orchestrator, MiuMiu is the external engineering orchestrator, and AI Share owns the canonical `task_id` state across Inbox, Outbox, Status, and Results.

## Preview locally

Requires Python 3.10+ and no third-party packages.

```powershell
python .\server.py
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/). The server is only a local preview helper; nothing is deployed or published by this project.

On Windows, you can also double-click `START_PORTFOLIO_DEMO.cmd` to preview it on port 8766.

To use another port:

```powershell
$env:MISSION_CONTROL_PORT = "8766"
python .\server.py
```

## Portfolio safety

This clone uses only in-memory demo data. It does not read Hermes, Mnemosyne, Obsidian, real cron stores, external delivery channels, credentials, user telemetry, or host resource counters. Changes made in the UI reset when the demo server restarts.

The `references/` HTML files preserve the interactive Archify diagrams; the extracted SVGs in `docs/diagrams/` are the GitHub-friendly visual presentation layer.
