#!/usr/bin/env python3
"""
sha256_compare.py

DNA Sequence Comparator
Cryptographic hash-based DNA file comparison using SHA-256.

Usage:
    python sha256_compare.py <file1> <file2> [chunk_size_mb]

Example:
    python sha256_compare.py dna1.txt dna2.txt 16

Default chunk size: 8 MB
"""

import hashlib
import os
import sys
import time


def sha256_file(path, chunk_size_bytes):
    sha = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(chunk_size_bytes)
            if not data:
                break
            sha.update(data)

    return sha.hexdigest()


def main():
    if len(sys.argv) < 3:
        print("Usage: python sha256_compare.py <file1> <file2> [chunk_size_mb]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    chunk_size_mb = 8
    if len(sys.argv) >= 4:
        chunk_size_mb = int(sys.argv[3])

    chunk_size_bytes = chunk_size_mb * 1024 * 1024

    # Optional early size check (optimization)
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    if size1 != size2:
        print("========================================")
        print("DNA Sequence Comparator")
        print("----------------------------------------")
        print(f"File 1: {file1}")
        print(f"File 2: {file2}")
        print("----------------------------------------")
        print("Result: NOT EQUAL (file sizes differ)")
        print("========================================")
        sys.exit(2)

    start_time = time.perf_counter()

    hash1 = sha256_file(file1, chunk_size_bytes)
    hash2 = sha256_file(file2, chunk_size_bytes)

    end_time = time.perf_counter()

    equal = (hash1 == hash2)

    print("========================================")
    print("DNA Sequence Comparator")
    print("----------------------------------------")
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")
    print(f"Chunk Size: {chunk_size_mb} MB")
    print("----------------------------------------")
    print(f"SHA-256 File 1: {hash1}")
    print(f"SHA-256 File 2: {hash2}")
    print("----------------------------------------")
    print(f"Result: {'EQUAL' if equal else 'NOT EQUAL'}")
    print(f"Time Elapsed: {end_time - start_time:.6f} seconds")
    print("========================================")

    sys.exit(0 if equal else 2)


if __name__ == "__main__":
    main()
