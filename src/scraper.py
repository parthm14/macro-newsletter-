# src/scraper.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Sequence
import logging
import time

import feedparser

from .config import FEED_URLS


@dataclass
class Article:
    title: str
    link: str
    source: str
    published: Optional[datetime]
    summary: str


def _parse_entry(entry, source: str) -> Article:
    """
    Convert a single feedparser entry into our Article dataclass.
    """
    title = entry.get("title", "(no title)")
    link = entry.get("link", "")
    summary = entry.get("summary", "") or entry.get("description", "")

    # Parse published/updated timestamp if available
    published_dt: Optional[datetime] = None
    struct_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if struct_time:
        published_dt = datetime.fromtimestamp(time.mktime(struct_time))

    return Article(
        title=title,
        link=link,
        source=source,
        published=published_dt,
        summary=summary,
    )


def fetch_feed(url: str, source_name: Optional[str] = None) -> List[Article]:
    """
    Fetch a single RSS/Atom feed and return a list of Article objects.
    """
    source = source_name or url
    logging.info("Fetching feed: %s", url)

    parsed = feedparser.parse(url)

    if parsed.bozo:
        logging.warning("Feed parse issue for %s: %s", url, parsed.bozo_exception)

    articles: List[Article] = []
    for entry in parsed.entries:
        try:
            article = _parse_entry(entry, source)
            articles.append(article)
        except Exception as exc:
            logging.exception("Failed to parse entry from %s: %s", source, exc)

    logging.info("Fetched %d articles from %s", len(articles), source)
    return articles


def fetch_all_feeds(feed_urls: Sequence[str]) -> List[Article]:
    """
    Fetch all feeds and return a combined list of Article objects.
    """
    all_articles: List[Article] = []
    for url in feed_urls:
        try:
            articles = fetch_feed(url)
            all_articles.extend(articles)
        except Exception as exc:
            logging.exception("Error fetching feed %s: %s", url, exc)
    return all_articles


if __name__ == "__main__":
    # Simple manual test: run `python -m src.scraper` from project root
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logging.info("Testing fetch_all_feeds with FEED_URLS = %s", FEED_URLS)
    articles = fetch_all_feeds(FEED_URLS)
    logging.info("Total articles fetched: %d", len(articles))

    for a in articles[:5]:
        print(f"- {a.source}: {a.title}")