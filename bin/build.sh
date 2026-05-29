#!/bin/bash

pip install pyinstaller
pip install pillow

# keep --windowed cuz i originally had it in the batch script
pyinstaller \
  --distpath "$PWD/.." \
  --onefile \
  --add-data "$PWD/../content:content" \
  --windowed \
  --clean \
  --optimize 2 \
  --icon "$PWD/../content/icon.png" \
  --version-file version.txt \
  "$PWD/../main.py"

rm -f "$PWD/../PyMaker"

mv "$PWD/../main" "$PWD/../PyMaker"

rm -rf build

read -p "Press enter key to continue..."
