"""BigBoyMission portfolio demo server.

This server intentionally uses deterministic in-memory demo data. It never
reads a Hermes installation, a real database, credentials, cron files, or
machine telemetry.
"""

from __future__ import annotations

import copy
import json
import os
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
REFERENCES = ROOT / "references"
HOST = os.environ.get("MISSION_CONTROL_HOST", "127.0.0.1")
PORT = int(os.environ.get("MISSION_CONTROL_PORT", "8765"))
DEMO_TZ = timezone(timedelta(hours=-5))


def stamp(hours_ago=0, minutes_ago=0):
    return (datetime.now(DEMO_TZ) - timedelta(hours=hours_ago, minutes=minutes_ago)).isoformat(timespec="seconds")


def task(task_id, title, body, assignee, status, priority, block_kind=None, started=False, completed=False):
    return {
        "id": task_id,
        "title": title,
        "body": body,
        "assignee": assignee,
        "status": status,
        "priority": priority,
        "createdAt": stamp(hours_ago=18),
        "startedAt": stamp(hours_ago=3) if started else None,
        "completedAt": stamp(hours_ago=1) if completed else None,
        "heartbeatAt": stamp(minutes_ago=4) if started and not completed else None,
        "currentRun": {"id": 12, "profile": assignee, "status": "running"} if started and not completed else None,
        "blockKind": block_kind,
        "block_kind": block_kind,
        "blockRecurrences": 1 if block_kind else 0,
        "completionContract": "demo-only",
        "workerPid": 42012 if started and not completed else None,
        "maxRuntime": 1800,
        "lastError": "Awaiting operator decision" if block_kind else "",
        "result": "Demo result verified" if completed else "",
        "sessionId": "demo-session-001" if started else None,
    }


TASKS = [
    task("demo_001", "Build live operations summary", "Create the overview cards and service pulse for the portfolio demonstration.", "big-it-manager", "running", 90, started=True),
    task("demo_002", "Review AI Share handoff contract", "Confirm that BigBoy and MiuMiu exchange one canonical task_id through Inbox, Outbox, Status, and Results.", "bigboy", "blocked", 100, block_kind="needs_input"),
    task("demo_003", "Prepare portfolio release brief", "Turn the completed demo build into a concise release note and walkthrough.", "big-career-mentor", "ready", 70),
    task("demo_004", "Validate memory retention flow", "Check the demo memory search surface and verify that results remain human-readable.", "big-auditor", "scheduled", 50),
    task("demo_005", "Model property workflow", "Document a reusable property operations workflow with clear ownership and evidence.", "big-property-manager", "done", 40, completed=True),
    task("demo_006", "Run paper-trading risk review", "Review a simulated trading plan without placing an order or connecting to a broker.", "big-trading-manager", "triage", 80),
    task("demo_007", "Audit release evidence", "Verify that the portfolio clone contains no live credentials, personal paths, or production integrations.", "big-auditor", "done", 95, completed=True),
    task("demo_008", "Research local-first hosting", "Compare LAN hosting patterns and document a safe local-only deployment path.", "nemo", "done", 30, completed=True),
    task("demo_009", "Route engineering overflow", "Show how an eligible engineering slice can be routed to MiuMiu through AI Share.", "nerdy", "ready", 60),
]


AGENT_META = [
    ("bigboy", "BigBoy", "Hermes executive orchestrator coordinating decisions, routing, and evidence.", 0, "Executive orchestrator", "Portfolio Owner / final authority", 48),
    ("miumiu", "MiuMiu", "External engineering orchestrator receiving work through AI Share and returning the same task_id.", 1, "External engineering orchestrator", "Portfolio Owner / AI Share", 0),
    ("big-it-manager", "Big IT Manager", "Owns implementation, review, testing, diagnostics, and production readiness.", 2, "Manager", "Hermes Agent Fleet", 32),
    ("big-property-manager", "Big Property Manager", "Coordinates property operations, records, maintenance, leases, and evidence.", 2, "Manager", "Hermes Agent Fleet", 28),
    ("big-trading-manager", "Big Trading Manager", "Owns research, strategy, risk review, and paper-trading governance.", 2, "Manager", "Hermes Agent Fleet", 31),
    ("big-career-mentor", "Big Career Mentor", "Turns career signals into practical priorities, actions, and weekly reviews.", 2, "Manager", "Hermes Agent Fleet", 26),
    ("trader", "Trader", "Execution specialist limited to plans approved by Big Trading Manager.", 3, "Trading specialist", "Big Trading Manager", 18),
    ("security-guy", "Security Guy", "Independently checks authorization, evidence, and action boundaries.", 3, "Security specialist", "Hermes Agent Fleet", 22),
    ("big-auditor", "Big Auditor", "Verifies scope, authoritative sources, execution evidence, and read-back.", 3, "Audit specialist", "Hermes Agent Fleet", 24),
    ("nerdy", "Nerdy", "Maintains governance, identities, durable memory, and knowledge hygiene.", 3, "Specialist", "Hermes Agent Fleet", 27),
    ("nemo", "Nemo", "Handles bounded research and returns concise, sourced findings.", 3, "Specialist", "Hermes Agent Fleet", 20),
]


CRON_JOBS = [
    {"id": "demo_watchdog", "name": "Demo exception watchdog", "profile": "bigboy", "schedule": "Every 6 hours", "scheduleExpr": "0 */6 * * *", "enabled": True, "state": "scheduled", "lastRun": stamp(hours_ago=2), "nextRun": stamp(hours_ago=-4), "lastStatus": "ok", "lastError": None, "delivery": "demo notification", "noAgent": True, "script": "demo_watchdog.py", "prompt": "Check the demo gateway and remain silent when healthy.", "skills": []},
    {"id": "demo_daily_brief", "name": "Daily operations brief", "profile": "bigboy", "schedule": "07:30 local", "scheduleExpr": "30 7 * * *", "enabled": True, "state": "scheduled", "lastRun": stamp(hours_ago=6), "nextRun": stamp(hours_ago=-18), "lastStatus": "ok", "lastError": None, "delivery": "demo notification", "noAgent": False, "script": None, "prompt": "Summarize open work, blockers, and next actions using demo data only.", "skills": ["weekly-review-planning"]},
    {"id": "demo_memory_check", "name": "Memory consistency check", "profile": "nerdy", "schedule": "Weekdays at 09:00", "scheduleExpr": "0 9 * * 1-5", "enabled": True, "state": "scheduled", "lastRun": stamp(hours_ago=4), "nextRun": stamp(hours_ago=-20), "lastStatus": "ok", "lastError": None, "delivery": "demo notification", "noAgent": False, "script": None, "prompt": "Review the demo memory index and flag stale facts.", "skills": ["memory-hygiene"]},
    {"id": "demo_release_review", "name": "Portfolio release review", "profile": "big-auditor", "schedule": "Fridays at 16:00", "scheduleExpr": "0 16 * * 5", "enabled": False, "state": "paused", "lastRun": stamp(hours_ago=30), "nextRun": None, "lastStatus": "paused", "lastError": None, "delivery": "demo notification", "noAgent": False, "script": None, "prompt": "Verify the demo build is safe to publish.", "skills": ["artifact-audit"]},
]


COMMENTS = {
    "demo_002": [{"id": 1, "author": "BigBoy", "body": "Demo blocker: choose whether the engineering overflow path should be included in the release walkthrough.", "createdAt": stamp(hours_ago=1)}],
    "demo_001": [{"id": 2, "author": "Big IT Manager", "body": "Working through the dashboard verification checklist.", "createdAt": stamp(minutes_ago=8)}],
}
EVENTS = {
    "demo_001": [{"id": 1, "runId": 12, "kind": "heartbeat", "payload": "Demo worker is active and reporting progress.", "createdAt": stamp(minutes_ago=4)}],
    "demo_002": [{"id": 2, "runId": None, "kind": "blocked", "payload": "Awaiting owner decision.", "createdAt": stamp(hours_ago=1)}],
}


def task_counts():
    counts = {"archived": 2, "blocked": 0, "done": 0, "ready": 0, "running": 0, "triage": 0, "scheduled": 0, "todo": 0}
    for item in TASKS:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    return counts


def work_payload():
    counts = task_counts()
    blockers = [copy.deepcopy(x) for x in TASKS if x["status"] == "blocked"]
    workers = [{"taskId": "demo_001", "title": "Build live operations summary", "profile": "big-it-manager", "runId": 12, "status": "running", "heartbeatAt": stamp(minutes_ago=4)}]
    return {"exists": True, "counts": counts, "tasks": copy.deepcopy(TASKS), "workers": workers, "blockers": blockers, "recentEvents": [{"kind": "heartbeat", "taskId": "demo_001", "createdAt": stamp(minutes_ago=4)}]}


def agents_payload():
    result = []
    for agent_id, label, mission, level, level_name, reports_to, skills in AGENT_META:
        owned = [x for x in TASKS if x["assignee"] == agent_id]
        open_tasks = [x for x in owned if x["status"] not in ("done", "archived")]
        blocked = [x for x in open_tasks if x["status"] == "blocked"]
        running = [x for x in open_tasks if x["status"] == "running"]
        jobs = [x for x in CRON_JOBS if x["profile"] == agent_id]
        explicit = "online" if agent_id == "miumiu" else "working" if running else "blocked" if blocked else "ready" if open_tasks or jobs else "idle"
        result.append({
            "id": agent_id, "label": label, "mission": mission, "skills": skills, "memoryFiles": 3 if agent_id in ("bigboy", "nerdy") else 1,
            "hasSoul": True, "status": explicit, "statusReason": "Demo worker evidence is present" if running else "Needs operator decision" if blocked else "Assigned work is queued or scheduled" if open_tasks or jobs else "No open work or cron assignment",
            "gatewayOnline": agent_id != "miumiu", "processes": [{"pid": 42012, "profile": agent_id, "purpose": "demo worker", "command": "portfolio-demo"}] if running else [],
            "openTasks": len(open_tasks), "blockedTasks": len(blocked), "doneTasks": len([x for x in owned if x["status"] == "done"]), "tasks": copy.deepcopy(owned),
            "currentTask": copy.deepcopy((running or open_tasks or [None])[0]), "workers": [{"taskId": "demo_001", "runId": 12}] if running else [], "cronJobs": copy.deepcopy(jobs), "cronCount": len(jobs), "enabledCronCount": len([x for x in jobs if x["enabled"]]),
            "sessions": [], "sessionCount": 0, "lastActivity": stamp(minutes_ago=4) if running else stamp(hours_ago=2) if owned else None,
            "external": agent_id == "miumiu", "reportsThrough": "AI Share" if agent_id == "miumiu" else None, "canonicalTaskKey": "task_id" if agent_id == "miumiu" else None,
            "hierarchyLevel": level, "hierarchyLabel": level_name, "reportsTo": reports_to,
        })
    return {"agents": result, "gateway": {"state": "demo online", "servedProfiles": [x[0] for x in AGENT_META if x[0] != "miumiu"]}, "counts": {k: len([x for x in result if x["status"] == k]) for k in ("blocked", "working", "online", "ready", "idle")}}


def cron_payload():
    return {"jobs": copy.deepcopy(CRON_JOBS), "executions": [{"id": "demo-exec-001", "jobId": "demo_watchdog", "source": "demo scheduler", "processId": "demo", "pid": "—", "status": "completed", "claimedAt": stamp(hours_ago=2), "startedAt": stamp(hours_ago=2), "finishedAt": stamp(hours_ago=2), "error": None, "delivery": "suppressed in demo", "progressAt": None}], "count": len(CRON_JOBS)}


def runtime_payload():
    return {"gateway": {"state": "running", "pid": "demo", "updatedAt": stamp(minutes_ago=1), "version": "portfolio-demo", "activeAgents": 1, "platforms": {"demo": {"state": "connected", "needs_attention": False}}, "servedProfiles": [x[0] for x in AGENT_META if x[0] != "miumiu"]}, "activeLeases": [{"lease_id": "demo-lease-001", "metadata": {"demo": True}, "pid": "demo", "session_id": "demo-session-001", "started_at": stamp(hours_ago=1), "surface": "portfolio demo", "updated_at": stamp(minutes_ago=2)}], "sessions": [{"id": "demo-session-001", "source": "demo", "name": "demo-session-001", "model": "demo-model", "startedAt": stamp(hours_ago=1), "endedAt": None, "messages": 24, "toolCalls": 8, "sessionKey": "demo"}], "profileProcesses": [], "resources": {"cpuPercent": 18, "memoryTotal": 32 * 1024**3, "memoryFree": 18 * 1024**3, "disks": [{"name": "Demo disk", "total": 512 * 1024**3, "free": 318 * 1024**3}], "gpus": [{"name": "Demo GPU", "memory": 8192, "driver": "simulated"}], "gpuUsage": [{"name": "Demo GPU", "memoryTotal": 8192, "memoryUsed": 1536, "memoryFree": 6656, "utilization": 12}], "capturedAt": stamp()}}


def ai_share_payload():
    lanes = {"inbox": [copy.deepcopy(TASKS[5])], "outbox": [copy.deepcopy(TASKS[2])], "status": [copy.deepcopy(TASKS[0]), copy.deepcopy(TASKS[1])], "results": [copy.deepcopy(TASKS[4]), copy.deepcopy(TASKS[6]), copy.deepcopy(TASKS[7])]}
    return {"owner": {"name": "Portfolio Owner", "role": "Owner / final authority"}, "orchestrators": [{"name": "BigBoy", "role": "Hermes Executive Orchestrator", "direction": "bidirectional", "state": "connected"}, {"name": "MiuMiu", "role": "External engineering orchestrator", "direction": "bidirectional", "state": "external / task_id routed"}], "canonical": {"name": "AI Share", "fields": ["Inbox", "Outbox", "Status", "Results"], "taskKey": "task_id", "source": "demo Kanban adapter"}, "systems": [{"name": "Hermes Agent Fleet", "role": "Execution and specialist reports", "state": "connected"}, {"name": "Kanban", "role": "Active task ownership", "state": "connected"}, {"name": "Mnemosyne", "role": "Durable memory", "state": "connected"}, {"name": "Obsidian", "role": "Human-readable knowledge", "state": "demo knowledge surface"}], "fleet": [{"name": "Big IT Manager", "reportsTo": "Hermes Agent Fleet"}, {"name": "Big Property Manager", "reportsTo": "Hermes Agent Fleet"}, {"name": "Big Trading Manager", "reportsTo": "Hermes Agent Fleet", "children": ["Trader"]}, {"name": "Big Career Mentor", "reportsTo": "Hermes Agent Fleet"}, {"name": "Security Guy", "reportsTo": "Hermes Agent Fleet"}, {"name": "Big Auditor", "reportsTo": "Hermes Agent Fleet"}, {"name": "Nerdy", "reportsTo": "Hermes Agent Fleet"}, {"name": "Nemo", "reportsTo": "Hermes Agent Fleet"}], "lanes": lanes, "counts": {"inbox": len(lanes["inbox"]), "outbox": len(lanes["outbox"]), "status": len(lanes["status"]), "results": len(lanes["results"])}, "note": "Demo data preserves one canonical task_id across the coordination surfaces."}


def overview_payload():
    counts = task_counts()
    return {"now": stamp(), "dateLabel": datetime.now(DEMO_TZ).strftime("%A, %B %d, %Y"), "activeProfile": "bigboy", "profiles": len(AGENT_META), "skills": sum(x[-1] for x in AGENT_META), "mcp": ["Demo memory", "Demo scheduler", "Demo connector"], "activeMemory": {"path": "demo-data/mnemosyne-demo.db", "exists": True, "working": 7, "episodic": 12, "tables": ["working_memory", "episodic_memory", "canonical_facts", "audit_log"], "memories": 19}, "sharedMemory": {"path": "demo-data/shared-memory.db", "exists": True, "working": 14, "episodic": 31, "tables": ["working_memory", "episodic_memory", "facts"]}, "board": {"counts": counts, "workers": work_payload()["workers"], "blockers": work_payload()["blockers"], "tasks": copy.deepcopy(TASKS)}, "cron": {"count": len(CRON_JOBS), "enabled": len([x for x in CRON_JOBS if x["enabled"]]), "executions": cron_payload()["executions"]}, "runtime": runtime_payload(), "services": [{"name": "Demo Hermes gateway", "state": "online", "detail": "Portfolio simulator / 11 agents"}, {"name": "Demo Kanban board", "state": "online", "detail": f"{sum(counts.values())} tasks / 1 active worker"}, {"name": "Demo scheduler", "state": "configured", "detail": f"{len([x for x in CRON_JOBS if x['enabled']])} enabled jobs / simulated runs"}, {"name": "Demo memory", "state": "online", "detail": "19 working and episodic records"}]}


MEMORIES = [{"source": "demo-memory", "table": "canonical_facts", "timestamp": stamp(hours_ago=1), "content": "AI Share preserves one canonical task_id across orchestrators, Kanban, and results."}, {"source": "demo-memory", "table": "working_memory", "timestamp": stamp(hours_ago=3), "content": "BigBoy coordinates decisions while managers retain ownership of their domain work."}, {"source": "demo-memory", "table": "facts", "timestamp": stamp(hours_ago=6), "content": "Portfolio mode is deliberately disconnected from production credentials and external delivery."}]


def memory_payload(query):
    query = (query or "").lower().strip()
    return {"query": query, "results": [x for x in MEMORIES if not query or query in (x["content"] + x["table"] + x["source"]).lower()]}


def task_detail(task_id):
    item = next((x for x in TASKS if x["id"] == task_id), None)
    if not item:
        return {"error": "demo task not found"}
    return {"task": copy.deepcopy(item), "runs": [{"id": 12, "profile": item["assignee"], "pid": "demo", "status": "running" if item["status"] == "running" else "completed", "startedAt": item["startedAt"], "heartbeatAt": item["heartbeatAt"], "summary": "Simulated portfolio run evidence."}] if item["startedAt"] else [], "comments": copy.deepcopy(COMMENTS.get(task_id, [])), "events": copy.deepcopy(EVENTS.get(task_id, []))}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        size = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(size) or b"{}")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/overview": return self.send_json(overview_payload())
        if parsed.path == "/api/work": return self.send_json(work_payload())
        if parsed.path == "/api/agents": return self.send_json(agents_payload())
        if parsed.path == "/api/cron": return self.send_json(cron_payload())
        if parsed.path == "/api/runtime": return self.send_json(runtime_payload())
        if parsed.path == "/api/ai-share": return self.send_json(ai_share_payload())
        if parsed.path == "/api/memory": return self.send_json(memory_payload(parse_qs(parsed.query).get("q", [""])[0]))
        if parsed.path.startswith("/api/task/"): return self.send_json(task_detail(parsed.path.rsplit("/", 1)[-1]))
        if parsed.path == "/reference/ai-share-agent-architecture.html": return self.send_file(REFERENCES / "ai-share-agent-architecture.html", "text/html; charset=utf-8")
        if parsed.path == "/reference/mission-control-unified-architecture.html": return self.send_file(REFERENCES / "mission-control-unified-architecture.html", "text/html; charset=utf-8")
        target = ROOT / ("index.html" if parsed.path == "/" else parsed.path.lstrip("/"))
        if target.is_file() and ROOT in target.resolve().parents and target.suffix in (".html", ".css", ".js"):
            return self.send_file(target, "text/html; charset=utf-8" if target.suffix == ".html" else "text/css; charset=utf-8" if target.suffix == ".css" else "application/javascript; charset=utf-8")
        return self.send_json({"error": "not found"}, 404)

    def send_file(self, path, content_type):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_PATCH(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")
        if len(parts) == 4 and parts[:2] == ["api", "cron"]:
            job = next((x for x in CRON_JOBS if x["profile"] == parts[2] and x["id"] == parts[3]), None)
            if not job: return self.send_json({"error": "demo cron job not found"}, 404)
            payload = self._body()
            for key in ("name", "deliver", "schedule_expr", "schedule_display", "prompt", "enabled"):
                if key in payload:
                    target = {"deliver": "delivery", "schedule_expr": "scheduleExpr", "schedule_display": "schedule"}.get(key, key)
                    job[target] = payload[key]
            job["state"] = "scheduled" if job["enabled"] else "paused"
            return self.send_json({"ok": True, "backup": f"demo-backups/{job['id']}-{int(time.time())}.json", "job": copy.deepcopy(job)})
        return self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")
        if len(parts) == 5 and parts[:2] == ["api", "cron"] and parts[4] == "run":
            job = next((x for x in CRON_JOBS if x["profile"] == parts[2] and x["id"] == parts[3]), None)
            if not job: return self.send_json({"error": "demo cron job not found"}, 404)
            job["lastRun"] = stamp(); job["lastStatus"] = "queued"
            return self.send_json({"ok": True, "status": "queued", "demo": True})
        if len(parts) == 4 and parts[:2] == ["api", "task"] and parts[3] == "comment":
            item = next((x for x in TASKS if x["id"] == parts[2]), None)
            if not item: return self.send_json({"error": "demo task not found"}, 404)
            payload = self._body(); body = str(payload.get("body", "")).strip()
            if not body: return self.send_json({"error": "comment is required"}, 400)
            if not body.lower().startswith("[user-input]"): body = "[user-input] " + body
            previous = item["status"]
            if previous in ("done", "archived"): return self.send_json({"error": "demo completed tasks cannot be retriggered"}, 409)
            promoted = previous not in ("running", "ready")
            if promoted: item["status"] = "ready"; item["block_kind"] = None; item["blockKind"] = None
            comment = {"id": int(time.time()), "author": "Portfolio Owner", "body": body, "createdAt": stamp()}
            COMMENTS.setdefault(item["id"], []).insert(0, comment)
            return self.send_json({"ok": True, "inputType": "user-input", "promoted": promoted, "previousStatus": previous, "status": item["status"], "comment": comment}, 201)
        return self.send_json({"error": "not found"}, 404)


if __name__ == "__main__":
    print(f"BigBoyMission portfolio demo running at http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
