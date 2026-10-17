export interface CacheEntry<T = any> {
  id?: number;
  key: string;
  data: T;
  hash: string;
  timestamp: number;
  accessCount: number;
  lastAccessed: number;
  size: number;
  ttl: number;
}

class IndexedDBStore {
  private static instance: IndexedDBStore;
  private db: IDBDatabase | null = null;
  private readonly config = {
    dbName: 'PRISM9-EdgeStore',
    version: 1,
  };

  private constructor() {}

  static getInstance(): IndexedDBStore {
    if (!IndexedDBStore.instance) {
      IndexedDBStore.instance = new IndexedDBStore();
    }
    return IndexedDBStore.instance;
  }

  async init(): Promise<void> {
    if (this.db) return;
    if (typeof indexedDB === 'undefined') return;

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.config.dbName, this.config.version);

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains('computations')) {
          const store = db.createObjectStore('computations', { keyPath: 'key' });
          store.createIndex('lastAccessed', 'lastAccessed', { unique: false });
        }
      };

      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onerror = () => reject(new Error('IndexedDB initialization failed'));
    });
  }

  async set<T>(entry: CacheEntry<T>): Promise<void> {
    if (typeof indexedDB === 'undefined') return;
    if (!this.db) await this.init();
    if (!this.db) return;

    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction(['computations'], 'readwrite');
      const store = tx.objectStore('computations');
      const record = {
        ...entry,
        accessCount: entry.accessCount || 0,
        lastAccessed: Date.now(),
        size: estimateSize(entry.data),
      };
      const req = store.put(record);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }

  async get<T>(key: string): Promise<T | null> {
    if (typeof indexedDB === 'undefined') return null;
    if (!this.db) await this.init();
    if (!this.db) return null;

    return new Promise((resolve) => {
      const tx = this.db!.transaction(['computations'], 'readonly');
      const store = tx.objectStore('computations');
      const request = store.get(key);

      request.onsuccess = () => {
        const entry = request.result as CacheEntry<T>;
        if (!entry || Date.now() - entry.timestamp > entry.ttl * 1000) {
          resolve(null);
          return;
        }
        entry.accessCount++;
        entry.lastAccessed = Date.now();
        this.set(entry).catch(() => {});
        resolve(entry.data);
      };

      request.onerror = () => resolve(null);
    });
  }

  async delete(key: string): Promise<void> {
    if (typeof indexedDB === 'undefined') return;
    if (!this.db) await this.init();
    if (!this.db) return;

    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction(['computations'], 'readwrite');
      const req = tx.objectStore('computations').delete(key);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }

  async getStats(): Promise<{ size: number; entries: number }> {
    if (typeof indexedDB === 'undefined' || !this.db) {
      return { size: 0, entries: 0 };
    }

    return new Promise((resolve) => {
      const tx = this.db!.transaction(['computations'], 'readonly');
      const request = tx.objectStore('computations').getAll();
      request.onsuccess = () => {
        const entries = (request.result || []) as CacheEntry[];
        resolve({
          size: entries.reduce((acc, e) => acc + (e.size || 0), 0),
          entries: entries.length,
        });
      };
      request.onerror = () => resolve({ size: 0, entries: 0 });
    });
  }
}

function estimateSize(obj: any): number {
  try {
    return new Blob([JSON.stringify(obj)]).size;
  } catch {
    return 0;
  }
}

export const DeviceCache = IndexedDBStore.getInstance();
