#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${B2Q_REPRO_VENV:-${ROOT}/.venv-reproduce}"
BUILD_DIR="${B2Q_REPRO_BUILD:-${ROOT}/.repro-build}"

"${PYTHON:-python3}" -m venv "${VENV_DIR}"
VENV_BIN="${VENV_DIR}/bin"
export PATH="${VENV_BIN}:${PATH}"
"${VENV_BIN}/python" -m pip install --upgrade pip setuptools wheel cmake

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
"${VENV_BIN}/python" -m pip download --no-deps --no-build-isolation kenlm==0.3.0 \
  -d "${BUILD_DIR}"
tar -xzf "${BUILD_DIR}"/kenlm-0.3.0.tar.gz -C "${BUILD_DIR}"
MAX_ORDER=10 "${VENV_BIN}/python" -m pip install --no-build-isolation \
  "${BUILD_DIR}/kenlm-0.3.0"

"${VENV_BIN}/python" - <<'PY'
import kenlm
print("kenlm import ok", kenlm)
PY

echo "reproduction env ready: ${VENV_DIR}"
