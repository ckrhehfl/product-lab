#!/usr/bin/env bash
set -euo pipefail

python3 -m compileall product_lab tests
bash scripts/test.sh
