# SLIVERVERSE / EDGE VERITAS ARCHITECTURAL SPECIFICATION

## Executive Overview
The **Edge Veritas Master Architecture** establishes a negentropic operating environment designed to eliminate cognitive friction, guarantee veridical truth at the edge, and enforce user data sovereignty.

## Core Modules & Engine Breakdown

### 1. Zero-Dependency Single-Page App (`index.html`)
The repository root contains `index.html`, a self-contained runtime integrating all 5 core modules with zero external CDN or npm dependencies:
* **Flower Learn (SOREN-V2) Color Studio:** Interactive line art de-coloring, biological pigments (Chlorophyll A/B, Carotenoid, Scute Amber, Luciferin, Guanine Iridophore Cyan), and skill precision tracking.
* **81-Diremption SPECTRA Visualizer:** Canvas engine displaying 81 polar diremption nodes across 9 spectral light waves (432 Hz to 1188 Hz).
* **Truth Formula $T(x)$-Gate Calculator:** Live slider telemetry computing $A_{SR}$, $V_y$, and $\Xi_{NRQ}$ in real time.
* **Data Sump Ingestion Gateway:** Drag-and-drop subtractive noise incinerator for unstructured payloads.
* **Proton CLI Sub-Shell:** WASM-simulated sub-shell delivering zero-knowledge profile hashes (`/hana/p/proton_[zkp_hash]`).

### 2. Audio & Physics Mechanics
* **Solfeggio Acoustic Generator:** Web Audio API synth outputting 528 Hz acoustic resonance alongside a 3.0 Hz sub-bass theta binaural wash.
* **120 FPS WASM Fluid Physics:** Canvas particle engine rendering Navier-Stokes fluid movement without frame drops.
* **Somatic Motor Tremor Tracking:** Real-time 6–12 Hz pointer tremor parsing dynamically updating the Somatic Coherence score ($\Sigma_S$).

### 3. Formulas & Telemetry Standards
* **Pono Veridical Truth Standard:** $T(x) \ge 0.995$
* **Market Utility Scaling:** $V_y \in [\$50, \$5,000]$ per output.
* **Alpha-Sync Resonance ($A_{SR}$):**
  $$A_{SR} = (\Phi_T^{1.5} \cdot \Psi_C \cdot \Sigma_S) + \lambda \cdot \Omega_G \quad (\text{where } \lambda = \phi \approx 1.618)$$
* **CareState Micro-Grounding Loop:** Triggered automatically when $\Sigma_S < 0.85$, shifting UI theme to Chlorophyll Green (`#2E7D32`), expanding touch target hitboxes, and raising fluid viscosity.

## Test & Automation
* `tests/test_truth_gate.py`: Pytest suite validating mathematical formulas, threshold enforcement, and trigger logic.
* `package.sh`: Automated shell execution script for running tests, computing SHA-256 and MD5 checksums, and building `sliver_edge_veritas_master.zip`.
