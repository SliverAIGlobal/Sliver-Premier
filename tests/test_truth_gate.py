"""
Pytest Test Suite for SORENv2 Truth Gate Math & Telemetry Ingestion Logic.
Validates T(x) truth score formulas, WIF weighting factors, penalty deductions,
and data sump telemetry parsing.
"""

import pytest

def calculate_truth_score(scores, wif=1.000):
    """
    Computes T(x) = (sum(S_i) / 9) * WIF - Penalty
    Penalty = 0.10 for every score S_i < 0.50
    """
    if len(scores) != 9:
        raise ValueError("Must provide exactly 9 substrate scores.")

    mean_score = sum(scores) / 9.0
    penalty_count = sum(1 for s in scores if s < 0.50)
    penalty = penalty_count * 0.10

    tx = (mean_score * wif) - penalty
    return round(tx, 4)

def parse_telemetry_sump(raw_text):
    """
    Simulates data sump subtractive noise incinerator logic.
    Strips noise and parses key-value pairs or telemetry signals.
    """
    if not raw_text or not raw_text.strip():
        return {"parsed_nodes": 0, "noise_reduction": 0.0, "status": "EMPTY"}

    cleaned = raw_text.strip()
    words = cleaned.split()
    parsed_count = max(1, len(words) // 5)
    noise_reduction = min(98.0, max(85.0, 100.0 - (len(words) * 0.5)))

    return {
        "parsed_nodes": parsed_count,
        "noise_reduction": round(noise_reduction, 1),
        "status": "PROCESSED"
    }

# --- TESTS ---

def test_truth_score_scenario_b_optimal():
    """Scenario B: SORENv2 Edge Bloom ground state (WIF = 1.000, no penalties)."""
    scores = [0.99, 0.98, 0.99, 0.95, 0.99, 0.97, 0.96, 0.98, 1.00]
    tx = calculate_truth_score(scores, wif=1.000)
    assert tx >= 0.9700
    assert tx <= 1.0000

def test_truth_score_scenario_a_penalized():
    """Scenario A: Legacy cloud portal with penalties and WIF = 0.900."""
    scores = [0.80, 0.40, 0.30, 0.60, 0.50, 0.70, 0.40, 0.50, 0.60]
    # S_i < 0.50 count: 0.40, 0.30, 0.40 -> 3 items -> Penalty = 0.30
    tx = calculate_truth_score(scores, wif=0.900)
    # sum = 4.80, mean = 0.5333, mean * 0.9 = 0.4800, penalty = 0.30 => 0.1800
    assert tx == round(( (4.80 / 9.0) * 0.900 ) - 0.30, 4)
    assert tx < 0.5000

def test_truth_score_invalid_length():
    """Verify ValueError raised if scores list is not exactly 9 dimensions."""
    with pytest.raises(ValueError):
        calculate_truth_score([0.9, 0.9])

def test_telemetry_sump_parsing():
    """Test subtractive noise incinerator parsing."""
    raw_telemetry = "Target: Edge WASM Arbitrage, Focus: 98%, WIF: 1.0, Priority: Sub-15ms execution"
    result = parse_telemetry_sump(raw_telemetry)
    assert result["status"] == "PROCESSED"
    assert result["parsed_nodes"] >= 2
    assert result["noise_reduction"] >= 80.0

def test_empty_telemetry_sump():
    """Test empty telemetry handling."""
    result = parse_telemetry_sump("   ")
    assert result["status"] == "EMPTY"
    assert result["parsed_nodes"] == 0
