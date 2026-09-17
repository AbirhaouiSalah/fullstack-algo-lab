export const benchmarkInput: unknown[] = [
  [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
  ],
];

export function solve(matrix: number[][]): number[] {
  // Ligne 10
  if (matrix.length === 0 || matrix[0]!.length === 0) return [];

  const result: number[] = [];
  let top = 0;
  let bottom = matrix.length - 1;
  let left = 0;
  let right = matrix[0]!.length - 1;

  while (top <= bottom && left <= right) {
    for (let col = left; col <= right; col++) result.push(matrix[top]![col]!);
    top++;

    for (let row = top; row <= bottom; row++) result.push(matrix[row]![right]!);
    right--;

    if (top <= bottom) {
      for (let col = right; col >= left; col--) result.push(matrix[bottom]![col]!);
      bottom--;
    }

    if (left <= right) {
      for (let row = bottom; row >= top; row--) result.push(matrix[row]![left]!);
      left++;
    }
  }

  return result;
}
