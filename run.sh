#!/bin/bash
# Script d'exécution pour Linux/Mac
# Naturalisation CAE Prediction

echo "═══════════════════════════════════════════════════════════════════"
echo "  Naturalisation CAE Prediction v1.0"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Vérifier venv
if [ ! -f ".venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please create it with: python -m venv .venv"
    exit 1
fi

echo "[INFO] Activating virtual environment..."
source .venv/bin/activate

echo "[INFO] Running prediction pipeline..."
echo ""

# Run main script
python src/main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  Pipeline completed successfully!"
    echo "═══════════════════════════════════════════════════════════════════"
else
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  Pipeline failed!"
    echo "═══════════════════════════════════════════════════════════════════"
    exit 1
fi
