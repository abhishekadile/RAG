#!/usr/bin/env python
"""Generate seminar notebooks with exercise/solution pattern."""
import json
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

NOTEBOOKS = {
    "01_ingestion": {
        "title": "# 01 — Ingestion Pipeline\n\n**Learning objectives:**\n- Load documents from multiple sources\n- Apply chunking strategies\n- Embed and index into ChromaDB",
        "sections": [
            {
                "intro": "## Setup\n\nImport modules and print configuration.",
                "setup": "import sys\nfrom pathlib import Path\n\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nif str(ROOT) not in sys.path:\n    sys.path.insert(0, str(ROOT))\n\nfrom src.config import FALLBACK_DIR, print_config\nprint_config()",
            },
            {
                "intro": "## Load Documents\n\nLoad the bundled SQuAD fallback corpus.",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Load the SQuAD fallback corpus and print:\n#   - Number of documents loaded\n#   - First document's text (first 200 chars)\n#   - First document's metadata\n\n# YOUR CODE HERE\ndocuments = ???\n\nprint(f\"Loaded: {???} documents\")\nprint(f\"First doc preview: {???}\")\nprint(f\"Metadata: {???}\")",
                "solution": "# ── SOLUTION (expand to see) ──────────────────────────────────────────────\nfrom src.ingestion.loader import load_documents\nfrom src.config import FALLBACK_DIR\n\ndocuments = load_documents(FALLBACK_DIR / \"squad_sample.json\")\n\nprint(f\"Loaded: {len(documents)} documents\")\nprint(f\"First doc preview: {documents[0].text[:200]}\")\nprint(f\"Metadata: {documents[0].metadata}\")",
            },
            {
                "intro": "## Chunk Documents\n\nSplit documents into retrieval-sized chunks.",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Chunk documents using the 'sentence' strategy.\n# Print the number of nodes created.\n\n# YOUR CODE HERE\nfrom src.ingestion.chunker import chunk_documents\n\nnodes = ???\nprint(f\"Created {???} nodes\")",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.ingestion.chunker import chunk_documents\nfrom src.ingestion.embedder import configure_embed_model\n\nembed_model = configure_embed_model()\nnodes = chunk_documents(documents, strategy=\"sentence\")\nprint(f\"Created {len(nodes)} nodes\")",
            },
            {
                "intro": "## Build Vector Index\n\nEmbed chunks and store in ChromaDB.",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Build a ChromaDB index from the nodes.\n\n# YOUR CODE HERE\nfrom src.retrieval.store import get_or_create_index\n\nindex = ???\nprint(\"Index ready!\")",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.retrieval.store import get_or_create_index\n\nindex = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)\nprint(f\"Index ready with {len(nodes)} nodes!\")",
            },
        ],
    },
    "02_retrieval": {
        "title": "# 02 — Retrieval Pipeline\n\n**Learning objectives:**\n- Dense vector retrieval\n- BM25 sparse retrieval\n- Hybrid retrieval fusion",
        "sections": [
            {
                "intro": "## Setup",
                "setup": "import sys\nfrom pathlib import Path\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT))\n\nfrom src.config import FALLBACK_DIR, print_config\nfrom src.ingestion.loader import load_documents\nfrom src.ingestion.chunker import chunk_documents\nfrom src.ingestion.embedder import configure_embed_model\nfrom src.retrieval.store import get_or_create_index\n\nprint_config()\ndocuments = load_documents(FALLBACK_DIR / \"squad_sample.json\")\nembed_model = configure_embed_model()\nnodes = chunk_documents(documents, strategy=\"sentence\")\nindex = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)",
            },
            {
                "intro": "## Dense Retrieval",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Retrieve top-5 chunks for: \"When was George Washington born?\"\n\nquery = \"When was George Washington born?\"\n\n# YOUR CODE HERE\ndense_results = ???\n\nfor i, r in enumerate(dense_results):\n    print(f\"{i+1}. {r.node.get_content()[:100]}...\")",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.retrieval.retriever import get_dense_retriever\nfrom src.utils.display import print_retrieval_results\n\nquery = \"When was George Washington born?\"\ndense = get_dense_retriever(index, top_k=5)\ndense_results = dense.retrieve(query)\nprint_retrieval_results(dense_results)",
            },
            {
                "intro": "## Hybrid Retrieval",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Use hybrid retrieval (dense + BM25) for the same query.\n\n# YOUR CODE HERE\nhybrid_results = ???\nprint(f\"Retrieved {???} chunks\")",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.retrieval.retriever import get_hybrid_retriever\n\nhybrid = get_hybrid_retriever(index, nodes, top_k=5)\nhybrid_results = hybrid.retrieve(query)\nprint_retrieval_results(hybrid_results, \"Hybrid Results\")",
            },
        ],
    },
    "03_generation": {
        "title": "# 03 — Generation Pipeline\n\n**Learning objectives:**\n- Build a RAG query engine\n- Prompt engineering for grounded answers\n- Inspect source citations",
        "sections": [
            {
                "intro": "## Setup",
                "setup": "import sys\nfrom pathlib import Path\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT))\n\nfrom src.config import FALLBACK_DIR, print_config\nfrom src.ingestion.loader import load_documents\nfrom src.ingestion.chunker import chunk_documents\nfrom src.ingestion.embedder import configure_embed_model\nfrom src.retrieval.store import get_or_create_index\n\nprint_config()\ndocuments = load_documents(FALLBACK_DIR / \"squad_sample.json\")\nembed_model = configure_embed_model()\nnodes = chunk_documents(documents, strategy=\"sentence\")\nindex = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)",
            },
            {
                "intro": "## Build Query Engine",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Build a query engine with hybrid retrieval and reranking.\n\n# YOUR CODE HERE\nquery_engine = ???\nprint(\"Query engine ready!\")",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.generation.generator import build_query_engine\n\nquery_engine = build_query_engine(index, nodes=nodes, use_hybrid=True, use_reranker=True)\nprint(\"Query engine ready!\")",
            },
            {
                "intro": "## Ask Questions",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Ask: \"What is the capital of France?\" and print the answer.\n\nquestion = \"What is the capital of France?\"\n\n# YOUR CODE HERE\nresponse = ???\nprint(response)",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.generation.generator import query_with_sources\nfrom src.utils.display import print_qa_result\n\nquestion = \"What is the capital of France?\"\nresult = query_with_sources(query_engine, question)\nprint_qa_result(question, result[\"answer\"], result[\"sources\"])",
            },
        ],
    },
    "04_evaluation": {
        "title": "# 04 — Evaluation Pipeline\n\n**Learning objectives:**\n- Build test sets from SQuAD\n- Run RAGAS metrics\n- Interpret evaluation scores",
        "sections": [
            {
                "intro": "## Setup",
                "setup": "import sys\nfrom pathlib import Path\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT))\n\nfrom src.config import print_config\nprint_config()",
            },
            {
                "intro": "## Load Test Set",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Load 5 QA pairs from the SQuAD fallback test set.\n\n# YOUR CODE HERE\ntestset = ???\nprint(f\"Loaded {???} test samples\")\nprint(testset[0])",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.evaluation.testset import load_squad_testset\n\ntestset = load_squad_testset(sample_size=5)\nprint(f\"Loaded {len(testset)} test samples\")\nprint(testset[0])",
            },
            {
                "intro": "## Run Evaluation",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Run the full RAG pipeline on test questions and evaluate with RAGAS.\n\n# YOUR CODE HERE\n# Hint: use build_query_engine, query_with_sources, evaluate_rag\n\nscores = ???\nprint(scores)",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.config import FALLBACK_DIR\nfrom src.evaluation.evaluator import evaluate_rag, print_eval_summary\nfrom src.generation.generator import build_query_engine, query_with_sources\nfrom src.ingestion.loader import load_documents\nfrom src.ingestion.chunker import chunk_documents\nfrom src.ingestion.embedder import configure_embed_model\nfrom src.retrieval.store import get_or_create_index\n\ndocuments = load_documents(FALLBACK_DIR / \"squad_sample.json\")\nembed_model = configure_embed_model()\nnodes = chunk_documents(documents, strategy=\"sentence\")\nindex = get_or_create_index(nodes=nodes, embed_model=embed_model)\nengine = build_query_engine(index, nodes=nodes)\n\nquestions, answers, contexts, gts = [], [], [], []\nfor item in testset:\n    r = query_with_sources(engine, item[\"question\"])\n    questions.append(item[\"question\"])\n    answers.append(r[\"answer\"])\n    contexts.append([s[\"text\"] for s in r[\"sources\"]] or [item[\"context\"]])\n    gts.append(item[\"ground_truth\"])\n\nscores = evaluate_rag(questions, answers, contexts, gts)\nprint_eval_summary(scores)",
            },
        ],
    },
    "05_advanced": {
        "title": "# 05 — Advanced RAG Patterns\n\n**Learning objectives:**\n- HyDE (Hypothetical Document Embedding)\n- Query rewriting\n- Reranking before generation",
        "sections": [
            {
                "intro": "## Setup",
                "setup": "import sys\nfrom pathlib import Path\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT))\n\nfrom llama_index.core import Settings\nfrom src.config import FALLBACK_DIR, print_config\nfrom src.ingestion.loader import load_documents\nfrom src.ingestion.chunker import chunk_documents\nfrom src.ingestion.embedder import configure_embed_model\nfrom src.retrieval.store import get_or_create_index\nfrom src.utils.fallback import get_llm\n\nprint_config()\ndocuments = load_documents(FALLBACK_DIR / \"squad_sample.json\")\nembed_model = configure_embed_model()\nnodes = chunk_documents(documents, strategy=\"sentence\")\nindex = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)\nllm = get_llm()\nSettings.llm = llm",
            },
            {
                "intro": "## Query Rewriting",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Rewrite a vague query to be more retrieval-friendly.\n\noriginal = \"Who led the revolution?\"\n\n# YOUR CODE HERE\nrewritten = ???\nprint(f\"Original: {original}\")\nprint(f\"Rewritten: {rewritten}\")",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.generation.prompts import QUERY_REWRITE_TEMPLATE\n\noriginal = \"Who led the revolution?\"\nprompt = QUERY_REWRITE_TEMPLATE.format(query_str=original)\nrewritten = llm.complete(prompt).text.strip()\nprint(f\"Original: {original}\")\nprint(f\"Rewritten: {rewritten}\")",
            },
            {
                "intro": "## HyDE + Reranking",
                "exercise": "# ── EXERCISE ──────────────────────────────────────────────────────────────\n# Generate a hypothetical document, retrieve, and rerank.\n\nquery = \"Who was the first president?\"\n\n# YOUR CODE HERE\nreranked = ???\nprint(f\"Top result: {reranked[0].node.get_content()[:200]}...\")",
                "solution": "# ── SOLUTION ──────────────────────────────────────────────────────────────\nfrom src.generation.prompts import HYDE_TEMPLATE\nfrom src.retrieval.retriever import get_hybrid_retriever\nfrom src.retrieval.reranker import build_reranker\nfrom src.utils.display import print_retrieval_results\n\nquery = \"Who was the first president?\"\nhyde_prompt = HYDE_TEMPLATE.format(query_str=query)\nhypothetical = llm.complete(hyde_prompt).text.strip()\n\nretriever = get_hybrid_retriever(index, nodes, top_k=10)\nretrieved = retriever.retrieve(hypothetical[:500])\nprint_retrieval_results(retrieved[:5], \"Before Reranking\")\n\nreranker = build_reranker(top_n=3)\nreranked = reranker.postprocess_nodes(retrieved, query_str=query)\nprint_retrieval_results(reranked, \"After Reranking\")",
            },
        ],
    },
}


def make_cell(cell_type, source, metadata=None):
    """Create a valid nbformat v4 cell (code cells include outputs + execution_count)."""
    meta = metadata or {}
    if cell_type == "code":
        return new_code_cell(source=source, metadata=meta)
    return new_markdown_cell(source=source, metadata=meta)


def build_notebook(spec):
    cells = [make_cell("markdown", spec["title"])]
    for section in spec["sections"]:
        if "intro" in section:
            cells.append(make_cell("markdown", section["intro"]))
        if "setup" in section:
            cells.append(make_cell("code", section["setup"]))
        if "exercise" in section:
            cells.append(make_cell("code", section["exercise"]))
        if "solution" in section:
            cells.append(
                make_cell(
                    "code",
                    section["solution"],
                    metadata={"jupyter": {"source_hidden": True}},
                )
            )
    nb = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "RAG Seminar (Python 3.11)",
                "language": "python",
                "name": "rag-seminar",
            },
            "language_info": {"name": "python", "version": "3.11.0"},
        },
    )
    nbformat.validate(nb)
    return nb


def main():
    out_dir = Path(__file__).parent.parent / "notebooks"
    out_dir.mkdir(exist_ok=True)
    for name, spec in NOTEBOOKS.items():
        nb = build_notebook(spec)
        path = out_dir / f"{name}.ipynb"
        with open(path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"Created {path}")


if __name__ == "__main__":
    main()
