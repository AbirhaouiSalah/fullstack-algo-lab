export const benchmarkInput: unknown[] = ["A man, a plan, a canal: Panama"];

function isAlphanumeric(code: number): boolean {
  return (
    (code >= 48 && code <= 57) || // 0-9
    (code >= 65 && code <= 90) || // A-Z
    (code >= 97 && code <= 122) // a-z
  );
}

function toLowerCode(code: number): number {
  return code >= 65 && code <= 90 ? code + 32 : code;
}

//export function solve(s: string): boolean {
//  let left = 0;
//  let right = s.length - 1;
//
//  while (left < right) {
//    const leftCode = s.charCodeAt(left);
//    const rightCode = s.charCodeAt(right);
//
//    if (!isAlphanumeric(leftCode)) {
//      left++;
//      continue;
//    }
//    if (!isAlphanumeric(rightCode)) {
//      right--;
//      continue;
//    }
//    if (toLowerCode(leftCode) !== toLowerCode(rightCode)) return false;
//
//    left++;
//    right--;
//  }
//
//  return true;



function is_valid_palindrome(s: string): boolean {
  let left = 0;
  let right = s.length - 1;

  while (left < right) {
    const leftCode = s.charCodeAt(left);
    const rightCode = s.charCodeAt(right);

    if (!isAlphanumeric(leftCode)) {
      left++;
      continue;
    }
    if (!isAlphanumeric(rightCode)) {
      right--;
      continue;
    }
    if (toLowerCode(leftCode) !== toLowerCode(rightCode)) return false;

    left++;
    right--;
  }

  return true;
}

export function solve(s: string): boolean {
  // commencer par lowercase et filtrer les caractères non alphanumériques
  s = s.toLowerCase().replace(/[^a-z0-9]/g, "");
  return is_valid_palindrome(s);
}
