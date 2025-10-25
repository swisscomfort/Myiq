#!/usr/bin/env bash
# Build standalone executable using PyInstaller
# Creates a portable scanner binary that includes all dependencies
set -euo pipefail

echo "========================================="
echo "Building Standalone Scanner with PyInstaller"
echo "========================================="
echo ""

# Add .local/bin to PATH if needed
export PATH="$HOME/.local/bin:$PATH"

# Check if PyInstaller is installed
if ! command -v pyinstaller >/dev/null 2>&1; then
    echo "PyInstaller not found. Installing..."
    python3 -m pip install pyinstaller --user
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✓ PyInstaller found: $(which pyinstaller)"
echo ""

# Create spec file for better control
cat > crypto-scanner.spec <<'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['tools/modules/search.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='crypto-scanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOF

echo "Building executable..."
echo "This may take a few minutes..."
echo ""

# Build with spec file
pyinstaller --clean --noconfirm crypto-scanner.spec

# Check if successful
if [ -f "dist/crypto-scanner" ]; then
    echo ""
    echo "========================================="
    echo "✓ BUILD SUCCESSFUL!"
    echo "========================================="
    echo ""
    echo "Executable: dist/crypto-scanner"
    echo "Size:       $(du -h dist/crypto-scanner | cut -f1)"
    echo ""
    echo "Usage:"
    echo "  ./dist/crypto-scanner --root /path/to/scan --outdir /path/to/output"
    echo ""
    echo "Test it:"
    echo "  ./dist/crypto-scanner --help"
    echo ""
    echo "To distribute:"
    echo "  cp dist/crypto-scanner /media/usb-stick/"
    echo "  # or"
    echo "  scp dist/crypto-scanner user@remote:/tmp/"
    echo ""

    # Test the executable
    echo "Testing executable..."
    if ./dist/crypto-scanner --help >/dev/null 2>&1; then
        echo "✓ Executable runs correctly"
    else
        echo "⚠ Warning: Executable may have issues"
    fi
    echo ""
else
    echo "❌ Build failed. Check output above for errors."
    exit 1
fi
