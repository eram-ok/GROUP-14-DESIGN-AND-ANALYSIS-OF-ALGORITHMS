"""
CSC2107: Design & Analysis of Algorithms
Assignment 5.1 — Naive vs. Memoized Fibonacci

This source file implements:
1. Algorithm A — Naive Recursive Fibonacci
2. Algorithm B — Recursive Fibonacci with Memoization
3. Function-call counters
4. Correctness verification for n = 0 to 20
5. Timing experiments using time.perf_counter()
6. Results tables
7. Function-call graphs
8. Recursion-limit investigation
9. Two fixes for reaching n = 1000
10. Demonstration of the fibtable[n] zero-value issue
"""

import time
import sys
import math
import matplotlib.pyplot as plt


# ============================================================
# PART 1: IMPLEMENTATION
# ============================================================

# Global counter for Algorithm A
calls_a = 0


def fib_naive(n):
    """
    Algorithm A: naive recursive Fibonacci.

    Counts every invocation using the global variable calls_a.
    """
    global calls_a

    calls_a += 1

    if n == 0 or n == 1:
        return n

    return fib_naive(n - 1) + fib_naive(n - 2)


# Global counter and memoization dictionary for Algorithm B
calls_b = 0
fibtable = {}


def fib_memo(n):
    """
    Algorithm B: recursive Fibonacci with memoization.

    Previously computed Fibonacci values are stored in fibtable.
    Counts every invocation using the global variable calls_b.
    """
    global calls_b

    calls_b += 1

    if n in fibtable:
        return fibtable[n]

    if n == 0 or n == 1:
        value = n
    else:
        value = fib_memo(n - 1) + fib_memo(n - 2)

    fibtable[n] = value
    return value


# ============================================================
# PART 1.3: VERIFY BOTH ALGORITHMS FOR n = 0 TO 20
# ============================================================

def verify_algorithms():
    """Check that both algorithms return the same values for n = 0 to 20."""
    global calls_a, calls_b

    print("\nPART 1.3: VERIFYING CORRECTNESS")
    print("n\tNaive\tMemoized\tSame?")

    for n in range(21):
        calls_a = 0
        result_a = fib_naive(n)

        calls_b = 0
        fibtable.clear()
        result_b = fib_memo(n)

        print(
            n,
            result_a,
            result_b,
            result_a == result_b,
            sep="\t"
        )


# ============================================================
# PART 2.1(a): EXPERIMENT WITH ALGORITHM A
# ============================================================

def experiment_naive():
    """
    Run Algorithm A for:
    n = 5, 10, 15, 20, 25, 30, 35.

    Stop if one completed run takes longer than 60 seconds.
    """
    global calls_a

    naive_n = [5, 10, 15, 20, 25, 30, 35]
    naive_results = []

    print("\nPART 2.1(a): ALGORITHM A")

    for n in naive_n:
        calls_a = 0

        start = time.perf_counter()
        result = fib_naive(n)
        end = time.perf_counter()

        elapsed = end - start

        naive_results.append(
            (n, calls_a, elapsed)
        )

        print(
            f"n={n}, "
            f"calls={calls_a}, "
            f"time={elapsed:.6f} seconds"
        )

        if elapsed > 60:
            print(
                "Execution exceeded 60 seconds. "
                "Experiment stopped."
            )
            break

    return naive_results


# ============================================================
# PART 2.1(b): EXPERIMENT WITH ALGORITHM B
# ============================================================

def experiment_memoized():
    """
    Run Algorithm B for:
    n = 10, 50, 100, 200, 500, 1000.

    fibtable is cleared before every run.
    A RecursionError is caught and reported if it occurs.
    """
    global calls_b

    memo_n = [10, 50, 100, 200, 500, 1000]
    memo_results = []

    print("\nPART 2.1(b): ALGORITHM B")

    for n in memo_n:
        calls_b = 0
        fibtable.clear()

        start = time.perf_counter()

        try:
            result = fib_memo(n)

            end = time.perf_counter()
            elapsed = end - start

            memo_results.append(
                (n, calls_b, elapsed)
            )

            print(
                f"n={n}, "
                f"calls={calls_b}, "
                f"time={elapsed:.6f} seconds"
            )

        except RecursionError:
            end = time.perf_counter()
            elapsed = end - start

            print(
                f"n={n}: RecursionError "
                f"after {calls_b} calls "
                f"and {elapsed:.6f} seconds"
            )

    return memo_results


# ============================================================
# RESULTS TABLES
# ============================================================

def print_results_table(title, results):
    """Display a simple results table."""
    print(f"\n{title}")
    print(f"{'n':<10}{'calls':<20}{'time (s)':<20}")

    for n, calls, elapsed in results:
        print(
            f"{n:<10}"
            f"{calls:<20}"
            f"{elapsed:<20.8f}"
        )


# ============================================================
# GRAPHS
# ============================================================

def plot_naive_calls(naive_results):
    """
    Plot n against calls for Algorithm A.
    A logarithmic y-axis is used because the calls grow exponentially.
    """
    naive_x = [row[0] for row in naive_results]
    naive_calls = [row[1] for row in naive_results]

    plt.figure()
    plt.plot(
        naive_x,
        naive_calls,
        marker="o"
    )
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("Number of Function Calls (log scale)")
    plt.title("Algorithm A: Naive Fibonacci Function Calls")
    plt.grid(True)
    plt.show()


def plot_memo_calls(memo_results):
    """Plot n against calls for Algorithm B."""
    memo_x = [row[0] for row in memo_results]
    memo_calls = [row[1] for row in memo_results]

    plt.figure()
    plt.plot(
        memo_x,
        memo_calls,
        marker="o"
    )
    plt.xlabel("n")
    plt.ylabel("Number of Function Calls")
    plt.title("Algorithm B: Memoized Fibonacci Function Calls")
    plt.grid(True)
    plt.show()


# ============================================================
# PART 3.5: ESTIMATE ALGORITHM A FOR n = 1000
# ============================================================

def fib_iterative_for_estimate(n):
    """
    Small iterative Fibonacci helper used only to obtain F(1001)
    without using the slow naive recursive algorithm.
    """
    if n == 0:
        return 0

    previous = 0
    current = 1

    for _ in range(2, n + 1):
        previous, current = current, previous + current

    return current


def estimate_naive_1000(naive_results):
    """
    Estimate the number of calls and execution time for Algorithm A at n = 1000
    using the latest measured call rate from the experiment.
    """
    if not naive_results:
        print("\nNo Algorithm A measurements are available for estimation.")
        return

    measured_n, measured_calls, measured_time = naive_results[-1]

    if measured_time <= 0:
        print("\nMeasured execution time is too small for a reliable estimate.")
        return

    call_rate = measured_calls / measured_time

    f_1001 = fib_iterative_for_estimate(1001)
    estimated_calls = 2 * f_1001 - 1

    estimated_seconds = estimated_calls / call_rate
    estimated_years = estimated_seconds / (60 * 60 * 24 * 365.25)

    print("\nPART 3.5: ESTIMATE FOR ALGORITHM A AT n = 1000")
    print(
        f"Measured run used n={measured_n}, "
        f"{measured_calls} calls in {measured_time:.8f} seconds."
    )
    print(f"Measured call rate ≈ {call_rate:.3e} calls/second.")
    print(f"Estimated calls for n=1000 = {estimated_calls:.4e}")
    print(f"Estimated time ≈ {estimated_seconds:.4e} seconds")
    print(f"Estimated time ≈ {estimated_years:.4e} years")


# ============================================================
# PART 4.1: PUSH ALGORITHM B TO n = 1000
# ============================================================

def test_memoized_1000_current_settings():
    """
    Test Algorithm B at n = 1000 using the current Python recursion limit.
    """
    global calls_b

    print("\nPART 4.1: ALGORITHM B AT n = 1000")
    print("Python recursion limit:", sys.getrecursionlimit())

    calls_b = 0
    fibtable.clear()

    try:
        start = time.perf_counter()

        result_1000_default = fib_memo(1000)

        end = time.perf_counter()

        print("F(1000) =", result_1000_default)
        print("Calls =", calls_b)
        print("Time =", end - start, "seconds")

    except RecursionError as error:
        end = time.perf_counter()

        print("RecursionError:", error)
        print("Calls before failure =", calls_b)
        print("Time before failure =", end - start, "seconds")


# ============================================================
# PART 4.2: FIX ONE — INCREASE THE RECURSION LIMIT
# ============================================================

def fix_one_increase_recursion_limit():
    """
    Increase Python's recursion limit and rerun the memoized algorithm.
    """
    global calls_b

    print("\nPART 4.2: FIX ONE — INCREASE RECURSION LIMIT")

    sys.setrecursionlimit(5000)
    print("New recursion limit:", sys.getrecursionlimit())

    calls_b = 0
    fibtable.clear()

    start = time.perf_counter()
    result_1000 = fib_memo(1000)
    end = time.perf_counter()

    print("F(1000) =", result_1000)
    print("Calls =", calls_b)
    print("Time =", end - start, "seconds")


# ============================================================
# PART 4.3: FIX TWO — BOTTOM-UP ITERATIVE FIBONACCI
# ============================================================

def fib_iterative(n):
    """
    Bottom-up iterative Fibonacci.

    Time complexity: O(n)
    Extra working space: O(1)
    """
    if n == 0:
        return 0

    previous = 0
    current = 1

    for _ in range(2, n + 1):
        previous, current = (
            current,
            previous + current
        )

    return current


def test_iterative_1000():
    """Run the bottom-up iterative fix for n = 1000."""
    print("\nPART 4.3: FIX TWO — BOTTOM-UP ITERATIVE")

    start = time.perf_counter()
    iterative_result = fib_iterative(1000)
    end = time.perf_counter()

    print("F(1000) =", iterative_result)
    print("Time =", end - start, "seconds")


# ============================================================
# PART 4.4: PROBLEM WITH `if fibtable[n]`
# ============================================================

def demonstrate_zero_value_issue():
    """
    Demonstrate why checking `if fibtable[n]` is unsafe for F(0) = 0.

    The value 0 is stored, but bool(0) is False.
    The safer check is: if n in fibtable
    """
    print("\nPART 4.4: ZERO-VALUE CHECK")

    test_table = {0: 0}

    print("Stored value:", test_table[0])
    print("Boolean test:", bool(test_table[0]))
    print("Key exists:", 0 in test_table)

    print(
        "\nSafer memoization check:\n"
        "if n in fibtable:\n"
        "    return fibtable[n]"
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    verify_algorithms()

    naive_results = experiment_naive()
    memo_results = experiment_memoized()

    print_results_table(
        "Algorithm A Results Table",
        naive_results
    )

    print_results_table(
        "Algorithm B Results Table",
        memo_results
    )

    plot_naive_calls(naive_results)
    plot_memo_calls(memo_results)

    estimate_naive_1000(naive_results)

    # Run Algorithm B at n = 1000 using the current Python settings first.
    test_memoized_1000_current_settings()

    # Then demonstrate the two proposed fixes.
    fix_one_increase_recursion_limit()
    test_iterative_1000()

    # Demonstrate the fibtable[n] zero-value issue.
    demonstrate_zero_value_issue()


if __name__ == "__main__":
    main()
