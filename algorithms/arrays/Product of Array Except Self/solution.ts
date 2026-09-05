/**
 * Product of Array Except Self
 * https://leetcode.com/problems/product-of-array-except-self/
 *
 * Contraintes :
 *  - 2 <= nums.length <= 100 000
 *  - -30 <= nums[i] <= 30
 *  - Chaque produit (et chaque produit de préfixe/suffixe) tient dans un
 *    entier 32 bits.
 *
 * Consigne du follow-up : résoudre en O(n) SANS division.
 */

// ============================================================
// Approche 1 — Force brute
// Complexité : O(n^2) temps, O(n) espace (sortie)
//
// Pour chaque index i, on reparcourt tout le tableau en ignorant i.
// ============================================================
export function productExceptSelfBruteForce(nums: number[]): number[] {
  const n = nums.length;
  const result: number[] = new Array(n).fill(1);

  for (let i = 0; i < n; i++) {
    let product = 1;
    for (let j = 0; j < n; j++) {
      if (j === i) continue;
      product *= nums[j]!; // sûr : j < n = nums.length
    }
    result[i] = product;
  }

  return result;
}

// ============================================================
// Approche 2 — Division (à éviter : ne respecte pas la contrainte
// du follow-up, mais utile pour comprendre le problème et gérer
// le cas des zéros)
// Complexité : O(n) temps, O(1) espace supplémentaire
//
// Idée : total = produit de tous les éléments.
//   - si aucun zéro dans nums   -> output[i] = total / nums[i]
//   - si exactement un zéro (à l'index z) -> seul output[z] est non nul,
//     et vaut le produit de tous les éléments SAUF le zéro
//   - si au moins deux zéros    -> tout le résultat est à 0
// ============================================================
export function productExceptSelfDivision(nums: number[]): number[] {
  const n = nums.length;
  const result: number[] = new Array(n).fill(0);

  let zeroCount = 0;
  let zeroIndex = -1;
  let productNonZero = 1;

  for (let i = 0; i < n; i++) {
    const value = nums[i]!;
    if (value === 0) {
      zeroCount++;
      zeroIndex = i;
    } else {
      productNonZero *= value;
    }
  }

  if (zeroCount > 1) {
    return result; // déjà rempli de 0
  }

  if (zeroCount === 1) {
    result[zeroIndex] = productNonZero;
    return result;
  }

  // Aucun zéro : division classique
  for (let i = 0; i < n; i++) {
    result[i] = productNonZero / nums[i]!;
  }
  return result;
}

// ============================================================
// Approche 3 — Préfixe / Suffixe (deux tableaux auxiliaires)
// Complexité : O(n) temps, O(n) espace supplémentaire
//
// prefix[i]  = produit de nums[0..i-1]
// suffix[i]  = produit de nums[i+1..n-1]
// output[i]  = prefix[i] * suffix[i]
// ============================================================
export function productExceptSelfPrefixSuffix(nums: number[]): number[] {
  const n = nums.length;
  const prefix: number[] = new Array(n).fill(1);
  const suffix: number[] = new Array(n).fill(1);
  const result: number[] = new Array(n).fill(1);

  for (let i = 1; i < n; i++) {
    prefix[i] = prefix[i - 1]! * nums[i - 1]!;
  }

  for (let i = n - 2; i >= 0; i--) {
    suffix[i] = suffix[i + 1]! * nums[i + 1]!;
  }

  for (let i = 0; i < n; i++) {
    result[i] = prefix[i]! * suffix[i]!;
  }

  return result;
}

// ============================================================
// Approche 4 — Optimale : O(n) temps, O(1) espace supplémentaire
// (le tableau de sortie ne compte pas comme espace auxiliaire)
//
// Idée : on réutilise le tableau de sortie pour stocker d'abord
// les produits de préfixe, puis on multiplie "en place" par les
// produits de suffixe au fur et à mesure d'un second passage,
// sans jamais matérialiser le tableau suffix.
// ============================================================
export function productExceptSelfOptimal(nums: number[]): number[] {
  const n = nums.length;
  const result: number[] = new Array(n).fill(1);

  // 1er passage : result[i] = produit de tous les éléments à gauche de i
  let prefix = 1;
  for (let i = 0; i < n; i++) {
    result[i] = prefix;
    prefix *= nums[i]!;
  }

  // 2e passage : on multiplie par le produit de tous les éléments à droite de i
  let suffix = 1;
  for (let i = n - 1; i >= 0; i--) {
    result[i] = result[i]! * suffix;
    suffix *= nums[i]!;
  }

  return result;
}

// Version recommandée par défaut
export const productExceptSelf = productExceptSelfOptimal;