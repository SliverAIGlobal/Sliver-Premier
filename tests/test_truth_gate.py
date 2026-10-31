"""
Unit Test Suite: Truth Gate T(x), Yield Scaling Vy, ASR Resonance, NRQ, & CareState Triggers
"""

import pytest
import math

def calculate_tx(cs: float, ni: float, ev: float) -> float:
    """Calculates Truth Score T(x) weighted combination."""
    return (0.4 * cs) + (0.35 * ni) + (0.25 * ev)

def calculate_vy(tx: float) -> float:
    """Calculates Veridical Yield Vy scaling from $50 floor up to $5,000 max for T(x) >= 0.995."""
    if tx < 0.9950:
        return 0.0
    return 50.0 + (5000.0 - 50.0) * ((tx - 0.9950) / (1.0000 - 0.9950))

def calculate_asr(tx: float, cs: float, ss: float, og: float) -> float:
    """Calculates Alpha-Sync Resonance Score ASR with Golden Ratio lambda = 1.61803398875."""
    golden_ratio = 1.61803398875
    return (math.pow(tx, 1.5) * cs * ss) + (golden_ratio * og)

def calculate_nrq(vy: float, b: float, r: float, cl: float) -> float:
    """Calculates Negentropic Resonance Quotient NRQ."""
    if cl <= 0.00001:
        cl = 0.00001
    return (vy * b * r) / cl

def check_carestate_trigger(coherence_s: float) -> bool:
    """Returns True if CareState micro-grounding loop should trigger (S < 0.85)."""
    return coherence_s < 0.85

def test_truth_gate_pono_standard():
    assert calculate_tx(0.998, 0.995, 0.997) >= 0.9950
    assert calculate_tx(0.800, 0.800, 0.800) < 0.9950

def test_yield_scaling_vy():
    assert calculate_vy(0.9950) == 50.0
    assert calculate_vy(1.0000) == 5000.0
    assert calculate_vy(0.9900) == 0.0

def test_asr_resonance_golden_ratio():
    asr = calculate_asr(1.0, 1.0, 1.0, 1.0)
    assert abs(asr - (1.0 + 1.61803398875)) < 1e-6

def test_nrq_calculations():
    nrq = calculate_nrq(50.0, 1.0, 1.0, 0.1)
    assert abs(nrq - 500.0) < 1e-6

def test_carestate_trigger_logic():
    assert check_carestate_trigger(0.82) is True
    assert check_carestate_trigger(0.95) is False
