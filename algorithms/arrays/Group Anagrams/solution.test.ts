import { describe, it, expect } from "vitest";
import { groupAnagrams, groupAnagramsSort } from "./solution";

// Test suite for the "Group Anagrams" problem, covering both optimal and alternative implementations.

/** Helper: sort groups and strings inside groups for order-independent comparison */
function normalize(groups: string[][]): string[][] {
  return groups
    .map((g) => [...g].sort())
    .sort((a, b) => a[0]?.localeCompare(b[0] ?? "") ?? 0);
}

describe("groupAnagrams – frequency key (optimal)", () => {
  it("Example 1 – multiple groups", () => {
    const input = ["act", "pots", "tops", "cat", "stop", "hat"];
    const result = groupAnagrams(input);
    const expected = [["hat"], ["act", "cat"], ["stop", "pots", "tops"]];
    expect(normalize(result)).toEqual(normalize(expected));
  });

  it("Example 2 – single string", () => {
    expect(groupAnagrams(["x"])).toEqual([["x"]]);
  });

  it("Example 3 – empty string", () => {
    expect(groupAnagrams([""])).toEqual([[""]]);
  });

  it("all anagrams of each other", () => {
    const input = ["eat", "tea", "ate", "eta"];
    const result = groupAnagrams(input);
    expect(result).toHaveLength(1);
    expect(result[0]!.sort()).toEqual(["ate", "eat", "eta", "tea"]);
  });

  it("no anagrams – every string alone", () => {
    const input = ["a", "b", "c"];
    const result = groupAnagrams(input);
    expect(normalize(result)).toEqual([["a"], ["b"], ["c"]]);
  });

  it("handles empty array", () => {
    expect(groupAnagrams([])).toEqual([]);
  });

  it("handles strings of different lengths", () => {
    const input = ["ab", "ba", "abc", "cba", "a"];
    const result = groupAnagrams(input);
    const expected = [["a"], ["ab", "ba"], ["abc", "cba"]];
    expect(normalize(result)).toEqual(normalize(expected));
  });

  it("many identical strings", () => {
    const input = ["aa", "aa", "aa"];
    const result = groupAnagrams(input);
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual(["aa", "aa", "aa"]);
  });
});

describe("groupAnagramsSort – sorting key (acceptable)", () => {
  it("produces same grouping as optimal version", () => {
    const cases = [
      ["act", "pots", "tops", "cat", "stop", "hat"],
      ["x"],
      [""],
      ["eat", "tea", "ate"],
      ["a", "b", "c"],
      ["ab", "ba", "abc", "cba"],
    ];

    for (const input of cases) {
      const a = normalize(groupAnagrams(input));
      const b = normalize(groupAnagramsSort(input));
      expect(a).toEqual(b);
    }
  });
});