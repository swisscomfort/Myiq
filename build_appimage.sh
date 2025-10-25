#!/usr/bin/env bash
# Build AppImage for Linux distribution
# Creates a self-contained, portable Linux application
set -euo pipefail

echo "Building AppImage for Linux..."

# Check dependencies
if ! command -v appimagetool >/dev/null 2>&1; then
    echo "Downloading appimagetool..."
    wget -O appimagetool https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool
fi

# Create AppDir structure
APPDIR="CryptoScanner.AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/lib"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# Copy Python and dependencies
cp -r tools/ "$APPDIR/usr/lib/"
cp -r yara_rules/ "$APPDIR/usr/lib/"

# Create wrapper script
cat > "$APPDIR/usr/bin/crypto-scanner" <<'EOF'
#!/usr/bin/env bash
APPDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
export PYTHONPATH="$APPDIR/usr/lib:$PYTHONPATH"
exec python3 "$APPDIR/usr/lib/tools/modules/search.py" "$@"
EOF
chmod +x "$APPDIR/usr/bin/crypto-scanner"

# Create .desktop file
cat > "$APPDIR/crypto-scanner.desktop" <<EOF
[Desktop Entry]
Name=Crypto Scanner
Exec=crypto-scanner
Icon=crypto-scanner
Type=Application
Categories=Utility;Security;
EOF

# Create AppRun
cat > "$APPDIR/AppRun" <<'EOF'
#!/usr/bin/env bash
APPDIR="$(dirname "$(readlink -f "$0")")"
exec "$APPDIR/usr/bin/crypto-scanner" "$@"
EOF
chmod +x "$APPDIR/AppRun"

# Build AppImage
./appimagetool "$APPDIR" CryptoScanner-x86_64.AppImage

echo ""
echo "✓ AppImage created: CryptoScanner-x86_64.AppImage"
echo "✓ Size: $(du -h CryptoScanner-x86_64.AppImage | cut -f1)"
echo ""
echo "Usage:"
echo "  chmod +x CryptoScanner-x86_64.AppImage"
echo "  ./CryptoScanner-x86_64.AppImage --root /path/to/scan --outdir /output"
