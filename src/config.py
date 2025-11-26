# src/config.py
from __future__ import annotations

import os
from typing import List
from pathlib import Path

from dotenv import load_dotenv

# -------------------------------------------------
# Base setup: load .env from project root
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)


def _split_csv(value: str) -> List[str]:
    """
    Helper: turn a comma-separated string into a clean list.
    """
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


# -------------------------------------------------
# SendGrid / email config
# -------------------------------------------------

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "")
TO_EMAILS = _split_csv(os.getenv("TO_EMAILS", ""))


# -------------------------------------------------
# RSS FEEDS – broad, macro-heavy source list
# -------------------------------------------------

DEFAULT_FEED_URLS = [
    # --- Bloomberg: core macro + markets ---
    "https://feeds.bloomberg.com/economics/news.rss",
    "https://feeds.bloomberg.com/markets/news.rss",

    # --- Reuters: macro / business / global markets (may be blocked on some networks) ---
    "http://feeds.reuters.com/news/economy",
    "http://feeds.reuters.com/reuters/globalmarketsNews",
    "http://feeds.reuters.com/reuters/businessNews",

    # --- MarketWatch: top business/markets stories ---
    "https://feeds.marketwatch.com/marketwatch/topstories/",

    # --- CNBC: US Top News & Analysis (economy/markets heavy) ---
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",

    # --- Financial Times: markets + central banks ---
    "http://feeds2.feedburner.com/ft/markets",
    "https://www.ft.com/central-banks?format=rss",

    # --- The Economist: economics section ---
    "http://www.economist.com/sections/economics/rss.xml",

    # --- Central banks & BIS: core macro policy sources ---
    "https://www.federalreserve.gov/feeds/press_all.xml",
    "https://www.ecb.europa.eu/rss/press.html",
    "https://www.bankofengland.co.uk/rss/news",
    "https://www.bis.org/doclist/cbspeeches.rss",
]

FEED_URLS = _split_csv(os.getenv("FEED_URLS", "")) or DEFAULT_FEED_URLS


# -------------------------------------------------
# MACRO KEYWORDS – tight & focused
# -------------------------------------------------

DEFAULT_MACRO_KEYWORDS = [
    # Monetary policy & central banks
    "rate hike",
    "rate cut",
    "interest rate",
    "benchmark rate",
    "policy rate",
    "fomc",
    "federal reserve",
    "fed",
    "ecb",
    "european central bank",
    "bank of england",
    "boe",
    "boj",
    "bank of japan",
    "central bank",
    "policy meeting",
    "monetary policy",
    "tightening",
    "easing",
    "quantitative easing",
    "quantitative tightening",
    "qe",
    "qt",

    # Inflation & prices
    "inflation",
    "cpi",
    "ppi",
    "core inflation",
    "headline inflation",
    "disinflation",
    "deflation",

    # GDP, growth, recession
    "gdp",
    "economic growth",
    "recession",
    "soft landing",
    "hard landing",
    "contraction",
    "expansion",

    # Labour market
    "unemployment",
    "jobless claims",
    "labor market",
    "labour market",
    "wage growth",
    "employment",

    # Yields, bonds, and rates markets
    "yield",
    "bond market",
    "treasury",
    "treasuries",
    "gilt",
    "bund",
    "sofr",

    # Fiscal policy
    "fiscal",
    "budget deficit",
    "government spending",
    "public debt",
    "sovereign debt",

    # Global institutions
    "imf",
    "world bank",
    "oecd",

    # Macro / systemic risk
    "currency crisis",
    "financial stability",
    "systemic risk",
]

MACRO_KEYWORDS = _split_csv(os.getenv("MACRO_KEYWORDS", "")) or DEFAULT_MACRO_KEYWORDS


# -------------------------------------------------
# Newsletter subject
# -------------------------------------------------

NEWSLETTER_SUBJECT = os.getenv("NEWSLETTER_SUBJECT", "Daily Macro Brief")


# -------------------------------------------------
# Max number of articles in the newsletter
# -------------------------------------------------

MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", "20"))