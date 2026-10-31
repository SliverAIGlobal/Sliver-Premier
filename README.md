# Sliver-Premier • Atemporal Reweaver WASM Substrate (Node SIPES-HI-808)

The Atemporal Reweaver is a quantum timeline harmonization web application powered by a WebAssembly (WASM) core compiled from Rust (`wasm32-unknown-unknown`).

## Architecture

- **WASM Core (`wasm/src/lib.rs`)**:
  - `compute_biometrics`: High-performance PeriSensor biometric drift & entropic damping.
  - `compute_garden_leaves`: Geometry and coordinate generation for the Lumina Garden SVG.
  - `synthesize_wav`: Low-level zero-allocation 16-bit PCM to RIFF/WAVE container synthesis.
  - `verify_truth_metric`: OMNI AI Truth Gate $T(x) \ge 0.995$ validation.
- **Frontend SPA (`index.html`)**:
  - React 18 single-page application with Tailwind CSS.
  - Zero external bundler requirement; inlined Base64 WASM bridge (`dist/wasm_loader.js`).
  - Online Google Gemini 2.5 Flash / Gemini TTS support with graceful offline simulation fallback.
  - Web Speech API integration for speech-to-text input.
  - TokeX economy, feature unlocking, and downloadable session logs.

## Building the WASM Module

```bash
./build.sh
```

## Running the Application

Serve the root directory using any static web server:

```bash
python3 -m http.server 3000
# or
npx serve -l 3000
```
