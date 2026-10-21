// A bounded TTL LRU cache with normalized keys and hit/miss accounting.
// Normalized-query cache; punctuation can conflate meaning, without embeddings.
// Keys use the normalized query string directly rather than a SHA-256 digest
// (the Python version hashes for fixed-length keys; functionally equivalent).

interface Entry {
  value: string;
  expiresAt: number;
}

export class SemanticCache {
  private data = new Map<string, Entry>();
  hits = 0;
  misses = 0;

  constructor(private maxEntries = 100, private ttlMs = 300_000, private clock: () => number = Date.now) {
    if (maxEntries < 1 || ttlMs <= 0) throw new Error("maxEntries and ttlMs must be positive");
  }

  static key(query: string, model = "default", version = "1"): string {
    const normalized = query.toLowerCase().replace(/['\u2018\u2019]/gu, "").replace(/\p{P}/gu, " ").trim().split(/\s+/).join(" ");
    return `${model}\0${version}\0${normalized}`;
  }

  get(query: string, model = "default", version = "1"): string | null {
    const key = SemanticCache.key(query, model, version);
    const entry = this.data.get(key);
    if (!entry || entry.expiresAt <= this.clock()) {
      if (entry) this.data.delete(key);
      this.misses++;
      return null;
    }
    this.data.delete(key);
    this.data.set(key, entry);
    this.hits++;
    return entry.value;
  }

  put(query: string, value: string, model = "default", version = "1"): void {
    const key = SemanticCache.key(query, model, version);
    this.data.delete(key);
    this.data.set(key, { value, expiresAt: this.clock() + this.ttlMs });
    while (this.data.size > this.maxEntries) {
      const oldest = this.data.keys().next().value;
      if (oldest === undefined) break;
      this.data.delete(oldest);
    }
  }

  stats() {
    const total = this.hits + this.misses;
    return { entries: this.data.size, hits: this.hits, misses: this.misses, hit_rate: total ? this.hits / total : 0 };
  }
}

export function evaluateAll() {
  let time = 0;
  const cache = new SemanticCache(2, 1000, () => time);
  cache.put("What is the price?", "It's $8/mo");
  cache.get("what   is the PRICE?"); // normalized hit
  cache.get("unrelated question"); // miss
  cache.put("second query", "answer 2");
  cache.put("third query", "answer 3"); // evicts "What is the price?" (LRU, capacity 2)
  const evicted = cache.get("What is the price?") === null;
  time += 2000; // past TTL
  const expired = cache.get("second query") === null;
  const stats = cache.stats();
  const normalization = new SemanticCache();
  normalization.put("What's the price?", "answer");
  const punctuationHit = normalization.get("whats the price") === "answer";
  const spellingMiss = normalization.get("whats the prize") === null;
  return { ...stats, lru_eviction_works: evicted, ttl_expiry_works: expired,
    punctuation_hit_works: punctuationHit, spelling_miss_works: spellingMiss };
}
