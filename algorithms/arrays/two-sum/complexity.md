# Complexity Analysis: Two Sum

## Time Complexity

- **Brute force:** O(n^2) â€” nested loop over all pairs.
- **Hash map:** O(n) â€” single pass, O(1) average lookup/insert.

## Space Complexity

- **Brute force:** O(1) extra space.
- **Hash map:** O(n) for the map in the worst case (no solution found until
  the last element).

## Tradeoffs

The hash map trades space for time, which is almost always worth it unless
memory is severely constrained.
