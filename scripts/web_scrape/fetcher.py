"""HTTP fetching and HTML-to-markdown helpers shared by the site scrapers.

This module owns the network layer (a single pooled session with retries and a
polite delay) and the conversion of an HTML fragment into clean markdown. It has
no knowledge of either target site or of where documents are stored.
"""

from __future__ import annotations

import re
import time

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_md

# --------------------------------------------------------------------------- #
# Request configuration
# --------------------------------------------------------------------------- #

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
REQUEST_TIMEOUT = 30          # seconds
POLITE_DELAY = 1.0            # seconds between page requests, to avoid hammering servers
ASSET_DELAY = 0.3            # shorter pause between image/asset downloads
MAX_RETRIES = 3

_session = requests.Session()
_session.headers.update(REQUEST_HEADERS)


# --------------------------------------------------------------------------- #
# Networking
# --------------------------------------------------------------------------- #

def fetch(url: str) -> BeautifulSoup | None:
    """Fetch a URL with retries and return a parsed BeautifulSoup tree.

    Returns None if the page could not be retrieved. Raw bytes are handed to
    BeautifulSoup directly so it can sniff the document's declared charset.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = _session.get(url, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            time.sleep(POLITE_DELAY)
            return BeautifulSoup(resp.content, "lxml")
        except requests.RequestException as exc:
            print(f"  ! fetch failed ({attempt}/{MAX_RETRIES}) {url}: {exc}")
            time.sleep(POLITE_DELAY * attempt)
    return None


def download_bytes(url: str) -> tuple[bytes, str] | None:
    """Download a binary asset, returning (content, content_type) or None."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = _session.get(url, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            time.sleep(ASSET_DELAY)
            return resp.content, resp.headers.get("Content-Type", "")
        except requests.RequestException as exc:
            print(f"    ! asset fetch failed ({attempt}/{MAX_RETRIES}) {url}: {exc}")
            time.sleep(ASSET_DELAY * attempt)
    return None


# --------------------------------------------------------------------------- #
# Text / markdown helpers
# --------------------------------------------------------------------------- #

def slugify(text: str) -> str:
    """Turn an article title into a safe, lowercase filename slug."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)   # drop punctuation
    text = re.sub(r"[\s_-]+", "-", text)   # collapse whitespace to single dash
    return text.strip("-") or "untitled"


def clean_markdown(md: str) -> str:
    """Tidy markdownify output: collapse excess blank lines and stray spaces."""
    # Normalise line endings.
    md = md.replace("\r\n", "\n").replace("\r", "\n")
    # Strip trailing whitespace on each line.
    md = "\n".join(line.rstrip() for line in md.split("\n"))
    # Collapse 3+ blank lines into a single blank line.
    md = re.sub(r"\n{3,}", "\n\n", md)
    # Remove zero-width / non-breaking-space artifacts.
    md = md.replace("\u200B", "").replace("\xa0", " ")
    return md.strip() + "\n"


def html_fragment_to_markdown(node) -> str:
    """Convert a BeautifulSoup element's inner HTML into clean markdown."""
    md = html_to_md(
        str(node),
        heading_style="ATX",      # use #, ## headings
        bullets="-",
        strip=["script", "style"],
        # Keep prose clean: don't backslash-escape punctuation like "long-term"
        # or "1." — the noise only hurts downstream embedding quality.
        escape_misc=False,
        escape_asterisks=False,
        escape_underscores=False,
    )
    return clean_markdown(md)
