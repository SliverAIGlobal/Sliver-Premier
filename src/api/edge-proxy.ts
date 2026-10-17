const RATE_LIMIT_CONFIG = {
  MAX_REQUESTS_PER_MINUTE: 60,
  BURST_LIMIT: 10,
};

class EdgeProxy {
  private static instance: EdgeProxy;
  private requestCounts = new Map<string, number>();
  private lastReset = Date.now();

  private constructor() {}

  static getInstance(): EdgeProxy {
    if (!EdgeProxy.instance) {
      EdgeProxy.instance = new EdgeProxy();
    }
    return EdgeProxy.instance;
  }

  async proxy<T>(endpoint: string, options: RequestInit, cacheTTL = 60): Promise<T> {
    if (!this.checkRateLimit(endpoint)) {
      throw new Error('Rate limit exceeded');
    }

    const cacheKey = `${endpoint}:${JSON.stringify(options.body || {})}`;
    const cached = await this.getFromCache<T>(cacheKey, cacheTTL);
    if (cached) return cached;

    try {
      const response = await fetch(endpoint, options);
      if (!response.ok) throw new Error(`API error: ${response.status}`);

      const data = await response.json();
      await this.cacheResponse(cacheKey, data, cacheTTL);
      return data;
    } catch (error) {
      console.warn('Direct API failed, routing to edge proxy:', error);
      return this.proxyThroughEdge<T>(endpoint, options, cacheTTL);
    }
  }

  private async proxyThroughEdge<T>(endpoint: string, options: RequestInit, cacheTTL: number): Promise<T> {
    const response = await fetch('/api/proxy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(options.headers as Record<string, string>) },
      body: JSON.stringify({ targetUrl: endpoint, method: options.method || 'GET', body: options.body }),
    });

    if (!response.ok) throw new Error(`Edge proxy failed: ${response.status}`);
    const data = await response.json();
    await this.cacheResponse(`${endpoint}:${JSON.stringify(options.body || {})}`, data, cacheTTL);
    return data;
  }

  private checkRateLimit(key: string): boolean {
    const now = Date.now();
    if (now - this.lastReset > 60000) {
      this.requestCounts.clear();
      this.lastReset = now;
    }

    const current = this.requestCounts.get(key) || 0;
    if (current >= RATE_LIMIT_CONFIG.MAX_REQUESTS_PER_MINUTE) return false;

    this.requestCounts.set(key, current + 1);
    return true;
  }

  private async getFromCache<T>(key: string, ttl: number): Promise<T | null> {
    if (typeof caches === 'undefined') return null;
    try {
      const cache = await caches.open('edge-api-cache');
      const request = new Request(key);
      const cached = await cache.match(request);
      if (!cached) return null;

      const response = await cached.json();
      if (Date.now() - (response.timestamp || 0) > ttl * 1000) return null;
      return response.data;
    } catch {
      return null;
    }
  }

  private async cacheResponse(key: string, data: any, ttl: number): Promise<void> {
    if (typeof caches === 'undefined') return;
    try {
      const cache = await caches.open('edge-api-cache');
      const response = new Response(JSON.stringify({ data, timestamp: Date.now(), ttl }), {
        headers: { 'Content-Type': 'application/json' },
      });
      await cache.put(key, response);
    } catch (error) {
      console.warn('Cache write failed:', error);
    }
  }
}

export const EdgeProxyClient = EdgeProxy.getInstance();
