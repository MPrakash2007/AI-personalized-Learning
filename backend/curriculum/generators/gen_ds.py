"""
Generates complete, exam-oriented academic dataset for all 15 Data Structures (DS) topics.
Saves to backend/curriculum/data/ds.json.
"""
import os
import json

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "ds.json"))

DS_TOPICS = {
    "complexity-analysis": {
        "title": "Asymptotic Analysis & Big-O Notation",
        "subject": "ds",
        "exam_definition": (
            "Asymptotic Analysis is a mathematical framework for evaluating the runtime and memory efficiency of algorithms "
            "as input size $n$ approaches infinity, characterized by asymptotic bounds: Big-O ($O$, upper bound), Big-Omega ($\\Omega$, lower bound), "
            "and Big-Theta ($\\Theta$, tight bound)."
        ),
        "remember": "Asymptotic Bounds: Big-O = Worst-case Upper Bound | Big-Omega = Best-case Lower Bound | Big-Theta = Tight Exact Bound.",
        "core_concept": (
            "Measuring algorithm execution in raw seconds is flawed because hardware, OS load, and compilers vary wildly. "
            "Asymptotic analysis abstracts away hardware constants to focus strictly on the mathematical rate of growth of operations $f(n)$ "
            "relative to input size $n$. Master Theorem provides a closed-form formula for solving divide-and-conquer recurrence relations."
        ),
        "key_points": [
            "Big-O ($O$): Formal upper bound: $f(n) \\le c \\cdot g(n)$ for all $n \\ge n_0$. Represents worst-case growth rate.",
            "Big-Omega ($\\Omega$): Formal lower bound: $f(n) \\ge c \\cdot g(n)$ for all $n \\ge n_0$. Represents best-case lower limit.",
            "Big-Theta ($\\Theta$): Tight bound: $c_1 \\cdot g(n) \\le f(n) \\le c_2 \\cdot g(n)$. Holds iff an algorithm is bounded by both $O$ and $\\Omega$.",
            "Growth Hierarchy: $O(1) < O(\\log n) < O(\\sqrt{n}) < O(n) < O(n \\log n) < O(n^2) < O(2^n) < O(n!)$.",
            "Space Complexity: Auxiliary memory used by the algorithm (excluding input) + call stack recursion depth."
        ],
        "classification": {
            "title": "Standard Time Complexity Classes",
            "items": [
                {"name": "Constant Time O(1)", "desc": "Execution time is independent of input size (e.g. array indexing, hash map lookup)."},
                {"name": "Logarithmic Time O(log n)", "desc": "Problem space is cut in half each step (e.g. binary search, balanced BST search)."},
                {"name": "Linear Time O(n)", "desc": "Single pass through input data (e.g. linear search, array traversal)."},
                {"name": "Linearithmic O(n log n)", "desc": "Optimal comparison sorting boundary (e.g. Merge Sort, Heap Sort)."},
                {"name": "Quadratic Time O(n^2)", "desc": "Nested loops over input (e.g. Bubble Sort, Insertion Sort)."},
                {"name": "Exponential Time O(2^n)", "desc": "Recursive branching (e.g. naive Fibonacci, subset sum brute-force)."}
            ]
        },
        "how_it_works": {
            "title": "Master Theorem for Divide-and-Conquer Recurrences",
            "steps": [
                "1. Express recurrence relation in canonical form: $T(n) = a T(n/b) + f(n)$, where $a \\ge 1, b > 1$.",
                "2. Calculate critical exponent: $c_{\\text{crit}} = \\log_b a$.",
                "3. Case 1 (Subproblems dominate): If $f(n) = O(n^c)$ where $c < \\log_b a$, then $T(n) = \\Theta(n^{\\log_b a})$.",
                "4. Case 2 (Equal work at all levels): If $f(n) = \\Theta(n^{\\log_b a} \\log^k n)$, then $T(n) = \\Theta(n^{\\log_b a} \\log^{k+1} n)$.",
                "5. Case 3 (Root dominates): If $f(n) = \\Omega(n^c)$ where $c > \\log_b a$, and regularity condition holds ($a f(n/b) \\le k f(n)$), then $T(n) = \\Theta(f(n))$."
            ],
            "diagram": "Recurrence T(n) = aT(n/b) + f(n) ──> Compare f(n) vs n^(log_b a) ──> Case 1 / Case 2 / Case 3 ──> Theta bound"
        },
        "example": {
            "title": "Master Theorem Applied to Merge Sort Recurrence",
            "scenario": "Merge sort divides array into 2 halves, solves them recursively, and merges in linear time.",
            "code": (
                "// Recurrence relation for Merge Sort:\n"
                "// T(n) = 2T(n/2) + Theta(n)\n\n"
                "// Here: a = 2, b = 2, f(n) = n^1\n"
                "// log_b(a) = log_2(2) = 1\n\n"
                "// Compare f(n) = n^1 with n^(log_b a) = n^1:\n"
                "// Since f(n) = Theta(n^(log_b a) * log^0 n), this is Master Theorem CASE 2 (k = 0).\n\n"
                "// Solution:\n"
                "// T(n) = Theta(n^(log_b a) * log^(k+1) n)\n"
                "// T(n) = Theta(n^1 * log^1 n) = Theta(n log n)"
            )
        },
        "comparison": {
            "title": "Big-O vs Big-Omega vs Big-Theta",
            "headers": ["Notation", "Mathematical Definition", "Bound Type", "Analogy"],
            "rows": [
                ["Big-O ($O$)", "$f(n) \\le c \\cdot g(n)$ for $n \\ge n_0$", "Asymptotic Upper Bound (Worst-case ceiling)", "Speed limit: cannot run slower than this bound"],
                ["Big-Omega ($\\Omega$)", "$f(n) \\ge c \\cdot g(n)$ for $n \\ge n_0$", "Asymptotic Lower Bound (Best-case floor)", "Minimum cost: will take at least this many operations"],
                ["Big-Theta ($\\Theta$)", "$c_1 g(n) \\le f(n) \\le c_2 g(n)$ for $n \\ge n_0$", "Asymptotic Tight Bound (Exact growth rate)", "Exact bracket: sandwiched tightly between upper and lower constants"]
            ]
        },
        "formulas": [
            {"name": "Formal Big-O Limit Definition", "formula": "lim_{n -> inf} (f(n) / g(n)) < inf", "explanation": "If the limit is a finite non-negative constant, f(n) = O(g(n))."},
            {"name": "Master Theorem Recurrence", "formula": "T(n) = a * T(n/b) + Theta(n^d)", "explanation": "d < log_b a -> O(n^(log_b a)) | d = log_b a -> O(n^d log n) | d > log_b a -> O(n^d)."}
        ],
        "exam_tip": "Do NOT confuse 'Worst Case' with 'Big-O'. Big-O is a mathematical upper bound that can describe ANY case (best, average, or worst). Saying 'QuickSort's best-case time is $O(n \\log n)$' is mathematically 100% correct.",
        "common_confusion": {
            "wrong": "An algorithm with time complexity O(1) always finishes in 1 CPU cycle.",
            "correct": "O(1) means execution time is CONSTANT and does not scale with input size n. It could take 1 cycle or 10,000 cycles, as long as that number never changes with n.",
            "explanation": "Accessing array element arr[5000] is O(1) whether array has 10,000 items or 10 billion items."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Define Big-Theta (Theta) notation formally with its mathematical condition.",
                "a": "A function $f(n) = \\Theta(g(n))$ if and only if there exist positive constants $c_1, c_2,$ and $n_0$ such that $0 \\le c_1 \\cdot g(n) \\le f(n) \\le c_2 \\cdot g(n)$ for all $n \\ge n_0$. It represents an asymptotically tight bound."
            },
            {
                "marks": "5-Mark Question",
                "q": "State the Master Theorem for solving divide-and-conquer recurrences with all three cases.",
                "a": "For recurrence $T(n) = a T(n/b) + f(n)$ with $a \\ge 1, b > 1$:\n1. Case 1: If $f(n) = O(n^{\\log_b a - \\epsilon})$ for some $\\epsilon > 0$, then $T(n) = \\Theta(n^{\\log_b a})$.\n2. Case 2: If $f(n) = \\Theta(n^{\\log_b a} \\log^k n)$ for $k \\ge 0$, then $T(n) = \\Theta(n^{\\log_b a} \\log^{k+1} n)$.\n3. Case 3: If $f(n) = \\Omega(n^{\\log_b a + \\epsilon})$ for some $\\epsilon > 0$ and $a f(n/b) \\le c f(n)$ for $c < 1$, then $T(n) = \\Theta(f(n))$."
            },
            {
                "marks": "10-Mark Question",
                "q": "Solve the recurrence relations using Master Theorem or Recursion Tree method: (a) T(n) = 4T(n/2) + n, (b) T(n) = 2T(n/2) + n log n, (c) T(n) = T(n-1) + n.",
                "a": "1. (a) $T(n) = 4T(n/2) + n$:\n   - $a = 4, b = 2, f(n) = n^1$.\n   - $\\log_b a = \\log_2 4 = 2$.\n   - Compare $f(n) = n^1$ with $n^{\\log_b a} = n^2$. Since $1 < 2$, this is Case 1.\n   - Solution: $T(n) = \\Theta(n^2)$.\n2. (b) $T(n) = 2T(n/2) + n \\log n$:\n   - $a = 2, b = 2, f(n) = n^1 \\log^1 n$.\n   - $\\log_b a = \\log_2 2 = 1$.\n   - $f(n) = \\Theta(n^1 \\log^1 n)$, which is Case 2 with $k = 1$.\n   - Solution: $T(n) = \\Theta(n^{\\log_b a} \\log^{k+1} n) = \\Theta(n \\log^2 n)$.\n3. (c) $T(n) = T(n-1) + n$:\n   - Decreasing recurrence (Master Theorem does not apply!).\n   - Unrolling: $T(n) = T(n-2) + (n-1) + n = \\dots = T(0) + \\sum_{i=1}^n i = \\frac{n(n+1)}{2} = \\Theta(n^2)$."
            }
        ],
        "revision_60s": [
            "Big-O = Upper Bound (worst case); Omega = Lower Bound; Theta = Tight Bound.",
            "Order: 1 < log n < n < n log n < n^2 < 2^n < n!.",
            "Master Theorem: T(n) = aT(n/b) + f(n); compare f(n) to n^(log_b a).",
            "Recursion stack depth counts toward Auxiliary Space Complexity.",
            "Constants and lower-order terms are dropped in asymptotic analysis."
        ]
    },

    "arrays": {
        "title": "Arrays & Multi-Dimensional Matrix Operations",
        "subject": "ds",
        "exam_definition": (
            "An Array is a contiguous linear data structure storing fixed-size elements of identical data type, providing "
            "direct $O(1)$ random access through memory index offsetting based on the base address."
        ),
        "remember": "Row-Major 2D Address: Base + [(i * NumCols) + j] * ElementSize | Column-Major: Base + [(j * NumRows) + i] * ElementSize.",
        "core_concept": (
            "Arrays map elements sequentially to adjacent physical memory words. This layout provides exceptional CPU cache locality "
            "(spatial locality). However, insertion and deletion require $O(n)$ element shifting, and size is fixed at declaration "
            "(unless using dynamic amortized resizing arrays like Java ArrayList or C++ vector)."
        ),
        "key_points": [
            "Direct Indexing: Accessing element at index $i$ takes $O(1)$ time via formula: $\\text{Base} + i \\times \\text{ElementSize}$.",
            "Row-Major Order (C, C++, Java): Stores consecutive elements row by row in RAM.",
            "Column-Major Order (Fortran, MATLAB): Stores elements column by column in RAM.",
            "Insertion / Deletion Overhead: Inserting at index 0 requires shifting $n$ elements right ($O(n)$); deleting at index 0 shifts $n-1$ elements left ($O(n)$).",
            "Dynamic Array Resizing: Doubles capacity upon filling; geometric expansion achieves $O(1)$ amortized insertion.",
            "Two Pointers & Sliding Window: Standard $O(n)$ algorithmic paradigms for array optimization problems."
        ],
        "classification": {
            "title": "Array Types & Layouts",
            "items": [
                {"name": "One-Dimensional (1D) Array", "desc": "Linear contiguous sequence of memory cells indexed 0 to N-1."},
                {"name": "Two-Dimensional (2D) Array", "desc": "Matrix organized into rows and columns, stored in Row-Major or Column-Major order."},
                {"name": "Jagged / Ragged Array", "desc": "Array of arrays where each row can have a different number of columns."},
                {"name": "Dynamic Array (ArrayList/vector)", "desc": "Resizable array backed by static array that automatically doubles upon saturation."}
            ]
        },
        "how_it_works": {
            "title": "Two-Dimensional Row-Major vs Column-Major Addressing",
            "steps": [
                "1. Given 2D array $A[M][N]$ with lower bounds $0$ and base address $B$.",
                "2. Row-Major Order (RMO): Memory fills row 0, then row 1, etc. Address = $B + [(i \\times N) + j] \\times W$, where $W$ is element byte size.",
                "3. Column-Major Order (CMO): Memory fills column 0, then column 1, etc. Address = $B + [(j \\times M) + i] \\times W$.",
                "4. For 1-based indexing ($i$ from $1 \\dots M$, $j$ from $1 \\dots N$): RMO = $B + [((i-1) \\times N) + (j-1)] \\times W$."
            ],
            "diagram": "Row-Major Memory: [Row 0 (N elements)] [Row 1 (N elements)] ... [Row M-1]\nColumn-Major:    [Col 0 (M elements)] [Col 1 (M elements)] ... [Col N-1]"
        },
        "example": {
            "title": "Row-Major Address Calculation Numerical",
            "scenario": "Array $A[10][20]$ of integers (4 bytes each) with base address 2000. Find address of $A[6][14]$ assuming 0-based row-major order.",
            "code": (
                "Given:\n"
                "Base Address B = 2000\n"
                "Rows M = 10, Columns N = 20\n"
                "Element Size W = 4 bytes\n"
                "Target: A[i][j] = A[6][14] (0-based indexing)\n\n"
                "Row-Major Formula:\n"
                "Address(A[i][j]) = B + [(i * N) + j] * W\n\n"
                "Calculation:\n"
                "Offset = (6 * 20) + 14 = 120 + 14 = 134 elements\n"
                "Address = 2000 + (134 * 4) = 2000 + 536 = 2536\n\n"
                "If Column-Major Order:\n"
                "Offset = (j * M) + i = (14 * 10) + 6 = 140 + 6 = 146 elements\n"
                "Address = 2000 + (146 * 4) = 2000 + 584 = 2584"
            )
        },
        "comparison": {
            "title": "Static Array vs Dynamic Array (ArrayList / vector)",
            "headers": ["Feature", "Static Array", "Dynamic Array"],
            "rows": [
                ["Size Flexibility", "Fixed at compilation or initialization; cannot be resized", "Grows dynamically at runtime"],
                ["Memory Allocation", "Stack or Heap (single contiguous block)", "Heap memory with internal resizing mechanism"],
                ["Insertion Time", "N/A (fixed capacity)", "$O(1)$ amortized ($O(n)$ worst-case during copy-resize)"],
                ["Memory Overhead", "Zero extra overhead beyond stored elements", "Unused buffer capacity overhead (usually 1.5x - 2x)"],
                ["Cache Locality", "Maximum hardware cache hit rate", "Maximum hardware cache hit rate (contiguous memory)"]
            ]
        },
        "formulas": [
            {"name": "2D Row-Major Address Formula", "formula": "Addr(A[i][j]) = Base + ((i - L1) * N2 + (j - L2)) * W", "explanation": "Where L1, L2 are lower index bounds, N2 is number of columns, W is element byte size."},
            {"name": "2D Column-Major Address Formula", "formula": "Addr(A[i][j]) = Base + ((j - L2) * N1 + (i - L1)) * W", "explanation": "Where N1 is number of rows."}
        ],
        "exam_tip": "In university exam problems, check whether indexing is 0-based or 1-based! If given bounds are $A[1\\dots M][1\\dots N]$, remember to subtract 1 from indices $i$ and $j$ before multiplying.",
        "common_confusion": {
            "wrong": "Dynamic array insertion always takes O(1) time.",
            "correct": "Dynamic array insertion takes O(1) AMORTIZED time. When the underlying array is full, doubling the array requires allocating new memory and copying all n elements, costing O(n) worst-case time.",
            "explanation": "Because doubling happens infrequently, n insertions cost 2n operations total, averaging 2 operations per insert = O(1)."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Why does an array provide O(1) random access time?",
                "a": "Because array elements are stored in contiguous memory cells of identical byte width, the physical memory address of any element at index $i$ is directly computed in a single mathematical step: $\\text{Address} = \\text{Base} + i \\times \\text{ElementSize}$, requiring no traversal."
            },
            {
                "marks": "5-Mark Question",
                "q": "Derive the address calculation formula for a 2D array in Row-Major and Column-Major order.",
                "a": "Let array $A[1\\dots M, 1\\dots N]$ have base address $B$ and element size $W$:\n1. Row-Major: Elements are stored row by row. To reach row $i$, we skip $(i - 1)$ full rows, each containing $N$ elements. Within row $i$, we skip $(j - 1)$ elements. Total offset = $[(i - 1)N + (j - 1)]$. $\\text{Address} = B + [(i - 1)N + (j - 1)] \\times W$.\n2. Column-Major: Elements are stored column by column. To reach column $j$, we skip $(j - 1)$ full columns, each containing $M$ elements. Within column $j$, we skip $(i - 1)$ elements. $\\text{Address} = B + [(j - 1)M + (i - 1)] \\times W$."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain Kadane's Algorithm for Maximum Subarray Sum. Trace it on array [-2, 1, -3, 4, -1, 2, 1, -5, 4] and analyze its time and space complexity.",
                "a": "1. Concept: Kadane's Algorithm computes the maximum sum contiguous subarray in a single $O(n)$ pass using dynamic programming principles. At each index $i$, we decide whether to extend the current subarray sum or start a new subarray at $arr[i]$.\n2. Algorithm:\n   - Maintain `max_so_far = arr[0]`, `curr_max = arr[0]`.\n   - For $i = 1 \\dots n-1$:\n     - `curr_max = max(arr[i], curr_max + arr[i])`\n     - `max_so_far = max(max_so_far, curr_max)`\n3. Trace on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`:\n   - i=0: curr=-2, max=-2\n   - i=1 (1): curr = max(1, -2+1) = 1, max = 1\n   - i=2 (-3): curr = max(-3, 1-3) = -2, max = 1\n   - i=3 (4): curr = max(4, -2+4) = 4, max = 4\n   - i=4 (-1): curr = max(-1, 4-1) = 3, max = 4\n   - i=5 (2): curr = max(2, 3+2) = 5, max = 5\n   - i=6 (1): curr = max(1, 5+1) = 6, max = 6\n   - i=7 (-5): curr = max(-5, 6-5) = 1, max = 6\n   - i=8 (4): curr = max(4, 1+4) = 5, max = 6\n   Result: Maximum subarray sum is 6 (subarray [4, -1, 2, 1]).\n4. Complexity: Time = $O(n)$, Space = $O(1)$ auxiliary memory."
            }
        ],
        "revision_60s": [
            "Array: contiguous fixed-size linear structure with O(1) random access.",
            "Row-major: Row offset + Column offset -> B + [i*Cols + j] * W.",
            "Column-major: Column offset + Row offset -> B + [j*Rows + i] * W.",
            "Insertion/Deletion at head takes O(n) shifts.",
            "Amortized dynamic array doubling achieves O(1) average insertion.",
            "Kadane's algorithm solves maximum subarray sum in O(n) time and O(1) space."
        ]
    },

    "strings": {
        "title": "Strings & Pattern Matching Algorithms",
        "subject": "ds",
        "exam_definition": (
            "A String is a sequence of characters terminated by a null delimiter ('\\0' in C) or encapsulated in an immutable object (Java/Python), "
            "analyzed using string algorithms such as KMP (Knuth-Morris-Pratt), Rabin-Karp, and Trie structures."
        ),
        "remember": "KMP Prefix Function (LPS array): LPS[i] stores the length of the longest proper prefix of pat[0..i] that is also a suffix of pat[0..i].",
        "core_concept": (
            "Naive pattern searching scans text $T$ of length $N$ with pattern $P$ of length $M$ in $O(N \\cdot M)$ worst-case time. "
            "Advanced algorithms eliminate redundant re-comparisons: KMP precomputes the Longest Prefix Suffix (LPS) array to shift the pattern "
            "in $O(N + M)$ time; Rabin-Karp uses rolling polynomial hashes in $O(N + M)$ average time."
        ),
        "key_points": [
            "String Immutability: In Java/Python, strings are immutable; modifying a string creates a new object. StringBuilder/StringBuffer provides mutable $O(1)$ appends.",
            "Naive Pattern Matching: Compares characters one by one; backtracks text pointer upon mismatch ($O(N \\cdot M)$ worst case).",
            "KMP Algorithm: Never backtracks the text pointer; uses precomputed LPS table to jump pattern upon mismatch in $O(N + M)$ time.",
            "LPS Array: Longest Proper Prefix that is also a Suffix (proper prefix excludes the entire string itself).",
            "Rabin-Karp Algorithm: Calculates rolling hash of length $M$ windows using Horner's polynomial rule; resolves hash collisions via direct string verification.",
            "Trie (Prefix Tree): Tree data structure for storing strings where each node represents a character, enabling $O(L)$ prefix lookup."
        ],
        "classification": {
            "title": "String Pattern Matching Algorithms",
            "items": [
                {"name": "Naive Search", "desc": "Slides pattern character by character; checks all positions. Time: O((N - M + 1) * M)."},
                {"name": "KMP (Knuth-Morris-Pratt)", "desc": "Uses LPS failure function to skip redundant comparisons. Time: O(N + M), Space: O(M)."},
                {"name": "Rabin-Karp", "desc": "Uses rolling hash values to compare pattern with text substrings. Time: O(N + M) average."},
                {"name": "Boyer-Moore", "desc": "Scans pattern from right to left using Bad Character and Good Suffix heuristics. Sub-linear O(N/M) average."},
                {"name": "Aho-Corasick", "desc": "Trie-based finite automaton for simultaneous multi-pattern matching in O(N + M + Z) time."}
            ]
        },
        "how_it_works": {
            "title": "KMP LPS Table Construction & Matching Flow",
            "steps": [
                "1. LPS Construction: Initialize `lps[0] = 0`, `len = 0`, `i = 1`.",
                "2. If `pat[i] == pat[len]`: increment `len`, set `lps[i] = len`, increment `i`.",
                "3. If mismatch and `len > 0`: fallback `len = lps[len - 1]` without incrementing `i`.",
                "4. If mismatch and `len == 0`: set `lps[i] = 0`, increment `i`.",
                "5. Text Matching: Compare `txt[i]` and `pat[j]`. On mismatch with `j > 0`, update `j = lps[j - 1]` (never backtrack text pointer `i`)."
            ],
            "diagram": "Pattern: A B A B C\nLPS Table: [0, 0, 1, 2, 0] ──> Mismatch at 'C' resets pattern index to LPS[3]=2 ('A B') without moving text pointer backward."
        },
        "example": {
            "title": "KMP LPS Array Construction Example",
            "scenario": "Construct the LPS array for the pattern: `A A B A A A`.",
            "code": (
                "Pattern: A  A  B  A  A  A\n"
                "Index:   0  1  2  3  4  5\n\n"
                "Trace:\n"
                "i=0: pat[0]='A' -> LPS[0] = 0\n"
                "i=1: pat[1]=='A' == pat[0] -> len=1, LPS[1]=1\n"
                "i=2: pat[2]=='B' != pat[1], len=LPS[0]=0. pat[2]!='A' -> LPS[2]=0\n"
                "i=3: pat[3]=='A' == pat[0] -> len=1, LPS[3]=1\n"
                "i=4: pat[4]=='A' == pat[1] -> len=2, LPS[4]=2\n"
                "i=5: pat[5]=='A' != pat[2] ('B'). Fallback len=LPS[1]=1.\n"
                "     pat[5]=='A' == pat[len]=pat[1] -> len=2, LPS[5]=2\n\n"
                "Final LPS Array = [0, 1, 0, 1, 2, 2]"
            )
        },
        "comparison": {
            "title": "Naive vs KMP vs Rabin-Karp",
            "headers": ["Algorithm", "Preprocessing Time", "Matching Time (Worst)", "Matching Time (Avg)", "Key Mechanism"],
            "rows": [
                ["Naive Search", "$O(1)$", "$O((N-M+1)M)$", "$O(N)$", "Brute-force sliding window with full backtracks"],
                ["KMP", "$O(M)$", "$O(N)$", "$O(N)$", "LPS array avoids backtracking text pointer"],
                ["Rabin-Karp", "$O(M)$", "$O(N \\cdot M)$ (many collisions)", "$O(N + M)$", "Rolling polynomial hash calculation"],
                ["Trie Search", "$O(\\sum L)$", "$O(L)$", "$O(L)$", "Prefix tree character path traversal"]
            ]
        },
        "formulas": [
            {"name": "Rabin-Karp Rolling Hash Formula", "formula": "H_next = (d * (H_prev - txt[i] * h) + txt[i + M]) % q", "explanation": "Where d is alphabet size, q is prime modulus, h = d^(M-1) % q."},
            {"name": "KMP Total Operations Bound", "formula": "Total Comparisons <= 2N", "explanation": "Text index i increments N times; j decreases at most N times."}
        ],
        "exam_tip": "When calculating the LPS table in an exam, remember: 'Proper prefix' means the prefix CANNOT be the entire string itself. For pattern 'AAAA', proper prefixes are 'A', 'AA', 'AAA'.",
        "common_confusion": {
            "wrong": "String concatenation in a loop (s += c) is efficient in languages like Java or Python.",
            "correct": "Because strings are immutable, s += c creates a new string object and copies all previous characters every iteration, turning an N-length loop into an O(N^2) disaster.",
            "explanation": "Always use StringBuilder in Java or list.append() followed by ''.join() in Python for O(N) total construction."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the LPS array in the KMP algorithm?",
                "a": "The LPS (Longest Prefix Suffix) array is a precomputed table where $LPS[i]$ represents the length of the longest proper prefix of pattern substring $pat[0\\dots i]$ that is also a suffix of $pat[0\\dots i]$, allowing the algorithm to skip redundant comparisons during a mismatch."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the Rabin-Karp pattern matching algorithm and how rolling hash works.",
                "a": "1. Concept: Rabin-Karp calculates a hash value for the pattern of length $M$ and compares it to hash values of all $M$-length substrings of text $T$.\n2. Rolling Hash: Instead of recalculating the hash from scratch in $O(M)$ time for each window, the rolling hash subtracts the leading character and adds the trailing character in $O(1)$ time: $H_{k+1} = (d \\cdot (H_k - T[k] \\cdot d^{M-1}) + T[k+M]) \\pmod q$.\n3. Verification: When window hash matches pattern hash, a direct character-by-character comparison verifies whether it is a true match or a spurious hash collision."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain the KMP (Knuth-Morris-Pratt) algorithm. Trace the LPS array and search process for Text = 'ABABDABACDABABCABAB' and Pattern = 'ABABCABAB'.",
                "a": "1. LPS Array Calculation for Pattern 'ABABCABAB':\n   - A -> 0\n   - AB -> 0\n   - ABA -> 1 (prefix 'A' == suffix 'A')\n   - ABAB -> 2 (prefix 'AB' == suffix 'AB')\n   - ABABC -> 0\n   - ABABCA -> 1\n   - ABABCAB -> 2\n   - ABABCABA -> 3\n   - ABABCABAB -> 4 (prefix 'ABAB' == suffix 'ABAB')\n   - LPS = [0, 0, 1, 2, 0, 1, 2, 3, 4].\n2. Matching Trace:\n   - Text: 'ABABDABACDABABCABAB'\n   - Compare at index 0: 'ABAB' matches, index 4 'D' != 'C'.\n   - Mismatch at j=4: j resets to LPS[3] = 2 ('AB'). Next comparison is txt[4] ('D') with pat[2] ('A').\n   - Text pointer i never moves backwards!\n   - Pattern advances until exact match found at index 10.\n3. Complexity Analysis: Preprocessing takes $O(M)$ time and space; searching takes $O(N)$ comparisons. Total time complexity = $O(N + M)$."
            }
        ],
        "revision_60s": [
            "String immutability means string += char in a loop is O(N^2); use StringBuilder for O(N).",
            "Naive pattern search takes O(N * M) worst-case time.",
            "KMP runs in O(N + M) time and never backtracks the text pointer.",
            "LPS[i] = length of longest proper prefix that is also a suffix.",
            "Rabin-Karp uses O(1) rolling polynomial hash; checks collisions explicitly."
        ]
    },

    "linked-lists": {
        "title": "Linked Lists: Singly, Doubly & Circular",
        "subject": "ds",
        "exam_definition": (
            "A Linked List is a linear dynamic data structure composed of nodes where each node encapsulates data and one or more "
            "pointer/reference links to subsequent nodes, providing $O(1)$ insertions and deletions given node pointers."
        ),
        "remember": "Floyd's Cycle Detection (Tortoise and Hare): Slow pointer advances 1 step, Fast pointer advances 2 steps. They meet iff a cycle exists.",
        "core_concept": (
            "Unlike arrays, linked list nodes are allocated dynamically and scattered across heap memory, completely eliminating the need "
            "for contiguous memory allocation and dynamic resizing overhead. However, linked lists forfeit $O(1)$ random indexing, requiring "
            "$O(n)$ sequential traversal to access the $k$-th element, and incur extra memory overhead for pointers."
        ),
        "key_points": [
            "Singly Linked List: Each node contains `data` and `next` pointer; unidirectional traversal.",
            "Doubly Linked List (DLL): Nodes contain `prev`, `data`, and `next` pointers; enables bidirectional traversal and $O(1)$ node deletion.",
            "Circular Linked List: The last node's `next` pointer loops back to the head node (or dummy sentinel).",
            "Time Complexities: Access: $O(n)$, Search: $O(n)$, Insertion at Head: $O(1)$, Insertion at Tail (with tail pointer): $O(1)$, Deletion at given node pointer (DLL): $O(1)$.",
            "Floyd's Cycle Algorithm: Detects cycle in $O(n)$ time and $O(1)$ auxiliary space. Distance from head to cycle start equals distance from meeting point to cycle start.",
            "Reversal: In-place reversal of singly linked list requires 3 pointers: `prev`, `curr`, `next`."
        ],
        "classification": {
            "title": "Types of Linked Lists",
            "items": [
                {"name": "Singly Linked List", "desc": "Unidirectional nodes containing data and single forward next pointer."},
                {"name": "Doubly Linked List (DLL)", "desc": "Bidirectional nodes containing prev and next pointers. Supports O(1) arbitrary node removal."},
                {"name": "Circular Singly Linked List", "desc": "Tail node points back to the first node. Ideal for round-robin schedulers."},
                {"name": "Circular Doubly Linked List", "desc": "Head's prev points to tail; tail's next points to head. Cleanest sentinel implementation (Linux kernel list_head)."}
            ]
        },
        "how_it_works": {
            "title": "Floyd's Cycle Finding & Entry Point Resolution",
            "steps": [
                "1. Initialize `slow = head` and `fast = head`.",
                "2. Loop while `fast != null` and `fast.next != null`:\n   - `slow = slow.next` (1 step)\n   - `fast = fast.next.next` (2 steps)",
                "3. If `slow == fast`, a cycle is detected! Break loop.",
                "4. If loop terminates naturally, the list is linear with no cycle.",
                "5. To find cycle starting node: Reset `slow = head`, leave `fast` at intersection point.",
                "6. Advance both `slow` and `fast` 1 step at a time; the node where they meet is the exact cycle entry point."
            ],
            "diagram": "Head ──(L steps)──> [Cycle Entry] ──(K steps)──> [Meeting Point]\nProof: Distance(Head -> Entry) == Distance(Meeting Point -> Entry) traversing the loop."
        },
        "example": {
            "title": "In-Place Singly Linked List Reversal in C++",
            "scenario": "Reverses a singly linked list in $O(n)$ time and $O(1)$ space using 3 pointers.",
            "code": (
                "struct ListNode {\n"
                "    int val;\n"
                "    ListNode* next;\n"
                "    ListNode(int x) : val(x), next(nullptr) {}\n"
                "};\n\n"
                "ListNode* reverseList(ListNode* head) {\n"
                "    ListNode* prev = nullptr;\n"
                "    ListNode* curr = head;\n"
                "    while (curr != nullptr) {\n"
                "        ListNode* nextNode = curr->next; // Save next node\n"
                "        curr->next = prev;               // Reverse link pointer\n"
                "        prev = curr;                     // Advance prev pointer\n"
                "        curr = nextNode;                 // Advance curr pointer\n"
                "    }\n"
                "    return prev; // prev is the new head of reversed list\n"
                "}"
            )
        },
        "comparison": {
            "title": "Array vs Singly Linked List vs Doubly Linked List",
            "headers": ["Operation", "Array", "Singly Linked List", "Doubly Linked List"],
            "rows": [
                ["Random Access (index i)", "$O(1)$", "$O(n)$ (must traverse)", "$O(n)$ (must traverse)"],
                ["Insert / Delete at Head", "$O(n)$ (must shift)", "$O(1)$", "$O(1)$"],
                ["Insert / Delete at Tail", "$O(1)$ amortized", "$O(1)$ (with tail pointer)", "$O(1)$ (with tail pointer)"],
                ["Delete given Node pointer", "$O(n)$ (must shift)", "$O(n)$ (must find prev node)", "$O(1)$ (node->prev->next = node->next)"],
                ["Memory Overhead", "Zero pointer overhead", "1 pointer per element", "2 pointers per element"]
            ]
        },
        "formulas": [
            {"name": "Floyd Cycle Distance Equivalence", "formula": "L = (n * C) - k", "explanation": "Where L is head-to-cycle distance, C is cycle circumference, k is entry-to-meeting distance."}
        ],
        "exam_tip": "When reversing a linked list or deleting nodes in an exam, always watch out for NULL pointer exceptions! Explicitly verify the base cases: `head == NULL` and `head->next == NULL`.",
        "common_confusion": {
            "wrong": "Deleting a node from a singly linked list given only a pointer to that node takes O(1) time.",
            "correct": "You cannot cleanly delete a node in O(1) time in a singly linked list without knowing its predecessor, because you cannot update prev->next.",
            "explanation": "A hack exists (copy next node's data into current node and delete next node), but it fails if the target node is the tail node!"
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the primary advantage of a Doubly Linked List over a Singly Linked List?",
                "a": "A Doubly Linked List allows bidirectional traversal (forward and backward) and enables deleting a given node in $O(1)$ time without traversing from the head, because the node has direct access to its predecessor via `node->prev`."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain Floyd's Cycle Detection algorithm (Tortoise and Hare). Prove how the cycle entry point is located.",
                "a": "1. Detection: Advance slow pointer by 1 step and fast pointer by 2 steps. If they meet, a cycle exists. If fast reaches NULL, no cycle.\n2. Proof of Entry Point:\n   - Let $L$ = distance from head to cycle entry, $C$ = cycle circumference, $k$ = distance from entry to meeting point.\n   - Distance traveled by slow = $L + k$.\n   - Distance traveled by fast = $L + k + n \\cdot C$.\n   - Since fast travels twice as fast: $2(L + k) = L + k + n \\cdot C \\implies L = n \\cdot C - k = (n - 1)C + (C - k)$.\n   - Notice that $(C - k)$ is the remaining distance from the meeting point back to the cycle entry!\n   - Therefore, moving one pointer to head and keeping the other at the meeting point and advancing both at speed 1 guarantees they will meet at the cycle entry."
            },
            {
                "marks": "10-Mark Question",
                "q": "Write algorithms and explain with diagrams: (a) In-place reversal of a Singly Linked List, (b) Finding the middle element in a single pass.",
                "a": "1. (a) In-place Reversal:\n   - Pointers: `prev = NULL`, `curr = head`, `next = NULL`.\n   - Loop: `while (curr) { next = curr->next; curr->next = prev; prev = curr; curr = next; }`\n   - Set `head = prev`.\n   - Diagram: Illustrate how pointer directions flip between successive nodes.\n   - Complexity: Time $O(n)$, Space $O(1)$.\n2. (b) Middle Element in Single Pass:\n   - Pointers: `slow = head`, `fast = head`.\n   - Loop: `while (fast != NULL && fast->next != NULL) { slow = slow->next; fast = fast->next->next; }`\n   - When fast reaches end (or last node), slow is positioned exactly at the middle element ($n/2$).\n   - Handles both even and odd length lists gracefully."
            }
        ],
        "revision_60s": [
            "Linked list nodes allocated dynamically in heap; no resizing needed.",
            "Array has O(1) random access; Linked list has O(n) access.",
            "Reversal requires 3 pointers: prev, curr, next.",
            "Floyd's algorithm: slow (1x), fast (2x) detect cycle in O(n) time and O(1) space.",
            "DLL enables O(1) arbitrary node deletion using node->prev."
        ]
    },

    "stacks": {
        "title": "Stacks & Expression Evaluation",
        "subject": "ds",
        "exam_definition": (
            "A Stack is a linear LIFO (Last-In, First-Out) data structure supporting $O(1)$ push and pop operations at a single interface "
            "called the Top, used extensively in expression parsing (Infix to Postfix), parenthesis validation, and runtime call stacks."
        ),
        "remember": "Stack Principle: LIFO (Last-In, First-Out). Elements are pushed and popped exclusively from the Top pointer.",
        "core_concept": (
            "The stack models nested execution contexts. Compilers rely on stacks to parse mathematical expressions and evaluate postfix "
            "(Reverse Polish Notation) expressions without operator ambiguity or parentheses. The OS runtime manages subroutine calls "
            "and local variable scopes through the activation records on the Call Stack."
        ),
        "key_points": [
            "Core Operations: push(x) adds to top ($O(1)$), pop() removes top ($O(1)$), peek()/top() views top ($O(1)$), isEmpty() checks count ($O(1)$).",
            "Stack Overflow vs Underflow: Overflow occurs pushing to a full fixed-size stack; Underflow occurs popping from an empty stack.",
            "Expression Notations: Infix ($A + B$, human readable), Postfix ($A B +$, Reverse Polish Notation, optimal for computers), Prefix ($+ A B$, Polish Notation).",
            "Operator Precedence & Associativity: Brackets > Exponential ($^$, right-to-left) > Multiply/Divide ($*$, $/$, left-to-right) > Add/Subtract ($+$, $-$, left-to-right).",
            "Monotonic Stack: Stack maintaining elements in strictly increasing or decreasing order; solves Next Greater Element in $O(n)$ time."
        ],
        "classification": {
            "title": "Stack Implementation Strategies",
            "items": [
                {"name": "Array-Based Stack", "desc": "Fixed-size or dynamic array using integer `top` index. Fast cache locality, but static array risks overflow."},
                {"name": "Linked List-Based Stack", "desc": "Dynamic nodes inserted/removed at head. Zero overflow risk (limited only by RAM), but extra pointer overhead."}
            ]
        },
        "how_it_works": {
            "title": "Infix to Postfix Conversion (Shunting-Yard Algorithm)",
            "steps": [
                "1. Initialize an empty operator stack and an empty postfix output string.",
                "2. Scan infix expression from left to right token by token.",
                "3. If token is an operand (letter/number), append directly to output.",
                "4. If token is '(', push onto stack.",
                "5. If token is ')', pop from stack to output until '(' is encountered, then discard '('.",
                "6. If token is an operator: while stack is non-empty and precedence(stack.top) >= precedence(operator) [or > if right-associative], pop stack to output. Then push current operator.",
                "7. At end of expression, pop all remaining operators from stack to output."
            ],
            "diagram": "Infix: A + B * C ──> Scan A (Output) ──> Scan + (Push) ──> Scan B (Output) ──> Scan * (Push, higher prec) ──> Scan C (Output) ──> Empty Stack ──> Postfix: A B C * +"
        },
        "example": {
            "title": "Evaluating Postfix Expression Using Stack in Java",
            "scenario": "Evaluate the postfix expression: `5 3 + 8 2 - *`.",
            "code": (
                "// Expression: 5 3 + 8 2 - *\n"
                "Stack<Integer> stack = new Stack<>();\n\n"
                "// 1. Push 5 -> [5]\n"
                "// 2. Push 3 -> [5, 3]\n"
                "// 3. Op '+': pop 3, pop 5 -> compute 5 + 3 = 8 -> push 8 -> [8]\n"
                "// 4. Push 8 -> [8, 8]\n"
                "// 5. Push 2 -> [8, 8, 2]\n"
                "// 6. Op '-': pop 2, pop 8 -> compute 8 - 2 = 6 -> push 6 -> [8, 6]\n"
                "// 7. Op '*': pop 6, pop 8 -> compute 8 * 6 = 48 -> push 48 -> [48]\n"
                "// Result = 48"
            )
        },
        "comparison": {
            "title": "Infix vs Prefix vs Postfix Notations",
            "headers": ["Feature", "Infix Notation", "Prefix Notation (Polish)", "Postfix Notation (Reverse Polish)"],
            "rows": [
                ["Operator Position", "Between operands ($A + B$)", "Before operands ($+ A B$)", "After operands ($A B +$)"],
                ["Parentheses Needed?", "Yes (required to override precedence)", "Never needed", "Never needed"],
                ["Evaluation Order", "Requires complex parsing rules", "Right-to-left scan with stack", "Left-to-right scan with stack"],
                ["Computer Efficiency", "Low — complex compiler grammar", "High", "Highest — standard bytecode execution model (JVM, Forth)"]
            ]
        },
        "formulas": [
            {"name": "Stack Size Invariant", "formula": "0 <= top <= MAX_SIZE - 1", "explanation": "top = -1 represents empty stack; top = MAX_SIZE - 1 represents full stack."}
        ],
        "exam_tip": "In Infix to Postfix questions, remember that the exponential operator ($^$) has RIGHT-TO-LEFT associativity! So $2^3^2$ evaluates as $2^{(3^2)} = 2^9 = 512$, not $(2^3)^2 = 64$.",
        "common_confusion": {
            "wrong": "When evaluating postfix expressions, the first popped element is the left operand.",
            "correct": "The first popped element is the RIGHT (second) operand, and the second popped element is the LEFT (first) operand!",
            "explanation": "For division: op2 = pop(); op1 = pop(); result = op1 / op2. Reversing them produces catastrophic inverted divisions."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the difference between Stack Overflow and Stack Underflow?",
                "a": "Stack Overflow occurs when an attempt is made to push an element onto a stack that has already reached its maximum allocated capacity. Stack Underflow occurs when an attempt is made to pop an element from an empty stack."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain how to test for balanced parentheses in an expression using a stack.",
                "a": "1. Algorithm: Traverse expression string character by character.\n2. If an opening bracket (`(`, `{`, `[`) is encountered, push it onto the stack.\n3. If a closing bracket (`)`, `}`, `]`) is encountered:\n   - If stack is empty, return false (mismatched closing bracket).\n   - Pop top element from stack. If it does not correspond to the matching opening type, return false.\n4. When traversal finishes, if stack is empty return true (balanced); otherwise return false (unclosed brackets).\n5. Complexity: Time $O(n)$, Space $O(n)$."
            },
            {
                "marks": "10-Mark Question",
                "q": "Convert the infix expression: `(A + B) * C - (D - E) ^ (F + G)` to postfix using a tabular trace of the stack and output.",
                "a": "1. Expression: `(A + B) * C - (D - E) ^ (F + G)`\n2. Trace Table:\n   - Token '(': Stack: [(], Output: []\n   - Token 'A': Stack: [(], Output: [A]\n   - Token '+': Stack: [(, +], Output: [A]\n   - Token 'B': Stack: [(, +], Output: [A, B]\n   - Token ')': Pop until '(' -> Stack: [], Output: [A, B, +]\n   - Token '*': Stack: [*], Output: [A, B, +]\n   - Token 'C': Stack: [*], Output: [A, B, +, C]\n   - Token '-': '*' has higher precedence than '-'. Pop '*' -> Stack: [-], Output: [A, B, +, C, *]\n   - Token '(': Stack: [-, (], Output: [A, B, +, C, *]\n   - Token 'D': Stack: [-, (], Output: [A, B, +, C, *, D]\n   - Token '-': Stack: [-, (, -], Output: [A, B, +, C, *, D]\n   - Token 'E': Stack: [-, (, -], Output: [A, B, +, C, *, D, E]\n   - Token ')': Pop until '(' -> Stack: [-], Output: [A, B, +, C, *, D, E, -]\n   - Token '^': Stack: [-, ^], Output: [A, B, +, C, *, D, E, -]\n   - Token '(': Stack: [-, ^, (], Output: [A, B, +, C, *, D, E, -]\n   - Token 'F': Stack: [-, ^, (], Output: [..., F]\n   - Token '+': Stack: [-, ^, (, +], Output: [..., F]\n   - Token 'G': Stack: [-, ^, (, +], Output: [..., F, G]\n   - Token ')': Pop '+' -> Stack: [-, ^], Output: [..., F, G, +]\n   - End of input: Pop remaining stack: '^', then '-' .\n3. Final Postfix: `A B + C * D E - F G + ^ -`."
            }
        ],
        "revision_60s": [
            "Stack is LIFO: push, pop, peek all run in O(1) time.",
            "Parentheses checking: push opening, pop on matching closing; stack must be empty at end.",
            "Infix to Postfix: operands go to output; operators pushed based on precedence.",
            "Postfix evaluation: pop op2, then op1; push (op1 OP op2).",
            "Next Greater Element solved in O(n) using a Monotonic Stack."
        ]
    },

    "queues": {
        "title": "Queues & Circular Queue Implementations",
        "subject": "ds",
        "exam_definition": (
            "A Queue is a linear FIFO (First-In, First-Out) data structure where elements are inserted at the Rear (enqueue) and removed "
            "from the Front (dequeue), optimized via Circular Queue arrays to prevent false overflow."
        ),
        "remember": "Circular Queue Indexing: Front = (Front + 1) % N | Rear = (Rear + 1) % N. Eliminates linear queue memory drift.",
        "core_concept": (
            "Linear array queues suffer from False Overflow: after multiple enqueues and dequeues, the `rear` pointer reaches the array end "
            "even when slots at the beginning are empty. The Circular Queue wraps pointers modulo array capacity $N$, reusing deallocated slots. "
            "Queues model asynchronous buffers, printer spoolers, and Breadth-First Search (BFS)."
        ),
        "key_points": [
            "FIFO Principle: First element enqueued is the first element dequeued.",
            "Linear Queue False Overflow: `rear == MAX - 1` triggers overflow even if `front > 0` has empty slots.",
            "Circular Queue Solution: Uses modulo arithmetic: `rear = (rear + 1) % capacity`.",
            "Circular Queue Full Condition: `(rear + 1) % capacity == front` (reserving 1 empty slot) or maintaining an explicit `count` variable.",
            "Double-Ended Queue (Deque): Allows insertion and deletion at both ends in $O(1)$ time.",
            "Priority Queue: Elements dequeued based on priority value rather than arrival order, implemented via Binary Heaps."
        ],
        "classification": {
            "title": "Types of Queues",
            "items": [
                {"name": "Simple Linear Queue", "desc": "Array or list where elements enter at rear and exit at front. Suffers from false overflow in linear arrays."},
                {"name": "Circular Queue", "desc": "Last position connects back to the first using modulo arithmetic to reuse empty slots."},
                {"name": "Deque (Double-Ended Queue)", "desc": "Supports push/pop at both front and rear ends. Can act as both stack and queue."},
                {"name": "Priority Queue", "desc": "Elements have associated priority; highest priority element is dequeued first (backed by Binary Heap)."}
            ]
        },
        "how_it_works": {
            "title": "Circular Queue Modulo Mechanics",
            "steps": [
                "1. Initialize `front = -1`, `rear = -1`, and fixed capacity $N$.",
                "2. IsEmpty Check: `front == -1`.",
                "3. IsFull Check: `(rear + 1) % N == front`.",
                "4. Enqueue(x): If full, trigger overflow. If empty, set `front = 0, rear = 0`. Else `rear = (rear + 1) % N`. Store `arr[rear] = x`.",
                "5. Dequeue(): If empty, trigger underflow. Store `item = arr[front]`. If `front == rear` (last item), reset `front = -1, rear = -1`. Else `front = (front + 1) % N`. Return `item`."
            ],
            "diagram": "Array of size 5: [ X | X | A | B | C ]\n                  front=2        rear=4\nEnqueue(D): rear = (4 + 1) % 5 = 0 -> [ D | X | A | B | C ] (Wraps around to index 0!)"
        },
        "example": {
            "title": "Circular Queue Implementation in C",
            "scenario": "A circular queue of capacity 5 demonstrating enqueue wrap-around.",
            "code": (
                "#include <stdio.h>\n"
                "#define SIZE 5\n\n"
                "int items[SIZE];\n"
                "int front = -1, rear = -1;\n\n"
                "int isFull() {\n"
                "    return ((rear + 1) % SIZE == front);\n"
                "}\n"
                "int isEmpty() {\n"
                "    return (front == -1);\n"
                "}\n"
                "void enqueue(int element) {\n"
                "    if (isFull()) {\n"
                "        printf(\"Queue is Full!\\n\");\n"
                "        return;\n"
                "    }\n"
                "    if (front == -1) front = 0;\n"
                "    rear = (rear + 1) % SIZE;\n"
                "    items[rear] = element;\n"
                "}\n"
                "int dequeue() {\n"
                "    if (isEmpty()) return -1;\n"
                "    int element = items[front];\n"
                "    if (front == rear) {\n"
                "        front = -1; rear = -1; // Reset\n"
                "    } else {\n"
                "        front = (front + 1) % SIZE;\n"
                "    }\n"
                "    return element;\n"
                "}"
            )
        },
        "comparison": {
            "title": "Linear Queue vs Circular Queue",
            "headers": ["Feature", "Linear Queue (Array)", "Circular Queue (Array)"],
            "rows": [
                ["Memory Utilization", "Poor — empty slots created by dequeue cannot be reused", "Optimal — deallocated slots are reused via modulo wrapping"],
                ["False Overflow", "Occurs frequently when `rear == MAX - 1` even if front slots are empty", "Completely eliminated"],
                ["Pointer Advancement", "`rear = rear + 1`, `front = front + 1`", "`rear = (rear + 1) % N`, `front = (front + 1) % N`"],
                ["Full Condition", "`rear == MAX - 1`", "`(rear + 1) % N == front`"],
                ["Applications", "Simple buffers where array resets regularly", "OS CPU scheduling, network packet buffers, audio ring buffers"]
            ]
        },
        "formulas": [
            {"name": "Circular Queue Next Rear", "formula": "rear = (rear + 1) % Capacity", "explanation": "Calculates wrapped pointer position for enqueue."},
            {"name": "Circular Queue Current Count", "formula": "Count = (rear - front + Capacity) % Capacity + 1", "explanation": "Calculates number of active items in circular queue when non-empty."}
        ],
        "exam_tip": "In circular queue exam traces, remember: When the LAST remaining element is dequeued (`front == rear`), you MUST reset both `front = -1` and `rear = -1` to mark the queue empty!",
        "common_confusion": {
            "wrong": "A circular queue requires a circular linked list.",
            "correct": "Circular queues are most commonly implemented on flat, linear arrays using modulo arithmetic (%) on integer indices.",
            "explanation": "No physical circular hardware or pointers are needed; modulo arithmetic creates the circular abstraction."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is False Overflow in a linear queue and how is it resolved?",
                "a": "False Overflow occurs in a linear array queue when the rear pointer reaches the end of the array (`rear == SIZE - 1`), causing enqueue to report overflow even though previous dequeue operations have created free empty slots at the front. It is resolved using a Circular Queue with modulo arithmetic."
            },
            {
                "marks": "5-Mark Question",
                "q": "Write the conditions for Queue Full and Queue Empty in a Circular Queue of size N.",
                "a": "1. Queue Empty Condition: `front == -1` (or in a design where front always leads, `front == rear` when count is 0).\n2. Queue Full Condition: `(rear + 1) % N == front`.\n   - Explanation: If advancing rear by 1 step modulo $N$ lands exactly on front, the queue has filled all available slots without colliding with front.\n3. Reset on Empty: When `front == rear` during dequeue, resetting `front = -1, rear = -1` returns the queue to initial clean empty state."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain how to implement a Queue using two Stacks. Provide the enqueue and dequeue algorithms and derive their amortized time complexity.",
                "a": "1. Architecture: Maintain two stacks: `Stack1` (inbox) and `Stack2` (outbox).\n2. Enqueue(x) Algorithm:\n   - Simply push element $x$ onto `Stack1`.\n   - Time Complexity: $O(1)$.\n3. Dequeue() Algorithm:\n   - If both `Stack1` and `Stack2` are empty, trigger Queue Underflow.\n   - If `Stack2` is empty:\n     - While `Stack1` is not empty:\n       - Pop from `Stack1` and push onto `Stack2` (this reverses the order from LIFO to FIFO!).\n   - Pop and return top element from `Stack2`.\n4. Amortized Analysis:\n   - Each element is pushed onto Stack1 once ($O(1)$), popped from Stack1 to Stack2 once ($O(1)$), and popped from Stack2 to exit once ($O(1)$).\n   - Total work for $N$ operations is $3N$ steps, giving $O(1)$ Amortized time complexity per dequeue."
            }
        ],
        "revision_60s": [
            "Queue is FIFO: Enqueue at Rear, Dequeue at Front.",
            "Linear queue suffers from false overflow.",
            "Circular queue uses modulo: next = (curr + 1) % N.",
            "Circular full: (rear + 1) % N == front; Empty: front == -1.",
            "Queue using 2 stacks achieves O(1) amortized time."
        ]
    },

    "hashing": {
        "title": "Hashing & Hash Tables",
        "subject": "ds",
        "exam_definition": (
            "A Hash Table is an associative data structure that maps keys to array bucket indices via a mathematical Hash Function, "
            "providing $O(1)$ average time complexity for insert, lookup, and delete operations, resolving collisions via Chaining or Open Addressing."
        ),
        "remember": "Load Factor (alpha) = n / m (n = total keys, m = total table slots). Rehashing triggers when alpha exceeds threshold (typically 0.75).",
        "core_concept": (
            "Direct address tables require memory equal to the universe of all possible keys, which is impossible for large keys like strings. "
            "Hashing compresses large key spaces into a table of size $m$. Because multiple keys can map to the same slot (Pigeonhole Principle), "
            "collisions are mathematically inevitable. Collision resolution strategies are divided into Separate Chaining (linked lists) and "
            "Open Addressing (probing within the table)."
        ),
        "key_points": [
            "Hash Function Properties: Deterministic, uniform distribution (avoids clustering), fast $O(1)$ computation, minimizes collisions.",
            "Load Factor ($\\alpha$): Ratio $\\alpha = n / m$. For open addressing, $\\alpha < 1$; for chaining, $\\alpha$ can be $> 1$.",
            "Separate Chaining: Each bucket holds a linked list of colliding entries. Handles high load factors gracefully; worst-case lookup $O(n)$.",
            "Open Addressing: All elements stored directly in the hash table array. Collisions probed sequentially.",
            "Linear Probing: $h(k, i) = (h'(k) + i) \\pmod m$. Suffers from Primary Clustering (long contiguous blocks of occupied slots).",
            "Quadratic Probing: $h(k, i) = (h'(k) + c_1 i + c_2 i^2) \\pmod m$. Eliminates primary clustering; suffers from Secondary Clustering.",
            "Double Hashing: $h(k, i) = (h_1(k) + i \\cdot h_2(k)) \\pmod m$. Best open addressing method; eliminates clustering."
        ],
        "classification": {
            "title": "Collision Resolution Techniques",
            "items": [
                {"name": "Separate Chaining (Open Hashing)", "desc": "Buckets maintain linked lists or balanced red-black trees (Java 8 HashMap) of colliding keys."},
                {"name": "Linear Probing", "desc": "Searches for next free slot linearly: (hash + i) % m. Simple, but forms primary clusters."},
                {"name": "Quadratic Probing", "desc": "Searches slots using quadratic step: (hash + c1*i + c2*i^2) % m to spread entries."},
                {"name": "Double Hashing", "desc": "Uses secondary hash function as probe step: (h1(k) + i * h2(k)) % m. Minimizes clustering."}
            ]
        },
        "how_it_works": {
            "title": "Collision Resolution via Double Hashing",
            "steps": [
                "1. Compute primary hash: $idx = h_1(k) = k \\pmod m$.",
                "2. If `table[idx]` is empty, insert key at `idx` and terminate.",
                "3. If collision occurs, compute secondary hash step: $step = h_2(k) = R - (k \\pmod R)$, where $R$ is prime $< m$.",
                "4. For probe sequence $i = 1, 2, \\dots, m-1$:\n   - New probe slot: $pos = (idx + i \\times step) \\pmod m$.\n   - If `table[pos]` is empty, insert key and terminate.",
                "5. Deletion in Open Addressing requires marking slot as 'DELETED' (tombstone) to prevent breaking search chains."
            ],
            "diagram": "Key k ──> h1(k) ──[Occupied]──> Step = h2(k) ──> Probe (h1 + 1*h2)%m ──> Probe (h1 + 2*h2)%m ──> Free Slot Found"
        },
        "example": {
            "title": "Linear Probing Numerical Collision Trace",
            "scenario": "Table size $m = 7$, hash function $h(k) = k \\pmod 7$. Insert keys: 10, 20, 5, 8, 15.",
            "code": (
                "Table size m = 7 | h(k) = k % 7\n\n"
                "1. Insert 10: h(10) = 10 % 7 = 3. Slot 3 is empty -> Table[3] = 10\n"
                "2. Insert 20: h(20) = 20 % 7 = 6. Slot 6 is empty -> Table[6] = 20\n"
                "3. Insert 5:  h(5)  = 5 % 7  = 5. Slot 5 is empty -> Table[5] = 5\n"
                "4. Insert 8:  h(8)  = 8 % 7  = 1. Slot 1 is empty -> Table[1] = 8\n"
                "5. Insert 15: h(15) = 15 % 7 = 1. Collision at slot 1!\n"
                "   Linear Probe i=1: (1 + 1) % 7 = 2. Slot 2 is empty -> Table[2] = 15\n\n"
                "Final Table:\n"
                "[0]: empty | [1]: 8 | [2]: 15 | [3]: 10 | [4]: empty | [5]: 5 | [6]: 20"
            )
        },
        "comparison": {
            "title": "Separate Chaining vs Open Addressing",
            "headers": ["Feature", "Separate Chaining", "Open Addressing"],
            "rows": [
                ["Storage Location", "Colliding elements stored outside table in linked lists", "All elements stored directly in main table array"],
                ["Load Factor ($\\alpha$)", "Can exceed 1.0 ($\\alpha > 1$)", "Strictly bounded: $\\alpha < 1.0$ (typically $\\le 0.70$)"],
                ["Deletion Complexity", "Simple node unlinking from linked list", "Requires 'DELETED' tombstone markers to preserve search chains"],
                ["Cache Performance", "Poor (pointer dereferences scatter across RAM)", "High (contiguous array traversal enjoys CPU cache hits)"],
                ["Sensitivity to Load", "Graceful degradation as $\\alpha$ increases", "Performance degrades catastrophically as $\\alpha \\to 1$"]
            ]
        },
        "formulas": [
            {"name": "Load Factor", "formula": "alpha = n / m", "explanation": "Where n is number of stored elements, m is number of table slots."},
            {"name": "Double Hashing Probing Formula", "formula": "h(k, i) = (h1(k) + i * h2(k)) % m", "explanation": "h2(k) must never evaluate to 0 and must be coprime with m."}
        ],
        "exam_tip": "When performing Double Hashing in exams, ensure $h_2(k)$ never evaluates to 0! A common formula used is $h_2(k) = R - (k \\pmod R)$ where $R < m$ is a prime number. If $h_2(k) = 0$, probing would get stuck infinitely in the same slot.",
        "common_confusion": {
            "wrong": "Hash tables guarantee O(1) time complexity in all cases.",
            "correct": "Hash tables guarantee O(1) AVERAGE time complexity. If a pathological input causes all keys to collide into the same bucket, lookup degrades to O(n) worst-case time.",
            "explanation": "Modern engines like Java 8 convert chains to Red-Black Trees when length > 8, improving worst case to O(log n)."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is Primary Clustering in hashing and which collision resolution method causes it?",
                "a": "Primary Clustering is the phenomenon where contiguous occupied slots coalesce into large blocks, causing subsequent colliding keys to probe through increasingly long runs of filled slots. It is caused by Linear Probing."
            },
            {
                "marks": "5-Mark Question",
                "q": "Why is Tombstone / Lazy Deletion necessary in Open Addressing hash tables?",
                "a": "1. Problem: In open addressing, when looking up a key that had collided during insertion, the search algorithm probes until it finds the key or hits an empty slot (which signals the key is absent).\n2. Issue with Naive Deletion: If a slot in the middle of a probe chain is simply cleared to NULL/empty, subsequent lookups for keys inserted after that collision will terminate prematurely at the empty slot and erroneously report that the key does not exist.\n3. Solution: Mark deleted slots with a special dummy 'DELETED' tombstone. The search algorithm continues past tombstones, while insert can overwrite tombstones."
            },
            {
                "marks": "10-Mark Question",
                "q": "Given keys: 50, 700, 76, 85, 92, 73, 101 and table size m = 7 with h1(k) = k % 7 and h2(k) = 5 - (k % 5). Insert using Double Hashing and show detailed step-by-step calculations.",
                "a": "1. Formulas: $h_1(k) = k \\pmod 7$, $h_2(k) = 5 - (k \\pmod 5)$, Probe: $P(k, i) = (h_1(k) + i \\cdot h_2(k)) \\pmod 7$.\n2. Step-by-Step Inserts:\n   - Key 50: $h_1(50) = 50 \\% 7 = 1$. Slot 1 empty -> Table[1] = 50.\n   - Key 700: $h_1(700) = 700 \\% 7 = 0$. Slot 0 empty -> Table[0] = 700.\n   - Key 76: $h_1(76) = 76 \\% 7 = 6$. Slot 6 empty -> Table[6] = 76.\n   - Key 85: $h_1(85) = 85 \\% 7 = 1$. Collision at slot 1!\n     $h_2(85) = 5 - (85 \\% 5) = 5 - 0 = 5$.\n     i=1: $(1 + 1 \\times 5) \\% 7 = 6$. Slot 6 is occupied (76)!\n     i=2: $(1 + 2 \\times 5) \\% 7 = 11 \\% 7 = 4$. Slot 4 is empty -> Table[4] = 85.\n   - Key 92: $h_1(92) = 92 \\% 7 = 1$. Collision at slot 1!\n     $h_2(92) = 5 - (92 \\% 5) = 5 - 2 = 3$.\n     i=1: $(1 + 1 \\times 3) \\% 7 = 4$. Slot 4 occupied (85)!\n     i=2: $(1 + 2 \\times 3) \\% 7 = 7 \\% 7 = 0$. Slot 0 occupied (700)!\n     i=3: $(1 + 3 \\times 3) \\% 7 = 10 \\% 7 = 3$. Slot 3 empty -> Table[3] = 92.\n3. Final Table:\n   [0]: 700, [1]: 50, [2]: empty, [3]: 92, [4]: 85, [5]: empty, [6]: 76."
            }
        ],
        "revision_60s": [
            "Hash tables offer O(1) average lookup, insert, and delete.",
            "Load factor alpha = n / m; triggers rehashing when exceeded.",
            "Chaining handles collisions via linked lists per bucket.",
            "Linear probing causes primary clustering.",
            "Double hashing: h(k, i) = (h1(k) + i*h2(k)) % m eliminates clustering.",
            "Open addressing requires 'DELETED' tombstones to preserve search chains."
        ]
    },

    "trees": {
        "title": "Trees & Binary Tree Traversals",
        "subject": "ds",
        "exam_definition": (
            "A Tree is a hierarchical non-linear data structure consisting of nodes connected by edges, rooted at a primary node "
            "where each node contains data and references to child nodes, traversed recursively via Preorder, Inorder, Postorder, and Level-Order."
        ),
        "remember": "Tree Traversals: Preorder = Root-Left-Right | Inorder = Left-Root-Right | Postorder = Left-Right-Root | Level-Order = BFS (Queue).",
        "core_concept": (
            "Linear data structures (arrays, linked lists) have search vs insertion performance trade-offs. Hierarchical tree structures "
            "model real-world hierarchical relationships (file systems, HTML DOM, compiler ASTs) and enable logarithmic search times. "
            "Binary trees limit each node to at most two children (left and right)."
        ),
        "key_points": [
            "Tree Terminology: Root (top node), Leaf (node with zero children), Height (longest path from node to leaf), Depth (distance from root to node).",
            "Full Binary Tree: Every node has either 0 or 2 children.",
            "Complete Binary Tree: Every level is completely filled, except possibly the last level which is filled strictly from left to right.",
            "Perfect Binary Tree: All internal nodes have 2 children and all leaves are at the exact same depth ($N = 2^{h+1} - 1$).",
            "DFS Traversals: Preorder (Root, L, R), Inorder (L, Root, R), Postorder (L, R, Root) — all execute in $O(n)$ time.",
            "BFS Traversal (Level-Order): Traverses nodes level-by-level horizontally using a FIFO Queue in $O(n)$ time.",
            "Tree Construction Property: A unique binary tree can be reconstructed from Inorder + Preorder OR Inorder + Postorder traversals (Inorder is mandatory!)."
        ],
        "classification": {
            "title": "Binary Tree Classifications",
            "items": [
                {"name": "Full Binary Tree", "desc": "Every node has exactly 0 or 2 children (no node has 1 child)."},
                {"name": "Complete Binary Tree", "desc": "All levels filled except possibly the last, which is filled from left to right (basis for Binary Heaps)."},
                {"name": "Perfect Binary Tree", "desc": "All interior nodes have 2 children and all leaf nodes are at identical depth."},
                {"name": "Degenerate (Skewed) Tree", "desc": "Every internal node has only one child; effectively degenerates into a singly linked list with O(n) height."}
            ]
        },
        "how_it_works": {
            "title": "Constructing Unique Binary Tree from Inorder & Preorder",
            "steps": [
                "1. Preorder sequence: Root is always the FIRST element (`preorder[0]`).",
                "2. Locate root in Inorder sequence: Elements to the left of root form the Left Subtree; elements to the right form the Right Subtree.",
                "3. Count number of elements in Left Subtree ($k$).",
                "4. In Preorder, the next $k$ elements belong to the Left Subtree; the remaining belong to the Right Subtree.",
                "5. Recurse for Left Subtree and Right Subtree to construct root's left and right child pointers."
            ],
            "diagram": "Preorder: [ Root | Left Subtree (k items) | Right Subtree ]\nInorder:  [ Left Subtree (k items) | ROOT | Right Subtree ]"
        },
        "example": {
            "title": "Level-Order (BFS) Traversal Implementation in Java",
            "scenario": "Traverse a binary tree level by level using a FIFO Queue.",
            "code": (
                "void printLevelOrder(TreeNode root) {\n"
                "    if (root == null) return;\n"
                "    Queue<TreeNode> queue = new LinkedList<>();\n"
                "    queue.add(root);\n\n"
                "    while (!queue.isEmpty()) {\n"
                "        TreeNode current = queue.poll();\n"
                "        System.out.print(current.val + \" \");\n\n"
                "        if (current.left != null) queue.add(current.left);\n"
                "        if (current.right != null) queue.add(current.right);\n"
                "    }\n"
                "}"
            )
        },
        "comparison": {
            "title": "Full vs Complete vs Perfect Binary Tree",
            "headers": ["Property", "Full Binary Tree", "Complete Binary Tree", "Perfect Binary Tree"],
            "rows": [
                ["Child Constraint", "Every node has 0 or 2 children", "Every node has 0, 1, or 2 children", "Every non-leaf node has exactly 2 children"],
                ["Leaf Depth", "Leaves can be at varying depths", "Leaves on last level only (left-aligned)", "All leaves at the exact same depth $h$"],
                ["Total Nodes (height h)", "Variable: $2h + 1 \\le N \\le 2^{h+1} - 1$", "$2^h \\le N \\le 2^{h+1} - 1$", "Strictly $N = 2^{h+1} - 1$"],
                ["Array Storage", "Inflexible (sparse with nulls)", "Optimal (compact sequential array with 0 wasted slots)", "Optimal (compact sequential array)"]
            ]
        },
        "formulas": [
            {"name": "Maximum Nodes in Binary Tree of Height h", "formula": "N_max = 2^(h + 1) - 1", "explanation": "Where root is at height h = 0."},
            {"name": "Full Binary Tree Leaf Invariant", "formula": "Leaves = Internal_Nodes + 1", "explanation": "In any full binary tree, L = I + 1."}
        ],
        "exam_tip": "In exam tree reconstruction problems: Can you build a unique tree from Preorder and Postorder? NO! You CANNOT construct a unique binary tree from Preorder and Postorder alone (Inorder is mandatory because it tells you which nodes are on the left vs right).",
        "common_confusion": {
            "wrong": "Height and Depth of a tree node mean the same thing.",
            "correct": "Depth is the number of edges from the ROOT down to that node (root depth = 0). Height is the number of edges on the longest path from that node down to a LEAF (leaf height = 0).",
            "explanation": "Depth measures downward from root; Height measures upward from leaves."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the relationship between the number of leaf nodes and internal nodes with two children in a binary tree?",
                "a": "In any non-empty binary tree, the number of leaf nodes ($L$) is always exactly one greater than the number of internal nodes with two children ($n_2$): $L = n_2 + 1$."
            },
            {
                "marks": "5-Mark Question",
                "q": "Why is an Inorder traversal mandatory to uniquely reconstruct a binary tree?",
                "a": "1. Reason: Preorder tells us the root of the tree (it is always the first node), but gives no information on where the left subtree ends and the right subtree begins.\n2. Role of Inorder: In Inorder traversal (Left, Root, Right), all nodes appearing before the root belong strictly to the left subtree, and all nodes appearing after the root belong strictly to the right subtree.\n3. Conclusion: Without Inorder, one cannot partition child subtrees, resulting in multiple ambiguous tree topologies."
            },
            {
                "marks": "10-Mark Question",
                "q": "Construct a binary tree given: Inorder = [D, B, E, A, F, C] and Preorder = [A, B, D, E, C, F]. Write its Postorder traversal.",
                "a": "1. Step 1: Preorder root is 'A'.\n2. Step 2: Locate 'A' in Inorder: [D, B, E] is Left Subtree, [F, C] is Right Subtree.\n3. Step 3 (Left Subtree):\n   - Preorder sub-sequence: [B, D, E]. Root is 'B'.\n   - Inorder sub-sequence: [D, B, E]. 'D' is to left of 'B', 'E' is to right of 'B'.\n   - Left child of 'A' is 'B', left child of 'B' is 'D', right child of 'B' is 'E'.\n4. Step 4 (Right Subtree):\n   - Preorder sub-sequence: [C, F]. Root is 'C'.\n   - Inorder sub-sequence: [F, C]. 'F' is to left of 'C'.\n   - Right child of 'A' is 'C', left child of 'C' is 'F', right child of 'C' is NULL.\n5. Constructed Tree:\n        A\n       / \\\n      B   C\n     / \\  /\n    D   E F\n6. Postorder Traversal (Left, Right, Root): D, E, B, F, C, A."
            }
        ],
        "revision_60s": [
            "Binary tree: each node has at most 2 children.",
            "Preorder = Root-L-R; Inorder = L-Root-R; Postorder = L-R-Root.",
            "Level-order = BFS implemented with a FIFO Queue.",
            "Reconstruction requires Inorder + (Preorder OR Postorder).",
            "In any binary tree: Leaf Nodes = Nodes with 2 children + 1."
        ]
    },

    "bst": {
        "title": "Binary Search Trees (BST) & AVL Trees",
        "subject": "ds",
        "exam_definition": (
            "A Binary Search Tree (BST) is a node-based binary tree data structure where all keys in a node's left subtree are strictly "
            "less than the node's key, and all keys in the right subtree are strictly greater, providing $O(\\log n)$ operations in balanced BSTs (AVL/Red-Black)."
        ),
        "remember": "BST Inorder Invariant: An Inorder traversal of ANY valid BST always yields keys in strictly ASCENDING sorted order!",
        "core_concept": (
            "Unsorted linked lists require $O(n)$ search time. A standard BST provides $O(\\log n)$ search by halving the search space at each branch. "
            "However, inserting sorted keys into an unaugmented BST causes it to degenerate into a skewed linked list of height $O(n)$. "
            "Self-balancing AVL Trees enforce the height-balance property: $|Height(Left) - Height(Right)| \\le 1$, maintaining $O(\\log n)$ worst-case guarantees via tree rotations."
        ),
        "key_points": [
            "BST Invariant: $\\forall x \\in \\text{LeftSubtree}(u): x.\\text{key} < u.\\text{key}$, and $\\forall y \\in \\text{RightSubtree}(u): y.\\text{key} > u.\\text{key}$.",
            "BST Deletion Cases: 1) Leaf node (delete directly), 2) Node with 1 child (replace with child), 3) Node with 2 children (replace with Inorder Successor or Inorder Predecessor).",
            "Inorder Successor: The smallest node in the right subtree (leftmost child of right child).",
            "AVL Tree Balance Factor: $BF(node) = Height(LeftSubtree) - Height(RightSubtree) \\in \\{-1, 0, +1\\}$.",
            "AVL Tree Rotations: LL Rotation (Single Right), RR Rotation (Single Left), LR Rotation (Left-then-Right), RL Rotation (Right-then-Left).",
            "Time Complexity: Balanced BST (AVL): Search, Insert, Delete all $O(\\log n)$. Degenerate BST: $O(n)$."
        ],
        "classification": {
            "title": "AVL Tree Rotation Types",
            "items": [
                {"name": "LL Rotation (Right Rotation)", "desc": "Triggered by insertion into left child of left subtree (BF = +2, child BF = +1). Single right rotation balances tree."},
                {"name": "RR Rotation (Left Rotation)", "desc": "Triggered by insertion into right child of right subtree (BF = -2, child BF = -1). Single left rotation balances tree."},
                {"name": "LR Rotation (Double Rotation)", "desc": "Triggered by insertion into right child of left subtree (BF = +2, child BF = -1). Rotate left on child, then right on parent."},
                {"name": "RL Rotation (Double Rotation)", "desc": "Triggered by insertion into left child of right subtree (BF = -2, child BF = +1). Rotate right on child, then left on parent."}
            ]
        },
        "how_it_works": {
            "title": "BST Node Deletion with Two Children",
            "steps": [
                "1. Search tree recursively to locate the target node $Z$ to delete.",
                "2. If $Z$ has no children, set parent pointer to null and deallocate $Z$.",
                "3. If $Z$ has 1 child, update parent pointer to bypass $Z$ and point directly to $Z$'s child.",
                "4. If $Z$ has 2 children:\n   - Find Inorder Successor $S$ (minimum node in $Z$'s right subtree).\n   - Copy $S$'s key into $Z$'s node.\n   - Recursively delete node $S$ from the right subtree (since $S$ is guaranteed to have at most 1 right child!)."
            ],
            "diagram": "Delete Node (50) with 2 children:\n       50                 60 (Successor copied here)\n      /  \\               /  \\\n     30   70     ──>    30   70\n         /                  /\n       (60)                65 (Old 60 deleted)\n         \\\n          65"
        },
        "example": {
            "title": "AVL Tree Right Rotation (LL Imbalance)",
            "scenario": "Node 30 inserted into tree with root 50 and left child 40, causing LL imbalance at 50.",
            "code": (
                "// Before Rotation (LL Imbalance at 50, BF = +2):\n"
                "//        50 (BF = +2)\n"
                "//       /\n"
                "//      40 (BF = +1)\n"
                "//     /\n"
                "//    30 (BF = 0)\n\n"
                "// Right Rotation on Node 50:\n"
                "TreeNode rightRotate(TreeNode y) {\n"
                "    TreeNode x = y.left;        // x is 40\n"
                "    TreeNode T2 = x.right;      // T2 is null\n"
                "    x.right = y;                // 40 becomes new parent of 50\n"
                "    y.left = T2;\n"
                "    // Update heights...\n"
                "    return x;                   // x (40) is new root\n"
                "}\n\n"
                "// After Rotation (Balanced! BF = 0 for all):\n"
                "//        40\n"
                "//       /  \\\n"
                "//      30   50"
            )
        },
        "comparison": {
            "title": "Standard BST vs AVL Tree vs Red-Black Tree",
            "headers": ["Feature", "Standard BST", "AVL Tree", "Red-Black Tree"],
            "rows": [
                ["Balance Condition", "None (can degenerate into linear linked list)", "Strict: $|Height(L) - Height(R)| \\le 1$", "Relaxed: Path to farthest leaf $\\le 2 \\times$ path to nearest leaf"],
                ["Search Time (Worst)", "$O(n)$ (skewed)", "$O(\\log n)$ (fastest search due to strict balance)", "$O(\\log n)$"],
                ["Insertion / Deletion", "$O(n)$ worst-case", "$O(\\log n)$ (may require multiple rotations on delete)", "$O(\\log n)$ (at most 2 rotations on insert/delete)"],
                ["Practical Usage", "Simple educational structures", "Lookup-intensive systems (dictionaries)", "Insert/Delete-heavy systems (C++ std::map, Java TreeMap, Linux kernel scheduler)"]
            ]
        },
        "formulas": [
            {"name": "AVL Balance Factor", "formula": "BF(u) = Height(u.left) - Height(u.right)", "explanation": "Valid AVL node must satisfy BF in {-1, 0, 1}."},
            {"name": "Minimum Nodes in AVL Tree of Height h", "formula": "N(h) = N(h - 1) + N(h - 2) + 1", "explanation": "N(0) = 1, N(1) = 2, N(2) = 4, N(3) = 7 (Fibonacci-like growth)."}
        ],
        "exam_tip": "Remember: An Inorder traversal of ANY valid BST produces elements in strictly ascending sorted order. If an exam gives you a Preorder traversal of a BST, you can derive its Inorder traversal simply by sorting the keys!",
        "common_confusion": {
            "wrong": "To delete a BST node with two children, replace it with any child.",
            "correct": "Replacing with an arbitrary child violates the BST ordering invariant. You MUST replace it with its Inorder Successor (smallest key in right subtree) or Inorder Predecessor (largest key in left subtree).",
            "explanation": "Only the Inorder Successor or Predecessor preserves the property that all left descendants are smaller and right descendants are greater."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is an AVL Tree and what is its Balance Factor invariant?",
                "a": "An AVL tree is a self-balancing binary search tree where the difference between the heights of the left and right subtrees (the Balance Factor, $BF = h_L - h_R$) for every node is strictly bounded within $\\{-1, 0, +1\\}$, guaranteeing $O(\\log n)$ search height."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the four rotation types in an AVL Tree with their triggering imbalance conditions.",
                "a": "1. LL Rotation (Single Right): Inserted into left subtree of left child ($BF = +2$, child $BF = +1$). Rotate parent right.\n2. RR Rotation (Single Left): Inserted into right subtree of right child ($BF = -2$, child $BF = -1$). Rotate parent left.\n3. LR Rotation (Double: Left then Right): Inserted into right subtree of left child ($BF = +2$, child $BF = -1$). Rotate child left, then parent right.\n4. RL Rotation (Double: Right then Left): Inserted into left subtree of right child ($BF = -2$, child $BF = +1$). Rotate child right, then parent left."
            },
            {
                "marks": "10-Mark Question",
                "q": "Insert the keys: 21, 26, 30, 9, 4, 14, 28 into an initially empty AVL Tree. Show every step, identifying all imbalances and required rotations.",
                "a": "1. Insert 21: [21] (BF=0)\n2. Insert 26: 21 -> right 26 (BF(21) = -1)\n3. Insert 30: 21 -> 26 -> 30. Imbalance at 21 (BF = -2, 26 BF = -1) -> RR Imbalance!\n   - Perform Single Left Rotation on 21: Root becomes 26, left child 21, right child 30.\n4. Insert 9: 26 -> 21 -> left 9 (BF(26) = +1, BF(21) = +1)\n5. Insert 4: 21 -> 9 -> 4. Imbalance at 21 (BF = +2, 9 BF = +1) -> LL Imbalance!\n   - Perform Single Right Rotation on 21: Node 9 becomes left child of 26, children are 4 and 21.\n6. Insert 14: 26 -> 9 -> 21 -> left 14. Tree remains balanced!\n7. Insert 28: 26 -> 30 -> left 28. Tree remains balanced!\n8. Final Balanced AVL Tree Structure:\n         26\n       /    \\\n      9      30\n     / \\    /\n    4  21  28\n       /\n      14"
            }
        ],
        "revision_60s": [
            "BST invariant: Left < Root < Right.",
            "BST Inorder traversal ALWAYS yields sorted ascending order.",
            "Deleting node with 2 children: replace with Inorder Successor (min of right subtree).",
            "AVL balance factor = Height(Left) - Height(Right) in {-1, 0, +1}.",
            "4 AVL rotations: LL (Right), RR (Left), LR (Left-Right), RL (Right-Left)."
        ]
    },

    "heaps": {
        "title": "Heaps & Priority Queues",
        "subject": "ds",
        "exam_definition": (
            "A Binary Heap is a complete binary tree stored compactly in a contiguous 1D array satisfying the Heap Property "
            "(Max-Heap: parent $\\ge$ children; Min-Heap: parent $\\le$ children), supporting $O(1)$ peek, $O(\\log n)$ insert/extract, and $O(n)$ build."
        ),
        "remember": "Heap Array Indexing (0-based): Parent = (i - 1)/2 | Left Child = 2i + 1 | Right Child = 2i + 2.",
        "core_concept": (
            "Because a binary heap is structurally a Complete Binary Tree, it can be mapped into a 1D array with zero pointer overhead "
            "and zero wasted memory slots. Priority queues backed by binary heaps are fundamental in Dijkstra's Shortest Path algorithm, "
            "Prim's Minimum Spanning Tree algorithm, and Heap Sort."
        ),
        "key_points": [
            "Max-Heap Invariant: $A[\\text{parent}(i)] \\ge A[i]$ for all nodes $i > 0$. Maximum element is always at the root ($A[0]$).",
            "Min-Heap Invariant: $A[\\text{parent}(i)] \\le A[i]$ for all nodes $i > 0$. Minimum element is always at the root ($A[0]$).",
            "0-Based Array Mapping: Left child: $2i + 1$, Right child: $2i + 2$, Parent: $\\lfloor (i - 1) / 2 \\rfloor$.",
            "Heapify (Sift-Down): Restores heap property downward in $O(\\log n)$ time.",
            "Insert (Sift-Up): Appends element at the end of the array and bubbles it up to its correct rank in $O(\\log n)$ time.",
            "Build-Heap Efficiency: Building a heap from an unsorted array of size $n$ takes $O(n)$ time using bottom-up heapification, NOT $O(n \\log n)$.",
            "Heap Sort: In-place comparison sort running in guaranteed $O(n \\log n)$ time and $O(1)$ auxiliary memory."
        ],
        "classification": {
            "title": "Heap Data Structure Variants",
            "items": [
                {"name": "Max-Heap", "desc": "Every parent node is greater than or equal to its children. Root holds the absolute maximum key."},
                {"name": "Min-Heap", "desc": "Every parent node is less than or equal to its children. Root holds the absolute minimum key."},
                {"name": "Binary Heap", "desc": "Complete binary tree with 2 children per node, mapped sequentially to a contiguous array."},
                {"name": "Fibonacci Heap", "desc": "Advanced heap supporting O(1) amortized insert, find-min, and decrease-key operations."}
            ]
        },
        "how_it_works": {
            "title": "Extract-Max and Heapify Sift-Down Process",
            "steps": [
                "1. Save root element $A[0]$ as the extracted maximum.",
                "2. Move the last leaf element $A[n-1]$ to the root position $A[0]$ and decrement heap size by 1.",
                "3. Heapify Downward from root (index $i = 0$):\n   - Compute left child index $2i + 1$ and right child index $2i + 2$.\n   - Identify the largest key among parent $A[i]$, left child, and right child.\n   - If the largest is child $C$, swap $A[i]$ and $A[C]$.\n   - Recursively continue sift-down at index $C$.\n4. Terminate when parent is greater than both children or a leaf is reached."
            ],
            "diagram": "Extract Root (90) ──> Copy Last Leaf (12) to Root ──> Sift-Down 12 with Children (80, 70) ──> Swap 12 & 80"
        },
        "example": {
            "title": "Heapify Algorithm in Python",
            "scenario": "Bottom-up Max-Heapify implementation for array representation.",
            "code": (
                "def heapify(arr, n, i):\n"
                "    largest = i\n"
                "    left = 2 * i + 1\n"
                "    right = 2 * i + 2\n\n"
                "    if left < n and arr[left] > arr[largest]:\n"
                "        largest = left\n"
                "    if right < n and arr[right] > arr[largest]:\n"
                "        largest = right\n\n"
                "    if largest != i:\n"
                "        arr[i], arr[largest] = arr[largest], arr[i] # Swap\n"
                "        heapify(arr, n, largest) # Recurse down\n\n"
                "def build_max_heap(arr):\n"
                "    n = len(arr)\n"
                "    # Start from last non-leaf node (n//2 - 1) down to 0\n"
                "    for i in range(n // 2 - 1, -1, -1):\n"
                "        heapify(arr, n, i)"
            )
        },
        "comparison": {
            "title": "Binary Heap vs Binary Search Tree (BST)",
            "headers": ["Feature", "Binary Heap (Min/Max Heap)", "Binary Search Tree (BST)"],
            "rows": [
                ["Ordering Property", "Vertical ordering: Parent $\\ge$ Children (no left vs right order)", "Horizontal ordering: Left < Root < Right"],
                ["Array Storage", "Extremely compact in 1D array (zero pointer overhead)", "Requires dynamic nodes with left/right pointers"],
                ["Find Minimum", "$O(1)$ in Min-Heap (at root $A[0]$)", "$O(\\log n)$ (leftmost leaf node)"],
                ["Arbitrary Search", "$O(n)$ (must scan entire array; no horizontal order)", "$O(\\log n)$ in balanced BST"],
                ["Build Time", "$O(n)$ using bottom-up heapify", "$O(n \\log n)$ via sequential insertions"]
            ]
        },
        "formulas": [
            {"name": "Heap Array Indexing Formulas", "formula": "Parent(i) = (i - 1)//2 | Left(i) = 2i + 1 | Right(i) = 2i + 2", "explanation": "Applies for 0-based indexing without wasted slots."},
            {"name": "Build-Heap Mathematical Complexity", "formula": "Sum_{h=0}^{floor(log n)} (n / 2^(h+1)) * O(h) = O(n)", "explanation": "Converges to O(n) using arithmetic-geometric series."}
        ],
        "exam_tip": "Why is Build-Heap $O(n)$ instead of $O(n \\log n)$? Because most nodes are near the bottom of the tree! In a binary tree with $n$ nodes, $n/2$ nodes are leaves (height 0, requiring 0 work), $n/4$ nodes are at height 1 (1 swap), and only 1 node is at height $\\log n$. The summation converges to $O(n)$.",
        "common_confusion": {
            "wrong": "In a Max-Heap, the left child is always greater than the right child.",
            "correct": "There is ZERO ordering relationship between sibling nodes or between left and right subtrees in a heap.",
            "explanation": "A heap only enforces that parent >= children; the left child can be greater, smaller, or equal to the right child."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the time complexity of building a Binary Heap of n elements and why?",
                "a": "Building a binary heap takes $O(n)$ time using bottom-up heapification starting at the last non-leaf node ($n/2 - 1$). Although individual sift-down steps cost $O(\\log n)$, the vast majority of nodes are concentrated at the lowest levels of the tree where heights are tiny, causing the sum $\\sum_{h=0}^{\\log n} \\frac{n}{2^h} h$ to converge to $O(n)$."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain Heap Sort with its algorithm steps and analyze its time and space complexity.",
                "a": "1. Step 1 (Build Max-Heap): Transform the unsorted array into a Max-Heap in $O(n)$ time.\n2. Step 2 (Extract and Swap):\n   - Loop for $i = n - 1$ down to 1:\n     - Swap root $A[0]$ (current maximum) with the last element $A[i]$.\n     - Reduce the effective heap size by 1 (locking the maximum into its final sorted position at array tail).\n     - Call `heapify(A, i, 0)` on the root to restore heap property ($O(\\log n)$ work).\n3. Complexity: Step 1 is $O(n)$, Step 2 executes $(n-1)$ heapify calls of $O(\\log n)$ each. Total Time = $O(n \\log n)$ in all cases (worst, average, best). Space = $O(1)$ auxiliary memory (in-place)."
            },
            {
                "marks": "10-Mark Question",
                "q": "Given array: [4, 10, 3, 5, 1], build a Max-Heap step-by-step using bottom-up heapify. Then show the extraction of the first two maximum elements.",
                "a": "1. Initial Array: `[4, 10, 3, 5, 1]`, $n = 5$.\n   - Last non-leaf node = $\\lfloor 5/2 \\rfloor - 1 = 1$ (value 10).\n2. Build Heap Trace:\n   - Heapify at index 1 (val 10): Children are index 3 (5) and index 4 (1). Largest is 10. No swap.\n   - Heapify at index 0 (val 4): Children are index 1 (10) and index 2 (3). Largest is index 1 (10).\n     - Swap $A[0]$ and $A[1]$: Array becomes `[10, 4, 3, 5, 1]`.\n     - Recurse heapify at index 1 (val 4): Children are 5 and 1. Largest is 5.\n     - Swap $A[1]$ and $A[3]$: Array becomes `[10, 5, 3, 4, 1]`.\n   - Max-Heap Built: `[10, 5, 3, 4, 1]`.\n3. Extract First Maximum (10):\n   - Swap root (10) with last element (1): Array = `[1, 5, 3, 4 | 10]`, size = 4.\n   - Heapify root (1): Children are 5 and 3. Swap with 5 -> `[5, 1, 3, 4]`.\n   - Sift-down 1: Child is 4. Swap with 4 -> `[5, 4, 3, 1 | 10]`.\n   - Extracted Max = 10.\n4. Extract Second Maximum (5):\n   - Swap root (5) with last active (1): Array = `[1, 4, 3 | 5, 10]`, size = 3.\n   - Heapify root (1): Children are 4 and 3. Swap with 4 -> `[4, 1, 3 | 5, 10]`.\n   - Extracted Max = 5."
            }
        ],
        "revision_60s": [
            "Binary Heap is a Complete Binary Tree stored in a 1D array.",
            "Indexing: Left = 2i + 1, Right = 2i + 2, Parent = (i - 1)//2.",
            "Max-Heap: parent >= children; Min-Heap: parent <= children.",
            "Build-Heap takes O(n) time using bottom-up heapification.",
            "Heap Sort runs in O(n log n) time and O(1) auxiliary space."
        ]
    },

    "graphs": {
        "title": "Graphs: BFS, DFS & Shortest Path Algorithms",
        "subject": "ds",
        "exam_definition": (
            "A Graph $G = (V, E)$ is a non-linear data structure consisting of a set of vertices (nodes) $V$ and a set of edges $E$ "
            "connecting vertex pairs, traversed via BFS and DFS, with shortest paths computed via Dijkstra and Bellman-Ford."
        ),
        "remember": "Dijkstra: Greedy, requires non-negative edges, O((V + E) log V). Bellman-Ford: Dynamic Programming, handles negative edges, detects negative cycles, O(V * E).",
        "core_concept": (
            "Graphs model complex networks: road systems, computer networks, social graphs, and state spaces. Graphs can be Directed/Undirected, "
            "and Weighted/Unweighted. Traversal algorithms (BFS using Queue, DFS using Stack/Recursion) visit all reachable nodes in $O(V + E)$ time. "
            "Dijkstra computes single-source shortest paths on non-negative graphs; Bellman-Ford relaxes all edges $V-1$ times to handle negative weights."
        ),
        "key_points": [
            "Representations: Adjacency Matrix ($O(V^2)$ space, $O(1)$ edge query) vs Adjacency List ($O(V + E)$ space, optimal for sparse graphs).",
            "Breadth-First Search (BFS): Level-by-level traversal using a Queue; finds shortest path in unweighted graphs in $O(V + E)$ time.",
            "Depth-First Search (DFS): Deep branch traversal using Recursion/Stack; solves cycle detection and topological sorting in $O(V + E)$ time.",
            "Topological Sort: Linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every edge $u \\to v$, $u$ comes before $v$.",
            "Dijkstra's Algorithm: Greedy shortest path using Min-Heap priority queue in $O((V + E) \\log V)$ time; fails on negative weight edges.",
            "Bellman-Ford Algorithm: Relaxes all $|E|$ edges $|V|-1$ times in $O(V \\cdot E)$ time; detects negative weight cycles if a distance can still decrease on the $V$-th pass."
        ],
        "classification": {
            "title": "Graph Algorithm Paradigms",
            "items": [
                {"name": "BFS Traversal", "desc": "Uses FIFO Queue. Computes unweighted shortest path and connected components in O(V + E)."},
                {"name": "DFS Traversal", "desc": "Uses LIFO Stack/Recursion. Solves cycle detection, path finding, and topological sorting in O(V + E)."},
                {"name": "Dijkstra's Algorithm", "desc": "Greedy single-source shortest path for non-negative edge weights using Min-Heap. Time: O((V + E) log V)."},
                {"name": "Bellman-Ford Algorithm", "desc": "Dynamic programming shortest path handling negative edge weights and negative cycle detection. Time: O(V * E)."},
                {"name": "Floyd-Warshall Algorithm", "desc": "All-pairs shortest path dynamic programming matrix algorithm. Time: O(V^3)."}
            ]
        },
        "how_it_works": {
            "title": "Dijkstra's Shortest Path Algorithm Flow",
            "steps": [
                "1. Initialize `dist[source] = 0` and `dist[v] = infinity` for all other vertices $v \\in V$.",
                "2. Insert `(0, source)` into Min-Heap priority queue.",
                "3. While priority queue is not empty:\n   - Extract vertex $u$ with minimum distance `d`.\n   - If `d > dist[u]`, continue (stale entry).\n   - For each neighbor $v$ of $u$ with edge weight $w$:\n     - Edge Relaxation: If `dist[u] + w < dist[v]`:\n       - Update `dist[v] = dist[u] + w`.\n       - Insert `(dist[v], v)` into priority queue.\n4. Output `dist[]` array containing minimum distances from source."
            ],
            "diagram": "Extract Min-Distance Node u ──> Relax Edge (u, v): dist[u] + w < dist[v] ? ──[YES]──> Update dist[v] & Push to Min-Heap"
        },
        "example": {
            "title": "Dijkstra's Algorithm Implementation in Python",
            "scenario": "Single-source shortest path using heapq on an adjacency list.",
            "code": (
                "import heapq\n\n"
                "def dijkstra(graph, num_v, source):\n"
                "    dist = [float('inf')] * num_v\n"
                "    dist[source] = 0\n"
                "    pq = [(0, source)] # (distance, vertex)\n\n"
                "    while pq:\n"
                "        d, u = heapq.heappop(pq)\n"
                "        if d > dist[u]:\n"
                "            continue\n\n"
                "        for v, weight in graph[u]:\n"
                "            if dist[u] + weight < dist[v]: # Edge Relaxation\n"
                "                dist[v] = dist[u] + weight\n"
                "                heapq.heappush(pq, (dist[v], v))\n"
                "    return dist"
            )
        },
        "comparison": {
            "title": "Dijkstra's vs Bellman-Ford vs Floyd-Warshall",
            "headers": ["Algorithm", "Type", "Edge Weights", "Time Complexity", "Negative Cycle Detection"],
            "rows": [
                ["Dijkstra", "Single-Source Shortest Path (Greedy)", "Strictly Non-negative ($w \\ge 0$)", "$O((V + E) \\log V)$", "Cannot detect (fails/loops indefinitely)"],
                ["Bellman-Ford", "Single-Source Shortest Path (DP)", "Negative & Positive weights", "$O(V \\cdot E)$", "Yes: relaxation on $V$-th pass proves negative cycle"],
                ["Floyd-Warshall", "All-Pairs Shortest Path (DP)", "Negative & Positive weights", "$O(V^3)$", "Yes: negative diagonal entries $dist[i][i] < 0$"]
            ]
        },
        "formulas": [
            {"name": "Edge Relaxation Condition", "formula": "if dist[u] + weight(u, v) < dist[v]: dist[v] = dist[u] + weight(u, v)", "explanation": "Fundamental step in Dijkstra, Bellman-Ford, and DAG shortest path."},
            {"name": "Handshaking Lemma", "formula": "Sum of degrees of all vertices = 2 * |E|", "explanation": "Every edge contributes exactly 2 to the sum of vertex degrees."}
        ],
        "exam_tip": "In exam questions asking 'Why does Dijkstra fail on negative weight edges?': Give a simple 3-node counterexample: $A \\to B$ (weight 5), $A \\to C$ (weight 2), $C \\to B$ (weight -4). Dijkstra visits $C$ first, then $B$ with distance 5, locking $B$ as visited. It never updates $B$ to $2 + (-4) = -2$!",
        "common_confusion": {
            "wrong": "BFS can find the shortest path in any weighted graph.",
            "correct": "Standard BFS finds the shortest path ONLY in UNWEIGHTED graphs (or graphs where all edges have identical weight).",
            "explanation": "In weighted graphs, a path with more edges can have a smaller total weight than a direct single edge; Dijkstra is required."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is Topological Sorting and what type of graph is it defined for?",
                "a": "Topological Sorting is a linear ordering of vertices such that for every directed edge $u \\to v$, vertex $u$ appears before vertex $v$ in the ordering. It is defined ONLY for Directed Acyclic Graphs (DAGs); it is impossible if the graph contains a cycle."
            },
            {
                "marks": "5-Mark Question",
                "q": "How does the Bellman-Ford algorithm detect a negative weight cycle?",
                "a": "1. In any graph with $|V|$ vertices and no negative cycles, the shortest simple path contains at most $|V| - 1$ edges.\n2. Bellman-Ford relaxes all $|E|$ edges exactly $|V| - 1$ times, after which all shortest path distances are guaranteed to converge.\n3. Negative Cycle Check: Run a $V$-th pass over all edges. If for any edge $(u, v)$ with weight $w$, we find `dist[u] + w < dist[v]`, it mathematically proves that a negative weight cycle exists in the graph, as distances can decrease indefinitely."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain Prim's and Kruskal's algorithms for Minimum Spanning Trees (MST). Compare their approaches, time complexities, and suitability for dense vs sparse graphs.",
                "a": "1. Minimum Spanning Tree (MST): A subset of edges connecting all $|V|$ vertices with no cycles having minimal total edge weight ($|V| - 1$ edges).\n2. Kruskal's Algorithm (Edge-centric):\n   - Sort all $|E|$ edges in non-decreasing order of weight ($O(E \\log E)$).\n   - Use Disjoint Set Union (DSU / Union-Find) to process edges sequentially.\n   - If adding edge $(u, v)$ connects two different disjoint sets (does not form a cycle), include it in the MST and union the sets.\n   - Time Complexity: $O(E \\log E) = O(E \\log V)$. Best suited for Sparse Graphs ($E \\ll V^2$).\n3. Prim's Algorithm (Vertex-centric):\n   - Start from an arbitrary root vertex. Maintain a cut dividing visited from unvisited vertices.\n   - At each step, use a Min-Heap to select the minimum weight crossing edge connecting a visited vertex to an unvisited vertex.\n   - Add chosen vertex to visited set; update neighbor key weights.\n   - Time Complexity: $O((V + E) \\log V)$ using Min-Heap. Best suited for Dense Graphs ($E \\approx V^2$)."
            }
        ],
        "revision_60s": [
            "Graph representations: Adjacency List O(V + E) space; Matrix O(V^2) space.",
            "BFS uses Queue; finds shortest path in unweighted graphs.",
            "DFS uses Stack/Recursion; solves cycle detection and topological sorting.",
            "Dijkstra: Greedy, non-negative weights, O((V + E) log V) via Min-Heap.",
            "Bellman-Ford: relaxes all edges V-1 times; detects negative cycles in O(V * E).",
            "Kruskal uses DSU (edges); Prim uses Min-Heap (vertices)."
        ]
    },

    "sorting": {
        "title": "Sorting Algorithms & Stability",
        "subject": "ds",
        "exam_definition": (
            "Sorting is the algorithmic arrangement of elements in a specified comparison order (ascending or descending), "
            "categorized by time/space complexity, stability (preserving relative order of equal keys), and adaptiveness."
        ),
        "remember": "Stable Sorts: Merge Sort, Insertion Sort, Bubble Sort. Unstable Sorts: QuickSort, HeapSort, Selection Sort.",
        "core_concept": (
            "Comparison-based sorting algorithms have a fundamental mathematical lower bound of $\\Omega(n \\log n)$ time. "
            "Algorithms like QuickSort provide fastest in-practice cache performance despite an $O(n^2)$ worst case; Merge Sort guarantees "
            "$O(n \\log n)$ time and stability at the cost of $O(n)$ auxiliary memory; non-comparison sorts (Counting Sort, Radix Sort) "
            "achieve linear $O(n + k)$ time by exploiting key boundaries."
        ),
        "key_points": [
            "Stability: A sorting algorithm is Stable if elements with equal keys maintain their original relative input order.",
            "Comparison Sort Lower Bound: $\\Omega(n \\log n)$ decision tree depth theorem.",
            "QuickSort: Divide-and-conquer using a Pivot; average $O(n \\log n)$, worst-case $O(n^2)$ on already-sorted arrays without randomized pivot.",
            "MergeSort: Divide-and-conquer splitting into halves; guaranteed $O(n \\log n)$ in all cases; stable; requires $O(n)$ extra memory.",
            "HeapSort: Builds Max-Heap and repeatedly swaps root to end; guaranteed $O(n \\log n)$ in-place ($O(1)$ space); unstable.",
            "Linear Non-Comparison Sorts: Counting Sort ($O(n + k)$), Radix Sort ($O(d \\cdot (n + k))$) bypass the comparison lower bound."
        ],
        "classification": {
            "title": "Sorting Algorithm Categories",
            "items": [
                {"name": "Quadratic Sorts O(n^2)", "desc": "Bubble Sort, Selection Sort, Insertion Sort. Simple; Insertion Sort is optimal for small or nearly sorted arrays."},
                {"name": "Log-Linear Comparison Sorts O(n log n)", "desc": "Merge Sort (guaranteed, stable), QuickSort (fastest cache locality, unstable), Heap Sort (in-place, unstable)."},
                {"name": "Linear Non-Comparison Sorts O(n)", "desc": "Counting Sort, Radix Sort, Bucket Sort. Bypass decision tree lower bound by exploiting integer key properties."}
            ]
        },
        "how_it_works": {
            "title": "Lomuto Partitioning in QuickSort",
            "steps": [
                "1. Choose rightmost element as pivot: $pivot = arr[high]$.",
                "2. Initialize partition index pointer: $i = low - 1$.",
                "3. Loop $j$ from $low$ to $high - 1$:\n   - If $arr[j] \\le pivot$:\n     - Increment $i$.\n     - Swap $arr[i]$ with $arr[j]$.",
                "4. Swap $arr[i + 1]$ with $arr[high]$ (places pivot in its exact final sorted position).",
                "5. Return pivot index $i + 1$."
            ],
            "diagram": "[ Elements <= Pivot | Elements > Pivot | Unexamined | Pivot ]\n low                i                   j            high"
        },
        "example": {
            "title": "Merge Sort Algorithm Implementation in Java",
            "scenario": "Divide-and-conquer merge sort implementation.",
            "code": (
                "void mergeSort(int[] arr, int l, int r) {\n"
                "    if (l < r) {\n"
                "        int m = l + (r - l) / 2;\n"
                "        mergeSort(arr, l, m);       // Sort left half\n"
                "        mergeSort(arr, m + 1, r);   // Sort right half\n"
                "        merge(arr, l, m, r);        // Merge sorted halves\n"
                "    }\n"
                "}\n"
                "void merge(int[] arr, int l, int m, int r) {\n"
                "    int n1 = m - l + 1, n2 = r - m;\n"
                "    int[] L = new int[n1]; int[] R = new int[n2];\n"
                "    for (int i = 0; i < n1; i++) L[i] = arr[l + i];\n"
                "    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];\n"
                "    int i = 0, j = 0, k = l;\n"
                "    while (i < n1 && j < n2) {\n"
                "        if (L[i] <= R[j]) arr[k++] = L[i++]; // <= ensures STABILITY\n"
                "        else arr[k++] = R[j++];\n"
                "    }\n"
                "    while (i < n1) arr[k++] = L[i++];\n"
                "    while (j < n2) arr[k++] = R[j++];\n"
                "}"
            )
        },
        "comparison": {
            "title": "Comprehensive Sorting Algorithm Comparison",
            "headers": ["Algorithm", "Best Time", "Average Time", "Worst Time", "Space", "Stability"],
            "rows": [
                ["Bubble Sort", "$O(n)$ (adaptive)", "$O(n^2)$", "$O(n^2)$", "$O(1)$", "Stable"],
                ["Insertion Sort", "$O(n)$ (adaptive)", "$O(n^2)$", "$O(n^2)$", "$O(1)$", "Stable"],
                ["Selection Sort", "$O(n^2)$", "$O(n^2)$", "$O(n^2)$", "$O(1)$", "Unstable"],
                ["Merge Sort", "$O(n \\log n)$", "$O(n \\log n)$", "$O(n \\log n)$", "$O(n)$", "Stable"],
                ["QuickSort", "$O(n \\log n)$", "$O(n \\log n)$", "$O(n^2)$", "$O(\\log n)$", "Unstable"],
                ["Heap Sort", "$O(n \\log n)$", "$O(n \\log n)$", "$O(n \\log n)$", "$O(1)$", "Unstable"],
                ["Counting Sort", "$O(n + k)$", "$O(n + k)$", "$O(n + k)$", "$O(k)$", "Stable"]
            ]
        },
        "formulas": [
            {"name": "Comparison Sort Lower Bound", "formula": "Height >= log_2(n!) = Omega(n log n)", "explanation": "A decision tree sorting n elements must have at least n! leaves."},
            {"name": "QuickSort Worst-Case Recurrence", "formula": "T(n) = T(n - 1) + Theta(n) = Theta(n^2)", "explanation": "Occurs when pivot is consistently the minimum or maximum element."}
        ],
        "exam_tip": "If an exam question asks: 'Which algorithm is best for sorting a nearly sorted array or small array ($n < 50$)?', the answer is INSERTION SORT! It runs in $O(n)$ linear time on nearly sorted inputs and has minimal constant overhead.",
        "common_confusion": {
            "wrong": "QuickSort is always faster than Merge Sort.",
            "correct": "QuickSort is faster in practice due to smaller constant factors and excellent cache locality, but its worst-case runtime is O(n^2). Merge Sort guarantees O(n log n) and stability.",
            "explanation": "For linked lists and external disk sorting, Merge Sort strictly outperforms QuickSort."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is a Stable Sorting Algorithm? Name two stable and two unstable sorting algorithms.",
                "a": "A sorting algorithm is Stable if it preserves the relative original input order of records with equal keys. Stable: Merge Sort, Insertion Sort (and Bubble Sort). Unstable: QuickSort, Heap Sort (and Selection Sort)."
            },
            {
                "marks": "5-Mark Question",
                "q": "Prove that any comparison-based sorting algorithm requires at least Omega(n log n) comparisons in the worst case.",
                "a": "1. Decision Tree Model: Any comparison sort can be modeled as a binary decision tree where each internal node represents a comparison $A[i] \\le A[j]$ and each leaf represents one of the $n!$ possible permutations of $n$ elements.\n2. Tree Height and Leaves: A binary tree of height $h$ can have at most $2^h$ leaves. Therefore: $2^h \\ge n! \\implies h \\ge \\log_2(n!)$.\n3. Stirling's Approximation: By Stirling's formula, $\\log_2(n!) = \\sum_{i=1}^n \\log_2 i \\ge \\sum_{i=n/2}^n \\log_2(n/2) = \\frac{n}{2} \\log_2(n/2) = \\Omega(n \\log n)$.\n4. Conclusion: Worst-case number of comparisons $h = \\Omega(n \\log n)$."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain QuickSort with Lomuto or Hoare partitioning. Trace it on array [10, 80, 30, 90, 40, 50, 70] and discuss how to mitigate the O(n^2) worst-case time.",
                "a": "1. QuickSort Principle: Divide-and-conquer algorithm that selects a pivot, partitions the array such that all elements $< pivot$ are to its left and all elements $> pivot$ are to its right, and recursively sorts both sub-arrays.\n2. Trace on `[10, 80, 30, 90, 40, 50, 70]` (Pivot = 70):\n   - $i = -1$\n   - $j=0$ (10 <= 70): $i=0$, swap 10 with 10. `[10, 80, 30, 90, 40, 50, 70]`\n   - $j=1$ (80 > 70): no swap.\n   - $j=2$ (30 <= 70): $i=1$, swap 80 and 30. `[10, 30, 80, 90, 40, 50, 70]`\n   - $j=3$ (90 > 70): no swap.\n   - $j=4$ (40 <= 70): $i=2$, swap 80 and 40. `[10, 30, 40, 90, 80, 50, 70]`\n   - $j=5$ (50 <= 70): $i=3$, swap 90 and 50. `[10, 30, 40, 50, 80, 90, 70]`\n   - End loop: Swap pivot 70 with $A[i+1] = A[4]$ (80). `[10, 30, 40, 50, 70, 90, 80]`\n   - Pivot 70 is placed at index 4. Left subarray: `[10, 30, 40, 50]`, Right: `[90, 80]`.\n3. Mitigating $O(n^2)$ Worst-Case:\n   - Randomized QuickSort: Choose random element as pivot ($O(n \\log n)$ expected).\n   - Median-of-Three: Pivot is median of first, middle, and last elements.\n   - Introsort: Switch to HeapSort if recursion depth exceeds $2 \\log n$ (used in C++ `std::sort`)."
            }
        ],
        "revision_60s": [
            "Comparison sort lower bound is Omega(n log n).",
            "Stable sorts preserve relative order of equal keys (Merge, Insertion, Bubble).",
            "QuickSort: fastest in practice, but O(n^2) worst case without randomized pivot.",
            "MergeSort: guaranteed O(n log n), stable, requires O(n) auxiliary memory.",
            "HeapSort: guaranteed O(n log n) in-place (O(1) memory), unstable.",
            "Insertion Sort is O(n) on nearly sorted data."
        ]
    },

    "searching": {
        "title": "Searching Algorithms & Binary Search Variants",
        "subject": "ds",
        "exam_definition": (
            "Searching is the algorithmic process of locating the position of a target key within a collection, transitioning from "
            "$O(n)$ Linear Search on unsorted data to $O(\\log n)$ Binary Search on sorted datasets and monotonic predicates."
        ),
        "remember": "Binary Search Midpoint: Use mid = low + (high - low) / 2 to prevent 32-bit integer overflow bug!",
        "core_concept": (
            "Linear search scans every element sequentially in $O(n)$ time. When data is sorted, Binary Search divides the search space "
            "in half each iteration, achieving $O(\\log n)$ logarithmic runtime. Binary search principles extend beyond simple key lookup "
            "to 'Binary Search on Answer' (monotonic predicate search) to solve optimization problems."
        ),
        "key_points": [
            "Linear Search: Unsorted data, scans sequentially, $O(n)$ time, $O(1)$ space.",
            "Binary Search Precondition: The array or search space MUST be sorted (or monotonic).",
            "Midpoint Overflow Prevention: `mid = (low + high) / 2` causes integer overflow when `low + high > 2^31 - 1`. Correct: `mid = low + (high - low) / 2`.",
            "Lower Bound / Upper Bound: Lower bound finds first element $\\ge target$; Upper bound finds first element $> target$.",
            "Interpolation Search: Predicts probe position based on value: $pos = low + \\frac{target - arr[low]}{arr[high] - arr[low]} \\times (high - low)$. Takes $O(\\log \\log n)$ on uniformly distributed data.",
            "Binary Search on Answer: Finds optimal value $X$ satisfying predicate $P(X)$ where $P$ is monotonic (false, false, ..., true, true)."
        ],
        "classification": {
            "title": "Searching Algorithm Paradigms",
            "items": [
                {"name": "Linear Search", "desc": "Sequential scan over unsorted data. Time: O(n)."},
                {"name": "Binary Search", "desc": "Halves search interval on sorted data. Time: O(log n)."},
                {"name": "Interpolation Search", "desc": "Probes near estimated position for uniformly distributed sorted integers. Time: O(log log n)."},
                {"name": "Exponential Search", "desc": "Finds range [2^k, 2^(k+1)] bounding target, then applies binary search. Ideal for unbounded/infinite lists."}
            ]
        },
        "how_it_works": {
            "title": "Binary Search Iterative Execution Flow",
            "steps": [
                "1. Initialize search boundaries: `low = 0` and `high = n - 1`.",
                "2. While `low <= high`:\n   - Compute safe midpoint: `mid = low + (high - low) / 2`.\n   - If `arr[mid] == target`: return `mid` (Target found!).\n   - If `arr[mid] < target`: target must be in right half -> set `low = mid + 1`.\n   - If `arr[mid] > target`: target must be in left half -> set `high = mid - 1`.",
                "3. If loop exits (`low > high`), target does not exist in array -> return -1."
            ],
            "diagram": "Array: [ 2 | 5 | 8 | 12 | 16 | 23 | 38 | 56 | 72 | 91 ]   Target = 23\n        low=0              mid=4(16)            high=9\nSince 23 > 16: set low = mid + 1 = 5 ──> Search space halved to [23, 38, 56, 72, 91]"
        },
        "example": {
            "title": "Binary Search Implementation in C++",
            "scenario": "Iterative binary search with safe midpoint calculation.",
            "code": (
                "int binarySearch(const vector<int>& arr, int target) {\n"
                "    int low = 0;\n"
                "    int high = (int)arr.size() - 1;\n\n"
                "    while (low <= high) {\n"
                "        // Prevents integer overflow: (low + high) can exceed INT_MAX\n"
                "        int mid = low + (high - low) / 2;\n\n"
                "        if (arr[mid] == target) {\n"
                "            return mid; // Target found at index mid\n"
                "        } else if (arr[mid] < target) {\n"
                "            low = mid + 1; // Discard left half\n"
                "        } else {\n"
                "            high = mid - 1; // Discard right half\n"
                "        }\n"
                "    }\n"
                "    return -1; // Target not found\n"
                "}"
            )
        },
        "comparison": {
            "title": "Linear Search vs Binary Search vs Interpolation Search",
            "headers": ["Algorithm", "Precondition", "Best Time", "Average Time", "Worst Time", "Space"],
            "rows": [
                ["Linear Search", "None (works on unsorted data)", "$O(1)$", "$O(n)$", "$O(n)$", "$O(1)$"],
                ["Binary Search", "Data must be sorted", "$O(1)$", "$O(\\log n)$", "$O(\\log n)$", "$O(1)$ iterative"],
                ["Interpolation Search", "Data must be sorted and uniformly distributed", "$O(1)$", "$O(\\log \\log n)$", "$O(n)$ (skewed distribution)", "$O(1)$"]
            ]
        },
        "formulas": [
            {"name": "Safe Midpoint Calculation", "formula": "mid = low + (high - low) / 2", "explanation": "Mathematically equivalent to (low + high)/2 but prevents 32-bit integer overflow."},
            {"name": "Binary Search Comparisons", "formula": "Max Comparisons = floor(log_2 n) + 1", "explanation": "Maximum iterations before search space is reduced to 0."}
        ],
        "exam_tip": "Always write `mid = low + (high - low) / 2` instead of `(low + high) / 2` in code snippets and exam papers. Mention that this fixes the famous 32-bit signed integer overflow bug discovered by Joshua Bloch at Google.",
        "common_confusion": {
            "wrong": "Binary search can only be used to find an element in an array.",
            "correct": "Binary search can be applied to ANY monotonic function or decision space (Binary Search on Answer) to find minimum or maximum values satisfying a condition.",
            "explanation": "Examples: Book Allocation Problem, Aggressive Cows, Koko Eating Bananas, Capacity to Ship Packages."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "Why is mid calculated as low + (high - low) / 2 instead of (low + high) / 2 in Binary Search?",
                "a": "In programming languages with fixed-width integer types (like C, C++, Java), if `low` and `high` are both large positive integers near $2^{31} - 1$, their sum `low + high` overflows into a negative number, resulting in a negative array index and crash. `low + (high - low) / 2` avoids this overflow completely."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain the concept of Binary Search on Answer with a classic example.",
                "a": "1. Concept: If an optimization problem asks for the minimum or maximum value $X$ satisfying a condition $P(X)$, and the predicate $P(X)$ is monotonic (i.e. if $P(k)$ is true, then $P(k+1)$ is also true), we can binary search the answer range $[low, high]$.\n2. Monotonicity: Check function `isValid(mid)` runs in $O(n)$ time.\n3. Example (Painter's Partition / Book Allocation): To find the minimum possible maximum workload assigned to $K$ workers, we binary search across workload range $[\max(arr), \sum arr]$.\n4. Overall Complexity: $O(n \\log(\\sum arr))$. Transforms complex optimization into simple binary search."
            },
            {
                "marks": "10-Mark Question",
                "q": "Explain how to search for a target key in a Rotated Sorted Array (e.g. [4, 5, 6, 7, 0, 1, 2]) in O(log n) time without un-rotating the array.",
                "a": "1. Observation: If a sorted array is rotated at some pivot, at least one half of the array (either left half `[low..mid]` or right half `[mid..high]`) is GUARANTEED to be strictly sorted.\n2. Algorithm:\n   - Compute `mid = low + (high - low) / 2`.\n   - If `arr[mid] == target`, return `mid`.\n   - Check if Left Half is Sorted (`arr[low] <= arr[mid]`):\n     - If target lies within sorted range (`arr[low] <= target < arr[mid]`): search left half (`high = mid - 1`).\n     - Else: search right half (`low = mid + 1`).\n   - Else Right Half is Sorted (`arr[mid] <= arr[high]`):\n     - If target lies within sorted range (`arr[mid] < target <= arr[high]`): search right half (`low = mid + 1`).\n     - Else: search left half (`high = mid - 1`).\n3. Complexity: At each step, half the array is discarded. Time complexity is strictly $O(\\log n)$ and auxiliary space is $O(1)$."
            }
        ],
        "revision_60s": [
            "Linear search: O(n) on unsorted data.",
            "Binary search: O(log n) on sorted data.",
            "Always use mid = low + (high - low) / 2 to prevent overflow.",
            "Interpolation search is O(log log n) for uniformly distributed data.",
            "Rotated sorted array search runs in O(log n) by identifying the sorted half."
        ]
    },

    "greedy": {
        "title": "Greedy Algorithms & Optimization",
        "subject": "ds",
        "exam_definition": (
            "A Greedy Algorithm is an algorithmic paradigm that builds up a solution piece by piece, always choosing the locally optimal "
            "choice at each stage with the hope of finding a global optimum, satisfying Greedy-Choice Property and Optimal Substructure."
        ),
        "remember": "Greedy Criteria: 1) Greedy-Choice Property (locally optimal choice yields global optimum), 2) Optimal Substructure (optimal solution contains optimal sub-solutions).",
        "core_concept": (
            "Unlike Dynamic Programming which systematically explores all subproblems, a greedy algorithm commits irrevocably to the immediate "
            "best choice without backtracking. While greedy algorithms do not work for all optimization problems (e.g. 0/1 Knapsack fails), "
            "they produce provably optimal solutions for Fractional Knapsack, Activity Selection, Huffman Coding, Dijkstra, and Kruskal."
        ),
        "key_points": [
            "Greedy-Choice Property: A globally optimal solution can be arrived at by making locally optimal (greedy) choices.",
            "Optimal Substructure: An optimal solution to the problem contains optimal solutions to its subproblems.",
            "Activity Selection Problem: Sort activities by finishing time ($f_i$); greedily select next activity whose start time $\\ge$ previous finish time in $O(n \\log n)$ time.",
            "Fractional Knapsack: Greedily take items with highest Value-to-Weight ratio ($v_i / w_i$); optimal solution in $O(n \\log n)$ time.",
            "0/1 Knapsack: Items cannot be broken; greedy fails! Requires Dynamic Programming.",
            "Huffman Coding: Lossless data compression building prefix-free codes using a Min-Heap; frequent characters receive shortest bit codes in $O(n \\log n)$ time."
        ],
        "classification": {
            "title": "Classic Greedy Problems",
            "items": [
                {"name": "Activity Selection / Interval Scheduling", "desc": "Sort by end time; pick maximum non-overlapping intervals in O(n log n)."},
                {"name": "Fractional Knapsack", "desc": "Sort items by value/weight ratio; take fractional portions of remaining capacity in O(n log n)."},
                {"name": "Huffman Coding", "desc": "Build optimal prefix code tree using Min-Heap based on character frequencies in O(n log n)."},
                {"name": "Job Sequencing with Deadlines", "desc": "Sort jobs by profit; schedule in latest available slot before deadline in O(n^2) or O(n log n) with DSU."}
            ]
        },
        "how_it_works": {
            "title": "Huffman Coding Tree Construction",
            "steps": [
                "1. Create a leaf node for each character with its frequency and insert into a Min-Heap.",
                "2. While Min-Heap contains more than 1 node:\n   - Extract node with lowest frequency: $left = \\text{extractMin()}$.\n   - Extract node with second lowest frequency: $right = \\text{extractMin()}$.\n   - Create a new internal node with frequency equal to $left.\\text{freq} + right.\\text{freq}$.\n   - Set its left child to $left$ and right child to $right$.\n   - Insert the new internal node back into the Min-Heap.",
                "3. The single remaining node in the Min-Heap is the root of the Huffman Tree.",
                "4. Assign '0' to left branches and '1' to right branches to generate variable-length prefix-free binary codes."
            ],
            "diagram": "Min-Heap: [C:12, B:15, A:45] ──> Combine C(12) + B(15) = Internal(27) ──> Combine Internal(27) + A(45) = Root(72)"
        },
        "example": {
            "title": "Fractional Knapsack Problem in Java",
            "scenario": "Sort items by value-to-weight ratio and greedily fill knapsack capacity.",
            "code": (
                "class Item {\n"
                "    int value, weight;\n"
                "    Item(int v, int w) { value = v; weight = w; }\n"
                "}\n\n"
                "double getMaxValue(Item[] items, int capacity) {\n"
                "    // Sort in descending order of value/weight ratio\n"
                "    Arrays.sort(items, (a, b) -> Double.compare((double)b.value / b.weight, (double)a.value / a.weight));\n\n"
                "    double totalValue = 0.0;\n"
                "    for (Item item : items) {\n"
                "        if (capacity >= item.weight) {\n"
                "            capacity -= item.weight;\n"
                "            totalValue += item.value;\n"
                "        } else {\n"
                "            // Take fractional portion\n"
                "            totalValue += ((double)item.value / item.weight) * capacity;\n"
                "            break; // Knapsack full\n"
                "        }\n"
                "    }\n"
                "    return totalValue;\n"
                "}"
            )
        },
        "comparison": {
            "title": "Greedy Method vs Dynamic Programming (DP)",
            "headers": ["Feature", "Greedy Algorithm", "Dynamic Programming (DP)"],
            "rows": [
                ["Decision Making", "Makes locally optimal choice at each step; never reconsiders or backtracks", "Considers all possible choices and subproblem combinations"],
                ["Subproblem Overlap", "Does not require overlapping subproblems", "Requires overlapping subproblems and memoization/tabulation"],
                ["Optimality", "Fails on many problems (e.g. 0/1 knapsack, traveling salesman)", "Guaranteed to find global optimum if optimal substructure holds"],
                ["Time Complexity", "Generally very fast: typically $O(n \\log n)$ or $O(n)$", "Generally slower: polynomial $O(n^2)$, $O(n^3)$, or pseudo-polynomial $O(n W)$"],
                ["Knapsack Problem", "Solves Fractional Knapsack optimally", "Required to solve 0/1 Knapsack optimally"]
            ]
        },
        "formulas": [
            {"name": "Value Density Ratio", "formula": "Ratio_i = Value_i / Weight_i", "explanation": "Greedy selection criterion for Fractional Knapsack."},
            {"name": "Average Huffman Code Length", "formula": "L_avg = Sum (freq_i * length_i) / Sum (freq_i)", "explanation": "Expected bits per character in compressed stream."}
        ],
        "exam_tip": "In Activity Selection: Always sort activities by FINISH TIME, NOT start time or duration! Sorting by start time or duration fails to maximize the number of non-overlapping activities.",
        "common_confusion": {
            "wrong": "The greedy approach can be used to solve the 0/1 Knapsack problem.",
            "correct": "Greedy FAILS for 0/1 Knapsack because items cannot be divided. Taking an item with high density may consume capacity that could have accommodated two other items with higher combined value.",
            "explanation": "Capacity 50: Item 1 (v=60, w=10, r=6), Item 2 (v=100, w=20, r=5), Item 3 (v=120, w=30, r=4). Greedy takes Item 1 + Item 2 (val 160, weight 30). Optimal takes Item 2 + Item 3 (val 220, weight 50)!"
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What are the two essential properties required for a Greedy Algorithm to produce an optimal solution?",
                "a": "1. Greedy-Choice Property: A globally optimal solution can be reached by choosing the locally optimal choice at each step without ever backtracking.\n2. Optimal Substructure: An optimal solution to the overall problem contains optimal solutions to its smaller subproblems."
            },
            {
                "marks": "5-Mark Question",
                "q": "Explain why the Greedy algorithm works for Fractional Knapsack but fails for 0/1 Knapsack.",
                "a": "1. Fractional Knapsack: We can take fractions of items. If we greedily take items with the highest value-per-pound ($v_i / w_i$), any knapsack space left over can be filled with a fractional slice of the next best item, leaving zero wasted capacity and guaranteeing an optimal solution.\n2. 0/1 Knapsack: Items must be taken completely or left behind. Choosing an item with the highest density can leave empty capacity that cannot be filled by remaining large items, resulting in lower total value than combining two lower-density items that pack the knapsack perfectly."
            },
            {
                "marks": "10-Mark Question",
                "q": "Given characters with frequencies: a: 5, b: 9, c: 12, d: 13, e: 16, f: 45. Construct the Huffman Tree, derive the prefix codes for each character, and calculate the average code length.",
                "a": "1. Min-Heap Initial State: `[(a, 5), (b, 9), (c, 12), (d, 13), (e, 16), (f, 45)]`\n2. Tree Construction Steps:\n   - Combine a(5) + b(9) -> Node T1(14). Heap: `[c:12, d:13, T1:14, e:16, f:45]`\n   - Combine c(12) + d(13) -> Node T2(25). Heap: `[T1:14, e:16, T2:25, f:45]`\n   - Combine T1(14) + e(16) -> Node T3(30). Heap: `[T2:25, T3:30, f:45]`\n   - Combine T2(25) + T3(30) -> Node T4(55). Heap: `[f:45, T4:55]`\n   - Combine f(45) + T4(55) -> Root(100).\n3. Binary Codes (Left=0, Right=1):\n   - f: 0 (1 bit)\n   - T4 -> 1:\n     - T2(left 0) -> c: 100 (3 bits), d: 101 (3 bits)\n     - T3(right 1) -> T1(left 0) -> a: 1100 (4 bits), b: 1101 (4 bits); e: 111 (3 bits)\n   - Codes: f='0', c='100', d='101', e='111', a='1100', b='1101'.\n4. Average Code Length:\n   - Total bits = $45(1) + 12(3) + 13(3) + 16(3) + 5(4) + 9(4) = 45 + 36 + 39 + 48 + 20 + 36 = 224$ bits.\n   - Average Length = $224 / 100 = 2.24$ bits per character (compared to 3 bits for fixed-length encoding, saving 25.3% space!)."
            }
        ],
        "revision_60s": [
            "Greedy makes the locally optimal choice at each step without backtracking.",
            "Activity selection: sort by finish time; pick non-overlapping.",
            "Fractional Knapsack: sort by value/weight ratio; greedy is optimal.",
            "0/1 Knapsack CANNOT be solved with greedy; requires Dynamic Programming.",
            "Huffman coding builds optimal prefix tree using Min-Heap."
        ]
    },

    "dynamic-programming": {
        "title": "Dynamic Programming: Memoization & Tabulation",
        "subject": "ds",
        "exam_definition": (
            "Dynamic Programming (DP) is an algorithmic paradigm that solves complex optimization problems by breaking them down "
            "into overlapping subproblems, storing intermediate subproblem results to eliminate redundant recomputation via "
            "Memoization (Top-Down) or Tabulation (Bottom-Up)."
        ),
        "remember": "Two Pillars of DP: 1) Overlapping Subproblems (subproblems repeat), 2) Optimal Substructure (optimal solution contains optimal sub-solutions).",
        "core_concept": (
            "Naive recursion often re-evaluates the exact same subproblems exponentially many times (e.g. naive Fibonacci takes $O(2^n)$ time). "
            "Dynamic Programming caches computed results in a table, reducing time complexity from exponential $O(2^n)$ to polynomial $O(n)$ or $O(n^2)$. "
            "Memoization uses recursion with a lookup cache; Tabulation fills an iterative table systematically from base cases upward."
        ),
        "key_points": [
            "Overlapping Subproblems: The same subproblems are solved repeatedly during recursive evaluation.",
            "Optimal Substructure: The optimal solution to the problem can be constructed from optimal solutions of its subproblems.",
            "Top-Down (Memoization): Retains recursive structure; checks cache before executing computation.",
            "Bottom-Up (Tabulation): Solves smaller base-case subproblems first and iteratively fills a table; zero recursion stack overhead.",
            "0/1 Knapsack Problem: $dp[i][w] = \\max(dp[i-1][w], \\text{val}[i-1] + dp[i-1][w - \\text{wt}[i-1]])$; solved in $O(n \\cdot W)$ pseudo-polynomial time.",
            "Longest Common Subsequence (LCS): Solved in $O(m \\cdot n)$ time using 2D DP table.",
            "Space Optimization: When $dp[i]$ depends only on row $i-1$, auxiliary space can be reduced from 2D $O(n \\cdot W)$ to 1D $O(W)$."
        ],
        "classification": {
            "title": "Classic Dynamic Programming Patterns",
            "items": [
                {"name": "0/1 Knapsack Pattern", "desc": "Subset sum, partition equal subset, target sum. Decisions: include or exclude item."},
                {"name": "Longest Common Subsequence (LCS)", "desc": "Edit Distance, Longest Palindromic Subsequence, Shortest Common Supersequence on two strings."},
                {"name": "Longest Increasing Subsequence (LIS)", "desc": "Russian doll envelopes, building bridges. Solvable in O(n^2) DP or O(n log n) with binary search."},
                {"name": "Matrix Chain Multiplication (MCM)", "desc": "Optimal parenthesis placement for matrix chain product. Interval DP in O(n^3) time."}
            ]
        },
        "how_it_works": {
            "title": "0/1 Knapsack Dynamic Programming Table Construction",
            "steps": [
                "1. Initialize 2D table `dp[N + 1][W + 1]` with all 0s.",
                "2. Base cases: If items $i = 0$ or knapsack capacity $w = 0$, then $dp[i][w] = 0$.",
                "3. Loop $i$ from 1 to $N$ (items), and $w$ from 1 to $W$ (capacity):\n   - If item weight $wt[i-1] > w$: item cannot fit -> $dp[i][w] = dp[i-1][w]$ (exclude item).\n   - Else item can fit -> choose maximum of excluding or including:\n     $dp[i][w] = \\max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]])$.",
                "4. Final answer is stored in `dp[N][W]`."
            ],
            "diagram": "dp[i][w] = max( EXCLUDE: dp[i-1][w], INCLUDE: val[i-1] + dp[i-1][w - wt[i-1]] )"
        },
        "example": {
            "title": "0/1 Knapsack Tabulation Implementation in C++",
            "scenario": "Bottom-up dynamic programming solution for 0/1 knapsack.",
            "code": (
                "int knapsack01(int W, const vector<int>& wt, const vector<int>& val, int n) {\n"
                "    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));\n\n"
                "    for (int i = 1; i <= n; i++) {\n"
                "        for (int w = 1; w <= W; w++) {\n"
                "            if (wt[i - 1] <= w) {\n"
                "                // Max of (Include item, Exclude item)\n"
                "                dp[i][w] = max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w]);\n"
                "            } else {\n"
                "                // Cannot include item\n"
                "                dp[i][w] = dp[i - 1][w];\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    return dp[n][W]; // Optimal value\n"
                "}"
            )
        },
        "comparison": {
            "title": "Memoization (Top-Down) vs Tabulation (Bottom-Up)",
            "headers": ["Parameter", "Memoization (Top-Down)", "Tabulation (Bottom-Up)"],
            "rows": [
                ["Approach", "Starts at original problem and recurses down to base cases", "Starts at base cases and builds up iteratively to target problem"],
                ["Overhead", "Recursion call stack overhead (risks StackOverflow on deep trees)", "Zero recursion overhead; simple iterative loops"],
                ["Subproblem Evaluation", "Solves only necessary reachable subproblems (lazy evaluation)", "Systematically evaluates all entries in the DP table"],
                ["Space Optimization", "Difficult to optimize state storage", "Easily optimized (e.g. 2D table reduced to 1D rolling array)"],
                ["Implementation", "Recursive function + hash map or lookup array", "Iterative for-loops + multi-dimensional array"]
            ]
        },
        "formulas": [
            {"name": "0/1 Knapsack Recurrence", "formula": "dp[i][w] = max(dp[i-1][w], val[i-1] + dp[i-1][w - wt[i-1]])", "explanation": "Where wt[i-1] <= w."},
            {"name": "LCS Recurrence", "formula": "dp[i][j] = (s1[i-1] == s2[j-1]) ? 1 + dp[i-1][j-1] : max(dp[i-1][j], dp[i][j-1])", "explanation": "Longest Common Subsequence state transition."}
        ],
        "exam_tip": "In 0/1 Knapsack problems, remember that the time complexity is $O(n \\cdot W)$. This is NOT polynomial time — it is PSEUDO-POLYNOMIAL time, because $W$ is represented by $\\log_2 W$ bits in computer memory.",
        "common_confusion": {
            "wrong": "Dynamic programming and Divide-and-Conquer are the exact same concept.",
            "correct": "Divide-and-Conquer divides problems into INDEPENDENT non-overlapping subproblems (e.g. Merge Sort). Dynamic Programming is used when subproblems OVERLAP heavily.",
            "explanation": "If subproblems do not overlap, caching offers zero benefit."
        },
        "faqs": [
            {
                "marks": "2-Mark Question",
                "q": "What is the difference between Memoization and Tabulation in Dynamic Programming?",
                "a": "Memoization is a Top-Down approach that maintains the recursive formulation and caches computed subproblem results in a lookup table. Tabulation is a Bottom-Up approach that solves base cases first and iteratively populates a table using loops, avoiding recursion call stack overhead."
            },
            {
                "marks": "5-Mark Question",
                "q": "Formulate the recurrence relation for the Longest Common Subsequence (LCS) of two strings X[1..m] and Y[1..n].",
                "a": "Let $LCS[i, j]$ denote the length of the longest common subsequence of prefixes $X[1\\dots i]$ and $Y[1\\dots j]$:\n1. Base Case: $LCS[i, j] = 0$ if $i = 0$ or $j = 0$.\n2. Match: If $X[i] == Y[j]$, then $LCS[i, j] = 1 + LCS[i-1, j-1]$.\n3. Mismatch: If $X[i] \\ne Y[j]$, then $LCS[i, j] = \\max(LCS[i-1, j], LCS[i, j-1])$.\n4. Overall Time Complexity: $O(m \\cdot n)$, Space Complexity: $O(m \\cdot n)$."
            },
            {
                "marks": "10-Mark Question",
                "q": "Solve the 0/1 Knapsack problem for Knapsack Capacity W = 7 with 4 items: Item 1 (w=1, v=1), Item 2 (w=3, v=4), Item 3 (w=4, v=5), Item 4 (w=5, v=7). Construct the complete DP table and find which items are included.",
                "a": "1. Items: (w=1,v=1), (w=3,v=4), (w=4,v=5), (w=5,v=7). $W = 7$.\n2. DP Table Construction ($dp[i][w]$):\n   - Row 0: all 0s (w=0..7)\n   - Row 1 (w=1, v=1): [0, 1, 1, 1, 1, 1, 1, 1]\n   - Row 2 (w=3, v=4):\n     - w=0..2: copies Row 1 -> [0, 1, 1]\n     - w=3: max(1, 4 + dp[1][0]) = 4\n     - w=4: max(1, 4 + dp[1][1]) = 5\n     - w=5: max(1, 4 + dp[1][2]) = 5\n     - w=6: max(1, 4 + dp[1][3]) = 5\n     - w=7: max(1, 4 + dp[1][4]) = 5\n     - Row 2: [0, 1, 1, 4, 5, 5, 5, 5]\n   - Row 3 (w=4, v=5):\n     - w=0..3: [0, 1, 1, 4]\n     - w=4: max(5, 5 + dp[2][0]) = 5\n     - w=5: max(5, 5 + dp[2][1]) = 6\n     - w=6: max(5, 5 + dp[2][2]) = 6\n     - w=7: max(5, 5 + dp[2][3]) = 9 (5 + 4 = 9!)\n     - Row 3: [0, 1, 1, 4, 5, 6, 6, 9]\n   - Row 4 (w=5, v=7):\n     - w=0..4: [0, 1, 1, 4, 5]\n     - w=5: max(6, 7 + dp[3][0]) = 7\n     - w=6: max(6, 7 + dp[3][1]) = 8\n     - w=7: max(9, 7 + dp[3][2]) = 9\n     - Row 4: [0, 1, 1, 4, 5, 7, 8, 9]\n3. Maximum Value: $dp[4][7] = 9$.\n4. Backtracking Included Items:\n   - $dp[4][7] == dp[3][7] (9 == 9) \\implies$ Item 4 NOT included.\n   - $dp[3][7] \\ne dp[2][7] (9 \\ne 5) \\implies$ Item 3 IS included! Capacity remaining = $7 - 4 = 3$.\n   - Look at $dp[2][3]$: $dp[2][3] \\ne dp[1][3] (4 \\ne 1) \\implies$ Item 2 IS included! Capacity remaining = $3 - 3 = 0$.\n   - Items included: Item 3 and Item 2. Total weight = $4 + 3 = 7$, Total value = $5 + 4 = 9$."
            }
        ],
        "revision_60s": [
            "DP requires Overlapping Subproblems and Optimal Substructure.",
            "Memoization = Top-Down recursion with cache.",
            "Tabulation = Bottom-Up iterative table filling.",
            "0/1 Knapsack runs in O(n * W) pseudo-polynomial time.",
            "LCS runs in O(m * n) time.",
            "Divide-and-conquer has non-overlapping subproblems; DP has overlapping subproblems."
        ]
    }
}

def generate():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(DS_TOPICS, f, indent=2, ensure_ascii=False)
    print(f"Generated complete DS dataset with {len(DS_TOPICS)} topics at: {DATA_PATH}")

if __name__ == "__main__":
    generate()
