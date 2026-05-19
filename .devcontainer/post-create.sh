#!/bin/bash
set -e

echo "=========================================="
echo "  RAG From Scratch — Codespace Setup"
echo "=========================================="

# Install UV
echo "[1/6] Installing UV..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# Create virtualenv and install deps
echo "[2/6] Installing Python dependencies with UV..."
uv venv .venv --python 3.11
uv sync

# Copy env example if .env doesn't exist
echo "[3/6] Setting up environment file..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  → .env created from .env.example. Add your API keys!"
fi

# Download SQuAD 2.0 fallback data
echo "[4/6] Downloading SQuAD fallback corpus..."
uv run python scripts/download_data.py

# Register Jupyter kernel
echo "[5/6] Registering Jupyter kernel..."
uv run python -m ipykernel install --user --name=rag-seminar --display-name="RAG Seminar (Python 3.11)"

# Run smoke test
echo "[6/6] Running smoke test..."
uv run python -c "
import chromadb
from sentence_transformers import SentenceTransformer
print('  ✓ ChromaDB OK')
print('  ✓ sentence-transformers OK')
print('')
print('========================================')
print('  Setup complete!')
print('  Run: make app    → start Gradio UI')
print('  Run: make nb     → start Jupyter')
print('  Run: make test   → run all scripts')
print('========================================')
"
