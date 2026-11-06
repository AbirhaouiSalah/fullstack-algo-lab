import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("caesar-cipher", () => {
  it("shifts letters and preserves punctuation/case", () => {
    expect(solve("Hello, World!", 3)).toBe("Khoor, Zruog!");
  });

  it("wraps around the end of the alphabet", () => {
    expect(solve("xyz", 3)).toBe("abc");
  });

  it("handles a shift of 0", () => {
    expect(solve("Hello", 0)).toBe("Hello");
  });

  it("handles a shift larger than 26", () => {
    expect(solve("abc", 29)).toBe("def");
  });

  it("handles a shift of upper bound", () => {
    expect(solve("ABC", 29)).toBe("DEF");
  });


  it("handles a negative shift", () => {
    expect(solve("abc", -1)).toBe("zab");
  });

  it("leaves digits and spaces untouched", () => {
    expect(solve("Room 42, now!", 1)).toBe("Sppn 42, opx!");
  });
});
