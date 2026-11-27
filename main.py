#!/usr/bin/env python3
"""Entry program for make.fun: 'Sum up 26 November's world news in one image'.

The picture is already in this repository as news_image.png: a front-page
collage of twelve stories from Thursday 26 November 2026, drawn by
make_news_image.py. This program only carries that finished picture to
the place the grader expects it, /output/entry.png.

Standard library only, no network, and the same bytes on every run,
because the picture file never changes here. For a local test run,
MAKEFUN_OUTPUT_DIR stands in for /output.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "news_image.png"
NAME = "entry.png"


def target_path() -> Path:
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        Path(chosen).mkdir(parents=True, exist_ok=True)
    except OSError:
        chosen = str(HERE / "out")
        Path(chosen).mkdir(parents=True, exist_ok=True)
    return Path(chosen) / NAME


def main() -> None:
    dest = target_path()
    shutil.copyfile(PICTURE, dest)
    with open(dest, "rb") as check:
        header = check.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", "copied file is not a PNG"
    # The gate also caps the picture at 1 MiB and 1024x1024; fail loudly
    # here instead of silently handing the grader an oversized file.
    assert dest.stat().st_size <= 1048576, "entry.png is over the 1 MiB gate"
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
