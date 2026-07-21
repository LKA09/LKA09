#!/usr/bin/env python3
"""Prepare a GitHub profile photo for ASCII conversion."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "profile-photo.png"
DEFAULT_OUTPUT = ROOT / "processed-photo.png"
OUTPUT_SIZE = 460


def prepare_photo(source_path: Path, output_path: Path) -> None:
    with Image.open(source_path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        image = ImageOps.fit(
            image,
            (OUTPUT_SIZE, OUTPUT_SIZE),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.42),
        )
        image = ImageOps.grayscale(image)
        image = ImageOps.autocontrast(image, cutoff=1)
        image = ImageEnhance.Contrast(image).enhance(1.25)
        image = ImageEnhance.Sharpness(image).enhance(1.5)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG", optimize=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prepare_photo(args.input, args.output)
    print(f"Prepared {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
