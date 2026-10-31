#!/usr/bin/env bash
# SORENv2 SLIVER VERITAS Automated Packaging & Checksum Script

set -e

echo "==========================================================="
echo " RUNNING AUTOMATED TEST SUITE"
echo "==========================================================="
python3 -m pytest tests/ -v

echo ""
echo "==========================================================="
echo " COMPILING PRODUCTION ARCHIVES & MANIFESTS"
echo "==========================================================="

mkdir -p release/

# Create zip archives
zip -q -r release/sliver_edge_veritas_master.zip index.html docs/ tests/ flower_learn.py adaptive_ingestion_engine.py init-learning-engine package.sh
zip -q -r release/flower_learn_soren_v2_production.zip index.html docs/ flower_learn.py

# Generate Root Checksums
sha256sum index.html docs/* tests/*.py flower_learn.py adaptive_ingestion_engine.py > checksums.sha256
md5sum index.html docs/* tests/*.py flower_learn.py adaptive_ingestion_engine.py > checksums.md5

# Copy checksums into release directory
cp checksums.sha256 release/
cp checksums.md5 release/

echo ""
echo "==========================================================="
echo " PACKAGING COMPLETE. ARCHIVES GENERATED IN release/"
echo "==========================================================="
ls -la release/
