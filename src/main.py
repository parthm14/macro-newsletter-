# src/main.py
from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone

from . import config
from .scraper import fetch_all_feeds
from .filter import filter_articles
from .email_builder import build_html_email, build_text_email
from .send_email import send_newsletter


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )


def run() -> None:
    configure_logging()
    logging.info("Starting Daily Macro Brief run (local send test)")

    logging.info("Using feeds: %s", config.FEED_URLS)
    all_articles = fetch_all_feeds(config.FEED_URLS)
    logging.info("Fetched total %d articles", len(all_articles))

    filtered = filter_articles(
        all_articles,
        config.MACRO_KEYWORDS,
        max_articles=config.MAX_ARTICLES,
    )
    logging.info(
        "Filtered down to %d macro-relevant articles (max %d)",
        len(filtered),
        config.MAX_ARTICLES,
    )

    if not filtered:
        logging.info("No relevant articles found; sending empty brief anyway.")

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    subject = f"{config.NEWSLETTER_SUBJECT} — {today_str}"

    html_body = build_html_email(subject, filtered)
    text_body = build_text_email(subject, filtered)

    logging.info("Sending newsletter to %d recipients", len(config.TO_EMAILS))
    send_newsletter(config.TO_EMAILS, subject, html_body, text_body)

    logging.info("Newsletter send completed.")


if __name__ == "__main__":
    run()