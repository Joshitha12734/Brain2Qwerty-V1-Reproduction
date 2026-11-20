#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
WORKERS="${B2Q_REPRO_WORKERS:-4}"
OUT_DIR="${B2Q_REPRO_OUT:-${ROOT}/out/reproduce_verified_main_gate}"

rm -rf "${OUT_DIR}"
mkdir -p "${OUT_DIR}"

"${PYTHON_BIN}" "${ROOT}/scripts/ensemble_decode_grid.py" \
  --input gate005="${ROOT}/inputs/verified-main-gate/gate005_full_test.csv" \
  --input late="${ROOT}/inputs/verified-main-gate/late_soup_test.csv" \
  --input seed101="${ROOT}/inputs/verified-main-gate/seed101_e10_test.csv" \
  --input seed202="${ROOT}/inputs/verified-main-gate/seed202_e26_test.csv" \
  --input l2e6="${ROOT}/inputs/verified-main-gate/l2reg_seed404_e6_test.csv" \
  --recipe gate005_late_s101_s202_l2e6_675_10_10_10_025:gate005=0.675,late=0.10,seed101=0.10,seed202=0.10,l2e6=0.025 \
  --lm "${ROOT}/lm/eswiki_9gram_chars.rescue.bin" \
  --out-dir "${OUT_DIR}" \
  --decode-top-raw 1 \
  --beam-sizes 200 \
  --max-labels 10 \
  --lm-weights 2.05 \
  --space-biases 0.0 \
  --repeat-penalties=-0.05 \
  --fold-mod 0 \
  --workers "${WORKERS}"

"${PYTHON_BIN}" - "${OUT_DIR}/decode_grid_summary.csv" <<'PY'
import csv
import math
import sys

path = sys.argv[1]
expected = {
    "recipe": "gate005_late_s101_s202_l2e6_675_10_10_10_025",
    "raw_CER": 0.3433872549613909,
    "CER_LM": 0.29096357106460957,
    "WER_LM": 0.560563820633256,
    "n_rows": 521,
    "n_subjects": 19,
}

with open(path, newline="") as handle:
    rows = list(csv.DictReader(handle))
if len(rows) != 1:
    raise SystemExit(f"expected exactly one decode row, got {len(rows)}")
row = rows[0]
if row["recipe"] != expected["recipe"]:
    raise SystemExit(f"recipe mismatch: {row['recipe']}")
for key in ("raw_CER", "CER_LM", "WER_LM"):
    actual = float(row[key])
    if not math.isclose(actual, expected[key], rel_tol=0.0, abs_tol=1e-15):
        raise SystemExit(f"{key} mismatch: {actual} != {expected[key]}")
for key in ("n_rows", "n_subjects"):
    actual = int(row[key])
    if actual != expected[key]:
        raise SystemExit(f"{key} mismatch: {actual} != {expected[key]}")
print("verified main-gate reproduction ok")
PY
