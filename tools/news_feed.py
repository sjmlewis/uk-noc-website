#!/usr/bin/env python3
"""Refresh data/news.json, the weekly round-up of Offset news shown on news.html.

Run from the repository folder:  python3 tools/news_feed.py

It copies the weekly round-up from its source list, checks every item (plain
text only: no links, no sources, no HTML) and saves the result. If the source
cannot be read, or anything in it looks wrong, it changes nothing.
"""
import datetime
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "news.json"
SOURCE = "https://raw.githubusercontent.com/sjmlewis/capital-website/main/tools/alerts.json"
UA = "UK-NOC website updater (+https://nationaloffsetcouncil.uk)"
DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")
ALLOWED = {"date", "added", "country", "title", "summary", "tag"}
LIMITS = {"country": 60, "title": 200, "summary": 800}


def main():
    try:
        req = urllib.request.Request(SOURCE, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            src = json.load(r)
    except Exception as e:
        print(f"Warning: could not read the news list ({e}); nothing changed.")
        return
    updated = str(src.get("updated", ""))
    items = src.get("items")
    if not DAY.match(updated) or not isinstance(items, list) or not 0 < len(items) <= 2000:
        print("Warning: the news list is not in the expected shape; nothing changed.")
        return
    clean = []
    for a in items:
        why = None
        if not isinstance(a, dict):
            why = "not an object"
        elif set(a) - ALLOWED:
            why = f"unexpected fields {sorted(set(a) - ALLOWED)}"
        elif not all(isinstance(a.get(k), str) and a[k].strip() for k in ("date", "country", "title", "summary")):
            why = "missing date, country, title or summary"
        elif not DATE.match(a["date"]):
            why = f"bad date {a['date']!r}"
        elif "added" in a and not (isinstance(a["added"], str) and DAY.match(a["added"])):
            why = "bad added date"
        elif "tag" in a and a["tag"] not in ("Civil", "Rules"):
            why = f"bad tag {a['tag']!r}"
        elif any(len(a[k]) > n for k, n in LIMITS.items()):
            why = "text too long"
        elif any(re.search(r"https?://|www\.|<|>", a[k]) for k in ("country", "title", "summary")):
            why = "contains a link or HTML"
        if why:
            print(f"Skipped an item ({why}).")
            continue
        item = {k: a[k].strip() for k in ("date", "added", "country", "title", "summary", "tag") if k in a}
        item.setdefault("added", updated)
        clean.append(item)
    if not clean:
        print("Warning: no usable items; nothing changed.")
        return
    out = {"updated": updated, "items": clean}
    DATA.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    if DATA.exists() and DATA.read_text(encoding="utf-8") == text:
        print("News list unchanged.")
        return
    DATA.write_text(text, encoding="utf-8")
    print(f"News list saved: {len(clean)} items, updated {updated}.")


if __name__ == "__main__":
    main()
