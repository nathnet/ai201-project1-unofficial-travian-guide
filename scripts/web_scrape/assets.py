"""Downloads article images into assets/ and rewrites <img> links to point there.

Called by the site scrapers on an article's content element *before* it is
converted to markdown. Each unique remote image is downloaded only once (cached
by URL, even across articles and re-runs) and stored under the project-root
``assets/`` directory. The <img> src is rewritten to a relative path
(``../assets/...``) that resolves from a document in ``documents/``.

assets/ sits outside documents/ on purpose, so it does not get ingested by the
RAG pipeline.
"""

from __future__ import annotations

import hashlib
import mimetypes
import os
import re
from urllib.parse import urljoin, urlparse

from fetcher import download_bytes
from storage import ASSETS_DIR

# Relative path from a documents/*.md file to the sibling assets/ directory.
_REL_PREFIX = "../assets"

# Remote image URL -> relative markdown path, reused within and across articles.
_url_cache: dict[str, str] = {}


def _asset_filename(url: str, content_type: str, digest: str) -> str:
    """Build a collision-proof asset filename: {url-hash}_{sanitized basename}."""
    base = os.path.basename(urlparse(url).path)
    base = re.sub(r"[^\w.\-]", "_", base).strip("_")
    name, ext = os.path.splitext(base)
    if not ext:
        ext = mimetypes.guess_extension((content_type or "").split(";")[0].strip()) or ".img"
        base = (name or "image") + ext
    return f"{digest}_{base}"


def _store(url: str) -> str | None:
    """Download a single image (or reuse a cached copy); return its relative path."""
    if url in _url_cache:
        return _url_cache[url]

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]

    # Idempotency across runs: a file with this URL's digest already on disk.
    existing = next(iter(ASSETS_DIR.glob(f"{digest}_*")), None)
    if existing is not None:
        rel = f"{_REL_PREFIX}/{existing.name}"
        _url_cache[url] = rel
        return rel

    result = download_bytes(url)
    if result is None:
        return None
    data, content_type = result
    filename = _asset_filename(url, content_type, digest)
    (ASSETS_DIR / filename).write_bytes(data)

    rel = f"{_REL_PREFIX}/{filename}"
    _url_cache[url] = rel
    return rel


def localize_images(content_el, page_url: str) -> int:
    """Download every <img> in content_el and point it at a local asset.

    Returns the number of images successfully localized. Images that fail to
    download keep their original remote src so the reference is not lost.
    """
    saved = 0
    for img in content_el.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src or src.startswith("data:"):
            continue
        abs_url = urljoin(page_url, src)
        if not abs_url.startswith(("http://", "https://")):
            continue

        rel = _store(abs_url)
        if rel is None:
            continue
        img["src"] = rel
        # Drop responsive-image attrs so the converter uses our local src only.
        for attr in ("srcset", "data-src", "data-lazy-src", "data-srcset"):
            if img.has_attr(attr):
                del img[attr]
        saved += 1
    return saved
