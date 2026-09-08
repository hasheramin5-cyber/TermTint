"""Benchmark script comparing TermTint performance against baselines."""

import sys
import time

from termtint import colored, enable_color

try:
    import colorama
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False


def benchmark(name: str, func, iterations: int = 100_000) -> float:
    """Run a function for N iterations and measure execution time."""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    ops_per_sec = iterations / elapsed if elapsed > 0 else 0
    print(f"| {name:<35} | {elapsed:>8.4f}s | {ops_per_sec:>12,.0f} ops/sec |")
    return elapsed


def main() -> None:
    iterations = 100_000
    enable_color()

    print("\n==========================================================")
    print(f" TermTint Micro-Benchmark ({iterations:,} iterations)")
    print(f" Python Version: {sys.version.split()[0]} on {sys.platform}")
    print("==========================================================\n")

    print("| Test Case                           | Total Time |     Throughput |")
    print("|-------------------------------------|------------|----------------|")

    # 1. TermTint colored() named color
    benchmark(
        "TermTint colored('text', 'green')",
        lambda: colored("hello world", "green"),
        iterations,
    )

    # 2. TermTint colored() with style
    benchmark(
        "TermTint colored(..., style='bold')",
        lambda: colored("hello world", "green", style="bold"),
        iterations,
    )

    # 3. TermTint colored() with RGB
    benchmark(
        "TermTint colored(..., rgb=(255, 80, 80))",
        lambda: colored("hello world", rgb=(255, 80, 80)),
        iterations,
    )

    # 4. TermTint colored() with 256-color
    benchmark(
        "TermTint colored(..., color256=196)",
        lambda: colored("hello world", color256=196),
        iterations,
    )

    # 5. Direct raw ANSI string baseline
    benchmark(
        "Raw ANSI string baseline",
        lambda: "\033[32mhello world\033[0m",
        iterations,
    )

    # 4. Optional Colorama benchmark
    if HAS_COLORAMA:
        colorama.init(autoreset=False)
        benchmark(
            "Colorama Fore.GREEN + text + RESET",
            lambda: f"{colorama.Fore.GREEN}hello world{colorama.Style.RESET_ALL}",
            iterations,
        )
    else:
        print("| Colorama (not installed)            |        N/A |            N/A |")

    print("\n----------------------------------------------------------")
    print(" Note: Micro-benchmarks vary based on OS, Python version,")
    print(" hardware, and workload. TermTint prioritizes zero runtime")
    print(" dependencies, correctness, and clean functional API.")
    print("----------------------------------------------------------\n")


if __name__ == "__main__":
    main()
