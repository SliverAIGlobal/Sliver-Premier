#!/usr/bin/env bash
# SLIVER Consortium Master Package Automation
set -euo pipefail

PACKAGE_NAME="sliver_edge_veritas_master"
BUILD_DIR="./build_${PACKAGE_NAME}"

echo "[+] Running Test Suites..."
pytest tests/ -v

echo "[+] Initializing Clean Build Directory..."
rm -rf "${BUILD_DIR}" "${PACKAGE_NAME}.zip"
mkdir -p "${BUILD_DIR}/docs" "${BUILD_DIR}/scripts" "${BUILD_DIR}/tests"

echo "[+] Staging Master Assets..."
cp index.html "${BUILD_DIR}/index.html"
cp docs/sliver_veritas_mastery_guide.md "${BUILD_DIR}/docs/" 2>/dev/null || true
cp docs/9sm_audit_results.md "${BUILD_DIR}/docs/" 2>/dev/null || true
cp tests/test_truth_gate.py "${BUILD_DIR}/tests/" 2>/dev/null || true
cp "$0" "${BUILD_DIR}/scripts/package.sh"

echo "[+] Generating SHA-256 & MD5 Checksums Inside Build Directory..."
cd "${BUILD_DIR}"
find . -type f ! -name "*.sha256" ! -name "*.md5" -exec sha256sum {} + > checksums.sha256
find . -type f ! -name "*.sha256" ! -name "*.md5" -exec md5sum {} + > checksums.md5

echo "[+] Archiving Package to Repository Root..."
zip -r "../${PACKAGE_NAME}.zip" .
cd ..

echo "[+] Generating Repository Root Manifests..."
sha256sum "${PACKAGE_NAME}.zip" > checksums.sha256
md5sum "${PACKAGE_NAME}.zip" > checksums.md5

echo "[✓] Build Complete: ${PACKAGE_NAME}.zip (T(x) >= 1.000 Verification Ready)"
