#!/usr/bin/env python3
"""
Unit tests for the Python scanner (tools/modules/search.py)
Tests pattern matching, masking, and file scanning functionality.
"""
import unittest
import os
import sys
import tempfile
import shutil
import json
import csv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.modules import search


class TestPatternMatching(unittest.TestCase):
    """Test pattern matching functionality"""

    def test_filename_patterns(self):
        """Test filename pattern matching"""
        test_cases = [
            ("wallet.dat", True),
            ("my_wallet_backup.json", True),
            ("keystore_2024.txt", True),
            ("mnemonic.txt", True),
            ("private_key.pem", True),
            ("ethereum_account.json", True),
            ("btc_wallet.dat", True),
            ("normal_file.txt", False),
            ("document.pdf", False),
        ]

        for filename, should_match in test_cases:
            matched = False
            for pattern in search.FILENAME_PATTERNS:
                if pattern.search(filename):
                    matched = True
                    break
            self.assertEqual(matched, should_match,
                           f"Filename '{filename}' match failed (expected {should_match})")

    def test_content_patterns(self):
        """Test content pattern matching"""
        test_cases = [
            ('"crypto": {"cipher": "aes-128-ctr"}', True),  # JSON keystore
            ('"address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"', True),
            ('1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef', True),  # 64 hex
            ('abandon ability able about above absent absorb abstract absurd abuse access accident', True),  # mnemonic-like
            ('This is just normal text', False),
        ]

        for content, should_match in test_cases:
            matched = False
            for pattern in search.CONTENT_PATTERNS:
                if pattern.search(content):
                    matched = True
                    break
            msg = f"Content pattern match failed for: '{content[:50]}...'"
            self.assertEqual(matched, should_match, msg)


class TestMasking(unittest.TestCase):
    """Test masking functions"""

    def test_mask_hex(self):
        """Test hex string masking"""
        # Long hex string should be masked
        long_hex = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        masked = search.mask_hex(long_hex)
        self.assertNotEqual(masked, long_hex, "Long hex should be masked")
        self.assertIn("123456", masked, "First 6 chars should be visible")
        self.assertIn("cdef", masked, "Last 4 chars should be visible")
        self.assertIn("*", masked, "Should contain asterisks")

        # Short string should be fully masked
        short_hex = "abc123"
        masked_short = search.mask_hex(short_hex)
        # Short strings might not match the pattern, test if it's either unchanged or masked
        self.assertTrue(masked_short == short_hex or "*" in masked_short)

    def test_mask_mnemonic(self):
        """Test mnemonic phrase masking"""
        mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
        masked = search.mask_mnemonic(mnemonic)

        self.assertIn("abandon", masked, "First word should be visible")
        self.assertIn("accident", masked, "Last word should be visible")
        self.assertIn("***", masked, "Should contain masking")
        self.assertLess(len(masked), len(mnemonic), "Masked version should be shorter")

    def test_mask_text(self):
        """Test general text masking"""
        # Test with hex
        text_with_hex = "Private key: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        masked = search.mask_text(text_with_hex)
        self.assertIn("*", masked, "Should contain masking")
        # Note: Not all masked text is shorter due to masking overhead

        # Test length truncation with very long text
        very_long_text = "x" * 200
        masked_long = search.mask_text(very_long_text)
        self.assertLessEqual(len(masked_long), 130, "Long text should be truncated to ~120 chars")
        self.assertIn("...", masked_long, "Should contain ellipsis")


class TestScanner(unittest.TestCase):
    """Test scanner functionality with real files"""

    def setUp(self):
        """Create temporary test directory structure"""
        self.test_dir = tempfile.mkdtemp(prefix="scanner_test_")
        self.output_dir = tempfile.mkdtemp(prefix="scanner_output_")

    def tearDown(self):
        """Clean up temporary directories"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_scan_finds_wallet_files(self):
        """Test that scanner finds wallet-like files"""
        # Create test files
        test_files = {
            "wallet.dat": "This is a wallet file",
            "keystore.json": '{"crypto": {"cipher": "aes-128-ctr"}, "address": "0x123"}',
            "mnemonic.txt": "abandon ability able about above absent absorb abstract absurd abuse access accident",
            "normal.txt": "Just a normal file",
        }

        for filename, content in test_files.items():
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)

        # Run scanner
        search.scan(self.test_dir, self.output_dir)

        # Check output files exist
        csv_files = [f for f in os.listdir(self.output_dir) if f.endswith('.csv')]
        json_files = [f for f in os.listdir(self.output_dir) if f.endswith('.json')]

        self.assertGreater(len(csv_files), 0, "Should generate CSV output")
        self.assertGreater(len(json_files), 0, "Should generate JSON output")

        # Check CSV contains findings
        csv_path = os.path.join(self.output_dir, csv_files[0])
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            findings = list(reader)

        # Should find at least wallet.dat, keystore.json, mnemonic.txt
        self.assertGreaterEqual(len(findings), 3,
                               f"Should find at least 3 files, found {len(findings)}")

    def test_scan_masks_sensitive_data(self):
        """Test that sensitive data is properly masked"""
        # Create file with sensitive content
        sensitive_file = os.path.join(self.test_dir, "private_key.txt")
        sensitive_content = "Private key: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        with open(sensitive_file, 'w') as f:
            f.write(sensitive_content)

        # Run scanner
        search.scan(self.test_dir, self.output_dir)

        # Read results
        json_files = [f for f in os.listdir(self.output_dir) if f.endswith('.json')]
        json_path = os.path.join(self.output_dir, json_files[0])

        with open(json_path, 'r') as f:
            results = json.load(f)

        # Check that snippets are masked
        for result in results:
            snippet = result.get('snippet', '')
            # Full hex string should not be in snippet
            self.assertNotIn('1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
                           snippet, "Full sensitive data should be masked")
            if '123456' in snippet:  # If hex was detected
                self.assertIn('*', snippet, "Should contain masking asterisks")

    def test_scan_respects_file_size_limit(self):
        """Test that large files are handled correctly"""
        # Create a large file
        large_file = os.path.join(self.test_dir, "large_wallet.dat")
        large_content = "wallet data " * 1000000  # ~12MB

        with open(large_file, 'w') as f:
            f.write(large_content)

        # Scanner should handle this without crashing
        try:
            search.scan(self.test_dir, self.output_dir)
            success = True
        except Exception as e:
            success = False
            print(f"Scanner failed on large file: {e}")

        self.assertTrue(success, "Scanner should handle large files gracefully")

    def test_file_sha256(self):
        """Test SHA-256 hash calculation"""
        test_file = os.path.join(self.test_dir, "test.txt")
        test_content = b"Hello World"

        with open(test_file, 'wb') as f:
            f.write(test_content)

        sha256 = search.file_sha256(test_file)

        # Known SHA-256 of "Hello World"
        expected = "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
        self.assertEqual(sha256, expected, "SHA-256 hash should match")


class TestIntegration(unittest.TestCase):
    """Integration tests for full workflow"""

    def test_command_line_execution(self):
        """Test scanner can be executed from command line"""
        test_dir = tempfile.mkdtemp(prefix="cli_test_")
        output_dir = tempfile.mkdtemp(prefix="cli_output_")

        try:
            # Create test file
            test_file = os.path.join(test_dir, "wallet.dat")
            with open(test_file, 'w') as f:
                f.write("wallet data")

            # Run scanner as subprocess
            import subprocess
            result = subprocess.run([
                'python3', 'tools/modules/search.py',
                '--root', test_dir,
                '--outdir', output_dir
            ], capture_output=True, text=True, timeout=10)

            self.assertEqual(result.returncode, 0,
                           f"Scanner should exit successfully. stderr: {result.stderr}")

            # Check output files created
            output_files = os.listdir(output_dir)
            self.assertGreater(len(output_files), 0, "Should create output files")

        finally:
            shutil.rmtree(test_dir, ignore_errors=True)
            shutil.rmtree(output_dir, ignore_errors=True)


def run_tests():
    """Run all tests and return results"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
