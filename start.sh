#!/usr/bin/env bash
# Start N background swarm workers on this laptop for p4 c6.
#   ./start.sh a 2      two workers on direction (a)      ./start.sh any 3   three workers, any task
# Env: SWARM_MODEL=sonnet (if you hit subscription limits), SWARM_TASK_MIN=25, SWARM_YOLO=1 (no permission prompts)
set -eu
cd "$(dirname "$0")"
DIR="${1:-any}"; N="${2:-2}"
[ -d .venv ] || { echo "Run ./setup_laptop.sh first"; exit 1; }
export PATH="$PWD/.venv/bin:$PATH"
export SWARM_HOME="${SWARM_HOME:-$HOME/swarm-workers}"
mkdir -p "$SWARM_HOME/logs"
HOST="$(hostname -s 2>/dev/null | tr -cd 'a-zA-Z0-9' | cut -c1-10)"
MATCH=(); [ "$DIR" != "any" ] && MATCH=(--match "($DIR)")
started=0; i=0
while [ "$started" -lt "$N" ]; do
  i=$((i+1)); NAME="${HOST}-${DIR}${i}"
  pgrep -f "work --name $NAME " >/dev/null && continue      # name already running on this laptop
  started=$((started+1))
  nohup "$PWD/.venv/bin/python" swarm.py work --name "$NAME" --problem p4 "${MATCH[@]+"${MATCH[@]}"}" \
        > "$SWARM_HOME/logs/$NAME.log" 2>&1 &
  echo "started $NAME  (log: $SWARM_HOME/logs/$NAME.log)"
  sleep 3
done
echo
echo "Watch:  ./status.sh        Logs:  tail -f $SWARM_HOME/logs/*.log        Stop:  ./stop.sh"
