# COLORWORKS MASTERS STUDIO — Consolidated Fine-Art Studio

A production-ready, offline-first fine-art coloring studio web application. Users convert photos to line art locally via Sobel edge detection, generate artwork from text prompts via progressive Edge AI, color with multiple media tools, watch animated ink-bleed journeys of 10 masterpieces, and export sellable animated wallpaper videos after passing a ≥85% precision gate.

## Key Features
- **100% Offline-First**: All image processing (Sobel de-colorer, ink-bleed flood fill, precision scoring) runs purely client-side in the browser. Zero image data leaves the device.
- **Two Consolidated Modes**:
  1. **Coloring Studio**: Photo upload, Sobel de-colorer sliders (Edge Sensitivity 20–160, Line Thickness 1–4×), progressive Edge AI prompt generation, drawing tools (brush, marker, pencil, spray, ink-bleed fill, emoji stamp, eraser) with somatic tremor smoothing (exponential low-pass filter α = 0.25), 12-color palette + 8 biochemical pigment swatches, 3 paper textures (Warm White, Vintage Cream, Midnight Ink), undo stack, and zoom/pan.
  2. **Journey Masterpieces**: 10 vector masterpieces (Blooming Skull, Ribcage Garden, Digital Realm, Shadow Wraith, Gothic Dragon, Spirit Stag, VR Goddess, Haunted Forest, Phoenix Skull, Cyber Serpent). Staggered ink-bleed reveal (3.0–6.0s duration, 0.5–3.0× bleed diffusion, pressure-swell lines, live ink palette switching).
- **Kaleidoscope Finale**: Finished artwork mirrors into 6/8/12 user-selectable facets with a vignette eyepiece overlay and auto-rotation (2–4 RPM) with drag spin.
- **Exports**: MediaRecorder MIME negotiation (MP4 H.264 preferred, WebM VP9 fallback):
  - Ken Burns animated wallpaper (5s, user soundtrack baked in).
  - Stroke time-lapse (5s, replay log safe).
  - Journey + kaleidoscope finale composite.
  - 2× high-res PNG for physical printing.
- **Precision Gate**: Score = coverage × (0.45 + 0.55 × accuracy). Reaching ≥85% unlocks exports and local marketplace listing JSON payload.
- **Edge AI Ladder**:
  - Tier 1: In-browser WebGPU LLM (Gemma-2-2B-it via `@mlc-ai/web-llm`) parsing prompt to style grammar JSON.
  - Tier 2A: Local companion (Ollama / FLUX.1) via silent-failing localhost probes.
  - Tier 2B: Seed-pinned procedural symmetric generator (mulberry32 PRNG).
- **Audio & Ambience**: User-supplied songs only (never bundled). "Focus Ambience" dual-oscillator (528 Hz sine + 3.0 Hz sub-bass theta difference).
- **i18n & Accessibility**: EN / ES / FR language switcher, SpeechSynthesis Read Aloud, somatic tremor filter, aria-labels, and full keyboard navigation.
- **Creator Publishing (Gumroad)**: Opt-in publishing flow with CC license selection, creator attestation, and mock testing mode via `?publishMock=1`.

## Testing
Run the automated test suite with Playwright:
```bash
python3 -m pytest tests/test_colorworld_playwright.py -v
```
To run the diagnostics harness in-browser, open `index.html` and click the stethoscope icon or invoke `window.runDiagnostics()` in the console.
