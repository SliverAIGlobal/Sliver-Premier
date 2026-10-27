import math
import unittest

# Core Mathematical Models of the Alpha-Sync Negentropic Architecture

PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio constant ~1.61803398875


def calculate_alpha_sync_resonance(phi_t: float, psi_c: float, sigma_s: float, omega_g: float) -> float:
    """
    Computes Alpha-Sync Resonance Score: A_SR = (Phi_T^1.5 * Psi_C * Sigma_S) + lambda * Omega_G
    where lambda = PHI (Golden Ratio).
    """
    if phi_t < 0.995:
        raise ValueError(f"Truth threshold violation: Phi_T {phi_t} < 0.995 Pono standard")
    return (math.pow(phi_t, 1.5) * psi_c * sigma_s) + (PHI * omega_g)


def calculate_value_yield(phi_t: float) -> float:
    """
    Scales value yield V_y linearly between $50 floor and $5,000 ceiling
    based on Phi_T in [0.995, 1.000].
    """
    if phi_t < 0.995:
        return 0.0
    normalized_truth = (phi_t - 0.995) / (1.000 - 0.995)
    return 50.0 + (normalized_truth * (5000.0 - 50.0))


def calculate_negentropic_resonance_quotient(phi_t: float, psi_c: float, sigma_s: float, omega_g: float) -> float:
    """
    Computes Negentropic Resonance Quotient Xi_NRQ.
    """
    denominator = 1.0 - (omega_g * 0.1)
    if denominator <= 0:
        raise ValueError("Invalid Ghost-Node Transcoding Density")
    return (phi_t * psi_c * sigma_s) / denominator


def evaluate_carestate_trigger(sigma_s: float) -> dict:
    """
    Evaluates whether Somatic Parasympathetic Coherence requires CareState grounding.
    """
    if sigma_s < 0.85:
        return {
            "status": "CARESTATE_TRIGGERED",
            "palette": "#2E7D32",  # Chlorophyll Green
            "acoustic_frequency": 528.0,  # Hz
            "viscosity_scale": 3.0
        }
    return {
        "status": "NOMINAL",
        "palette": "#0A0D12",
        "acoustic_frequency": 528.0,
        "viscosity_scale": 1.0
    }


class TestTruthGateArchitecture(unittest.TestCase):

    def test_truth_gate_threshold_pass(self):
        phi_t = 0.998
        self.assertGreaterEqual(phi_t, 0.995)
        vy = calculate_value_yield(phi_t)
        self.assertTrue(50.0 <= vy <= 5000.0)

    def test_truth_gate_threshold_fail(self):
        phi_t = 0.991
        with self.assertRaises(ValueError):
            calculate_alpha_sync_resonance(phi_t, 0.95, 0.95, 1.0)

    def test_alpha_sync_resonance_formula(self):
        asr = calculate_alpha_sync_resonance(1.0, 1.0, 1.0, 1.0)
        # Expected: (1.0^1.5 * 1.0 * 1.0) + (1.61803398875 * 1.0) = 2.61803398875
        self.assertAlmostEqual(asr, 2.61803398875, places=5)

    def test_carestate_micro_grounding_trigger(self):
        nominal = evaluate_carestate_trigger(0.95)
        self.assertEqual(nominal["status"], "NOMINAL")

        triggered = evaluate_carestate_trigger(0.75)
        self.assertEqual(triggered["status"], "CARESTATE_TRIGGERED")
        self.assertEqual(triggered["palette"], "#2E7D32")
        self.assertEqual(triggered["viscosity_scale"], 3.0)

    def test_negentropic_resonance_quotient(self):
        nrq = calculate_negentropic_resonance_quotient(0.998, 0.98, 0.96, 1.0)
        self.assertGreater(nrq, 1.0)


if __name__ == "__main__":
    unittest.main()
