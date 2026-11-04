#!/usr/bin/env python3
"""Builds a monolithic 100% self-contained single-file HTML version."""

with open('styles.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

with open('wasm_base64.txt', 'r', encoding='utf-8') as f:
    wasm_b64 = f.read().strip()

with open('audio-fx.js', 'r', encoding='utf-8') as f:
    audio_js = f.read()

with open('wasm-engine.js', 'r', encoding='utf-8') as f:
    wasm_js = f.read()

with open('pages-data.js', 'r', encoding='utf-8') as f:
    pages_js = f.read()

with open('stickers-data.js', 'r', encoding='utf-8') as f:
    stickers_js = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Replace stylesheet link
target_css = '<link rel="stylesheet" href="styles.css">'
assert target_css in index_html, "Target CSS link not found"
standalone = index_html.replace(target_css, f"<style>\n{css_content}\n</style>")

# Remove manifest link
standalone = standalone.replace('<link rel="manifest" href="manifest.json">', '')

# Replace scripts
scripts_block_start = '<!-- Embedded WASM Payload for Offline file:// Support -->'
scripts_block_end = '<script src="app.js"></script>'

start_idx = standalone.find(scripts_block_start)
end_idx = standalone.find(scripts_block_end) + len(scripts_block_end)

assert start_idx != -1 and end_idx != -1, "Script block not found"

replacement = f"""<!-- Embedded WASM Payload for 100% Offline Single-File Device Download -->
  <script>
    window.WASM_BASE64_PAYLOAD = "{wasm_b64}";
  </script>

  <!-- Inlined Procedural Audio Engine -->
  <script>
{audio_js}
  </script>

  <!-- Inlined WASM Bridge Engine -->
  <script>
{wasm_js}
  </script>

  <!-- Inlined 120 Vector Coloring Pages -->
  <script>
{pages_js}
  </script>

  <!-- Inlined 60 Magic Stickers -->
  <script>
{stickers_js}
  </script>

  <!-- Inlined Canvas Studio Core Engine -->
  <script>
{app_js}
  </script>"""

standalone = standalone[:start_idx] + replacement + standalone[end_idx:]

output_path = 'coloring-studio-ultra-standalone.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(standalone)

print(f"Generated {output_path} successfully ({len(standalone)} bytes).")
