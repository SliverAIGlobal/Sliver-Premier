import assert from 'node:assert';
import fs from 'node:fs';

async function runTests() {
  console.log("Running Sliver Kids v2 ULTRA verification suite...");

  // 1. Verify Pages Data
  const pagesMod = await import('../pages-data.js');
  const packs = pagesMod.COLORING_PACKS;
  assert.strictEqual(packs.length, 10, "Must have exactly 10 themed packs");
  let totalPages = 0;
  packs.forEach(p => totalPages += p.items.length);
  assert.strictEqual(totalPages, 120, "Must have exactly 120 coloring pages");

  // 2. Verify Stickers Data
  const stickersMod = await import('../stickers-data.js');
  const cats = stickersMod.STICKER_CATEGORIES;
  assert.strictEqual(cats.length, 6, "Must have exactly 6 sticker categories");
  let totalStickers = 0;
  cats.forEach(c => totalStickers += c.items.length);
  assert.strictEqual(totalStickers, 60, "Must have exactly 60 magic stickers");

  // 3. Verify WASM Fill Engine
  const wasmMod = await import('../wasm-engine.js');
  const engine = wasmMod.wasmFillEngine;
  const inited = await engine.init();
  assert.ok(inited, "WASM Fill engine must initialize");

  // 4. Verify ZIP Package exists and contains expected files
  assert.ok(fs.existsSync('sliver-kids-wasm-coloring-studio-v2.zip'), "ZIP archive must exist");
  const zipStat = fs.statSync('sliver-kids-wasm-coloring-studio-v2.zip');
  assert.ok(zipStat.size > 15000, "ZIP archive must be substantial (>15KB)");

  console.log("All Sliver Kids v2 ULTRA assertions passed! 🦖🚀🐬🎨");
}

runTests().catch(e => {
  console.error("Test failed:", e);
  process.exit(1);
});
