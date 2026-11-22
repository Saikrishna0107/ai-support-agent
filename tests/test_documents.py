"""Checks that every knowledge-base document is well formed.

Each document must start with a metadata header (front matter) like:

    ---
    title: Shipping Policy
    category: policy
    last_updated: 2026-11-01
    ---
"""

from datetime import date
from pathlib import Path

import pytest
import yaml

DOCS_DIR = Path(__file__).parent.parent / "data" / "raw"
ALLOWED_CATEGORIES = {"policy", "account", "support", "product", "troubleshooting"}
ALL_DOCS = sorted(DOCS_DIR.rglob("*.md"))


def split_front_matter(text: str) -> tuple[dict, str]:
    """Separate the metadata header from the document body."""
    assert text.startswith("---\n"), "file must start with a '---' header"
    header, body = text[4:].split("\n---\n", 1)
    return yaml.safe_load(header), body


def test_knowledge_base_has_enough_documents():
    assert len(ALL_DOCS) >= 20


# "parametrize" runs this test once per document, so a failure names the bad file
@pytest.mark.parametrize("path", ALL_DOCS, ids=lambda p: p.name)
def test_document_is_well_formed(path: Path):
    metadata, body = split_front_matter(path.read_text(encoding="utf-8"))

    assert isinstance(metadata.get("title"), str) and metadata["title"].strip()
    assert metadata.get("category") in ALLOWED_CATEGORIES
    assert isinstance(metadata.get("last_updated"), date)
    assert body.strip().startswith("# "), "body should start with a '# Title' heading"
    assert len(body.split()) >= 100, "document is too short to be useful"


def test_titles_are_unique():
    titles = [split_front_matter(p.read_text(encoding="utf-8"))[0]["title"] for p in ALL_DOCS]
    assert len(titles) == len(set(titles))
