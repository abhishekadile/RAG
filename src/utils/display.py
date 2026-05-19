"""Pretty printing helpers for notebooks and scripts."""
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def print_documents(documents, max_preview: int = 200):
    """Print a summary of loaded documents."""
    c = Console()
    c.print(f"\n[bold cyan]Loaded {len(documents)} documents[/bold cyan]")
    for i, doc in enumerate(documents[:5]):
        preview = doc.text[:max_preview].replace("\n", " ")
        title = doc.metadata.get("title", doc.metadata.get("file_name", f"doc_{i}"))
        c.print(Panel(preview + "...", title=str(title), expand=False))
    if len(documents) > 5:
        c.print(f"  ... and {len(documents) - 5} more")


def print_nodes(nodes, max_preview: int = 150):
    """Print a summary of chunked nodes."""
    c = Console()
    c.print(f"\n[bold cyan]Created {len(nodes)} nodes[/bold cyan]")
    for i, node in enumerate(nodes[:3]):
        preview = node.get_content()[:max_preview].replace("\n", " ")
        c.print(Panel(preview + "...", title=f"Node {i}", expand=False))


def print_retrieval_results(nodes_with_scores, title: str = "Retrieved Chunks"):
    """Print retrieved nodes with scores."""
    c = Console()
    t = Table(title=title, show_header=True)
    t.add_column("#", style="dim")
    t.add_column("Score", style="cyan")
    t.add_column("Text", style="white", max_width=80)

    for i, nws in enumerate(nodes_with_scores):
        score = f"{nws.score:.4f}" if nws.score is not None else "—"
        text = nws.node.get_content()[:120].replace("\n", " ")
        t.add_row(str(i + 1), score, text + "...")

    c.print(t)


def print_qa_result(question: str, answer: str, sources: List[dict] | None = None):
    """Print a Q&A result with optional sources."""
    c = Console()
    c.print(Panel(question, title="Question", style="bold blue"))
    c.print(Panel(answer, title="Answer", style="green"))
    if sources:
        for i, src in enumerate(sources):
            score = src.get("score")
            score_str = f" (score: {score:.4f})" if score is not None else ""
            preview = src["text"][:150].replace("\n", " ")
            c.print(Panel(preview + "...", title=f"Source {i + 1}{score_str}"))
