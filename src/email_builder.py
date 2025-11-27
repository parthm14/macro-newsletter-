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
    Build a nicer-looking HTML email / web page containing the given articles.
    This HTML is also what we'll serve as index.html for GitHub Pages.
    """
    articles_list = list(articles)

    if not articles_list:
        articles_html = """
        <tr>
          <td style="padding: 24px; text-align: center; color: #6b7280; font-size: 14px;">
            No macro-relevant stories found today.
          </td>
        </tr>
        """
    else:
        rows = []
        for a in articles_list:
            ts = _format_timestamp(a.published)
            ts_text = f"{ts}" if ts else ""
            source_text = a.source or "Unknown source"

            summary_text = a.summary.strip()
            if len(summary_text) > 280:
                summary_text = summary_text[:280].rstrip() + "..."

            rows.append(
                f"""
                <tr>
                  <td style="
                    padding: 16px 18px;
                    border-radius: 12px;
                    border: 1px solid #e5e7eb;
                    background-color: #ffffff;
                    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.08);
                    margin-bottom: 12px;
                  ">
                    <a href="{a.link}" style="
                      font-size: 16px;
                      font-weight: 600;
                      color: #0f172a;
                      text-decoration: none;
                      line-height: 1.4;
                    ">
                      {a.title}
                    </a>
                    <div style="margin-top: 6px; margin-bottom: 8px; font-size: 12px; color: #6b7280; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
                      <span style="
                        display: inline-block;
                        padding: 2px 8px;
                        border-radius: 999px;
                        background-color: #eff6ff;
                        color: #1d4ed8;
                        font-weight: 500;
                      ">
                        {source_text}
                      </span>
                      {f'<span style="color:#9ca3af;">• {ts_text}</span>' if ts_text else ''}
                    </div>
                    <div style="font-size: 13px; color: #374151; line-height: 1.5;">
                      {summary_text}
                    </div>
                  </td>
                </tr>
                <tr><td style="height: 10px;"></td></tr>
                """
            )

        articles_html = "\n".join(rows)

    display_title = "Daily Macro Brief"
    display_subtitle = "Curated macro & markets headlines from major global sources."

    html = f"""\
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>{subject}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body style="
  margin: 0;
  padding: 0;
  background: radial-gradient(circle at top left, #1e293b, #020617 55%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: transparent; padding: 24px 12px 40px;">
    <tr>
      <td align="center">
        <table width="720" cellpadding="0" cellspacing="0" border="0" style="
          max-width: 720px;
          background-color: #0b1120;
          border-radius: 18px;
          padding: 2px;
          box-shadow: 0 18px 45px rgba(15, 23, 42, 0.6);
        ">
          <tr>
            <td style="
              background: linear-gradient(145deg, #0f172a 0%, #020617 45%, #111827 100%);
              border-radius: 16px;
              padding: 22px 24px 18px;
              border: 1px solid rgba(148, 163, 184, 0.25);
            ">
              <!-- Header -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="text-align:left; vertical-align:top;">
                    <!-- ISMF logo + name -->
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                      <div style="
                        width:40px;
                        height:40px;
                        border-radius:10px;
                        overflow:hidden;
                        background-color:#ffffff;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        box-shadow:0 2px 6px rgba(15,23,42,0.35);
                      ">
                        <img src="ismf-logo.png" alt="ISMF logo" style="
                          max-width:36px;
                          max-height:36px;
                          display:block;
                        ">
                      </div>
                      <div style="font-size:15px; font-weight:600; color:#e5e7eb;">
                        Irish Student Managed Fund (ISMF)
                      </div>
                    </div>

                    <div style="font-size:11px; letter-spacing:0.16em; text-transform:uppercase; color:#93c5fd; margin-bottom:4px;">
                      Macro Newsletter · Beta
                    </div>
                    <h1 style="margin: 0 0 6px; font-size: 24px; line-height: 1.25; color:#e5e7eb;">
                      {display_title}
                    </h1>
                    <p style="margin: 0; font-size: 13px; color:#9ca3af;">
                      {display_subtitle}
                    </p>
                  </td>
                  <td style="text-align:right; vertical-align:top;">
                    <div style="
                      display:inline-block;
                      padding:6px 10px;
                      border-radius:999px;
                      background-color:rgba(15,23,42,0.85);
                      color:#e5e7eb;
                      font-size:11px;
                      border:1px solid rgba(148,163,184,0.35);
                    ">
                      {subject}
                    </div>
                  </td>
                </tr>
              </table>

              <!-- Divider -->
              <div style="margin: 14px 0 12px; border-bottom: 1px solid rgba(55, 65, 81, 0.7);"></div>

              <!-- Content area -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse: separate; border-spacing: 0;">
                {articles_html}
              </table>

              <!-- Footer -->
              <div style="margin-top: 18px; padding-top: 10px; border-top: 1px dashed rgba(55, 65, 81, 0.8); font-size:11px; color:#6b7280;">
                <div style="margin-bottom: 4px;">
                  Built as an automated macro newsletter prototype (Python · RSS · GitHub Pages).
                </div>
                <div style="color:#4b5563;">
                  This is a demo web view. In production it would be delivered daily by email.
                </div>
              </div>
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
    all_articles = fetch_all_feeds( FEED_URLS )
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