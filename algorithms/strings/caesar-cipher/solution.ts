export const benchmarkInput: unknown[] = ["Hello, World!", 3];

const UPPER_A = "A".charCodeAt(0);
const UPPER_Z = "Z".charCodeAt(0);
const LOWER_A = "a".charCodeAt(0);
const LOWER_Z = "z".charCodeAt(0);

export function solve(text: string, shift: number): string {
  //const normalizedShift = ((shift % 26) + 26) % 26;
  //let result = "";
//
  //for (let i = 0; i < text.length; i++) {
  //  const code = text.charCodeAt(i);
//
  //  if (code >= UPPER_A && code <= UPPER_Z) {
  //    result += String.fromCharCode(((code - UPPER_A + normalizedShift) % 26) + UPPER_A);
  //  } else if (code >= LOWER_A && code <= LOWER_Z) {
  //    result += String.fromCharCode(((code - LOWER_A + normalizedShift) % 26) + LOWER_A);
  //  } else {
  //    result += text[i];
  //  }
  //}
  let result = "";

  // A->Z :: 65->90
  // a->z :: 97->122
  let numShifted = shift;

  if (numShifted < 0) {
    numShifted = 26 + (numShifted % 26);
  }

  let numASCII_shifted ;
  let numASCII ;

  if (numShifted == 0) {return text;}
  if (text.length == 0) {return text;}

  for (let i = 0; i < text.length; i++) {
    numASCII = text.charCodeAt(i);
    if (numASCII >= UPPER_A && numASCII <= UPPER_Z) {
      numASCII_shifted = UPPER_A + (numASCII - UPPER_A + numShifted) % 26;
    }
    else if (numASCII >= LOWER_A && numASCII <= LOWER_Z) {
      numASCII_shifted = LOWER_A + (numASCII - LOWER_A + numShifted) % 26;
    }
    else {
      result += String.fromCharCode(numASCII);
      continue;
    }
    result += String.fromCharCode(numASCII_shifted);
  }
  return result;
}
