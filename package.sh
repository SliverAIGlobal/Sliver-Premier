#!/usr/bin/env bash
set -euo pipefail

echo "=========================================="
echo "Sliver Kids WASM Coloring Studio v2 ULTRA"
echo "Automated Packaging & Release Verification"
echo "=========================================="

DIST_NAME="sliver-kids-wasm-coloring-studio-v2"
RELEASE_DIR="release"
STAGE_DIR="/tmp/${DIST_NAME}"

# 1. Clean previous build staging
rm -rf "${RELEASE_DIR}" "${STAGE_DIR}"
mkdir -p "${RELEASE_DIR}" "${STAGE_DIR}"

# 2. Build WASM Core Engine
echo "🦀 [1/5] Compiling Rust WASM Core Engine..."
cargo build --release --target wasm32-unknown-unknown --manifest-path wasm_decolorizer/Cargo.toml
cargo test --manifest-path wasm_decolorizer/Cargo.toml

mkdir -p static/wasm
cp wasm_decolorizer/target/wasm32-unknown-unknown/release/wasm_decolorizer.wasm static/wasm/wasm_decolorizer.wasm

# 3. Regenerate embedded Base64 payload & build index.html
echo "📦 [2/5] Updating Embedded WASM Base64 & Compiling Data..."
python3 -c "
import base64
with open('static/wasm/wasm_decolorizer.wasm', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
with open('wasm_base64.txt', 'w') as f:
    f.write(b64)
"
python3 scripts/generate_pages.py
python3 scripts/generate_stickers.py
python3 scripts/build_index.py

# 4. Stage Assets into Release Directory Structure
echo "🚚 [3/5] Staging distribution assets..."
cp index.html "${STAGE_DIR}/"
cp styles.css "${STAGE_DIR}/"
cp app.js "${STAGE_DIR}/"
cp audio-fx.js "${STAGE_DIR}/"
cp wasm-engine.js "${STAGE_DIR}/"
cp pages-data.js "${STAGE_DIR}/"
cp stickers-data.js "${STAGE_DIR}/"
cp sw.js "${STAGE_DIR}/"
cp manifest.json "${STAGE_DIR}/"
cp MARKETING_COPY.md "${STAGE_DIR}/"

mkdir -p "${STAGE_DIR}/static/wasm"
cp static/wasm/wasm_decolorizer.wasm "${STAGE_DIR}/static/wasm/"

# 5. Create ZIP Package and Compute Manifests
echo "🗜️  [4/5] Compiling Release ZIP Archive..."
cd /tmp
zip -r "${OLDPWD}/${RELEASE_DIR}/${DIST_NAME}.zip" "${DIST_NAME}"
cd "${OLDPWD}"

echo "🔒 [5/5] Generating Checksum Manifests..."
sha256sum "${RELEASE_DIR}/${DIST_NAME}.zip" > "${RELEASE_DIR}/SHA256SUMS.txt"
md5sum "${RELEASE_DIR}/${DIST_NAME}.zip" > "${RELEASE_DIR}/MD5SUMS.txt"

# Display summary
echo "=========================================="
echo "🎉 Build & Packaging Successful!"
echo "Package: ${RELEASE_DIR}/${DIST_NAME}.zip"
ls -lh "${RELEASE_DIR}/${DIST_NAME}.zip"
cat "${RELEASE_DIR}/SHA256SUMS.txt"
echo "=========================================="
