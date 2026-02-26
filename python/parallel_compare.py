#!/usr/bin/env python3
"""
parallel_compare.py

DNA Sequence Comparator
Parallel file equality testing using multiprocessing.

Usage:
    python parallel_compare.py <file1> <file2> [chunk_size_mb]

Example:
    python parallel_compare.py dna1.txt dna2.txt 16

Default chunk size: 8 MB
"""

import os
import sys
import time
from multiprocessing import Pool, cpu_count


def compare_chunk(args):
    file1, file2, start, size = args

    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        f1.seek(start)
        f2.seek(start)

        data1 = f1.read(size)
        data2 = f2.read(size)

        return data1 == data2


def parallel_compare(file1, file2, chunk_size_bytes):
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    if size1 != size2:
        return False

    tasks = []
    for start in range(0, size1, chunk_size_bytes):
        remaining = min(chunk_size_bytes, size1 - start)
        tasks.append((file1, file2, start, remaining))

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(compare_chunk, tasks)

    return all(results)


def main():
    if len(sys.argv) < 3:
        print("Usage: python parallel_compare.py <file1> <file2> [chunk_size_mb]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    chunk_size_mb = 8
    if len(sys.argv) >= 4:
        chunk_size_mb = int(sys.argv[3])

    chunk_size_bytes = chunk_size_mb * 1024 * 1024

    start_time = time.perf_counter()
    equal = parallel_compare(file1, file2, chunk_size_bytes)
    end_time = time.perf_counter()

    print("========================================")
    print("DNA Sequence Comparator")
    print("----------------------------------------")
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")
    print(f"Chunk Size: {chunk_size_mb} MB")
    print(f"CPU Cores Used: {cpu_count()}")
    print("----------------------------------------")
    print(f"Result: {'EQUAL' if equal else 'NOT EQUAL'}")
    print(f"Time Elapsed: {end_time - start_time:.6f} seconds")
    print("========================================")

    sys.exit(0 if equal else 2)


if __name__ == "__main__":
    main()
