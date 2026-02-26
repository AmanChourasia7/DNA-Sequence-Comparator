# DNA Sequence Comparator

A High-Performance Framework for Genomic Sequence Equality Testing and Benchmarking

## Overview

The **DNA Sequence Comparator** is a research-focused software suite for efficient comparison of large-scale DNA sequence files. It implements multiple algorithmic strategies and provides automated benchmarking tools for performance evaluation.

* Designed for computational genomics and systems research
* Supports DNA sequences using only the nucleotide symbols: **A, G, C, T**
* Optimized for files ranging from millions to billions of characters

## Research Objectives

* Evaluate time complexity of large-scale sequence comparison
* Benchmark algorithmic approaches under realistic I/O constraints
* Compare raw memory comparison versus cryptographic hashing
* Analyze multiprocessing scalability on modern multi-core systems


## Implemented Methods

### 1. High-Performance C++ Chunked Comparison

* Binary file reading
* Large-buffer streaming (8–32 MB recommended)
* Fast memory comparison using `std::memcmp`
* Early termination on mismatch
* Optimized for compilation with `-O3 -march=native`

**Time Complexity:** O(n)  
**Memory Complexity:** O(buffer_size)


### 2. Parallel Multiprocessing Comparison (Python)

* File partitioning into fixed-size segments
* Multi-core execution via `multiprocessing.Pool`
* Best suited for high-speed SSD/NVMe storage

**Time Complexity:** O(n)  
**Scalability:** Hardware dependent (I/O-bound systems may limit gains)

### 3. SHA-256 Hash-Based Comparison

* Streaming cryptographic hashing
* Integrity verification approach
* Suitable for distributed validation pipelines

**Time Complexity:** O(n)  
**Advantage:** Enables persistent fingerprinting of genomic data

### 4. Automated Benchmarking Framework

* Measures execution time for each method
* Reports file size metadata
* Generates comparative timing plots
* Produces structured performance summaries


## Repository Structure

```
dna-sequence-comparator/
│
├── cpp/
│   └── compare.cpp
│
├── python/
│   ├── parallel_compare.py
│   ├── sha256_compare.py
│   └── benchmark.py
│
├── data/
│   └── sample_dna_files/
│
└── README.md
```



## Installation

### C++ Version

**Requirements:**
* GCC or Clang (C++17 or later)

**Compile:**
```
g++ -O3 -march=native cpp/compare.cpp -o compare
```


### Python Version

**Requirements:**
* Python 3.9+
* matplotlib

**Install dependencies:**
```
pip install matplotlib
```


## Usage

### C++ Comparison

```
./compare dna1.txt dna2.txt
```
* Outputs equality result and execution time (seconds)



### Python Multiprocessing Comparison

```
python python/parallel_compare.py dna1.txt dna2.txt
```



### SHA-256 Comparison

```
python python/sha256_compare.py dna1.txt dna2.txt
```


### Benchmark Execution

```
python python/benchmark.py dna1.txt dna2.txt
```
* Produces structured timing report, comparative bar graph, and file size summary


## Performance Considerations

* Performance is primarily I/O bound on HDD systems
* NVMe SSD recommended for multiprocessing experiments
* Larger buffer sizes improve throughput
* Cryptographic hashing introduces additional CPU overhead
* For extremely large files (>100GB), consider memory-mapped I/O



## Experimental Design Notes

For meaningful benchmarking:

* Test across multiple file sizes (1MB, 10MB, 100MB, 1GB)
* Record hardware configuration (CPU model, storage type, RAM)
* Repeat trials to reduce variance
* Report mean and standard deviation



## Limitations

* Assumes identical formatting between files
* Does not ignore whitespace or line breaks unless preprocessed
* Designed for plain-text DNA sequences only


## Future Extensions

* SIMD-accelerated comparison
* Non-cryptographic hashing (xxHash)
* Distributed comparison across cluster nodes
* Memory-mapped implementation
* Integration with FASTA parsing


## Contact

For research collaboration or academic inquiries, please open an issue in the repository.
