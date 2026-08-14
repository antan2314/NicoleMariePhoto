#!/usr/bin/env python3
"""
Optimize photos for the web.

For each source image, writes four files into the output directory:
    NAME.jpg        full size, JPEG
    NAME.webp       full size, WebP
    NAME-800.jpg    800px wide, JPEG
    NAME-800.webp   800px wide, WebP

The browser picks the smallest one it can use, via srcset in the HTML.

Usage:
    python tools/optimize_images.py SOURCE_DIR OUTPUT_DIR
    python tools/optimize_images.py SOURCE_DIR OUTPUT_DIR --manifest manifest.csv

A manifest is a CSV of `source_filename,output_name` so photos get
meaningful names (eng-01) instead of camera names (DSC_4821).

Notes on the choices here, since you'll rebuild this server-side later:

- EXIF is stripped by copying pixel data into a fresh image. Client
  photos routinely carry GPS coordinates; publishing those is a real
  privacy problem, not a theoretical one.
- Images are never upscaled. Enlarging a small source just makes a
  bigger file that looks the same.
- LANCZOS is the resampling filter to use for downscaling. The default
  is faster and visibly worse.
- Quality 82 for JPEG and 80 for WebP are the usual sweet spot. Above
  that, file size climbs faster than visible quality.
"""

import argparse
import csv
import sys
from pathlib import Path

from PIL import Image

WIDTHS = {"": None, "-800": 800}
JPEG_QUALITY = 82
WEBP_QUALITY = 80


def strip_metadata(image: Image.Image) -> Image.Image:
    """Return a copy holding only pixel data — no EXIF, no ICC, no GPS."""
    clean = Image.new(image.mode, image.size)
    clean.putdata(list(image.getdata()))
    return clean


def process(source: Path, out_dir: Path, name: str) -> list[tuple[str, int]]:
    with Image.open(source) as raw:
        image = strip_metadata(raw.convert("RGB"))

    written = []
    for suffix, target_width in WIDTHS.items():
        if target_width is None or target_width >= image.width:
            resized = image
        else:
            height = round(image.height * target_width / image.width)
            resized = image.resize((target_width, height), Image.LANCZOS)

        jpg = out_dir / f"{name}{suffix}.jpg"
        webp = out_dir / f"{name}{suffix}.webp"
        resized.save(jpg, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        resized.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
        written += [(jpg.name, jpg.stat().st_size), (webp.name, webp.stat().st_size)]

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--manifest", type=Path, help="CSV: source_filename,output_name")
    args = parser.parse_args()

    if not args.source_dir.is_dir():
        print(f"No such directory: {args.source_dir}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.manifest:
        with args.manifest.open() as handle:
            jobs = [(args.source_dir / row[0], row[1]) for row in csv.reader(handle) if row]
    else:
        jobs = [(path, path.stem) for path in sorted(args.source_dir.glob("*.jpg"))]

    total = 0
    for source, name in jobs:
        if not source.exists():
            print(f"  missing: {source.name}", file=sys.stderr)
            continue
        for filename, size in process(source, args.output_dir, name):
            total += size
        print(f"  {source.name} -> {name}")

    print(f"\n{len(jobs)} images, {total / 1_048_576:.1f} MB written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
