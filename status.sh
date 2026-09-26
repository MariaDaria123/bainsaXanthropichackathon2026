#!/usr/bin/env bash
# Live board for everyone (refreshes every 20 s). Ctrl-C to quit.
cd "$(dirname "$0")"; PY=.venv/bin/python; [ -x "$PY" ] || PY=python3
while true; do clear; "$PY" swarm.py status 2>/dev/null; echo; echo "(refreshing every 20 s; board: $PY swarm.py board --problem p4)"; sleep 20; done
