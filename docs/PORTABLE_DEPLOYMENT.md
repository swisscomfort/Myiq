# Portable Deployment Guide

Dieses Dokument beschreibt verschiedene Methoden, um den Scanner als transportables, komplettes Programm zu verpacken.

## 📦 Übersicht der Optionen

| Methode | Plattform | Größe | Komplexität | Forensik-Tauglich |
|---------|-----------|-------|-------------|-------------------|
| **PyInstaller** | Linux/Windows | ~30-50 MB | Niedrig | ✅ Ja |
| **Docker** | Alle | ~100-200 MB | Mittel | ✅ Ja |
| **AppImage** | Linux | ~40-60 MB | Mittel | ✅ Ja |
| **USB Live Stick** | Linux | ~500 MB+ | Hoch | ✅✅ Perfekt |
| **Zip Archive** | Alle | ~5 MB | Sehr niedrig | ⚠️ Benötigt Python |

---

## 1. PyInstaller (Einzelne Executable)

### Vorteile
- ✅ Einzelne ausführbare Datei
- ✅ Keine Python-Installation nötig
- ✅ Klein (~30-50 MB)
- ✅ Schnell zu erstellen

### Nachteile
- ❌ Plattform-spezifisch (Linux-Build läuft nur auf Linux)
- ❌ Shell-Scripts müssen separat bleiben

### Verwendung

```bash
# Build erstellen
chmod +x build_standalone.sh
./build_standalone.sh

# Executable testen
./dist/crypto-scanner --root /tmp/test --outdir /tmp/output

# Verteilen
cp dist/crypto-scanner /path/to/usb-stick/
```

### Verzeichnis-Struktur auf USB-Stick

```
usb-stick/
├── crypto-scanner          # Executable
├── yara_rules/             # Optional: YARA-Regeln
└── README.txt              # Anleitung
```

**Größe:** ~30-50 MB

---

## 2. Docker Container

### Vorteile
- ✅ Plattform-unabhängig (läuft überall mit Docker)
- ✅ Isoliert und sicher
- ✅ Reproduzierbar
- ✅ Einfach zu aktualisieren

### Nachteile
- ❌ Docker muss installiert sein
- ❌ Größer (~100-200 MB)
- ❌ Overhead durch Container

### Verwendung

```bash
# Container bauen
docker build -t crypto-scanner .

# Scan ausführen
docker run -v /evidence:/evidence crypto-scanner \
    --root /evidence \
    --outdir /evidence/reports

# Image exportieren (für Transport)
docker save crypto-scanner | gzip > crypto-scanner.tar.gz

# Auf anderem System laden
gunzip -c crypto-scanner.tar.gz | docker load
```

**Größe:** ~100-200 MB (komprimiert ~40-80 MB)

---

## 3. AppImage (Linux)

### Vorteile
- ✅ Sehr portabel für Linux
- ✅ Doppelklick-Ausführung
- ✅ Kein Root nötig
- ✅ Selbst-aktualisierend möglich

### Nachteile
- ❌ Nur Linux
- ❌ Komplexer Build-Prozess

### Verwendung

```bash
# AppImage bauen
chmod +x build_appimage.sh
./build_appimage.sh

# Ausführen
chmod +x CryptoScanner-x86_64.AppImage
./CryptoScanner-x86_64.AppImage --root /path --outdir /output
```

**Größe:** ~40-60 MB

---

## 4. USB Live Stick (Forensik-Optimal) ⭐

### Vorteile
- ✅✅ **Perfekt für Forensik**
- ✅ Bootfähig
- ✅ Komplettes Toolkit inklusive
- ✅ Offline verwendbar
- ✅ Chain-of-Custody konform

### Nachteile
- ❌ Größer (500 MB+)
- ❌ Benötigt USB-Stick
- ❌ Längere Erstellung

### Verwendung

```bash
# USB-Stick erstellen (VORSICHT: Löscht alle Daten!)
chmod +x create_portable_usb.sh
sudo ./create_portable_usb.sh /dev/sdX

# Auf Zielsystem verwenden
# 1. USB-Stick einstecken
# 2. Mounten (wenn nicht automatisch)
# 3. ./RUN_SCANNER.sh ausführen
```

### Inhalt des USB-Sticks

```
CryptoForensics/
├── RUN_SCANNER.sh          # Starter-Script
├── README.txt              # Anleitung
└── crypto-toolkit/         # Komplettes Repository
    ├── start.sh
    ├── scripts/
    ├── tools/
    ├── docs/
    └── templates/
```

**Größe:** ~500 MB (mit allen Docs und Tools)

---

## 5. Einfaches Zip-Archiv

### Vorteile
- ✅ Sehr einfach
- ✅ Klein (~5 MB)
- ✅ Plattform-unabhängig

### Nachteile
- ❌ Python muss auf Zielsystem installiert sein
- ❌ Dependencies müssen installiert werden

### Verwendung

```bash
# Archiv erstellen
make portable-zip

# Oder manuell
tar czf crypto-toolkit-portable.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='tests/' \
    .

# Auf Zielsystem
tar xzf crypto-toolkit-portable.tar.gz
cd crypto-toolkit
python3 tools/modules/search.py --help
```

**Größe:** ~5 MB

---

## 🎯 Empfehlungen nach Anwendungsfall

### Forensik vor Ort (Client-Besuch)
→ **USB Live Stick** (Option 4)
- Bootfähig
- Komplett eigenständig
- Alle Tools inklusive
- Chain-of-Custody Dokumentation dabei

### Remote-Scan (Scanner-Tool versenden)
→ **PyInstaller** (Option 1)
- Einzelne Datei
- Einfach per Email/Download
- Sofort lauffähig

### Labor-Umgebung (Wiederholte Verwendung)
→ **Docker** (Option 2)
- Reproduzierbar
- Isoliert
- Einfach aktualisierbar

### Linux-Workstations
→ **AppImage** (Option 3)
- Doppelklick-Ausführung
- Keine Installation nötig
- Portable

### Entwickler/IT-Profis
→ **Zip-Archiv** (Option 5)
- Python bereits vorhanden
- Volle Kontrolle
- Einfach modifizierbar

---

## 🔐 Sicherheitshinweise

### Für alle Methoden:
- ✅ Scanner ist read-only (keine Schreibzugriffe auf Quellen)
- ✅ Sensitive Daten werden maskiert
- ✅ SHA-256 Hashes für Integrität
- ✅ Offline-fähig (keine Netzwerk-Verbindung nötig)

### Zusätzlich bei USB Live Stick:
- ✅ GPG-Signierung möglich
- ✅ Chain-of-Custody Dokumentation
- ✅ Bootfähig (keine Manipulation des Host-Systems)
- ✅ Write-Protection empfohlen (Hardware-Schalter)

---

## 📋 Vergleichstabelle

| Feature | PyInstaller | Docker | AppImage | USB Stick | Zip |
|---------|-------------|--------|----------|-----------|-----|
| **Größe** | 30-50 MB | 100-200 MB | 40-60 MB | 500+ MB | 5 MB |
| **Python nötig** | ❌ Nein | ❌ Nein | ❌ Nein | ❌ Nein | ✅ Ja |
| **Plattformen** | 1 | Alle | Linux | Linux | Alle |
| **Boot-fähig** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **GUI inklusive** | ⚠️ Komplex | ✅ | ✅ | ✅ | ✅ |
| **Scripts inklusive** | ⚠️ Separat | ✅ | ✅ | ✅ | ✅ |
| **Forensik-Konform** | ✅ | ✅ | ✅ | ✅✅ | ⚠️ |
| **Chain-of-Custody** | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ |
| **Erstellungszeit** | 2 Min | 5 Min | 10 Min | 15 Min | 30 Sek |

---

## 🚀 Quick Start

### Schnellste Lösung (2 Minuten):
```bash
make build-standalone
cp dist/crypto-scanner /path/to/usb-stick/
```

### Forensik-Lösung (15 Minuten):
```bash
sudo make portable-usb DEVICE=/dev/sdX
```

### Universelle Lösung (5 Minuten):
```bash
make docker-build
make docker-save
# Datei crypto-scanner.tar.gz verteilen
```

---

## 🔧 Troubleshooting

### PyInstaller: "command not found"
```bash
pip3 install pyinstaller
```

### Docker: "permission denied"
```bash
sudo usermod -aG docker $USER
# Logout/Login erforderlich
```

### USB Stick: "Device busy"
```bash
sudo umount /dev/sdX*
sudo fuser -k /dev/sdX
```

### AppImage: "FUSE not available"
```bash
./CryptoScanner-x86_64.AppImage --appimage-extract
cd squashfs-root
./AppRun
```

---

## 📚 Siehe auch

- [Quick Start Guide](QUICK_START.md) - Erste Schritte
- [Operators Guide](OPERATORS_GUIDE.md) - Forensik-Workflows
- [Testing Guide](TESTING.md) - Portable Builds testen
- [Security Policy](../SECURITY.md) - Sicherheitsrichtlinien

---

**Letzte Aktualisierung:** 2025-10-25
**Version:** 1.0.0
