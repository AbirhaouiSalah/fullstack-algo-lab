import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("reverse-string-inplace", () => {
  it("reverses an even-length array", () => {
    const chars = ["h", "e", "l", "l", "o", "!"];
    solve(chars);
    expect(chars).toEqual(["!", "o", "l", "l", "e", "h"]);
  });

  it("reverses an odd-length array", () => {
    const chars = ["h", "e", "l", "l", "o"];
    solve(chars);
    expect(chars).toEqual(["o", "l", "l", "e", "h"]);
  });

  it("leaves a single-character array unchanged", () => {
    const chars = ["x"];
    solve(chars);
    expect(chars).toEqual(["x"]);
  });

  it("handles an empty array without throwing", () => {
    const chars: string[] = [];
    expect(() => solve(chars)).not.toThrow();
  });
});
