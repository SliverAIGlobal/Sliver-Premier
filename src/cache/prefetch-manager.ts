class PrefetchManager {
  private static instance: PrefetchManager;
  private queue: Set<string> = new Set();
  private processing = false;

  private constructor() {}

  static getInstance(): PrefetchManager {
    if (!PrefetchManager.instance) {
      PrefetchManager.instance = new PrefetchManager();
    }
    return PrefetchManager.instance;
  }

  async queueResources(urls: string[]): Promise<void> {
    urls.forEach((url) => this.queue.add(url));
    this.scheduleIdlePrefetch();
  }

  async processQueue(): Promise<void> {
    if (this.processing || typeof caches === 'undefined') return;
    this.processing = true;

    const urls = Array.from(this.queue);
    this.queue.clear();

    for (const url of urls) {
      try {
        const cache = await caches.open('prefetch-cache');
        const response = await fetch(url);
        if (response.ok) await cache.put(url, response);
      } catch (error) {
        console.warn(`[Prefetch] Failed: ${url}`, error);
      }
    }

    this.processing = false;
  }

  scheduleIdlePrefetch(): void {
    if (typeof window === 'undefined') return;
    if ('requestIdleCallback' in window) {
      (window as any).requestIdleCallback(() => this.processQueue());
    } else {
      setTimeout(() => this.processQueue(), 1000);
    }
  }
}

export const PrefetchMgr = PrefetchManager.getInstance();
