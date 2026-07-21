#!/usr/bin/env python3
"""Render a processed profile photo as a static ASCII art SVG."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "processed-photo.png"
DEFAULT_OUTPUT = ROOT / "lka09-ascii.svg"
DEFAULT_README = ROOT / "README.md"
ASCII_CHARS = "@%#*+=-:. "
SVG_WIDTH = 370
SVG_HEIGHT = 376
ASCII_COLUMNS = 58
CHARACTER_ASPECT_RATIO = 0.55
FONT_SIZE = 9.2
LINE_HEIGHT = 9.4


def photo_to_ascii(source_path: Path) -> list[str]:
    with Image.open(source_path) as source:
        image = ImageOps.exif_transpose(source).convert("L")
        aspect_ratio = image.height / image.width
        rows = max(1, round(ASCII_COLUMNS * aspect_ratio * CHARACTER_ASPECT_RATIO))
        image = image.resize((ASCII_COLUMNS, rows), Image.Resampling.LANCZOS)
        pixels = list(image.getdata())

    return [
        "".join(
            ASCII_CHARS[pixels[row * ASCII_COLUMNS + column] * len(ASCII_CHARS) // 256]
            for column in range(ASCII_COLUMNS)
        )
        for row in range(rows)
    ]


def render_svg(lines: list[str]) -> str:
    art_height = len(lines) * LINE_HEIGHT
    first_baseline = 32 + (SVG_HEIGHT - 32 - art_height) / 2 + FONT_SIZE
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">LKA09 ASCII portrait</title>',
        '<desc id="desc">GitHub profile photo rendered as character-based ASCII art</desc>',
        '<rect width="370" height="376" rx="12" fill="#0d1117"/>',
        '<rect x=".5" y=".5" width="369" height="375" rx="12" fill="none" stroke="#30363d"/>',
        '<line x1="0" y1="30" x2="370" y2="30" stroke="#30363d"/>',
        '<circle cx="20" cy="15" r="5" fill="#ff5f56"/>',
        '<circle cx="36" cy="15" r="5" fill="#ffbd2e"/>',
        '<circle cx="52" cy="15" r="5" fill="#27c93f"/>',
        '<text x="185" y="19" fill="#7d8590" font-size="12" text-anchor="middle" '
        'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
        'lka09@github: ~$ avatar --ascii</text>',
        f'<g fill="#39d353" font-size="{FONT_SIZE}" font-weight="700" '
        'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    ]
    for index, line in enumerate(lines):
        y = first_baseline + index * LINE_HEIGHT
        parts.append(
            f'<text x="18" y="{y:.1f}" xml:space="preserve">{html.escape(line)}</text>'
        )
    parts.extend(("</g>", "</svg>"))
    return "\n".join(parts) + "\n"


def update_readme_cache_key(readme_path: Path, svg: str) -> str:
    cache_key = hashlib.sha256(svg.encode("utf-8")).hexdigest()[:12]
    readme = readme_path.read_text(encoding="utf-8")
    updated, replacements = re.subn(
        r'src="\./lka09-ascii\.svg(?:\?v=[0-9a-f]+)?"',
        f'src="./lka09-ascii.svg?v={cache_key}"',
        readme,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError("Could not find the ASCII portrait image in README.md")
    readme_path.write_text(updated, encoding="utf-8", newline="\n")
    return cache_key


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--readme", type=Path, default=DEFAULT_README)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    lines = photo_to_ascii(args.input)
    svg = render_svg(lines)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8", newline="\n")
    cache_key = update_readme_cache_key(args.readme, svg)
    print(f"Generated {args.output} from {args.input} (cache key: {cache_key})")


if __name__ == "__main__":
    main()
