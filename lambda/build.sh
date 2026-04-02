#!/usr/bin/env bash
#
# Build a Lambda deployment zip for shipfamradio.
# Usage: bash build.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
ZIP_FILE="${SCRIPT_DIR}/shipfamradio-lambda.zip"

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# Install dependencies into build dir
pip install \
    --target "${BUILD_DIR}" \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: \
    -r "${SCRIPT_DIR}/requirements.txt" \
    2>&1 | tail -1

# If --only-binary fails for pure-python packages, fall back without platform constraint
pip install \
    --target "${BUILD_DIR}" \
    --upgrade \
    -r "${SCRIPT_DIR}/requirements.txt" \
    2>&1 | tail -1

# Copy application code
cp "${SCRIPT_DIR}/lambda_handler.py" "${BUILD_DIR}/"
cp -r "${SCRIPT_DIR}/app" "${BUILD_DIR}/app"
mkdir -p "${BUILD_DIR}/db"
cp "${SCRIPT_DIR}/db/app.db" "${BUILD_DIR}/db/"

# Clean up unnecessary files to reduce zip size
find "${BUILD_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "${BUILD_DIR}" -name "*.pyc" -delete 2>/dev/null || true
find "${BUILD_DIR}" -name "*.dist-info" -type d -exec rm -rf {} + 2>/dev/null || true

# Create zip
cd "${BUILD_DIR}"
rm -f "${ZIP_FILE}"
zip -r9 "${ZIP_FILE}" . -x "*.pyc" > /dev/null

ZIP_SIZE=$(du -sh "${ZIP_FILE}" | cut -f1)
echo "Built ${ZIP_FILE} (${ZIP_SIZE})"
