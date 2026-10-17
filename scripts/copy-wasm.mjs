import fs from 'node:fs';
import path from 'node:path';

const srcPkg = path.resolve('src/wasm/pkg');
const destPublic = path.resolve('public/pkg');

if (fs.existsSync(srcPkg)) {
  fs.mkdirSync(destPublic, { recursive: true });
  fs.cpSync(srcPkg, destPublic, { recursive: true });
  console.log('[copy-wasm] WASM pkg successfully copied to public/pkg');
} else {
  console.warn('[copy-wasm] src/wasm/pkg directory does not exist yet. Run wasm-pack build first.');
}
