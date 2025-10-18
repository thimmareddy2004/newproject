#!/usr/bin/env python3
"""
Download best-guess Wikimedia Commons image for each place in a JSON list.

Usage:
  python scripts/download_from_commons.py
  python scripts/download_from_commons.py --input static/data/karnataka_places.json --force

What it does:
 - For each place object in the JSON array, looks up Wikimedia Commons (search in namespace 6 - File:)
 - If it finds a likely file, fetches the image download URL and extmetadata (license, artist)
 - Downloads the image into ./static/images/<place_id>.<ext>
 - Adds/updates these fields in the JSON per-place:
     "image_filename": "hampi.jpg"
     "image_url": "https://upload.wikimedia.org/....jpg"
     "image_credit": "Author / License (from Commons extmetadata)"
 - Writes updated JSON to same path (backed up as .bak)
Notes:
 - Reliably works for well-known place names. For obscure names it may not find a good image.
 - You must run this locally; I cannot download on your behalf.
Dependencies:
   pip install requests
"""
from __future__ import annotations
import os, sys, time, json, argparse, re
from urllib.parse import quote_plus, urlparse
import requests

USER_AGENT = "KarnatakaImageDownloader/1.0 (https://example.local/)"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

OUT_IMAGES_DIR = os.path.join("static", "images")

HEADERS = {"User-Agent": USER_AGENT}
RETRIES = 3
RETRY_DELAY = 1.5

def read_json(path):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def safe_filename(s):
    # simple safe name for file saving
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', s)

def commons_search_file(name, limit=3):
    """
    Search Wikimedia Commons for File pages that match 'name'.
    Returns list of titles (e.g., ['File:Jog_falls,_Karnataka.jpg', ...])
    """
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": name,
        "srnamespace": 6,   # namespace 6 == File:
        "srlimit": limit,
    }
    for attempt in range(RETRIES):
        try:
            r = requests.get(COMMONS_API, params=params, headers=HEADERS, timeout=20)
            r.raise_for_status()
            data = r.json()
            hits = [item["title"] for item in data.get("query", {}).get("search", [])]
            return hits
        except Exception as e:
            print("  search error:", e)
            time.sleep(RETRY_DELAY)
    return []

def get_imageinfo_for_titles(titles):
    """
    Given a list of File:... titles, query imageinfo with extmetadata and url.
    Returns dict title->imageinfo dict or {} if not found.
    """
    if not titles:
        return {}
    # API wants pipe-separated titles
    titles_param = "|".join(titles)
    params = {
        "action": "query",
        "format": "json",
        "titles": titles_param,
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
    }
    try:
        r = requests.get(COMMONS_API, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        out = {}
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            title = page.get("title")
            ii = page.get("imageinfo")
            if ii and isinstance(ii, list):
                info = ii[0]
                out[title] = info
        return out
    except Exception as e:
        print("  imageinfo error:", e)
        return {}

def pick_best_imageinfo(name, candidates):
    """
    Given a place name and candidate title->imageinfo mapping, choose the best match.
    Heuristics:
     - prefer title that contains the name tokens (case-insensitive)
     - prefer larger images (no direct pixel info here, but extmetadata may have 'ImageWidth'/'ImageHeight')
     - fall back to first candidate
    """
    name_low = name.lower()
    scored = []
    for title, info in candidates.items():
        score = 0
        t_low = title.lower()
        if name_low in t_low:
            score += 30
        # extmetadata has PixelWidth/Height maybe
        ext = info.get("extmetadata", {}) or {}
        try:
            w = int(ext.get("ImageWidth", {}).get("value", 0) or 0)
            h = int(ext.get("ImageHeight", {}).get("value", 0) or 0)
            score += min(50, (w*h)//10000)  # prefer larger images
        except Exception:
            pass
        scored.append((score, title, info))
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[0][1:] if scored else (None, None)

def extract_license_credit(extmetadata):
    """
    Try to extract a readable credit string from extmetadata block.
    Returns string like 'Photographer / CC BY-SA 4.0' or None.
    """
    if not extmetadata:
        return None
    md = extmetadata
    parts = []
    # Artist
    if md.get("Artist", {}).get("value"):
        artist = md["Artist"]["value"]
        artist = re.sub(r'<.*?>', '', artist).strip()
        parts.append(artist)
    # License short name
    if md.get("LicenseShortName", {}).get("value"):
        lic = md["LicenseShortName"]["value"]
        parts.append(lic)
    # Credit string
    if parts:
        return " / ".join(parts)
    # fallback: credit field
    if md.get("Credit", {}).get("value"):
        c = re.sub(r'<.*?>', '', md["Credit"]["value"]).strip()
        return c
    return None

def download_url_to_file(url, out_path, force=False):
    if os.path.exists(out_path) and not force:
        print("  already exists:", out_path)
        return True
    for attempt in range(RETRIES):
        try:
            with requests.get(url, stream=True, headers=HEADERS, timeout=40) as r:
                r.raise_for_status()
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=64*1024):
                        if chunk:
                            f.write(chunk)
            return True
        except Exception as e:
            print("  download attempt failed:", e)
            time.sleep(RETRY_DELAY)
    return False

def ext_from_url(url):
    path = urlparse(url).path
    base = os.path.basename(path)
    if "." in base:
        return base.split(".")[-1].lower()
    return "jpg"

def main(json_path, force=False):
    places = read_json(json_path)
    if not isinstance(places, list):
        print("JSON must be an array of place objects.")
        return 2

    os.makedirs(OUT_IMAGES_DIR, exist_ok=True)
    # backup original
    backup_path = json_path + ".bak"
    if not os.path.exists(backup_path):
        write_json(backup_path, places)
        print("Backup written to", backup_path)

    failed = []
    succeeded = []

    for p in places:
        pid = p.get("id")
        pname = p.get("name") or pid
        print("\n==", pid, "|", pname)
        # skip if already has image_filename and file exists (unless force)
        existing = p.get("image_filename")
        if existing and os.path.exists(os.path.join(OUT_IMAGES_DIR, existing)) and not force:
            print("  already has image:", existing)
            succeeded.append(pid)
            continue

        # 1) search commons for file pages
        search_terms = [
            pname,
            f"{pname} Karnataka",
            f"{pname} India",
            pid.replace("_", " "),
        ]
        titles = []
        for term in search_terms:
            print("  searching commons for:", term)
            hits = commons_search_file(term, limit=6)
            if hits:
                titles.extend(hits)
            # small delay between searches
            time.sleep(0.6)

        titles = list(dict.fromkeys(titles))  # de-dupe, keep order
        if not titles:
            print("  No File: pages found on Commons for:", pname)
            failed.append((pid, "no_search_hits"))
            continue

        # 2) get imageinfo for candidate titles (batch)
        print("  candidate files:", titles[:6])
        info_map = get_imageinfo_for_titles(titles[:12])  # limit to first 12 titles
        if not info_map:
            print("  No imageinfo found for candidates.")
            failed.append((pid, "no_imageinfo"))
            continue

        # 3) pick the best candidate
        chosen_title, chosen_info = pick_best_imageinfo(pname, info_map)
        if not chosen_title:
            print("  couldn't pick a best image")
            failed.append((pid, "no_choice"))
            continue

        image_url = chosen_info.get("url") or chosen_info.get("descriptionurl")
        extmeta = chosen_info.get("extmetadata")
        credit = extract_license_credit(extmeta) or ""
        print("  chosen:", chosen_title)
        print("   url:", image_url)
        if not image_url:
            print("  no direct image URL available")
            failed.append((pid, "no_image_url"))
            continue

        ext = ext_from_url(image_url)
        out_name = f"{pid}.{ext}"
        out_path = os.path.join(OUT_IMAGES_DIR, out_name)

        ok = download_url_to_file(image_url, out_path, force=force)
        if not ok:
            print("  download failed for", image_url)
            failed.append((pid, "download_failed"))
            continue

        # update place entry metadata
        p["image_filename"] = out_name
        p["image_url"] = image_url
        if credit:
            p["image_credit"] = credit
        else:
            # fallback to the commons file page title as credit placeholder
            p["image_credit"] = chosen_title

        succeeded.append(pid)
        # polite pause to avoid hammering API
        time.sleep(0.8)

    # write updated JSON back (overwrite)
    write_json(json_path, places)
    print("\nSummary: succeeded:", len(succeeded), "failed:", len(failed))
    if failed:
        for f in failed[:40]:
            print(" -", f)
    return 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=os.path.join("static", "data", "karnataka_places.json"))
    ap.add_argument("--force", action="store_true", help="Force re-download even if images exist")
    args = ap.parse_args()
    rc = main(args.input, force=args.force)
    sys.exit(rc)
