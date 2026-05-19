"""
Document loader. Supports: PDF, Markdown, TXT, URL, SQuAD JSON.
Returns LlamaIndex Document objects in all cases.
"""
import json
from pathlib import Path
from typing import List

from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.readers.base import BaseReader


class SQuADLoader(BaseReader):
    """Load SQuAD 2.0 format JSON into LlamaIndex Documents."""

    def load_data(self, file_path: str | Path) -> List[Document]:
        with open(file_path) as f:
            squad = json.load(f)

        documents = []
        for article in squad["data"]:
            title = article["title"]
            for paragraph in article["paragraphs"]:
                context = paragraph["context"]
                qas = [
                    {
                        "question": qa["question"],
                        "answer": qa["answers"][0]["text"] if qa["answers"] else "",
                    }
                    for qa in paragraph["qas"]
                    if not qa["is_impossible"]
                ]
                documents.append(
                    Document(
                        text=context,
                        metadata={
                            "title": title,
                            "source": "squad",
                            "qa_count": len(qas),
                            "qas_json": json.dumps(qas),
                        },
                    )
                )
        return documents


def load_documents(source: str | Path) -> List[Document]:
    """
    Universal document loader.
    - Directory: loads all files recursively
    - .json: tries SQuAD format
    - URL (starts with http): fetches webpage
    - Single file: loads based on extension
    """
    source = str(source)

    if source.startswith("http"):
        from llama_index.readers.web import SimpleWebPageReader

        return SimpleWebPageReader(html_to_text=True).load_data([source])

    path = Path(source)
    if path.is_dir():
        return SimpleDirectoryReader(str(path), recursive=True).load_data()

    if path.suffix == ".json":
        return SQuADLoader().load_data(path)

    return SimpleDirectoryReader(input_files=[str(path)]).load_data()
