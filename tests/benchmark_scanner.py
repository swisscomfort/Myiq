#!/usr/bin/env python3
"""
Performance benchmark for scanner module.

Usage:
    python3 tests/benchmark_scanner.py [--files N] [--size SIZE] [--iterations N]

Examples:
    # Quick benchmark (100 files, 1 iteration)
    python3 tests/benchmark_scanner.py

    # Stress test (10000 files, 10 iterations)
    python3 tests/benchmark_scanner.py --files 10000 --iterations 10

    # Large file test (100 files @ 1MB each)
    python3 tests/benchmark_scanner.py --files 100 --size 1048576
"""

import sys
import os
import time
import tempfile
import shutil
import argparse
import statistics
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.modules import search
except ImportError:
    # Fallback import
    sys.path.insert(0, str(project_root / 'tools' / 'modules'))
    import search


def create_benchmark_data(root_dir, num_files=100, file_size=1024):
    """Create benchmark test files."""
    print(f"Creating {num_files} test files ({file_size} bytes each)...")

    patterns = {
        'wallet': b'This is a wallet.dat file with some test data',
        'keystore': b'{"crypto": {"cipher": "aes-128-ctr"}}',
        'mnemonic': b'word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12',
        'private_key': b'a1b2c3d4e5f6' * 10,
        'normal': b'Just a normal text file with regular content',
    }

    files_created = 0
    for i in range(num_files):
        pattern_type = list(patterns.keys())[i % len(patterns)]
        filename = f"{pattern_type}_{i:05d}.txt"
        filepath = root_dir / filename

        content = patterns[pattern_type] * (file_size // len(patterns[pattern_type]) + 1)
        content = content[:file_size]

        filepath.write_bytes(content)
        files_created += 1

    return files_created


def benchmark_scan(root_dir, outdir):
    """Benchmark a single scan operation."""
    start_time = time.time()

    # Scan directory
    search.scan(str(root_dir), str(outdir))

    elapsed = time.time() - start_time
    return elapsed


def main():
    parser = argparse.ArgumentParser(
        description='Benchmark scanner performance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--files',
        type=int,
        default=100,
        help='Number of test files to create (default: 100)'
    )
    parser.add_argument(
        '--size',
        type=int,
        default=1024,
        help='Size of each test file in bytes (default: 1024)'
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=1,
        help='Number of scan iterations (default: 1)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Scanner Performance Benchmark")
    print("=" * 60)
    print(f"Files:      {args.files}")
    print(f"File size:  {args.size} bytes")
    print(f"Iterations: {args.iterations}")
    print("=" * 60)

    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = Path(tmpdir) / 'test_data'
        root_dir.mkdir()

        # Create test data once
        files_created = create_benchmark_data(root_dir, args.files, args.size)
        print(f"✓ Created {files_created} test files\n")

        # Run benchmark iterations
        times = []
        for i in range(args.iterations):
            outdir = Path(tmpdir) / f'output_{i}'
            outdir.mkdir()

            print(f"Iteration {i+1}/{args.iterations}...", end=' ', flush=True)
            elapsed = benchmark_scan(root_dir, outdir)
            times.append(elapsed)
            print(f"{elapsed:.3f}s")

        print("\n" + "=" * 60)
        print("Results")
        print("=" * 60)

        if len(times) == 1:
            print(f"Scan time:  {times[0]:.3f}s")
            print(f"Files/sec:  {args.files / times[0]:.1f}")
            print(f"MB/sec:     {(args.files * args.size) / (times[0] * 1024 * 1024):.2f}")
        else:
            print(f"Min time:   {min(times):.3f}s")
            print(f"Max time:   {max(times):.3f}s")
            print(f"Mean time:  {statistics.mean(times):.3f}s")
            print(f"Median:     {statistics.median(times):.3f}s")
            if len(times) > 1:
                print(f"Std dev:    {statistics.stdev(times):.3f}s")

            avg_time = statistics.mean(times)
            print(f"\nFiles/sec:  {args.files / avg_time:.1f}")
            print(f"MB/sec:     {(args.files * args.size) / (avg_time * 1024 * 1024):.2f}")

        # Performance rating
        files_per_sec = args.files / statistics.mean(times)
        print("\n" + "=" * 60)
        print("Performance Rating")
        print("=" * 60)
        if files_per_sec > 1000:
            rating = "EXCELLENT"
            comment = "Scanner is very fast"
        elif files_per_sec > 500:
            rating = "GOOD"
            comment = "Scanner performance is good"
        elif files_per_sec > 100:
            rating = "ACCEPTABLE"
            comment = "Scanner performance is acceptable"
        else:
            rating = "SLOW"
            comment = "Scanner may need optimization"

        print(f"{rating}: {comment}")
        print(f"Throughput: {files_per_sec:.1f} files/sec")
        print("=" * 60)


if __name__ == '__main__':
    main()
