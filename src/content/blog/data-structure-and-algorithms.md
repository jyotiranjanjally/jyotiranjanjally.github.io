---
author: Jyoti Ranjan Jally
pubDatetime: 2024-07-02T10:22:00Z
modDatetime: 2025-07-02T10:22:47.400Z
title: Data Structure and Algorithms
featured: true
draft: false
tags:
  - dsa
description: An introduction to time complexity, space complexity, and asymptotic notations in data structures and algorithms.
---

# Time Complexity and Space Complexity

## Part 1: Time and Space Complexity

### What is Time Complexity?
Time complexity measures how much time an algorithm takes as the input size grows. We usually describe it in terms of n, where n is the size of the input.

Example:
- If you loop through an array of n elements once, the time complexity is O(n).
- If you have a nested loop (loop inside a loop), it might be O(n²).

#### Common Time Complexities

| Complexity | Name         | Example                                         |
|-------------|-------------|-------------------------------------------------|
| O(1)        | Constant    | Accessing an element by index in an array      |
| O(log n)    | Logarithmic | Binary search                                  |
| O(n)        | Linear      | Simple loop through an array                   |
| O(n log n)  | Linearithmic| Efficient sorting algorithms (e.g., Merge Sort)|
| O(n²)       | Quadratic   | Nested loops                                   |
| O(2ⁿ)       | Exponential | Recursive Fibonacci without memoization        |

### What is Space Complexity?
Space complexity measures how much extra memory an algorithm uses as the input grows.

Example:
- If your algorithm only uses a few variables regardless of n, it’s O(1).
- If it uses an extra array of size n, it’s O(n).

## Part 2: Asymptotic Notations

These notations describe how an algorithm behaves as n becomes large.

#### Big O Notation (O) — Worst Case
Describes the upper bound of an algorithm's running time.

Example: In linear search, worst case is O(n).

#### Omega Notation (Ω) — Best Case
Describes the lower bound (best performance possible).

Example: In linear search, if the element is the first one, best case is Ω(1).

#### Theta Notation (Θ) — Tight Bound
Describes the exact bound (when best and worst cases are similar).

Example: If an algorithm always runs in n log n time, it’s Θ(n log n).
