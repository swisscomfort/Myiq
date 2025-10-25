#!/usr/bin/env bash
# Quick demo of all portable build options
set -euo pipefail

echo "====================================="
echo "PORTABLE BUILD OPTIONS - QUICK DEMO"
echo "====================================="
echo ""

echo "1. PORTABLE ZIP (Smallest, requires Python)"
echo "   Command: make portable-zip"
echo "   Size:    ~140 KB (compressed)"
echo "   Usage:   Unpack and run with Python"
echo ""

echo "2. PYINSTALLER (Single Executable)"
echo "   Command: make build-standalone"
echo "   Size:    ~30-50 MB"
echo "   Usage:   ./dist/crypto-scanner --root /path --outdir /output"
echo ""

echo "3. DOCKER CONTAINER (Cross-Platform)"
echo "   Command: make docker-build && make docker-save"
echo "   Size:    ~100-200 MB (compressed 40-80 MB)"
echo "   Usage:   docker load < crypto-scanner.tar.gz"
echo "            docker run -v /data:/data crypto-scanner --root /data"
echo ""

echo "4. USB LIVE STICK (Forensic-Ready)"
echo "   Command: make portable-usb DEVICE=/dev/sdX"
echo "   Size:    ~500 MB+"
echo "   Usage:   Boot from USB or mount and run ./RUN_SCANNER.sh"
echo ""

echo "====================================="
echo "RECOMMENDATION BY USE CASE:"
echo "====================================="
echo ""
echo "📋 Quick forensic scan on-site:"
echo "   → USB Live Stick (Option 4)"
echo ""
echo "📧 Send scanner to remote client:"
echo "   → PyInstaller (Option 2)"
echo ""
echo "🔬 Lab environment / CI/CD:"
echo "   → Docker (Option 3)"
echo ""
echo "💻 IT professionals with Python:"
echo "   → Portable Zip (Option 1)"
echo ""

echo "====================================="
echo "QUICK START EXAMPLES:"
echo "====================================="
echo ""

# Check if we're in the right directory
if [ ! -f "tools/modules/search.py" ]; then
    echo "ERROR: Must be run from repository root"
    exit 1
fi

echo "Example 1: Create portable zip"
echo "  $ make portable-zip"
echo "  $ scp crypto-toolkit-portable.tar.gz user@remote:/tmp/"
echo ""

echo "Example 2: Build standalone executable"
echo "  $ make build-standalone"
echo "  $ cp dist/crypto-scanner /media/usb-stick/"
echo ""

echo "Example 3: Docker workflow"
echo "  $ make docker-build"
echo "  $ docker run -v /evidence:/evidence crypto-scanner --root /evidence"
echo ""

echo "Example 4: Create forensic USB (CAUTION: Erases device!)"
echo "  $ make portable-usb DEVICE=/dev/sdb"
echo "  $ # Boot from USB on target system"
echo ""

echo "====================================="
echo "For detailed documentation, see:"
echo "  docs/PORTABLE_DEPLOYMENT.md"
echo "====================================="
