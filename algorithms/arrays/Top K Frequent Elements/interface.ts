/**
 * interface.ts — Visualisation console des étapes de tri
 * (Top K Frequent Elements)
 *
 * Objectif : afficher, dans le terminal, l'évolution d'un tri sous forme
 * d'histogramme en barres (█), étape par étape, à une vitesse pensée
 * pour être suivie par un œil humain (pas juste une impression instantanée
 * du résultat final).
 *
 * Utilisation directe : `npx tsx interface.ts`
 */

import { pathToFileURL } from 'node:url';
import { topKFrequentSort } from './solution';

// ============================================================
// Couleurs ANSI (aucune dépendance externe)
// Fonctionne dans le terminal intégré VS Code et PowerShell moderne.
// ============================================================
const RESET = '\x1b[0m';
const DIM = '\x1b[2m';
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Contrainte "visible pour un humain" : on refuse de descendre sous ce délai,
// même si l'appelant demande une valeur plus basse. En dessous de ~120ms,
// l'œil ne distingue plus les étapes individuelles.
const MIN_HUMAN_DELAY_MS = 120;

function clampDelay(delayMs: number): number {
  return Math.max(delayMs, MIN_HUMAN_DELAY_MS);
}

// ============================================================
// Rendu d'un histogramme en barres
// ============================================================
export interface BarChartOptions {
  /** Largeur maximale d'une barre en caractères (défaut : 40) */
  maxBarWidth?: number;
  /** Indices en cours de comparaison (affichés en jaune) */
  compareIndices?: number[];
  /** Indices qui viennent d'être échangés (affichés en rouge) */
  swappedIndices?: number[];
  /** Indices définitivement triés (affichés en vert) */
  sortedIndices?: number[];
}

export function renderBarChart(values: number[], options: BarChartOptions = {}): string {
  const { maxBarWidth = 40, compareIndices = [], sortedIndices = [], swappedIndices = [] } = options;

  if (values.length === 0) return '(tableau vide)';

  const max = Math.max(...values.map((v) => Math.abs(v)), 1);
  const compareSet = new Set(compareIndices);
  const sortedSet = new Set(sortedIndices);
  const swappedSet = new Set(swappedIndices);

  const lines = values.map((value, i) => {
    const barLength = Math.max(1, Math.round((Math.abs(value) / max) * maxBarWidth));
    const bar = '█'.repeat(barLength);

    let color = CYAN;
    if (swappedSet.has(i)) color = RED;
    else if (compareSet.has(i)) color = YELLOW;
    else if (sortedSet.has(i)) color = GREEN;

    const valueLabel = String(value).padStart(5, ' ');
    const indexLabel = `[${i}]`.padStart(5, ' ');
    return `${DIM}${indexLabel}${RESET} ${valueLabel} ${color}${bar}${RESET}`;
  });

  return lines.join('\n');
}

// ============================================================
// Génération des étapes de tri (bubble sort instrumenté)
//
// Chaque étape est un instantané pur (aucun effet de bord), pour pouvoir
// être rejouée à la vitesse voulue par l'affichage, indépendamment du
// calcul lui-même.
// ============================================================
export interface SortStep {
  array: number[];
  compareIndices: number[];
  swappedIndices: number[];
  sortedIndices: number[];
  description: string;
}

export function bubbleSortSteps(input: number[]): SortStep[] {
  const array = [...input];
  const steps: SortStep[] = [];
  const n = array.length;
  const sorted: number[] = [];

  steps.push({
    array: [...array],
    compareIndices: [],
    swappedIndices: [],
    sortedIndices: [],
    description: 'État initial',
  });

  for (let i = 0; i < n - 1; i++) {
    let swappedInPass = false;

    for (let j = 0; j < n - 1 - i; j++) {
      const left = array[j]!;
      const right = array[j + 1]!;

      steps.push({
        array: [...array],
        compareIndices: [j, j + 1],
        swappedIndices: [],
        sortedIndices: [...sorted],
        description: `Comparaison entre l'index ${j} (${left}) et ${j + 1} (${right})`,
      });

      if (left > right) {
        array[j] = right;
        array[j + 1] = left;
        swappedInPass = true;

        steps.push({
          array: [...array],
          compareIndices: [],
          swappedIndices: [j, j + 1],
          sortedIndices: [...sorted],
          description: `Échange : ${right} passe avant ${left}`,
        });
      }
    }

    sorted.unshift(n - 1 - i);
    if (!swappedInPass) break;
  }

  const allIndices = Array.from({ length: n }, (_, i) => i);
  steps.push({
    array: [...array],
    compareIndices: [],
    swappedIndices: [],
    sortedIndices: allIndices,
    description: 'Tri terminé',
  });

  return steps;
}

// ============================================================
// Animation dans la console
// ============================================================
export interface AnimateOptions {
  /** Délai entre deux étapes en ms (plancher appliqué : voir MIN_HUMAN_DELAY_MS) */
  delayMs?: number;
  /** Largeur maximale des barres */
  maxBarWidth?: number;
}

export async function animateSortSteps(steps: SortStep[], options: AnimateOptions = {}): Promise<void> {
  const delay = clampDelay(options.delayMs ?? 400);

  for (const step of steps) {
    console.clear();
    console.log(
      renderBarChart(step.array, {
        maxBarWidth: options.maxBarWidth,
        compareIndices: step.compareIndices,
        swappedIndices: step.swappedIndices,
        sortedIndices: step.sortedIndices,
      })
    );
    console.log(`\n${DIM}${step.description}${RESET}`);
    await sleep(delay);
  }
}

/** Trie `values` et anime chaque étape ; retourne le tableau trié. */
export async function visualizeSort(values: number[], options: AnimateOptions = {}): Promise<number[]> {
  const steps = bubbleSortSteps(values);
  await animateSortSteps(steps, options);
  const lastStep = steps[steps.length - 1]!;
  return lastStep.array;
}

// ============================================================
// Démo spécifique à l'exercice : visualise le tri des fréquences
// utilisé par `topKFrequentSort`, puis met en évidence les k retenus.
// ============================================================
export async function visualizeTopKFrequentSort(
  nums: number[],
  k: number,
  options: AnimateOptions = {}
): Promise<void> {
  const freq = new Map<number, number>();
  for (const n of nums) freq.set(n, (freq.get(n) ?? 0) + 1);

  const entries = [...freq.entries()]; // [valeur, fréquence][]
  const counts = entries.map(([, count]) => count);

  console.log('Valeurs :', nums);
  console.log('Fréquences par valeur :', Object.fromEntries(entries));
  console.log(`\nAnimation du tri des fréquences (k = ${k}) :\n`);
  await sleep(clampDelay(options.delayMs ?? 400));

  const sortedCounts = await visualizeSort(counts, options);

  // Reconstruit la correspondance valeur -> fréquence triée pour affichage final
  const sortedDescending = [...sortedCounts].reverse();
  const topCounts = new Set(sortedDescending.slice(0, k));

  console.log('\nRésultat (via topKFrequentSort) :', topKFrequentSort(nums, k));
  console.log(`Fréquences retenues (${k} plus grandes) :`, [...topCounts]);
}

// ============================================================
// Point d'entrée exécutable directement : `npx tsx interface.ts`
// ============================================================
const isDirectRun =
  process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;

if (isDirectRun) {
  const demoNums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4,9, 9, 9, 9, 9,23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1];
  void visualizeTopKFrequentSort(demoNums, 2, { delayMs: 400 });
}