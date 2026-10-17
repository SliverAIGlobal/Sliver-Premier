export interface WasmLoadResult {
  ready: boolean;
  engine: any | null;
  fallbackMode: boolean;
  loadTimeMs: number;
}

class WasmLoader {
  private static instance: WasmLoader;
  private loaded = false;
  private engine: any = null;

  private constructor() {}

  static getInstance(): WasmLoader {
    if (!WasmLoader.instance) {
      WasmLoader.instance = new WasmLoader();
    }
    return WasmLoader.instance;
  }

  async load(): Promise<WasmLoadResult> {
    const startTime = performance.now();

    try {
      if (!this.supportsWasm()) {
        return this.fallbackResult(startTime, 'WASM not supported');
      }

      if (this.loaded && this.engine) {
        return {
          ready: true,
          engine: this.engine,
          fallbackMode: false,
          loadTimeMs: 0,
        };
      }

      const wasmPath = './wasm/pkg/prism9_wasm.js';
      const wasmModule: any = await import(/* @vite-ignore */ wasmPath);

      if (typeof wasmModule.default === 'function') {
        await wasmModule.default();
      }

      this.engine = new wasmModule.CognitiveEngine();
      this.loaded = true;

      const loadTime = performance.now() - startTime;
      console.log(`[WASM] Engine initialized in ${loadTime.toFixed(2)}ms`);

      return {
        ready: true,
        engine: this.engine,
        fallbackMode: false,
        loadTimeMs: loadTime,
      };
    } catch (error: any) {
      console.warn('[WASM] Load failed, utilizing JS fallback:', error?.message || error);
      return this.fallbackResult(startTime, error?.message || String(error));
    }
  }

  private supportsWasm(): boolean {
    return typeof WebAssembly === 'object' && typeof WebAssembly.instantiate === 'function';
  }

  private fallbackResult(loadStart: number, _reason: string): WasmLoadResult {
    return {
      ready: false,
      engine: null,
      fallbackMode: true,
      loadTimeMs: performance.now() - loadStart,
    };
  }
}

export const WasmManager = WasmLoader.getInstance();
