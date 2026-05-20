#!/bin/bash
set -e

echo "=========================================="
echo "  RAG From Scratch — Codespace Setup"
echo "=========================================="

# Install UV
echo "[1/6] Installing UV..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# CRITICAL: export PATH for THIS shell session immediately after install.
# Do not rely on ~/.bashrc — it only applies to new shells.
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile

# Verify UV is reachable before proceeding
if ! command -v uv &>/dev/null; then
  # Some older UV installers use ~/.cargo/bin
  export PATH="$HOME/.cargo/bin:$PATH"
  echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
fi

echo "  UV version: $(uv --version)"

# uv sync creates .venv automatically — DO NOT call uv venv first
echo "[2/6] Installing Python dependencies with UV..."
uv sync --python 3.11

# Copy env example if .env doesn't exist
echo "[3/6] Setting up environment file..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  → .env created from .env.example. Add your API keys!"
fi

# Download SQuAD data using uv run (ensures correct venv python)
echo "[4/6] Downloading SQuAD fallback corpus..."
uv run python scripts/download_data.py

# Register Jupyter kernel
echo "[5/6] Registering Jupyter kernel..."
uv run python -m ipykernel install --user \
  --name=rag-seminar \
  --display-name="RAG Seminar (Python 3.11)"

# Smoke test
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
