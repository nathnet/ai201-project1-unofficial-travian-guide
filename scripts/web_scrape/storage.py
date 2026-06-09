"""Persistence: writes scraped articles to documents/ and tracks them in scraped.md.

This module is the single owner of where output lives. It writes each cleaned
article to ``documents/{prefix}_{slug}.md`` and maintains ``scraped.md`` — the
index used both as a human-readable record and as the dedup key for re-runs.

The index is a markdown table, one row per article:

    |Source|Type|URL|
    |-|-|-|
    |{article title}|{Official/Unofficial}|{url}|
"""

from __future__ import annotations

import re
from pathlib import Path

from fetcher import slugify

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #

# scripts/web_scrape/ -> scripts/ -> project root -> documents/
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DOCUMENTS_DIR = ROOT_DIR / "documents"
# Images live outside documents/ so RAG ingestion (which walks documents/) skips them.
ASSETS_DIR = ROOT_DIR / "assets"
# Tracking file lives in the project root so it is not ingested as a document.
SCRAPED_INDEX = ROOT_DIR / "scraped.md"

INDEX_HEADER = "# Scraped articles\n\n|Source|Type|URL|\n|-|-|-|\n"


# --------------------------------------------------------------------------- #
# scraped.md index tracking
# --------------------------------------------------------------------------- #

def _escape_cell(value: str) -> str:
    """Make a string safe for a single markdown table cell."""
    value = re.sub(r"\s+", " ", value or "").strip()
    return value.replace("|", r"\|")


# Known table header rows (every format we've used), compared whitespace-insensitively.
_HEADER_ROWS = {
    "|source|url|",
    "|source|type|description|url|",
    "|source|type|url|",
}


def _is_header_or_separator(line: str) -> bool:
    """True for a table header row or a |-|-| separator row (not article data)."""
    compact = line.replace(" ", "").lower()
    if compact in _HEADER_ROWS:
        return True
    return bool(compact) and set(compact) <= set("|-:")


def _normalize_data_row(line: str) -> str | None:
    """Reshape any historical article row into the current |Source|Type|URL| form.

    Takes the first cell as the title, the second as the type, and the last as
    the URL — so extra columns from older formats (e.g. Description) are dropped.
    Returns None for rows that don't carry a URL.
    """
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 3 or not cells[-1].startswith("http"):
        return None
    title, article_type, url = cells[0], cells[1], cells[-1]
    return f"|{title}|{article_type}|{url}|"


def init_index(reset: bool = False) -> None:
    """Ensure scraped.md starts with the current header and uses the current columns.

    With reset=True (a --force run) the index is rebuilt from just the header so
    re-scraped articles don't pile up duplicate rows. Otherwise the header is
    normalised and existing rows are reshaped to the current column layout in
    place — this repairs older 2-/4-column files so the table renders correctly.
    """
    if reset or not SCRAPED_INDEX.exists():
        SCRAPED_INDEX.write_text(INDEX_HEADER, encoding="utf-8")
        return
    data_rows = []
    for line in SCRAPED_INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or _is_header_or_separator(line):
            continue
        normalized = _normalize_data_row(line)
        if normalized:
            data_rows.append(normalized)
    body = "\n".join(data_rows) + "\n" if data_rows else ""
    SCRAPED_INDEX.write_text(INDEX_HEADER + body, encoding="utf-8")


def load_scraped_urls() -> set[str]:
    """Read the URLs already recorded in scraped.md (the dedup key).

    Scans each row for the cell holding the URL so the parser is tolerant of
    column order / format changes.
    """
    if not SCRAPED_INDEX.exists():
        return set()
    urls: set[str] = set()
    for line in SCRAPED_INDEX.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        for cell in (c.strip() for c in line.strip("|").split("|")):
            if cell.startswith("http"):
                urls.add(cell)
                break
    return urls


def append_to_index(title: str, article_type: str, url: str) -> None:
    """Append a |Source|Type|URL| row, creating the file if needed."""
    if not SCRAPED_INDEX.exists():
        SCRAPED_INDEX.write_text(INDEX_HEADER, encoding="utf-8")
    row = f"|{_escape_cell(title)}|{article_type}|{url}|\n"
    with SCRAPED_INDEX.open("a", encoding="utf-8") as fh:
        fh.write(row)


def render_document(
    site_name: str,
    title: str,
    url: str,
    body_md: str,
    written_on: str | None = None,
) -> str:
    """Build the full markdown document: title, a metadata blockquote, then body.

    The metadata (Source / URL / optional Written on) lives in one blockquote so
    ingestion can pull the title and content while ignoring that block. Each
    metadata line ends with two spaces to force a hard line break within the
    quote, so they render on separate lines.
    """
    meta_lines = [f"Source: {site_name}", f"URL: {url}"]
    if written_on:
        meta_lines.append(f"Written on {written_on}")
    block = "  \n".join(f"> {line}" for line in meta_lines)
    return f"# {title}\n\n{block}\n\n---\n\n{body_md}"


def save_article(
    prefix: str,
    site_name: str,
    title: str,
    url: str,
    body_md: str,
    written_on: str | None = None,
) -> Path:
    """Write an article to documents/{prefix}_{slug}.md and record it in the index."""
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}_{slugify(title)}.md"
    path = DOCUMENTS_DIR / filename

    path.write_text(render_document(site_name, title, url, body_md, written_on), encoding="utf-8")

    # The index "Type" column is Official/Unofficial, derived from the prefix.
    article_type = "Official" if prefix == "official" else "Unofficial"
    append_to_index(title, article_type, url)
    return path
