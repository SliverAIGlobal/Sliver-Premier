#!/bin/bash
set -euo pipefail

echo "=========================================="
echo " Building Atemporal Reweaver WASM Core    "
echo "=========================================="

mkdir -p dist

cd wasm
cargo build --target wasm32-unknown-unknown --release
cd ..

cp wasm/target/wasm32-unknown-unknown/release/atemporal_reweaver_wasm.wasm dist/engine.wasm

WASM_SIZE=$(wc -c < dist/engine.wasm)
echo "Compiled dist/engine.wasm ($WASM_SIZE bytes)"

# Generate inlined Base64 WASM module for zero-dependency / offline loading
python3 -c '
import base64

with open("dist/engine.wasm", "rb") as f:
    wasm_bytes = f.read()

b64_str = base64.b64encode(wasm_bytes).decode("utf-8")

js_content = f"""// Auto-generated WASM binary loader for Atemporal Reweaver
export const ATEMPORAL_WASM_BASE64 = "{b64_str}";

export async function initWasmEngine() {{
  const binaryString = atob(ATEMPORAL_WASM_BASE64);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {{
    bytes[i] = binaryString.charCodeAt(i);
  }}
  const {{ instance }} = await WebAssembly.instantiate(bytes.buffer);
  return createWasmBridge(instance);
}}

export function createWasmBridge(instance) {{
  const {{
    memory,
    compute_biometrics,
    compute_garden_leaves,
    synthesize_wav,
    verify_truth_metric
  }} = instance.exports;

  return {{
    instance,
    memory,

    computeBiometrics(prevMetrics) {{
      const r1 = Math.random();
      const r2 = Math.random();
      const r3 = Math.random();
      const ptr = 1024; // static scratch region in WASM linear memory
      compute_biometrics(prevMetrics.joy, prevMetrics.stress, prevMetrics.bpm, r1, r2, r3, ptr);
      const f32 = new Float32Array(memory.buffer, ptr, 3);
      return {{
        joy: f32[0],
        stress: f32[1],
        bpm: f32[2]
      }};
    }},

    computeGardenLeaves(level) {{
      const ptr = 2048;
      const count = compute_garden_leaves(level, ptr);
      const f32 = new Float32Array(memory.buffer, ptr, count * 3);
      const leaves = [];
      for (let i = 0; i < count; i++) {{
        leaves.push({{
          x: f32[i * 3],
          y: f32[i * 3 + 1],
          r: f32[i * 3 + 2]
        }});
      }}
      return leaves;
    }},

    pcm16ToWavBlob(pcm16Array, sampleRate) {{
      const pcmLen = pcm16Array.length;
      const pcmByteLen = pcmLen * 2;
      const pcmOffset = 8192;
      const wavOffset = pcmOffset + pcmByteLen + 64;

      // Ensure WASM memory has sufficient pages
      const totalRequired = wavOffset + pcmByteLen + 128;
      if (memory.buffer.byteLength < totalRequired) {{
        const pagesNeeded = Math.ceil((totalRequired - memory.buffer.byteLength) / 65536);
        memory.grow(pagesNeeded);
      }}

      // Copy input PCM16 samples into WASM linear memory
      const wasmI16 = new Int16Array(memory.buffer, pcmOffset, pcmLen);
      wasmI16.set(pcm16Array);

      // Call WASM wave synthesizer
      const totalWavBytes = synthesize_wav(pcmOffset, pcmLen, sampleRate, wavOffset);

      // Slice out the WAV buffer directly from WASM memory
      const wavBytes = new Uint8Array(memory.buffer, wavOffset, totalWavBytes);
      return new Blob([wavBytes.slice()], {{ type: "audio/wav" }});
    }},

    verifyTruthMetric(joy, stress, level) {{
      return verify_truth_metric(joy, stress, level) === 1;
    }}
  }};
}}
"""

with open("dist/wasm_loader.js", "w") as out_f:
    out_f.write(js_content)

print("Generated dist/wasm_loader.js with inlined WASM module")
'

echo "WASM build complete!"
