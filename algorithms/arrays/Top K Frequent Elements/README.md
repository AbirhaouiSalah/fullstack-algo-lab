# Top K Frequent Elements

## Énoncé

On te donne :
- un tableau d'entiers `nums`
- un entier `k`

Tu dois retourner les **k éléments qui apparaissent le plus souvent** dans le tableau.
L'ordre du résultat n'a pas d'importance, et les tests garantissent que la réponse est **unique**.

## Contraintes

- `n = nums.length <= 10 000`
- `-1000 <= nums[i] <= 1000`
- `1 <= k <= nombre d'éléments distincts dans nums`

## Approches implémentées

| Fichier export              | Idée                                          | Complexité   | Espace |
|------------------------------|-----------------------------------------------|--------------|--------|
| `topKFrequentSort`           | Compter → trier par fréquence décroissante     | O(n log n)   | O(n)   |
| `topKFrequentHeap`            | Compter → min-heap de taille k                 | O(n log k)   | O(n+k) |
| `topKFrequentBucket`          | Compter → bucket sort indexé par fréquence     | **O(n)**     | O(n)   |

`topKFrequent` (export par défaut) pointe vers `topKFrequentBucket`, la version optimale.

## Pourquoi le bucket sort est linéaire

La fréquence maximale possible d'un élément est `n` (il ne peut pas apparaître plus
de `n` fois dans un tableau de taille `n`). On crée donc `n + 1` "seaux" indexés
directement par la fréquence :

```
buckets[1] = [valeurs apparaissant 1 fois]
buckets[2] = [valeurs apparaissant 2 fois]
...
buckets[n] = [valeurs apparaissant n fois]
```

Puis on parcourt les seaux **du plus fréquent vers le moins fréquent** et on
prend les k premières valeurs rencontrées. Aucune comparaison, aucun tri :
la fréquence sert directement d'index → O(n).

## Pourquoi le min-heap est souvent la réponse attendue en entretien

Quand `k` est petit devant `n`, `O(n log k)` bat `O(n log n)`. C'est aussi la
solution la plus généralisable si les contraintes changeaient (par exemple si
la fréquence maximale n'était pas bornée par `n`, ce qui casserait l'hypothèse
du bucket sort).

## Fichiers du dossier

- `solution.ts` — les 3 implémentations
- `solution.test.ts` — tests de correction (mêmes cas testés sur les 3 implémentations via `describe.each`)
- `solution.bench.ts` — benchmarks de performance (fichier séparé, à lancer avec `vitest bench`)

## Commandes

```bash
# Tests de correction
npx vitest run solution.test.ts

# Benchmarks (fichier séparé exprès)
npx vitest bench solution.bench.ts
```