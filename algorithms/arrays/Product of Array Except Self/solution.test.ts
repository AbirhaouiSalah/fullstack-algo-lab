import { describe, expect, it } from 'vitest';
import {
  productExceptSelfBruteForce,
  productExceptSelfDivision,
  productExceptSelfPrefixSuffix,
  productExceptSelfOptimal,
} from './solution';

const implementations = [
  { name: 'Force brute (O(n^2))', fn: productExceptSelfBruteForce },
  { name: 'Division (O(n), gère les zéros)', fn: productExceptSelfDivision },
  { name: 'Préfixe / Suffixe (O(n) temps, O(n) espace)', fn: productExceptSelfPrefixSuffix },
  { name: 'Optimale (O(n) temps, O(1) espace)', fn: productExceptSelfOptimal },
];

describe.each(implementations)('productExceptSelf — $name', ({ fn }) => {
  it('exemple 1 : nums = [1,2,4,6]', () => {
    expect(fn([1, 2, 4, 6])).toEqual([48, 24, 12, 8]);
  });

  it('exemple 2 : nums = [-1,0,1,2,3]', () => {
    expect(fn([-1, 0, 1, 2, 3])).toEqual([0, -6, 0, 0, 0]);
  });

  it('tableau minimal de taille 2', () => {
    expect(fn([3, 7])).toEqual([7, 3]);
  });

  it('deux zéros -> résultat entièrement nul', () => {
    expect(fn([0, 4, 0, 2])).toEqual([0, 0, 0, 0]);
  });

  it('un seul zéro, pas au bord', () => {
    expect(fn([2, 0, 3, 5])).toEqual([0, 30, 0, 0]);
  });

  it('gère les nombres négatifs (signe alterné)', () => {
    expect(fn([-1, -2, -3, -4])).toEqual([-24, -12, -8, -6]);
  });

  it('contient des 1 (élément neutre)', () => {
    expect(fn([1, 1, 1, 5])).toEqual([5, 5, 5, 1]);
  });

  it('valeurs identiques', () => {
    expect(fn([2, 2, 2, 2])).toEqual([8, 8, 8, 8]);
  });
});