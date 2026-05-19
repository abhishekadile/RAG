#!/usr/bin/env python
"""Download SQuAD 2.0 validation set (optional full corpus)."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SQUAD_DIR = ROOT / "data" / "squad"
FALLBACK_DIR = ROOT / "data" / "fallback"


def download_squad():
    """Download SQuAD 2.0 validation split if not present."""
    SQUAD_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SQUAD_DIR / "dev-v2.0.json"

    if out_path.exists():
        print(f"  SQuAD already downloaded: {out_path}")
        return out_path

    print("  Downloading SQuAD 2.0 validation set...")
    try:
        from datasets import load_dataset

        ds = load_dataset("squad_v2", split="validation[:500]")

        articles: dict = {}
        for row in ds:
            title = row["title"]
            if title not in articles:
                articles[title] = {"title": title, "paragraphs": {}}

            ctx = row["context"]
            if ctx not in articles[title]["paragraphs"]:
                articles[title]["paragraphs"][ctx] = []

            answers = row["answers"]
            answer_texts = answers.get("text", []) if isinstance(answers, dict) else []
            articles[title]["paragraphs"][ctx].append(
                {
                    "id": row["id"],
                    "question": row["question"],
                    "answers": [
                        {"text": t, "answer_start": answers["answer_start"][i]}
                        for i, t in enumerate(answer_texts)
                    ]
                    if answer_texts
                    else [],
                    "is_impossible": row.get("is_impossible", False),
                }
            )

        squad_format = {
            "version": "v2.0",
            "data": [
                {
                    "title": art["title"],
                    "paragraphs": [
                        {"context": ctx, "qas": qas}
                        for ctx, qas in art["paragraphs"].items()
                    ],
                }
                for art in articles.values()
            ],
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(squad_format, f)
        print(f"  [OK] Saved SQuAD subset to {out_path}")
        return out_path
    except Exception as e:
        print(f"  [WARN] Could not download full SQuAD: {e}")
        print("  Using bundled fallback data in data/fallback/")
        return None


def verify_fallback():
    """Verify bundled fallback data exists."""
    sample = FALLBACK_DIR / "squad_sample.json"
    if not sample.exists():
        raise FileNotFoundError(f"Missing bundled fallback: {sample}")
    with open(sample, encoding="utf-8") as f:
        data = json.load(f)
    n_articles = len(data["data"])
    n_qas = sum(len(p["qas"]) for a in data["data"] for p in a["paragraphs"])
    print(f"  [OK] Fallback corpus: {n_articles} articles, {n_qas} QA pairs")


if __name__ == "__main__":
    print("Setting up data...")
    verify_fallback()
    download_squad()
    print("  Data setup complete.")
