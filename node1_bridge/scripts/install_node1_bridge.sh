#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-/opt/ghostseal/node1_bridge}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo mkdir -p "$ROOT"
sudo rsync -a --delete "$SRC_DIR/" "$ROOT/"
sudo chown -R "${USER}:${USER}" "$ROOT"

python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install --upgrade pip
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements.txt"

echo "Installed Ghost Seal Node 1 bridge at $ROOT"
echo "Run: $ROOT/.venv/bin/python $ROOT/ghostseal_bridge.py --port /dev/ttyACM0 status"
