"""Find sound effects on Openverse and record where they came from.

usage: sfx.py search "rain on roof" [--limit 8] [--any-license]
       sfx.py get AUDIO_ID video/assets/ [--credits credits.md]
Search returns only licenses that allow commercial use unless --any-license is set. Check the source page before publishing.
"""
import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.openverse.org/v1/audio/"
HEADERS = {"User-Agent": "thai-story-shorts/1.0"}


def fetch_json(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=60) as response:
            return json.load(response)
    except (OSError, ValueError) as err:
        raise SystemExit(f"Openverse is not responding, try again later or use soundscape.py: {err}")


def search_url(query, limit, any_license=False):
    params = {"q": query, "page_size": limit}
    if not any_license:
        params["license_type"] = "commercial"
    return API + "?" + urllib.parse.urlencode(params)


def credit_line(item):
    return f"- {item.get('title') or item['id']} by {item.get('creator') or 'unknown'}, {item['license'].upper()} {item.get('license_version') or ''}, {item.get('foreign_landing_url') or item['url']}\n"


def get(audio_id, folder, credits):
    if not re.fullmatch(r"[0-9a-fA-F-]{36}", audio_id):
        raise SystemExit("AUDIO_ID must be an id from the search results")
    item = fetch_json(f"{API}{audio_id}/")
    extension = re.sub(r"\W", "", item.get("filetype") or "") or "mp3"
    target = Path(folder) / f"sfx-{audio_id[:8]}.{extension}"
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(item["url"], headers=HEADERS), timeout=120) as response:
        target.write_bytes(response.read())
    with open(credits, "a", encoding="utf-8") as out:
        out.write(credit_line(item))
    print("wrote", target, "and", credits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["search", "get"])
    ap.add_argument("value")
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--any-license", action="store_true")
    ap.add_argument("--credits", default="credits.md")
    args = ap.parse_args()
    if args.action == "get":
        if not args.folder:
            raise SystemExit("get needs a target folder")
        get(args.value, args.folder, args.credits)
        return
    for item in fetch_json(search_url(args.value, args.limit, args.any_license))["results"]:
        seconds = (item.get("duration") or 0) / 1000
        row = f"{item['id']}  {seconds:6.1f}s  {item['license']:8}  {item.get('title')}"
        print(row.encode("ascii", "backslashreplace").decode())


if __name__ == "__main__":
    main()
