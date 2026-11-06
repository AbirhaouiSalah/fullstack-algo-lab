/**
 * Group Anagrams
 * Arrays & Hashing – Medium
 *
 * Group strings that are anagrams of each other.
 * Optimal: frequency count of 26 letters as hash key → O(m · n)
 */

/**
 * Optimal solution – character frequency as key (no sorting).
 * Time:  O(m · n)   where m = strs.length, n = max string length
 * Space: O(m · n)   for the map + result
 */
export function groupAnagrams(strs: string[]): string[][] {
  const map = new Map<string, string[]>();

  for (const str of strs) {
    // Count frequency of each letter a-z
    const count = new Array(26).fill(0);
    for (const char of str) {
      count[char.charCodeAt(0) - 97]++; // 'a' = 97
    }

    // Build a unique key from the counts
    // e.g. "1#0#2#0#...#0"
    const key = count.join("#");

    if (!map.has(key)) {
      map.set(key, []);
    }
    map.get(key)!.push(str);
  }

  return Array.from(map.values());
}

/**
 * Alternative (acceptable but slower) – sort each string as key.
 * Time:  O(m · n log n)
 * Space: O(m · n)
 */
export function groupAnagramsSort(strs: string[]): string[][] {
  const map = new Map<string, string[]>();

  for (const str of strs) {
    const key = str.split("").sort().join("");
    if (!map.has(key)) {
      map.set(key, []);
    }
    map.get(key)!.push(str);
  }

  return Array.from(map.values());
}