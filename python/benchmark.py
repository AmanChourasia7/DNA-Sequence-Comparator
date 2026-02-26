#!/usr/bin/env python3
"""
benchmark.py

DNA Sequence Comparator
Automated benchmarking framework for DNA file comparison methods.

Benchmarked Methods:
    1. Sequential byte comparison
    2. Parallel multiprocessing comparison
    3. SHA-256 hash comparison

Usage:
    python benchmark.py <file1> <file2> [chunk_size_mb]

Example:
    python benchmark.py dna1.txt dna2.txt 16

Default chunk size: 8 MB
"""

import os
import sys
import time
import hashlib
import statistics
import multiprocessing as mp
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Method 1: Sequential Comparison
# ------------------------------------------------------------

def sequential_compare(file1, file2, chunk_size):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    if size1 != size2:
        return False

    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        while True:
            b1 = f1.read(chunk_size)
            b2 = f2.read(chunk_size)

            if b1 != b2:
                return False

            if not b1:
                break

    return True


# ------------------------------------------------------------
# Method 2: Parallel Comparison
# ------------------------------------------------------------

def compare_chunk(args):
    file1, file2, start, size = args
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        f1.seek(start)
        f2.seek(start)
        return f1.read(size) == f2.read(size)


def parallel_compare(file1, file2, chunk_size):
    size = os.path.getsize(file1)
    tasks = []

    for start in range(0, size, chunk_size):
        remaining = min(chunk_size, size - start)
        tasks.append((file1, file2, start, remaining))

    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(compare_chunk, tasks)

    return all(results)


# ------------------------------------------------------------
# Method 3: SHA-256 Comparison
# ------------------------------------------------------------

def sha256_file(path, chunk_size):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha.update(chunk)
    return sha.hexdigest()


def hash_compare(file1, file2, chunk_size):
    if os.path.getsize(file1) != os.path.getsize(file2):
        return False
    return sha256_file(file1, chunk_size) == sha256_file(file2, chunk_size)


# ------------------------------------------------------------
# Benchmark Utility
# ------------------------------------------------------------

def benchmark_method(name, func, trials, *args):
    times = []

    for _ in range(trials):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append(end - start)

    return {
        "mean": statistics.mean(times),
        "std": statistics.stdev(times) if len(times) > 1 else 0.0,
        "runs": times
    }


# ------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python benchmark.py <file1> <file2> [chunk_size_mb]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    chunk_size_mb = 8
    if len(sys.argv) >= 4:
        chunk_size_mb = int(sys.argv[3])

    chunk_size = chunk_size_mb * 1024 * 1024
    trials = 3

    if os.path.getsize(file1) != os.path.getsize(file2):
        print("Files differ in size. Benchmark aborted.")
        sys.exit(2)

    print("========================================")
    print("DNA Sequence Comparator")
    print("Benchmark Report")
    print("----------------------------------------")
    print(f"File Size: {os.path.getsize(file1) / (1024*1024):.2f} MB")
    print(f"Chunk Size: {chunk_size_mb} MB")
    print(f"Trials per Method: {trials}")
    print("========================================\n")

    results = {}

    results["Sequential"] = benchmark_method(
        "Sequential", sequential_compare, trials, file1, file2, chunk_size
    )

    results["Parallel"] = benchmark_method(
        "Parallel", parallel_compare, trials, file1, file2, chunk_size
    )

    results["SHA-256"] = benchmark_method(
        "SHA-256", hash_compare, trials, file1, file2, chunk_size
    )

    # Print Report
    for method, stats in results.items():
        print(f"{method}:")
        print(f"  Mean Time : {stats['mean']:.6f} sec")
        print(f"  Std Dev   : {stats['std']:.6f} sec")
        print()

    # Plot Results
    methods = list(results.keys())
    means = [results[m]["mean"] for m in methods]

    plt.bar(methods, means)
    plt.ylabel("Mean Time (seconds)")
    plt.title("DNA File Comparison Benchmark")
    plt.tight_layout()
    plt.savefig("benchmark_results.png", dpi=300)
    plt.show()

    print("Benchmark graph saved as: benchmark_results.png")
    print("========================================")


if __name__ == "__main__":
    main()
