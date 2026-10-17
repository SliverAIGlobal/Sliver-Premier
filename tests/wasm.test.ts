import { describe, it, expect } from 'vitest';

describe('PRISM 9 WASM Engine Integration', () => {
  it('validates WASM web target artifact exists in public/pkg', async () => {
    const fs = await import('node:fs');
    const path = await import('node:path');
    const wasmJsPath = path.resolve('public/pkg/prism9_wasm.js');
    const wasmBgPath = path.resolve('public/pkg/prism9_wasm_bg.wasm');

    expect(fs.existsSync(wasmJsPath)).toBe(true);
    expect(fs.existsSync(wasmBgPath)).toBe(true);
  });
});
