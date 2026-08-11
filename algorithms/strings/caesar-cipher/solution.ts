export const benchmarkInput: unknown[] = ["Hello, World!", 3];

const UPPER_A = "A".charCodeAt(0);
const UPPER_Z = "Z".charCodeAt(0);
const LOWER_A = "a".charCodeAt(0);
const LOWER_Z = "z".charCodeAt(0);

export function solve(text: string, shift: number): string {
  const normalizedShift = ((shift % 26) + 26) % 26;
  let result = "";

  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);

    if (code >= UPPER_A && code <= UPPER_Z) {
      result += String.fromCharCode(((code - UPPER_A + normalizedShift) % 26) + UPPER_A);
    } else if (code >= LOWER_A && code <= LOWER_Z) {
      result += String.fromCharCode(((code - LOWER_A + normalizedShift) % 26) + LOWER_A);
    } else {
      result += text[i];
    }
  }

  return result;
}
