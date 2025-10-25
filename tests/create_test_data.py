#!/usr/bin/env python3
"""
Test helper script - Creates test data for scanner testing
Usage: python3 tests/create_test_data.py [output_dir]
"""
import os
import sys
import argparse
import tempfile


def create_wallet_files(output_dir):
    """Create various wallet-like test files"""

    test_files = {
        # Wallet files
        "wallet.dat": "Bitcoin Core wallet data\nPrivate keys stored here",

        # Ethereum keystore
        "keystore.json": """{
    "crypto": {
        "cipher": "aes-128-ctr",
        "ciphertext": "1234567890abcdef",
        "kdf": "scrypt"
    },
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "version": 3
}""",

        # Mnemonic seed phrases
        "mnemonic.txt": "abandon ability able about above absent absorb abstract absurd abuse access accident",
        "seed_phrase.txt": "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong",

        # Private key files
        "private_key.pem": """-----BEGIN PRIVATE KEY-----
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
-----END PRIVATE KEY-----""",

        # Bitcoin wallet backup
        "bitcoin_wallet_backup.dat": "BTC wallet backup created 2024-01-01",

        # Ethereum account
        "ethereum_account.json": '{"address": "0x1234567890abcdef1234567890abcdef12345678"}',

        # MetaMask-like
        "metamask_vault.json": '{"data": "encrypted_vault_data", "salt": "random_salt"}',

        # Hardware wallet related
        "ledger_accounts.txt": "Account 0: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "trezor_recovery.txt": "witch collapse practice feed shame open despair creek road again ice least",

        # Normal files (should not trigger)
        "document.txt": "This is a normal document with no crypto content",
        "readme.md": "# Project README\nThis is documentation",
        "photo.jpg": "FAKE_JPEG_DATA",
    }

    print(f"Creating test files in: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    # Create subdirectories
    subdirs = ["wallets", "backups", "keys", "normal"]
    for subdir in subdirs:
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)

    # Place files in appropriate directories
    file_mapping = {
        "wallets": ["wallet.dat", "bitcoin_wallet_backup.dat", "metamask_vault.json"],
        "backups": ["mnemonic.txt", "seed_phrase.txt", "trezor_recovery.txt"],
        "keys": ["keystore.json", "private_key.pem", "ethereum_account.json", "ledger_accounts.txt"],
        "normal": ["document.txt", "readme.md", "photo.jpg"],
    }

    created_files = []
    for subdir, filenames in file_mapping.items():
        for filename in filenames:
            if filename in test_files:
                filepath = os.path.join(output_dir, subdir, filename)
                with open(filepath, 'w') as f:
                    f.write(test_files[filename])
                created_files.append(filepath)
                print(f"  ✓ {subdir}/{filename}")

    return created_files


def create_test_disk_image(output_path, size_mb=10):
    """Create a small test disk image"""
    print(f"\nCreating test disk image: {output_path} ({size_mb}MB)")

    try:
        # Create sparse file
        with open(output_path, 'wb') as f:
            f.seek(size_mb * 1024 * 1024 - 1)
            f.write(b'\0')

        print(f"  ✓ Created {size_mb}MB test image")
        return output_path
    except Exception as e:
        print(f"  ✗ Failed to create disk image: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Create test data for scanner testing")
    parser.add_argument('output_dir', nargs='?',
                       default=tempfile.mkdtemp(prefix="test_data_"),
                       help='Output directory for test files')
    parser.add_argument('--disk-image', action='store_true',
                       help='Also create a test disk image')
    parser.add_argument('--size', type=int, default=10,
                       help='Disk image size in MB (default: 10)')

    args = parser.parse_args()

    print("=" * 60)
    print("Test Data Generator")
    print("=" * 60)

    # Create test files
    created_files = create_wallet_files(args.output_dir)

    print(f"\n✓ Created {len(created_files)} test files")
    print(f"✓ Test data location: {args.output_dir}")

    # Optionally create disk image
    if args.disk_image:
        image_path = os.path.join(args.output_dir, "test_image.dd")
        create_test_disk_image(image_path, args.size)

    # Print usage instructions
    print("\n" + "=" * 60)
    print("Usage:")
    print("=" * 60)
    print(f"\n# Scan test data:")
    print(f"python3 tools/modules/search.py --root {args.output_dir} --outdir ./test_output")
    print(f"\n# Or use analyze script (if disk image created):")
    if args.disk_image:
        print(f"./scripts/analyze.sh {args.output_dir}/test_image.dd ./test_case")
    print(f"\n# Clean up test data:")
    print(f"rm -rf {args.output_dir}")
    print()


if __name__ == '__main__':
    main()
