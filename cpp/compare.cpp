/*
 * compare.cpp
 *
 * DNA Sequence Comparator
 *
 * High-performance chunked binary comparison for large DNA sequence files.
 *
 * Usage:
 *   ./compare <file1> <file2> [buffer_size_mb]
 *
 * Example:
 *   ./compare dna1.txt dna2.txt 16
 *
 * Default buffer size: 8 MB
 *
 * Compile:
 *   g++ -O3 -march=native -std=c++17 compare.cpp -o compare
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <cstring>
#include <chrono>
#include <filesystem>

namespace fs = std::filesystem;

bool compare_files(const std::string& file1_path,
                   const std::string& file2_path,
                   std::size_t buffer_size_bytes)
{
    std::ifstream file1(file1_path, std::ios::binary);
    std::ifstream file2(file2_path, std::ios::binary);

    if (!file1.is_open() || !file2.is_open()) {
        std::cerr << "Error: Unable to open one or both files.\n";
        return false;
    }

    // Quick size check before reading
    std::uintmax_t size1 = fs::file_size(file1_path);
    std::uintmax_t size2 = fs::file_size(file2_path);

    if (size1 != size2) {
        return false;
    }

    std::vector<char> buffer1(buffer_size_bytes);
    std::vector<char> buffer2(buffer_size_bytes);

    while (file1 && file2) {
        file1.read(buffer1.data(), buffer_size_bytes);
        file2.read(buffer2.data(), buffer_size_bytes);

        std::streamsize bytes_read1 = file1.gcount();
        std::streamsize bytes_read2 = file2.gcount();

        if (bytes_read1 != bytes_read2) {
            return false;
        }

        if (bytes_read1 == 0) {
            break; // EOF reached
        }

        if (std::memcmp(buffer1.data(), buffer2.data(), bytes_read1) != 0) {
            return false;
        }
    }

    return true;
}

int main(int argc, char* argv[])
{
    if (argc < 3) {
        std::cerr << "Usage: ./compare <file1> <file2> [buffer_size_mb]\n";
        return 1;
    }

    std::string file1 = argv[1];
    std::string file2 = argv[2];

    std::size_t buffer_size_mb = 8; // default
    if (argc >= 4) {
        buffer_size_mb = std::stoul(argv[3]);
    }

    std::size_t buffer_size_bytes = buffer_size_mb * 1024ULL * 1024ULL;

    auto start_time = std::chrono::high_resolution_clock::now();

    bool equal = compare_files(file1, file2, buffer_size_bytes);

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    std::cout << "========================================\n";
    std::cout << "DNA Sequence Comparator\n";
    std::cout << "----------------------------------------\n";
    std::cout << "File 1: " << file1 << "\n";
    std::cout << "File 2: " << file2 << "\n";
    std::cout << "Buffer Size: " << buffer_size_mb << " MB\n";
    std::cout << "----------------------------------------\n";
    std::cout << "Result: " << (equal ? "EQUAL" : "NOT EQUAL") << "\n";
    std::cout << "Time Elapsed: " << elapsed.count() << " seconds\n";
    std::cout << "========================================\n";

    return equal ? 0 : 2;
}
