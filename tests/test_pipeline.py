"""
Unit Test Suite: End-to-End Pipeline & Ingestion Tests
"""

import os
import sys
import pytest
from pathlib import Path

# Add root directory to python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adaptive_ingestion_engine import AdaptiveIngestionEngine
from flower_learn import generate_package, parse_args

def test_adaptive_ingestion_engine_stages():
    engine = AdaptiveIngestionEngine()
    raw = "Capillary Ink Diffusion & Sector Lock Architecture under 510nm green spectrum."
    result = engine.process(raw, {"target_type": "individual", "persona": "learner"})

    assert result["status"] == "PONO VERIFIED"
    assert result["truth_score_tx"] >= 0.9950
    assert "0x" in result["ledger_hash"]
    assert result["package_data"]["target_type"] == "individual"

def test_flower_learn_cli_generator(tmp_path):
    class DummyArgs:
        name = "Flower Learn"
        role = "Supreme Architect"
        ratio = "40/60"
        gate = 0.9950
        framework = "ELIP"
        modules = "Guidebook,Worksheet,Mandala,Rubric"
        ledger = "SLIVER-GRAND_LEDGER"
        output_dir = str(tmp_path)
        topic = "Capillary Diffusion Test"

    generate_package(DummyArgs())

    json_file = tmp_path / "flower-learn-package.json"
    md_file = tmp_path / "flower-learn-package.md"

    assert json_file.exists()
    assert md_file.exists()

    md_text = md_file.read_text(encoding="utf-8")
    assert "Capillary Diffusion Test" in md_text
    assert "T(x) >= 0.995" in md_text
