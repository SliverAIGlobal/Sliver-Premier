// Sliver Kids WASM Flood Fill Engine
export const WASM_FILL_BASE64 = "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";

class WasmFloodFillEngine {
  constructor() {
    this.ready = false;
    this.instance = null;
    this.memory = null;
  }

  async init() {
    try {
      const binStr = atob(WASM_FILL_BASE64);
      const bytes = new Uint8Array(binStr.length);
      for (let i = 0; i < binStr.length; i++) {
        bytes[i] = binStr.charCodeAt(i);
      }
      const { instance } = await WebAssembly.instantiate(bytes.buffer);
      this.instance = instance;
      this.memory = instance.exports.memory;
      this.ready = true;
      console.log("WASM Flood Fill Core initialized successfully.");
      return true;
    } catch (e) {
      console.warn("WASM instantiation fallback to JS:", e);
      this.ready = false;
      return false;
    }
  }

  floodFill(ctx, startX, startY, fillColorHex, tolerance = 32) {
    const canvas = ctx.canvas;
    const width = canvas.width;
    const height = canvas.height;
    const imgData = ctx.getImageData(0, 0, width, height);
    const pixelCount = width * height;

    // Parse target hex color to 32-bit RGBA little-endian (AABBGGRR in memory)
    const c = fillColorHex.replace("#", "");
    const r = parseInt(c.substring(0, 2), 16);
    const g = parseInt(c.substring(2, 4), 16);
    const b = parseInt(c.substring(4, 6), 16);
    const a = 255;
    const fillColorUint32 = (a << 24) | (b << 16) | (g << 8) | r;

    if (this.ready && this.instance && this.instance.exports.flood_fill) {
      // Ensure memory has enough pages
      // Need 4 bytes * pixelCount for image + 4 bytes * stack (e.g. 262144 items)
      const pixelBytes = pixelCount * 4;
      const stackCapacity = 262144;
      const stackBytes = stackCapacity * 4;
      const totalBytes = pixelBytes + stackBytes + 65536;

      if (this.memory.buffer.byteLength < totalBytes) {
        const pagesNeeded = Math.ceil((totalBytes - this.memory.buffer.byteLength) / 65536);
        this.memory.grow(pagesNeeded);
      }

      const pixelsPtr = 65536;
      const stackPtr = pixelsPtr + pixelBytes;

      // Copy imageData into WASM memory
      const wasmPixels = new Uint32Array(this.memory.buffer, pixelsPtr, pixelCount);
      const canvasPixels = new Uint32Array(imgData.data.buffer);
      wasmPixels.set(canvasPixels);

      const modified = this.instance.exports.flood_fill(
        pixelsPtr,
        width,
        height,
        Math.floor(startX),
        Math.floor(startY),
        fillColorUint32,
        tolerance,
        stackPtr,
        stackCapacity
      );

      if (modified > 0) {
        canvasPixels.set(new Uint32Array(this.memory.buffer, pixelsPtr, pixelCount));
        ctx.putImageData(imgData, 0, 0);
      }
      return modified;
    } else {
      // JS Scanline Flood Fill fallback
      return this.jsFloodFill(ctx, imgData, width, height, Math.floor(startX), Math.floor(startY), r, g, b, a, tolerance);
    }
  }

  jsFloodFill(ctx, imgData, width, height, startX, startY, fillR, fillG, fillB, fillA, tolerance) {
    const data = imgData.data;
    const getPixel = (x, y) => {
      const idx = (y * width + x) * 4;
      return [data[idx], data[idx + 1], data[idx + 2], data[idx + 3]];
    };

    const startPixel = getPixel(startX, startY);
    if (Math.abs(startPixel[0] - fillR) < 2 && Math.abs(startPixel[1] - fillG) < 2 && Math.abs(startPixel[2] - fillB) < 2) {
      return 0;
    }

    const colorMatch = (x, y) => {
      const idx = (y * width + x) * 4;
      const dr = Math.abs(data[idx] - startPixel[0]);
      const dg = Math.abs(data[idx + 1] - startPixel[1]);
      const db = Math.abs(data[idx + 2] - startPixel[2]);
      const da = Math.abs(data[idx + 3] - startPixel[3]);
      return (dr + dg + db + da) <= tolerance * 4;
    };

    const stack = [[startX, startY]];
    let modified = 0;

    while (stack.length) {
      const [x, y] = stack.pop();
      let left = x;
      while (left > 0 && colorMatch(left - 1, y)) left--;
      let right = x;
      while (right + 1 < width && colorMatch(right + 1, y)) right++;

      for (let cur = left; cur <= right; cur++) {
        const idx = (y * width + cur) * 4;
        data[idx] = fillR;
        data[idx + 1] = fillG;
        data[idx + 2] = fillB;
        data[idx + 3] = fillA;
        modified++;
      }

      for (const nextY of [y - 1, y + 1]) {
        if (nextY >= 0 && nextY < height) {
          let cur = left;
          while (cur <= right) {
            if (colorMatch(cur, nextY)) {
              stack.push([cur, nextY]);
              while (cur <= right && colorMatch(cur, nextY)) cur++;
            } else {
              cur++;
            }
          }
        }
      }
    }

    ctx.putImageData(imgData, 0, 0);
    return modified;
  }
}

export const wasmFillEngine = new WasmFloodFillEngine();
if (typeof window !== "undefined") {
  window.WasmFloodFillEngine = wasmFillEngine;
}
