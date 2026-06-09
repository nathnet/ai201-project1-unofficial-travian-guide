"""Scraper for the Unofficial Travian guides (unofficialtravian.com/guides/).

The guides index is a WordPress page whose links live in TablePress tables.
Those tables paginate (e.g. "1 to 10 of 11 entries"), but TablePress renders
*every* row into the static HTML and only paginates client-side with JavaScript
(DataTables). So selecting all rows from each table's <tbody> captures every
article without needing to drive the pager — see get_unofficial_article_urls().

Exposes two functions used by the orchestrator:
    - get_unofficial_article_urls()  -> list of unique article URLs from all tables
    - scrape_unofficial_article(url) -> (title, markdown_body)
"""

from __future__ import annotations

import re
from urllib.parse import urljoin

from assets import localize_images
from fetcher import fetch, html_fragment_to_markdown

UNOFFICIAL_BASE = "https://unofficialtravian.com"
GUIDES_URL = "https://unofficialtravian.com/guides/"
SOURCE_NAME = "Unofficial Travian"

# Article permalinks look like /YYYY/MM/DD/slug/ — match dated posts only.
ARTICLE_URL_RE = re.compile(
    r"^https?://unofficialtravian\.com/20\d{2}/\d{2}/\d{2}/[^/]+/?$"
)

# Leading byline: "(Originally) Posted on {date} by {author} ...".
_BYLINE_RE = re.compile(r"Posted on\s+(.+?)\s+by\b", re.IGNORECASE | re.DOTALL)


def _extract_written_date(content_el) -> str | None:
    """Pull the publish date out of the leading byline and remove that block.

    Articles open with either a <blockquote> (author avatar image + "Originally
    Posted on {date} by {author} on the now closed Official Blog. ...") or a
    plain <p> with the same sentence. The whole block — author image and
    attribution included — is dropped from the body; only the date is returned
    so the caller can record it in the document's metadata blockquote.
    """
    for el in content_el.find_all(["blockquote", "p"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        match = _BYLINE_RE.search(text)
        if match:
            date = re.sub(r"\s+", " ", match.group(1)).strip().rstrip(".,")
            el.decompose()
            return date
        # The first substantial block isn't a byline — stop looking.
        return None
    return None


def get_unofficial_article_urls() -> list[str]:
    """Collect every unique dated article permalink from the guides-page tables.

    All rows of every TablePress table are read straight from the static HTML
    (client-side pagination means later "pages" are already present). The same
    article is sometimes linked from more than one row — across tables and even
    within a single table — so URLs are de-duplicated while preserving order.
    """
    print(f"[unofficial] guides index: {GUIDES_URL}")
    soup = fetch(GUIDES_URL)
    if soup is None:
        return []

    urls: list[str] = []
    seen: set[str] = set()
    duplicates = 0
    tables = soup.select("table.tablepress")
    print(f"             {len(tables)} tables found")

    for table in tables:
        # Read every row, not just the visible page — see module docstring.
        for tr in table.select("tbody > tr"):
            link = tr.select_one("a[href]")
            if link is None:
                continue
            href = urljoin(UNOFFICIAL_BASE, link["href"].split("?")[0].split("#")[0])
            if not ARTICLE_URL_RE.match(href):
                continue
            if href in seen:
                duplicates += 1
                continue
            seen.add(href)
            urls.append(href)

    print(
        f"             {len(urls)} unique articles "
        f"({duplicates} duplicate row link(s) skipped)"
    )
    return urls


def scrape_unofficial_article(url: str, download_images: bool = True) -> tuple[str, str, str | None] | None:
    """Return (title, markdown_body, written_on) for an Unofficial Travian guide."""
    soup = fetch(url)
    if soup is None:
        return None

    title_el = soup.select_one("h1.entry-title")
    # The main post content is the first .entry-content; later ones belong to
    # the "related posts" widget, so scoping to <main> picks the right one.
    main = soup.select_one("main") or soup
    content_el = main.select_one(".entry-content")
    if title_el is None or content_el is None:
        print(f"  ! could not locate article body: {url}")
        return None

    # Drop related-posts blocks and share buttons if they live inside content.
    for junk in content_el.select(
        ".ast-related-posts-wrapper, .sharedaddy, .addtoany_share_save_container, "
        ".post-navigation, .ast-single-related-posts-container"
    ):
        junk.decompose()

    title = title_el.get_text(strip=True)
    # Pull the date out of the byline (and remove that block) before downloading
    # images, so the author avatar in it is never fetched.
    written_on = _extract_written_date(content_el)
    if download_images:
        localize_images(content_el, url)
    body_md = html_fragment_to_markdown(content_el)
    return title, body_md, written_on
