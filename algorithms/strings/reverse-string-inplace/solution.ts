export const benchmarkInput: unknown[] = [["h", "e", "l", "l", "o"]];

export function solve(chars: string[]): string[] {
  const inversed_str_arr: string[] = [];
  let index: number = 0; 


  for (let i =0; i < chars.length; i++) {
    index = Math.max(0, chars.length - i - 1);
    inversed_str_arr.push(chars[index]!);
  }

  return inversed_str_arr;

}
