#!/bin/bash
set -e

echo "=========================================================="
echo "SLIVERVERSE Edge Veritas Master Release Build & Test Runner"
echo "=========================================================="

echo "--> [1/4] Executing Python Unittest Suite..."
python3 -m unittest tests/test_truth_gate.py -v

echo "--> [2/4] Generating SHA-256 and MD5 Checksums..."
sha256sum index.html flower_learn_mini_engine.jsx posting_engine.py docs/SPECIFICATION.md tests/test_truth_gate.py *.png > checksums.sha256
md5sum index.html flower_learn_mini_engine.jsx posting_engine.py docs/SPECIFICATION.md tests/test_truth_gate.py *.png > checksums.md5

echo "--> Checksums Generated (SHA-256):"
cat checksums.sha256

echo "--> [3/4] Archiving Master Repository into sliver_edge_veritas_master.zip..."
zip -r sliver_edge_veritas_master.zip . -x "*.git*"

echo "=========================================================="
echo "BUILD SUCCESSFUL! Master release archive generated."
echo "=========================================================="
