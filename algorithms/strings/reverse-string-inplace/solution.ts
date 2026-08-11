export const benchmarkInput: unknown[] = [["h", "e", "l", "l", "o"]];

export function solve(chars: string[]): void {
  let left = 0;
  let right = chars.length - 1;

  while (left < right) {
    [chars[left]!, chars[right]!] = [chars[right]!, chars[left]!];
    left++;
    right--;
  }
}
