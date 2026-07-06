#!/usr/bin/env bash
set -e

# change to script directory
cd "$(dirname "$0")"

# coincurve requires Python <=3.13
# install via: sudo apt install python3.13  or  brew install python@3.13
PYTHON=python3.13

if ! command -v "$PYTHON" &>/dev/null; then
    echo "ERROR: $PYTHON not found. Install it and retry." >&2
    exit 1
fi

# create virtual environment if not already present
if [ ! -d ".venv" ]; then
    "$PYTHON" -m venv .venv
fi

# activate virtual environment
# shellcheck disable=SC1091
source .venv/bin/activate

# install/update dependencies
pip install -r requirements.txt

python brute.py
