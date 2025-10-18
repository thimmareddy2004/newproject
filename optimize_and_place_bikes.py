#!/usr/bin/env python3
"""
Optimize and place bike images into static/bikes using the app's expected filenames.

Usage (PowerShell):
  .\.venv\Scripts\python.exe optimize_and_place_bikes.py --src incoming

- Put your source images in the --src folder with the EXACT target names below:
    streetfighter-v4.jpg
    hayabusa.jpg
    zx10r.jpg
    bmw-s1000rr.jpg
    panigale-v4.jpg
    tiger-1200-rally-pro.jpg
    rocket-3r.jpg
    r1250gsa.jpg
    multistrada-v4s.jpg
    aprilia-rsv4.jpg

- The script will:
  * backup any existing file to static/bikes/.backup/<timestamp>/
  * resize to max 1600px on the longer side
  * save optimized JPEG (quality=80, progressive)
"""
import argparse
import os
import shutil
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow is required. Install with: .\\.venv\\Scripts\\pip.exe install Pillow")

TARGET_NAMES = [
    "streetfighter-v4.jpg",
    "hayabusa.jpg",
    "zx10r.jpg",
    "bmw-s1000rr.jpg",
    "panigale-v4.jpg",
    "tiger-1200-rally-pro.jpg",
    "rocket-3r.jpg",
    "r1250gsa.jpg",
    "multistrada-v4s.jpg",
    "aprilia-rsv4.jpg",
]

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def backup_existing(dest_dir: Path, fname: str, backup_root: Path):
    dst = dest_dir / fname
    if dst.exists():
        ensure_dir(backup_root)
        shutil.move(str(dst), str(backup_root / fname))

def optimize_image(src: Path, dst: Path, max_side: int = 1600, quality: int = 80):
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        scale = max(w, h) / max_side if max(w, h) > max_side else 1.0
        if scale > 1.0:
            nw, nh = int(w / scale), int(h / scale)
            im = im.resize((nw, nh), Image.LANCZOS)
        ensure_dir(dst.parent)
        im.save(dst, format="JPEG", quality=quality, optimize=True, progressive=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Folder containing your source images named exactly as target filenames")
    ap.add_argument("--dest", default="static/bikes", help="Destination folder (default: static/bikes)")
    ap.add_argument("--max", type=int, default=1600, help="Max long side in px (default 1600)")
    ap.add_argument("--quality", type=int, default=80, help="JPEG quality (default 80)")
    args = ap.parse_args()

    src_dir = Path(args.src)
    dest_dir = Path(args.dest)
    backup_dir = dest_dir / ".backup" / time.strftime("%Y%m%d-%H%M%S")

    if not src_dir.exists():
        raise SystemExit(f"Source folder not found: {src_dir}")

    ok = 0
    missing = []
    for name in TARGET_NAMES:
        src = src_dir / name
        if not src.exists():
            missing.append(name)
            continue
        backup_existing(dest_dir, name, backup_dir)
        optimize_image(src, dest_dir / name, max_side=args.max, quality=args.quality)
        print(f"[OK] {name} -> {dest_dir}")
        ok += 1

    if missing:
        print("\nMissing files (not processed):")
        for m in missing:
            print(" -", m)

    print(f"\nDone. processed={ok}, missing={len(missing)}, dest={dest_dir}")

if __name__ == "__main__":
    main()
