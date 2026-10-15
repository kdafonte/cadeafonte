#!/bin/sh
# Prepara o ambiente para renderizar artes (fontes, navegador headless, ffmpeg).
cd "$(dirname "$0")"
[ -d node_modules/@fontsource/fraunces ] || (npm init -y >/dev/null 2>&1; npm i @fontsource/fraunces @fontsource/ibm-plex-sans @fontsource/arimo >/dev/null 2>&1)
python3 -c "import playwright" 2>/dev/null || pip install --break-system-packages -q playwright
python3 -m playwright install chromium >/dev/null 2>&1
which ffmpeg >/dev/null || (apt-get install -y -qq ffmpeg >/dev/null 2>&1)
python3 -c "import numpy" 2>/dev/null || pip install --break-system-packages -q numpy
echo setup-ok
