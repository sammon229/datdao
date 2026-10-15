@echo off
setlocal
cd /d "%~dp0"
set MISSION_CONTROL_HOST=127.0.0.1
set MISSION_CONTROL_PORT=8766
echo BigBoyMission portfolio demo: http://127.0.0.1:8766/
python server.py
