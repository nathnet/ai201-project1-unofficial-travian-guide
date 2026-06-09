"""
A one-time script to scrape all articles from two websites, clean,
and save them into respective md format keeping the article structures.
Each article is saved in ../documents and add an entry in
a separate scraped.md file to keep track of files that have been scraped
in the format below with the URL being the id:
|Source|Type|URL|
|-|-|-|
|{Article title}|{Official/unofficial}|{URL}|

1. https://support.travian.com/en
Scrape all articles in 'Basic Gameplay', 'Advanced Gameplay',
'Around The Game', 'Game Guides' collections and save the documents in
the format of `official_{article_title}.md`. Each article follows URL format of
https://support.travian.com/en/articles/{article-name}

2. https://unofficialtravian.com/guides/
Scrape all articles in each table (each article follows URL format of
https://unofficialtravian.com/{year}/{month}/{article-name}) and save the documents
in the format of `unofficial_{article_title}.md`.


This file is the entry point. It wires together the focused modules:
    - fetcher.py      HTTP session + HTML-to-markdown helpers
    - storage.py      writing documents/ files and the scraped.md index
    - official.py     link discovery + article scraping for support.travian.com
    - unofficial.py   link discovery + article scraping for unofficialtravian.com

Usage
-----
    python scripts/scrape_articles.py            # scrape everything (skips already-scraped URLs)
    python scripts/scrape_articles.py --source official
    python scripts/scrape_articles.py --source unofficial
    python scripts/scrape_articles.py --force    # re-scrape even if already in scraped.md
"""

from __future__ import annotations

import argparse
import sys

import official
import unofficial
from storage import DOCUMENTS_DIR, SCRAPED_INDEX, init_index, load_scraped_urls, save_article


def run_source(
    label: str,
    prefix: str,
    source_name: str,
    url_getter,
    scraper,
    already_scraped: set[str],
    force: bool,
    download_images: bool,
) -> tuple[int, int]:
    """Scrape one site end-to-end. Returns (saved_count, skipped_count)."""
    print(f"\n=== {label} ===")
    article_urls = url_getter()
    saved = skipped = 0

    for i, url in enumerate(article_urls, 1):
        if not force and url in already_scraped:
            skipped += 1
            continue
        print(f"  [{i}/{len(article_urls)}] {url}")
        result = scraper(url, download_images=download_images)
        if result is None:
            continue
        title, body_md, written_on = result
        if not body_md.strip():
            print(f"  ! empty content, skipping: {url}")
            continue
        path = save_article(prefix, source_name, title, url, body_md, written_on)
        already_scraped.add(url)
        saved += 1
        print(f"      saved -> {path.name}")

    print(f"--- {label}: {saved} saved, {skipped} already scraped ---")
    return saved, skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scrape Travian guide articles to markdown.")
    parser.add_argument(
        "--source",
        choices=["official", "unofficial", "all"],
        default="all",
        help="Which site(s) to scrape (default: all).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-scrape and overwrite even if the URL is already in scraped.md.",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Skip downloading article images into assets/.",
    )
    args = parser.parse_args(argv)
    download_images = not args.no_images

    already_scraped = load_scraped_urls()
    print(f"{len(already_scraped)} URLs already recorded in {SCRAPED_INDEX.name}")
    # Normalise the index header/columns (and reset it entirely on a --force run).
    init_index(reset=args.force)

    total_saved = total_skipped = 0

    if args.source in ("official", "all"):
        s, k = run_source(
            "Official Travian Support",
            "official",
            official.SOURCE_NAME,
            official.get_official_article_urls,
            official.scrape_official_article,
            already_scraped,
            args.force,
            download_images,
        )
        total_saved += s
        total_skipped += k

    if args.source in ("unofficial", "all"):
        s, k = run_source(
            "Unofficial Travian Guides",
            "unofficial",
            unofficial.SOURCE_NAME,
            unofficial.get_unofficial_article_urls,
            unofficial.scrape_unofficial_article,
            already_scraped,
            args.force,
            download_images,
        )
        total_saved += s
        total_skipped += k

    print(f"\nDone. {total_saved} new articles saved, {total_skipped} skipped.")
    print(f"Documents in: {DOCUMENTS_DIR}")
    print(f"Index file:   {SCRAPED_INDEX}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
