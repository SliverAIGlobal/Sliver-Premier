// High-Speed WASM Memory & Decolorizer Bridge for Version 2 ULTRA
// Safe, offline-first client-side image line-art converter

class WasmDecolorizerEngine {
    constructor() {
        this.wasmInstance = null;
        this.isReady = false;
        this.initPromise = null;
    }

    async init() {
        if (this.initPromise) return this.initPromise;

        this.initPromise = (async () => {
            try {
                let bytes;
                // Try fetching co-located binary (if running on http / https / server)
                if (window.location.protocol.startsWith('http')) {
                    try {
                        const response = await fetch('static/wasm/wasm_decolorizer.wasm');
                        if (response.ok) {
                            bytes = await response.arrayBuffer();
                        }
                    } catch (e) {
                        console.warn('Direct fetch failed, falling back to base64 embedded binary', e);
                    }
                }

                // Fallback to embedded Base64 binary (guarantees file:// offline execution)
                if (!bytes && window.WASM_BASE64_PAYLOAD) {
                    const binaryString = atob(window.WASM_BASE64_PAYLOAD);
                    const len = binaryString.length;
                    const uint8 = new Uint8Array(len);
                    for (let i = 0; i < len; i++) {
                        uint8[i] = binaryString.charCodeAt(i);
                    }
                    bytes = uint8.buffer;
                }

                if (!bytes) {
                    throw new Error('No WASM binary source available');
                }

                const wasmModule = await WebAssembly.instantiate(bytes, {});
                this.wasmInstance = wasmModule.instance;
                this.isReady = true;
                console.log('⚡ WASM Decolorizer Engine successfully initialized in linear memory');
            } catch (err) {
                console.warn('WASM initialization note, JS fallback enabled:', err);
                this.isReady = false;
            }
        })();

        return this.initPromise;
    }

    // Process raw RGBA ImageData and return new converted line-art ImageData
    async processImage(imageData, options = {}) {
        await this.init();

        const {
            threshold = 40,
            thickness = 0,
            contrast = 130,
            invertMode = 0
        } = options;

        const width = imageData.width;
        const height = imageData.height;
        const numBytes = width * height * 4;

        if (this.isReady && this.wasmInstance) {
            const { alloc_buffer, free_buffer, decolorize, memory } = this.wasmInstance.exports;

            const inputPtr = alloc_buffer(numBytes);
            const outputPtr = alloc_buffer(numBytes);

            // Copy input image bytes into WASM linear memory
            const inputMem = new Uint8Array(memory.buffer, inputPtr, numBytes);
            inputMem.set(imageData.data);

            // Run high-throughput Sobel edge detection & morphological filter
            decolorize(inputPtr, outputPtr, width, height, threshold, thickness, contrast, invertMode);

            // Extract converted output bytes
            const outputMem = new Uint8Array(memory.buffer, outputPtr, numBytes);
            const resultData = new Uint8ClampedArray(outputMem);

            // Clean up memory
            free_buffer(inputPtr, numBytes);
            free_buffer(outputPtr, numBytes);

            return new ImageData(resultData, width, height);
        } else {
            // Pure JS Fallback (ensures 100% functionality regardless of browser environment)
            return this.jsDecolorizeFallback(imageData, options);
        }
    }

    jsDecolorizeFallback(imageData, options = {}) {
        const {
            threshold = 40,
            thickness = 0,
            contrast = 130,
            invertMode = 0
        } = options;

        const w = imageData.width;
        const h = imageData.height;
        const total = w * h;
        const src = imageData.data;
        const gray = new Uint8Array(total);

        const contrastFactor = contrast || 100;

        // Grayscale + Contrast
        for (let i = 0; i < total; i++) {
            const r = src[i * 4];
            const g = src[i * 4 + 1];
            const b = src[i * 4 + 2];
            const lum = (r * 299 + g * 587 + b * 114) / 1000;
            let adj = Math.floor(((lum - 128) * contrastFactor) / 100 + 128);
            if (adj < 0) adj = 0;
            if (adj > 255) adj = 255;
            gray[i] = adj;
        }

        // Gaussian Blur
        const blurredH = new Uint8Array(total);
        for (let y = 0; y < h; y++) {
            const row = y * w;
            for (let x = 0; x < w; x++) {
                const l = x > 0 ? gray[row + x - 1] : gray[row + x];
                const c = gray[row + x];
                const r = x + 1 < w ? gray[row + x + 1] : gray[row + x];
                blurredH[row + x] = Math.floor((l + c * 2 + r + 2) / 4);
            }
        }

        const blurred = new Uint8Array(total);
        for (let y = 0; y < h; y++) {
            const uRow = y > 0 ? (y - 1) * w : y * w;
            const cRow = y * w;
            const dRow = y + 1 < h ? (y + 1) * w : y * w;
            for (let x = 0; x < w; x++) {
                const u = blurredH[uRow + x];
                const c = blurredH[cRow + x];
                const d = blurredH[dRow + x];
                blurred[cRow + x] = Math.floor((u + c * 2 + d + 2) / 4);
            }
        }

        // Sobel Edge Detection
        const edges = new Uint8Array(total);
        for (let y = 1; y < h - 1; y++) {
            const yPrev = (y - 1) * w;
            const yCurr = y * w;
            const yNext = (y + 1) * w;
            for (let x = 1; x < w - 1; x++) {
                const p00 = blurred[yPrev + x - 1];
                const p02 = blurred[yPrev + x + 1];
                const p10 = blurred[yCurr + x - 1];
                const p12 = blurred[yCurr + x + 1];
                const p20 = blurred[yNext + x - 1];
                const p22 = blurred[yNext + x + 1];

                const p01 = blurred[yPrev + x];
                const p21 = blurred[yNext + x];

                const gx = (p02 + 2 * p12 + p22) - (p00 + 2 * p10 + p20);
                const gy = (p20 + 2 * p21 + p22) - (p00 + 2 * p01 + p02);
                const mag = Math.abs(gx) + Math.abs(gy);

                edges[yCurr + x] = mag >= threshold ? 255 : 0;
            }
        }

        // Output RGBA
        const outData = new Uint8ClampedArray(total * 4);
        const lineVal = invertMode === 0 ? 0 : 255;
        const bgVal = invertMode === 0 ? 255 : 0;

        for (let i = 0; i < total; i++) {
            const isEdge = edges[i] === 255;
            const color = isEdge ? lineVal : bgVal;
            const idx = i * 4;
            outData[idx] = color;
            outData[idx + 1] = color;
            outData[idx + 2] = color;
            outData[idx + 3] = 255;
        }

        return new ImageData(outData, w, h);
    }
}

window.wasmEngine = new WasmDecolorizerEngine();
