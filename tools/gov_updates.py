#!/usr/bin/env python3
"""Collect official GOV.UK publications on UK Offset for the UK-NOC website.

Reads GOV.UK's public search and content APIs (open, no key needed), keeps only
publications that are about defence Offset, and saves them in
data/gov_updates.json. tools/build_noc.py then shows them on the website.

Run from the repository folder:  python3 tools/gov_updates.py

It never deletes an update. If GOV.UK cannot be reached it changes nothing.
GOV.UK content is Crown copyright, re-used under the Open Government Licence v3.0.
"""
import datetime
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "gov_updates.json"
API = "https://www.gov.uk/api"
UA = "UK-NOC website updater (+https://nationaloffsetcouncil.uk)"
UK = ZoneInfo("Europe/London")
SINCE = "2025-01-01"  # publications before this date are left out
FIELDS = "title,link,description,public_timestamp,display_type"
SEARCHES = [
    # Every Ministry of Defence publication that mentions offset, newest first.
    # This one must work, or nothing is saved.
    {"q": "offset", "filter_organisations": "ministry-of-defence",
     "order": "-public_timestamp", "count": "50"},
    # Anything else on GOV.UK about the UK Offset Policy, most relevant first.
    {"q": "UK Offset Policy", "count": "50"},
]
# A publication counts only if it uses one of these phrases. This keeps out
# the many unrelated pages that mention "offset" in another sense
# (carbon offsetting, "to offset the cost", and so on).
RELEVANT = re.compile(
    r"(?<!carbon )(?<!carbon-)\b(?:"
    r"offset (?:policy|authority|agreements?|obligations?|commitments?|requirements?|consultation|"
    r"regime|arrangements?|programmes?|credits?|activit(?:y|ies)|proposals?|multipliers?|guidance|"
    r"thresholds?|projects?|plans?|value)"
    r"|offsets? policy|(?:uk|defence|british|national) offsets?\b|industrial participation)",
    re.I)
# GOV.UK's own names for each kind of page, used when the search does not give one.
TYPE_LABELS = {
    "policy_paper": "Policy paper", "press_release": "Press release", "news_story": "News story",
    "speech": "Speech", "oral_statement": "Oral statement to Parliament",
    "written_statement": "Written statement to Parliament", "authored_article": "Article",
    "open_consultation": "Open consultation", "closed_consultation": "Consultation",
    "consultation_outcome": "Consultation outcome", "guidance": "Guidance",
    "detailed_guide": "Guidance", "statutory_guidance": "Statutory guidance", "notice": "Notice",
    "correspondence": "Correspondence", "transparency": "Transparency data",
    "official_statistics": "Official statistics", "national_statistics": "Accredited official statistics",
    "independent_report": "Independent report", "corporate_report": "Corporate report",
    "form": "Form", "research": "Research", "policy": "Policy",
}


def get_json(url, tries=3):
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return None
            if n == tries - 1:
                raise
        except Exception:
            if n == tries - 1:
                raise
        time.sleep(4 * (n + 1))


def plain(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def stamp(ts):
    """A GOV.UK timestamp as UTC 'YYYY-MM-DDTHH:MM:SSZ', so two forms compare equal."""
    dt = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    return dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def uk_day(ts):
    dt = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    return dt.astimezone(UK).date().isoformat()


def as_text(v):
    if isinstance(v, str):
        return v
    if isinstance(v, list):  # some GOV.UK formats hold several versions of the same text
        for part in v:
            if isinstance(part, dict) and part.get("content_type") == "text/html":
                return part.get("content", "")
        return " ".join(p.get("content", "") for p in v if isinstance(p, dict))
    return ""


def content_text(c):
    d = c.get("details") or {}
    parts = [c.get("title") or "", c.get("description") or ""]
    for k in ("body", "summary", "introduction"):
        parts.append(as_text(d.get(k)))
    for doc in d.get("documents") or []:
        if isinstance(doc, str):
            parts.append(doc)
    for att in d.get("attachments") or []:
        if isinstance(att, dict):
            parts.append(att.get("title") or "")
    return plain(" ".join(parts))


def search(params):
    url = f"{API}/search.json?" + urllib.parse.urlencode({**params, "fields": FIELDS})
    data = get_json(url)
    if not data or not isinstance(data.get("results"), list):
        raise RuntimeError(f"GOV.UK search gave no results list for {params['q']!r}")
    return data["results"]


def make_item(path, hit, c):
    d = c.get("details") or {}
    published = uk_day(c.get("first_published_at") or c["public_updated_at"])
    updated = uk_day(c["public_updated_at"])
    note = ""
    if updated != published:
        for ch in d.get("change_history") or []:
            if ch.get("note") and stamp(ch.get("public_timestamp", "1970-01-01T00:00:00Z")) == stamp(c["public_updated_at"]):
                note = plain(ch["note"])
                break
    return {
        "path": path,
        "link": "https://www.gov.uk" + path,
        "title": plain(c.get("title")),
        "summary": plain(c.get("description")),
        "type": plain(hit.get("display_type") or d.get("document_type_label")
                      or TYPE_LABELS.get(c.get("document_type", ""))
                      or c.get("document_type", "").replace("_", " ").capitalize()),
        "orgs": [plain(o.get("title")) for o in (c.get("links") or {}).get("organisations", [])][:3],
        "published": published,
        "updated": updated,
        "note": note,
        "stamp": stamp(c["public_updated_at"]),
    }


def main():
    try:
        old = json.loads(DATA.read_text(encoding="utf-8"))
    except FileNotFoundError:
        old = {"checked": "", "items": [], "seen": {}}
    items = {it["path"]: it for it in old.get("items", [])}
    seen = dict(old.get("seen", {}))  # checked and found not to be about Offset, by timestamp

    hits = {}
    for n, params in enumerate(SEARCHES):
        try:
            results = search(params)
        except Exception as e:
            if n == 0:
                sys.exit(f"Could not read GOV.UK ({e}); nothing changed.")
            print(f"Warning: second search failed ({e}); carrying on.")
            continue
        for r in results:
            link = r.get("link") or ""
            if link.startswith("/") and r.get("public_timestamp") and link not in hits:
                hits[link] = r

    added, changed = [], []
    for path, hit in hits.items():
        ts = stamp(hit["public_timestamp"])
        if uk_day(ts) < SINCE:
            continue
        if path in items and items[path]["stamp"] == ts:
            continue
        if seen.get(path) == ts:
            continue
        try:
            c = get_json(API + "/content" + urllib.parse.quote(path))
        except Exception as e:
            print(f"Skipped for now (could not read {path}: {e})")
            continue
        time.sleep(0.3)
        if not c or c.get("locale", "en") != "en" or not c.get("public_updated_at"):
            continue
        if c.get("withdrawn_notice"):
            seen[path] = ts
            continue
        if not RELEVANT.search(content_text(c)):
            seen[path] = ts
            continue
        item = make_item(path, hit, c)
        (changed if path in items else added).append(item["title"])
        items[path] = item
        seen.pop(path, None)

    out = {
        "checked": datetime.datetime.now(UK).date().isoformat(),
        "items": sorted(items.values(), key=lambda it: it["stamp"], reverse=True),
        "seen": dict(sorted(seen.items())),
    }
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for t in added:
        print("New:", t)
    for t in changed:
        print("Updated:", t)
    print(f"{len(out['items'])} official updates saved; checked {out['checked']}.")


if __name__ == "__main__":
    main()
