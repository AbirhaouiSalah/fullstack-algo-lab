/**
 * 347. Top K Frequent Elements
 * https://leetcode.com/problems/top-k-frequent-elements/
 *
 * Contraintes :
 *  - n = nums.length <= 10 000
 *  - -1000 <= nums[i] <= 1000
 *  - 1 <= k <= nombre d'éléments distincts dans nums
 *  - La réponse est garantie unique.
 */

// ============================================================
// Approche 1 — Tri par fréquence
// Complexité : O(n log n) (dominée par le tri)
// Espace     : O(n)
// ============================================================
export function topKFrequentSort(nums: number[], k: number): number[] {
  const freq = new Map<number, number>();
  for (const n of nums) {
    freq.set(n, (freq.get(n) ?? 0) + 1);
  }

  return [...freq.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, k)
    .map(([value]) => value);
}

// ============================================================
// Approche 2 — Min-Heap de taille k
// Complexité : O(n log k)
// Espace     : O(n + k)
//
// Idée : on maintient un tas MIN de taille <= k contenant les
// éléments "les plus fréquents vus jusqu'ici". Si un nouvel élément
// a une fréquence plus grande que le minimum du tas, on le remplace.
// À la fin, le tas contient exactement les k éléments les plus fréquents.
// ============================================================
type HeapEntry = { value: number; count: number };

class MinHeap {
  private items: HeapEntry[] = [];

  get size(): number {
    return this.items.length;
  }

  push(entry: HeapEntry): void {
    this.items.push(entry);
    this.bubbleUp(this.items.length - 1);
  }

  pop(): HeapEntry | undefined {
    if (this.items.length === 0) return undefined;
    const top = this.items[0];
    const last = this.items.pop()!;
    if (this.items.length > 0) {
      this.items[0] = last;
      this.bubbleDown(0);
    }
    return top;
  }

  private bubbleUp(index: number): void {
    while (index > 0) {
      const parent = Math.floor((index - 1) / 2);
      // Sûr : `parent` et `index` sont toujours < this.items.length ici
      // (index vient de push(), parent est strictement plus petit).
      const parentEntry = this.items[parent]!;
      const current = this.items[index]!;
      if (parentEntry.count <= current.count) break;
      this.items[parent] = current;
      this.items[index] = parentEntry;
      index = parent;
    }
  }

  private bubbleDown(index: number): void {
    const n = this.items.length;
    while (true) {
      const left = 2 * index + 1;
      const right = 2 * index + 2;
      let smallest = index;

      // Sûr : on vérifie `left < n` / `right < n` avant chaque accès.
      if (left < n && this.items[left]!.count < this.items[smallest]!.count) smallest = left;
      if (right < n && this.items[right]!.count < this.items[smallest]!.count) smallest = right;
      if (smallest === index) break;

      const temp = this.items[smallest]!;
      this.items[smallest] = this.items[index]!;
      this.items[index] = temp;
      index = smallest;
    }
  }
}

export function topKFrequentHeap(nums: number[], k: number): number[] {
  const freq = new Map<number, number>();
  for (const n of nums) {
    freq.set(n, (freq.get(n) ?? 0) + 1);
  }

  const heap = new MinHeap();
  for (const [value, count] of freq) {
    heap.push({ value, count });
    if (heap.size > k) heap.pop();
  }

  const result: number[] = [];
  let entry: HeapEntry | undefined;
  while ((entry = heap.pop()) !== undefined) {
    result.push(entry.value);
  }
  return result;
}

// ============================================================
// Approche 3 — Bucket Sort (optimale)
// Complexité : O(n) — jamais de vrai tri, on indexe directement
//               par fréquence.
// Espace     : O(n)
//
// Idée : la fréquence maximale possible d'un élément est n
// (il ne peut pas apparaître plus de n fois dans un tableau
// de taille n). On crée donc n+1 "seaux" indexés par fréquence,
// puis on parcourt les seaux du plus fréquent au moins fréquent.
// ============================================================
export function topKFrequentBucket(nums: number[], k: number): number[] {
  const freq = new Map<number, number>();
  for (const n of nums) {
    freq.set(n, (freq.get(n) ?? 0) + 1);
  }

  // buckets[i] = liste des valeurs qui apparaissent exactement i fois
  const buckets: number[][] = Array.from({ length: nums.length + 1 }, () => []);
  for (const [value, count] of freq) {
    // Sûr : count <= nums.length par construction (freq.get ne peut pas
    // dépasser le nombre total d'éléments), donc buckets[count] existe.
    buckets[count]!.push(value);
  }

  const result: number[] = [];
  for (let count = buckets.length - 1; count >= 1 && result.length < k; count--) {
    for (const value of buckets[count]!) {
      result.push(value);
      if (result.length === k) break;
    }
  }

  return result;
}

// Version recommandée par défaut (utilisée par les autres exercices qui
// importeraient cette solution comme dépendance).
export const topKFrequent = topKFrequentBucket;