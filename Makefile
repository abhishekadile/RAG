.PHONY: setup app nb test eval clean help keys download

help:
	@echo "RAG From Scratch — Available commands"
	@echo ""
	@echo "  make setup    Install dependencies (UV)"
	@echo "  make app      Start Gradio frontend (port 7860)"
	@echo "  make nb       Start Jupyter (port 8888)"
	@echo "  make test     Run all fallback .py scripts"
	@echo "  make eval     Run RAGAS evaluation on SQuAD"
	@echo "  make clean    Delete ChromaDB and cached data"
	@echo "  make keys     Check which API keys are configured"

setup:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync
	cp -n .env.example .env || true
	uv run python scripts/download_data.py

app:
	uv run python app/main.py

nb:
	uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=''

test:
	uv run python scripts/run_all.py

eval:
	uv run python scripts/04_evaluation.py

clean:
	rm -rf .chroma_db
	rm -rf data/squad/*.json
	find . -type d -name __pycache__ -exec rm -rf {} +

keys:
	uv run python -c "from src.config import print_config; print_config()"

download:
	uv run python scripts/download_data.py
