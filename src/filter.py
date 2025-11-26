# src/filter.py
from __future__ import annotations

from typing import Iterable, List, Sequence, Set

from .scraper import Article, fetch_all_feeds
from .config import FEED_URLS, MACRO_KEYWORDS, MAX_ARTICLES


def filter_articles(
    articles: Iterable[Article],
    keywords: Sequence[str],
    max_articles: int | None = None,
) -> List[Article]:
    """
    Keep only articles whose title or summary contains at least one keyword.
    Deduplicate by link (falling back to title if link is missing).
    Sort by published timestamp (newest first, unknown timestamps last).
    Optionally cap the output to max_articles.
    """
    lower_keywords = [k.lower() for k in keywords]

    seen_keys: Set[str] = set()
    filtered: List[Article] = []

    for article in articles:
        haystack = f"{article.title} {article.summary}".lower()

        if not any(kw in haystack for kw in lower_keywords):
            continue

        key = article.link or article.title
        if key in seen_keys:
            continue

        seen_keys.add(key)
        filtered.append(article)

    # Sort newest → oldest
    filtered.sort(
        key=lambda a: (a.published is not None, a.published),
        reverse=True,
    )

    # Cap the list if requested
    if max_articles is not None and len(filtered) > max_articles:
        filtered = filtered[:max_articles]

    return filtered


if __name__ == "__main__":
    # Manual test: run `python -m src.filter` from project root
    import logging
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )

    logging.info("Fetching all feeds for filter test...")
    all_articles = fetch_all_feeds(FEED_URLS)
    logging.info("Fetched %d total articles", len(all_articles))

    filtered = filter_articles(all_articles, MACRO_KEYWORDS, max_articles=MAX_ARTICLES)
    logging.info(
        "After filtering, %d articles remain (capped at %d)",
        len(filtered),
        MAX_ARTICLES,
    )

    print("\n=== SAMPLE FILTERED ARTICLES (up to 10) ===")
    for i, a in enumerate(filtered[:10], start=1):
        print(f"{i}. {a.title} ({a.source})")