# src/email_builder.py
from __future__ import annotations

from typing import Iterable
from datetime import datetime

from .scraper import Article


def _format_timestamp(dt: datetime | None) -> str:
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M")


def build_html_email(
    subject: str,
    articles: Iterable[Article],
) -> str:
    """
    Build a simple but clean HTML email body containing the given articles.
    This HTML is also what we'll serve as index.html for GitHub Pages.
    """
    articles_list = list(articles)

    if not articles_list:
        body_html = "<p>No macro-relevant stories found today.</p>"
    else:
        rows = []
        for a in articles_list:
            ts = _format_timestamp(a.published)
            ts_html = f"<span style='color:#777;font-size:12px;'>{ts}</span>" if ts else ""
            source_html = f"<span style='font-weight:bold;'>{a.source}</span>"

            rows.append(
                f"""
                <tr>
                  <td style="padding: 8px 0; border-bottom: 1px solid #eee;">
                    <a href="{a.link}" style="font-size:15px; color:#0056b3; text-decoration:none;">
                      {a.title}
                    </a><br/>
                    <span style="font-size:13px; color:#555;">
                      {source_html}
                      {" · " if ts_html else ""}{ts_html}
                    </span><br/>
                    <span style="font-size:13px; color:#444;">
                      {a.summary[:280]}{"..." if len(a.summary) > 280 else ""}
                    </span>
                  </td>
                </tr>
                """
            )

        body_html = "\n".join(rows)

    html = f"""\
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>{subject}</title>
</head>
<body style="margin:0; padding:0; background-color:#f5f5f5;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;">
    <tr>
      <td align="center" style="padding:20px 10px;">
        <table width="600" cellpadding="0" cellspacing="0" border="0"
               style="background-color:#ffffff; border-radius:6px; padding:20px; font-family:Arial, sans-serif;">
          <tr>
            <td style="text-align:left;">
              <h1 style="margin:0 0 10px; font-size:24px;">Daily Macro Brief</h1>
              <p style="margin:0 0 10px; font-size:13px; color:#777;">
                Curated macro &amp; markets headlines from major sources.
              </p>
            </td>
          </tr>
          <tr><td><hr style="border:none; border-top:1px solid #ddd; margin:10px 0 20px;" /></td></tr>
          {body_html}
          <tr>
            <td style="padding-top:20px; font-size:11px; color:#999;">
              This is a preview build of the Daily Macro Brief.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return html


def build_text_email(
    subject: str,
    articles: Iterable[Article],
) -> str:
    """
    Build a plain-text version of the email (for clients that don't render HTML).
    """
    articles_list = list(articles)

    lines = [subject, "", "Daily Macro Brief", "==================", ""]

    if not articles_list:
        lines.append("No macro-relevant stories found today.")
    else:
        for i, a in enumerate(articles_list, start=1):
            ts = _format_timestamp(a.published)
            lines.append(f"{i}. {a.title}")
            if ts:
                lines.append(f"   ({a.source}, {ts})")
            else:
                lines.append(f"   ({a.source})")
            lines.append(f"   {a.link}")
            if a.summary:
                lines.append(
                    f"   {a.summary[:200]}{'...' if len(a.summary) > 200 else ''}"
                )
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Local preview: run `python -m src.email_builder` from project root
    import logging
    import sys
    from datetime import datetime, timezone

    from .config import FEED_URLS, MACRO_KEYWORDS, NEWSLETTER_SUBJECT, MAX_ARTICLES
    from .scraper import fetch_all_feeds
    from .filter import filter_articles

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )

    logging.info("Fetching feeds for email preview...")
    all_articles = fetch_all_feeds(FEED_URLS)
    logging.info("Fetched %d total articles", len(all_articles))

    filtered = filter_articles(all_articles, MACRO_KEYWORDS, max_articles=MAX_ARTICLES)
    logging.info(
        "After filtering and capping, %d articles remain (max %d)",
        len(filtered),
        MAX_ARTICLES,
    )

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    subject = f"{NEWSLETTER_SUBJECT} — {today_str}"

    html_body = build_html_email(subject, filtered)
    text_body = build_text_email(subject, filtered)

    # Write preview for local viewing
    preview_path = "preview.html"
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(html_body)

    # Write index.html for GitHub Pages (served at /)
    index_path = "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_body)

    logging.info("Wrote HTML preview to %s and %s", preview_path, index_path)

    print("\n=== TEXT VERSION (first ~40 lines) ===\n")
    for line in text_body.splitlines()[:40]:
        print(line)