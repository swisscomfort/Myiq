#!/usr/bin/env bash
# Create a bootable forensic USB stick with the scanner
# CAUTION: This will format the target device!
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /dev/sdX"
    echo ""
    echo "CAUTION: This will ERASE the target device!"
    echo "Available devices:"
    lsblk -d -o NAME,SIZE,TYPE,MOUNTPOINT | grep disk
    exit 2
fi

DEVICE="$1"

# Safety check
if [[ ! "$DEVICE" =~ ^/dev/sd[b-z]$ ]]; then
    echo "ERROR: Device must be /dev/sdX (not sda to avoid system disk)"
    exit 3
fi

echo "WARNING: This will ERASE $DEVICE"
echo "Press Ctrl+C to cancel, or wait 10 seconds to continue..."
sleep 10

echo "Creating portable forensic USB stick on $DEVICE..."

# Unmount if mounted
sudo umount "${DEVICE}"* 2>/dev/null || true

# Create partition
sudo parted -s "$DEVICE" mklabel gpt
sudo parted -s "$DEVICE" mkpart primary ext4 1MiB 100%
sudo parted -s "$DEVICE" set 1 boot on

# Format
PARTITION="${DEVICE}1"
sudo mkfs.ext4 -L "CryptoForensics" "$PARTITION"

# Mount
MOUNT_POINT="/mnt/crypto_usb"
sudo mkdir -p "$MOUNT_POINT"
sudo mount "$PARTITION" "$MOUNT_POINT"

# Copy toolkit
echo "Copying toolkit..."
sudo cp -r . "$MOUNT_POINT/crypto-toolkit/"
sudo chmod +x "$MOUNT_POINT/crypto-toolkit/start.sh"
sudo chmod +x "$MOUNT_POINT/crypto-toolkit/scripts/"*.sh

# Create autorun script
cat <<'EOF' | sudo tee "$MOUNT_POINT/RUN_SCANNER.sh" >/dev/null
#!/usr/bin/env bash
cd "$(dirname "$0")/crypto-toolkit"
echo "Crypto Recovery Toolkit - Portable Version"
echo "==========================================="
echo ""
echo "1. Create case and image disk:"
echo "   sudo ./start.sh /dev/sdX ./cases \"Client Name\""
echo ""
echo "2. Scan existing directory:"
echo "   python3 tools/modules/search.py --root /path --outdir ./output"
echo ""
echo "3. Launch GUI:"
echo "   python3 tools/gui/gui.py"
echo ""
read -p "Press Enter to continue..."
EOF
sudo chmod +x "$MOUNT_POINT/RUN_SCANNER.sh"

# Create README
cat <<'EOF' | sudo tee "$MOUNT_POINT/README.txt" >/dev/null
CRYPTO RECOVERY TOOLKIT - PORTABLE USB VERSION
==============================================

This USB stick contains a complete forensic toolkit for crypto asset recovery.

QUICK START:
1. Boot from USB or mount on any Linux system
2. Run: ./RUN_SCANNER.sh
3. Follow on-screen instructions

REQUIREMENTS:
- Linux system (Debian/Ubuntu recommended)
- Python 3.8+
- Root access for disk imaging

DOCUMENTATION:
See crypto-toolkit/docs/ for comprehensive guides

SECURITY NOTICE:
- All scans are read-only
- Sensitive data is automatically masked
- GPG signatures ensure chain of custody
- Works offline for maximum security

For support: See crypto-toolkit/README.md
EOF

# Sync and unmount
sudo sync
sudo umount "$MOUNT_POINT"

echo ""
echo "✓ Portable USB stick created successfully!"
echo "✓ Device: $DEVICE"
echo "✓ Label: CryptoForensics"
echo ""
echo "Usage:"
echo "  1. Mount USB stick on target system"
echo "  2. Run: ./RUN_SCANNER.sh"
echo "  3. Or: cd crypto-toolkit && python3 tools/modules/search.py --help"
