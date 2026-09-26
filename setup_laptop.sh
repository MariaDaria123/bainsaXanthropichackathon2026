#!/usr/bin/env bash
# One-time setup on each laptop (about 2 minutes). Run from the repo folder:  ./setup_laptop.sh
set -u
cd "$(dirname "$0")"
ok(){ printf "  \033[32mOK\033[0m  %s\n" "$1"; }; bad(){ printf "  \033[31m!!\033[0m  %s\n" "$1"; FAIL=1; }
FAIL=0
echo "Proof Pursuit swarm setup"
command -v git >/dev/null && ok "git" || bad "git missing: install Xcode tools (xcode-select --install)"
command -v python3 >/dev/null && ok "python3 $(python3 -V 2>&1 | cut -d' ' -f2)" || bad "python3 missing"
if command -v claude >/dev/null; then ok "claude $(claude --version 2>/dev/null | head -1)"
else bad "Claude Code missing: npm install -g @anthropic-ai/claude-code  then run 'claude' once to log in"; fi
[ "$FAIL" = 0 ] || { echo "Fix the items above, then re-run."; exit 1; }
[ -d .venv ] || python3 -m venv .venv
.venv/bin/python -m pip install -q --upgrade pip >/dev/null 2>&1
for pkg in $(cat requirements.txt); do
  .venv/bin/python -m pip install -q "$pkg" >/dev/null 2>&1 && ok "$pkg" || bad "$pkg failed (optional unless your task needs it)"
done
FAIL=0
git pull -q --rebase && ok "repo up to date" || bad "git pull failed"
git push --dry-run -q >/dev/null 2>&1 && ok "push access to GitHub" || bad "no push access: accept the collaborator invite, then run 'gh auth login' (or set up a GitHub token)"
.venv/bin/python problems/p4/lib/congruence.py >/dev/null 2>&1 && ok "problem library self-test" || bad "p4 library self-test failed"
echo
[ "$FAIL" = 0 ] && echo "Ready. Start workers with:  ./start.sh a 2     (direction a, b, c or any; number of workers)" \
                || echo "Almost ready: fix the items marked !! above."
