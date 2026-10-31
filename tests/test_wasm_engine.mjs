import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runTests() {
  console.log("Running WASM Engine Node.js Test Suite...");

  const wasmLoader = await import('../dist/wasm_loader.js');
  const engine = await wasmLoader.initWasmEngine();
  assert.ok(engine, "WASM Engine instance should be created");

  // 1. Test Biometrics Calculation
  const initialMetrics = { joy: 65, stress: 18, bpm: 68 };
  const nextMetrics = engine.computeBiometrics(initialMetrics);
  console.log("Next Metrics:", nextMetrics);
  assert.ok(nextMetrics.joy >= 15 && nextMetrics.joy <= 100, "Joy within bounds");
  assert.ok(nextMetrics.stress >= 5 && nextMetrics.stress <= 90, "Stress within bounds");
  assert.ok(nextMetrics.bpm >= 60 && nextMetrics.bpm <= 95, "BPM within bounds");

  // 2. Test Lumina Garden Leaf Generation
  for (let level = 0; level <= 5; level++) {
    const leaves = engine.computeGardenLeaves(level);
    const expectedCount = Math.min(60, (level + 1) * 12);
    assert.strictEqual(leaves.length, expectedCount, `Leaf count for level ${level} should be ${expectedCount}`);
    assert.ok(leaves[0].x > 0 && leaves[0].y > 0 && leaves[0].r >= 2, "Leaf coordinates valid");
  }

  // 3. Test WAV synthesis
  const sampleCount = 480;
  const pcm16 = new Int16Array(sampleCount);
  for (let i = 0; i < sampleCount; i++) {
    pcm16[i] = Math.sin(i / 10) * 10000;
  }
  const sampleRate = 24000;
  const wavBlob = engine.pcm16ToWavBlob(pcm16, sampleRate);
  assert.strictEqual(wavBlob.type, 'audio/wav', "Blob type must be audio/wav");
  const expectedSize = 44 + sampleCount * 2;
  assert.strictEqual(wavBlob.size, expectedSize, `Blob size must be ${expectedSize} bytes`);

  // Verify WAV header structure
  const arrayBuffer = await wavBlob.arrayBuffer();
  const uint8 = new Uint8Array(arrayBuffer);
  const headerStr = String.fromCharCode(...uint8.slice(0, 4));
  assert.strictEqual(headerStr, 'RIFF', "WAV file starts with RIFF");
  const waveStr = String.fromCharCode(...uint8.slice(8, 12));
  assert.strictEqual(waveStr, 'WAVE', "WAV container format is WAVE");
  const fmtStr = String.fromCharCode(...uint8.slice(12, 16));
  assert.strictEqual(fmtStr, 'fmt ', "fmt subchunk present");
  const dataStr = String.fromCharCode(...uint8.slice(36, 40));
  assert.strictEqual(dataStr, 'data', "data subchunk present");

  // 4. Test Truth Metric Gate
  assert.strictEqual(engine.verifyTruthMetric(65, 18, 0), true, "Truth metric satisfies threshold");
  assert.strictEqual(engine.verifyTruthMetric(100, 5, 3), true, "High coherence satisfies truth metric");

  console.log("All WASM Engine unit assertions PASSED successfully! 🌿✨");
}

runTests().catch(err => {
  console.error("Test failure:", err);
  process.exit(1);
});
