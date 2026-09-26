#!/usr/bin/env bash
# ./stop.sh        graceful: every worker on every laptop exits after its current task (pushes swarm/STOP)
# ./stop.sh --now  this laptop only: kill workers and their Claude sessions immediately
cd "$(dirname "$0")"; PY=.venv/bin/python; [ -x "$PY" ] || PY=python3
if [ "${1:-}" = "--now" ]; then pkill -f "swarm.py work" ; pkill -f "claude -p" ; echo "killed local workers"
else "$PY" swarm.py stop; fi
