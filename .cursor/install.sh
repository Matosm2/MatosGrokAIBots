#!/usr/bin/env bash
# Idempotent Cloud Agent install for the trading-bot FastAPI service.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT/trading-bot"

# The default image ships python3.12 but not the stdlib venv/ensurepip module
# that `python3.12 -m venv` needs. Install it only when missing.
if ! python3.12 -c "import ensurepip" >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3.12-venv
fi

# Create the virtualenv if it does not already exist or is broken.
if [ ! -x .venv/bin/python ]; then
  rm -rf .venv
  python3.12 -m venv .venv
fi

./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

echo "trading-bot install complete"
