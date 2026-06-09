"""Scraper for the official Travian support help center (support.travian.com).

The site is an Intercom-style help center that server-renders both its collection
listings and its article bodies, so a plain fetch + parse is enough.

Exposes two functions used by the orchestrator:
    - get_official_article_urls()  -> list of article URLs across the 4 collections
    - scrape_official_article(url) -> (title, markdown_body)
"""

from __future__ import annotations

import re
from urllib.parse import urljoin

from assets import localize_images
from fetcher import fetch, html_fragment_to_markdown

OFFICIAL_BASE = "https://support.travian.com"
SOURCE_NAME = "Travian: Legends Support"

# The four collections we were asked to scrape, with their stable slugs.
OFFICIAL_COLLECTIONS = {
    "Basic Gameplay": "/en/collections/66-basic-gameplay",
    "Advanced Gameplay": "/en/collections/73-advanced-gameplay",
    "Around The Game": "/en/collections/80-around-the-game",
    "Game Guides": "/en/collections/85-game-guides",
}

# Article permalinks look like /en/articles/123-some-slug.
_ARTICLE_HREF_RE = re.compile(r"/en/articles/\d+-")


def get_official_article_urls() -> list[str]:
    """Collect every /en/articles/... link across the four target collections."""
    urls: list[str] = []
    seen: set[str] = set()
    for name, path in OFFICIAL_COLLECTIONS.items():
        collection_url = urljoin(OFFICIAL_BASE, path)
        print(f"[official] collection: {name} -> {collection_url}")
        soup = fetch(collection_url)
        if soup is None:
            continue
        for a in soup.select('a[href*="/articles/"]'):
            href = a.get("href", "")
            if not _ARTICLE_HREF_RE.search(href):
                continue
            full = urljoin(OFFICIAL_BASE, href.split("?")[0].split("#")[0])
            if full not in seen:
                seen.add(full)
                urls.append(full)
        print(f"           {len(seen)} unique articles so far")
    return urls


def scrape_official_article(url: str, download_images: bool = True) -> tuple[str, str, None] | None:
    """Return (title, markdown_body, written_on) for an official support article.

    Official help-center articles carry no publish date, so written_on is None.
    """
    soup = fetch(url)
    if soup is None:
        return None

    title_el = soup.select_one("h1.article-title")
    content_el = soup.select_one("#article-content") or soup.select_one(
        ".article-content"
    )
    if title_el is None or content_el is None:
        print(f"  ! could not locate article body: {url}")
        return None

    title = title_el.get_text(strip=True)
    if download_images:
        localize_images(content_el, url)
    body_md = html_fragment_to_markdown(content_el)
    return title, body_md, None
