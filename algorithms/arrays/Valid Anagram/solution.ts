/**
 * Valid Anagram – Arrays & Hashing (Easy)
 *
 * Three implementations, one per hint:
 *   1. Sorting            (Hint 1)  → O(n log n)
 *   2. Two frequency maps (Hint 2/3) → O(n + m)
 *   3. Single count array (optimal)  → O(n + m) time / O(1) space
 */

/* ------------------------------------------------------------------ */
/*  Hint 1 – Sort both strings then compare                           */
/* ------------------------------------------------------------------ */
/**
 * Time:  O(n log n + m log m)
 * Space: O(n + m)  (depends on the JS engine sort)
 */
export function isAnagramSort(s: string, t: string): boolean {
  if (s.length !== t.length) return false;
  return s.split("").sort().join("") === t.split("").sort().join("");
}

/* ------------------------------------------------------------------ */
/*  Hint 2/3 – Frequency maps (Hash tables)                           */
/* ------------------------------------------------------------------ */
/**
 * Two separate Maps that count character frequencies.
 * Time:  O(n + m)
 * Space: O(1)   (at most 26 keys)
 */
export function isAnagramTwoMaps(s: string, t: string): boolean {
  if (s.length !== t.length) return false;

  const countS = new Map<string, number>();
  const countT = new Map<string, number>();

  for (const c of s) countS.set(c, (countS.get(c) ?? 0) + 1);
  for (const c of t) countT.set(c, (countT.get(c) ?? 0) + 1);

  if (countS.size !== countT.size) return false;

  for (const [char, freq] of countS) {
    if (countT.get(char) !== freq) return false;
  }
  return true;
}

/* ------------------------------------------------------------------ */
/*  Optimal – Single frequency array of size 26                       */
/* ------------------------------------------------------------------ */
/**
 * One pass: increment for s, decrement for t.
 * Time:  O(n + m)
 * Space: O(1)   (fixed array of 26)
 */
export function isAnagram(s: string, t: string): boolean {
  if (s.length !== t.length) return false;

  const count: number[] = new Array(26).fill(0);

  for (let i = 0; i < s.length; i++) {
    const sIdx = s.charCodeAt(i) - 97;
    const tIdx = t.charCodeAt(i) - 97;
    count[sIdx] = (count[sIdx] ?? 0) + 1;
    count[tIdx] = (count[tIdx] ?? 0) - 1;
  }

  return count.every((c) => c === 0);
}

/* ------------------------------------------------------------------ */
/*  Helper used by the performance suite                              */
/* ------------------------------------------------------------------ */
export type AnagramFn = (s: string, t: string) => boolean;

export const algorithms: { name: string; fn: AnagramFn }[] = [
  { name: "Sort (Hint 1)", fn: isAnagramSort },
  { name: "Two Maps (Hint 2/3)", fn: isAnagramTwoMaps },
  { name: "Count Array (Optimal)", fn: isAnagram },
];