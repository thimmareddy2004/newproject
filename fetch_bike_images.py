#!/usr/bin/env python3
"""
Fetches bike images into static/bikes/ using either:
  - a direct image URL, or
  - an official product PAGE URL (script auto-grabs the page's og:image / twitter:image)

Usage:
  python fetch_bike_images.py --map sources.json --out static/bikes --workers 8 --force
"""

import argparse, concurrent.futures, os, re, sys, time, ssl
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json
from io import BytesIO

# Optional JPEG conversion (recommended)
try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif")

VERIFY_SSL = True

def _get(url, timeout=30, accept=None, referer=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ImageFetcher/1.0; +https://example.com)",
        "Accept": accept or "*/*"
    }
    if referer:
        headers["Referer"] = referer
    req = Request(url, headers=headers)
    context = None if VERIFY_SSL else ssl._create_unverified_context()
    # urlopen supports context kwarg
    return urlopen(req, timeout=timeout, context=context)

def is_image_url(url: str) -> bool:
    u = url.lower().split("?")[0]
    return u.endswith(IMG_EXTS)

META_PATTERN = re.compile(
    r'<meta[^>]+(?:property|name)\s*=\s*["\'](?:og:image|twitter:image)["\'][^>]+content\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE
)

IMG_TAG_PATTERN = re.compile(
    r'<img[^>]+src\s*=\s*["\']([^"\']+)["\'][^>]*>',
    re.IGNORECASE
)

def pick_image_from_html(base_url: str, html: bytes) -> str | None:
    text = html.decode("utf-8", errors="ignore")
    # 1) prefer og:image / twitter:image
    m = META_PATTERN.search(text)
    if m:
        return urljoin(base_url, m.group(1).strip())
    # 2) else fall back to the largest-looking <img> by filename hint
    #    (hero, header, gallery, etc.)
    candidates = [urljoin(base_url, s) for s in IMG_TAG_PATTERN.findall(text)]
    # simple heuristic ranking
    def score(u: str) -> int:
        u2 = u.lower()
        pts = 0
        for kw in ("hero", "header", "main", "gallery", "default", "desktop", "cover", "og"):
            if kw in u2:
                pts += 3
        for kw in ("small", "thumb", "icon", "logo"):
            if kw in u2:
                pts -= 2
        # prefer non-svg
        if any(u2.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
            pts += 1
        return pts
    if candidates:
        candidates.sort(key=score, reverse=True)
        return candidates[0]
    return None

def download_image(url: str, referer: str | None = None, attempts: int = 2) -> tuple[bytes, str]:
    """Return (bytes, mime) or raise."""
    last_err = None
    for _ in range(max(1, attempts)):
        try:
            with _get(url, accept="image/*", referer=referer) as r:
                ctype = r.headers.get("Content-Type", "").lower()
                data = r.read()
                if not ctype or "text/html" in ctype:
                    raise ValueError(f"not-image: {ctype or 'unknown'}")
                return data, ctype
        except Exception as e:
            last_err = e
            time.sleep(0.5)
    raise last_err

def convert_to_jpeg_if_needed(data: bytes, ctype: str) -> bytes:
    if "jpeg" in ctype or "jpg" in ctype:
        return data
    if not HAVE_PIL:
        return data  # leave original bytes if Pillow not installed
    try:
        im = Image.open(BytesIO(data))
        rgb = im.convert("RGB")
        buf = BytesIO()
        rgb.save(buf, format="JPEG", quality=90)
        return buf.getvalue()
    except Exception:
        return data

def fetch_for_name(name: str, src_url: str, out_dir: str, force: bool = False) -> tuple[str, bool, str]:
    target = os.path.join(out_dir, name)
    os.makedirs(out_dir, exist_ok=True)

    if (not force) and os.path.exists(target) and os.path.getsize(target) > 0:
        return (name, True, "exists")

    try:
        # Case A: direct image URL
        if is_image_url(src_url):
            data, ctype = download_image(src_url)
        else:
            # Case B: page URL -> resolve hero image
            with _get(src_url, accept="text/html,application/xhtml+xml") as r:
                html = r.read()
            img_url = pick_image_from_html(src_url, html)
            if not img_url:
                return (name, False, "no og:image or <img> found")
            # sanitize spaces
            img_url = img_url.replace(' ', '%20')
            data, ctype = download_image(img_url, referer=src_url)

        data = convert_to_jpeg_if_needed(data, ctype)
        tmp = target + ".part"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, target)
        return (name, True, "ok")
    except (HTTPError, URLError) as e:
        return (name, False, f"{type(e).__name__}: {e}")
    except Exception as e:
        return (name, False, f"Error: {e}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True, help="Path to sources.json mapping {filename: url}")
    ap.add_argument("--out", default="static/bikes", help="Output dir (default: static/bikes)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--insecure", action="store_true", help="Disable SSL cert verification (use only if needed)")
    args = ap.parse_args()

    global VERIFY_SSL
    if args.insecure:
        VERIFY_SSL = False

    with open(args.map, "r", encoding="utf-8") as f:
        urlmap = json.load(f)

    jobs = sorted(urlmap.items())
    ok, fail, exist = 0, 0, 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(fetch_for_name, name, url, args.out, args.force) for name, url in jobs]
        for fut in concurrent.futures.as_completed(futs):
            name, success, msg = fut.result()
            if success and msg == "exists":
                exist += 1
                print(f"[=] {name}: already exists")
            elif success:
                ok += 1
                print(f"[OK] {name}: downloaded")
            else:
                fail += 1
                print(f"[x] {name}: {msg}", file=sys.stderr)

    print(f"\nDone. ok={ok}, existing={exist}, failed={fail}, total={len(jobs)}")
    if not HAVE_PIL:
        print("Note: Pillow not installed. Some images may not be JPEG. To force .jpg output, run: pip install pillow", file=sys.stderr)

if __name__ == "__main__":
    main()
