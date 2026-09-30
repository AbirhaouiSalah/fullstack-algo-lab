# Car Fleet

## Problem Statement

Cars travel toward a target on a one-lane road. A faster car cannot pass a
slower car ahead and joins its fleet. Return the number of fleets that arrive
at the target.

## Approach

Sort cars by starting position from nearest to farthest from the target. Track
arrival times; a car with an arrival time no greater than the fleet ahead joins
that fleet, otherwise it starts a new one.

## Complexity

See [complexity.md](./complexity.md).

## References

- [NeetCode: Car Fleet](https://neetcode.io/problems/car-fleet/question?list=neetcode150)
- [LeetCode: Car Fleet](https://leetcode.com/problems/car-fleet/)