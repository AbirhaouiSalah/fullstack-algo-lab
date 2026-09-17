import { describe, expect, it } from 'vitest';
import {
  topKFrequentSort,
  topKFrequentHeap,
  topKFrequentBucket,
} from './solution';

const implementations = [
  { name: 'Tri par fréquence (O(n log n))', fn: topKFrequentSort },
  { name: 'Min-Heap (O(n log k))', fn: topKFrequentHeap },
  { name: 'Bucket Sort (O(n))', fn: topKFrequentBucket },
];

function sorted(arr: number[]): number[] {
  return [...arr].sort((a, b) => a - b);
}

describe.each(implementations)('topKFrequent — $name', ({ fn }) => {
  it('exemple 1 : nums = [1,2,2,3,3,3], k = 2', () => {
    expect(sorted(fn([1, 2, 2, 3, 3, 3], 2))).toEqual([2, 3]);
  });

  it('exemple 2 : nums = [7,7], k = 1', () => {
    expect(fn([7, 7], 1)).toEqual([7]);
  });

  it('k égal au nombre d’éléments distincts', () => {
    expect(sorted(fn([1, 2, 3], 3))).toEqual([1, 2, 3]);
  });

  it('gère les nombres négatifs', () => {
    expect(sorted(fn([-1, -1, -2, -2, -2, 3], 2))).toEqual([-2, -1]);
  });

  it('un seul élément répété plusieurs fois, k = 1', () => {
    expect(fn([5, 5, 5, 5], 1)).toEqual([5]);
  });

  it('tableau vide de doublons (chaque valeur unique), k = 1', () => {
    const result = fn([9], 1);
    expect(result).toEqual([9]);
  });

  it('fréquences toutes égales : le résultat contient k valeurs valides', () => {
    const input = [1, 2, 3, 4];
    const result = sorted(fn(input, 2));
    expect(result).toHaveLength(2);
    for (const v of result) {
      expect(input).toContain(v);
    }
  });

  it('grand tableau avec une valeur dominante', () => {
    const nums = [...Array(500).fill(42), ...Array(10).fill(1), 2, 3];
    expect(fn(nums, 1)).toEqual([42]);
  });
});