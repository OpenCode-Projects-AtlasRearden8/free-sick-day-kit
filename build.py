#!/usr/bin/env python3
"""Build the Free Sick-Day Kit printables.

Renders every HTML file in sheets/ to a print-ready PDF in printables/
using WeasyPrint. Local-only: no network calls, no accounts, no telemetry.

Usage:
    python3 build.py            (build every sheet)
    python3 build.py name1 ...  (build only the named sheets, with or
                                 without the .html extension)
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname

from weasyprint import HTML
from weasyprint.urls import URLFetcherResponse

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "sheets"
OUT_DIR = ROOT / "printables"


def _file_url(path: Path) -> str:
    return path.resolve().as_uri()


def build_sheet(html_path: Path) -> Path:
    """Render one HTML sheet to a PDF next to build.py in printables/."""
    out_path = OUT_DIR / (html_path.stem + ".pdf")
    HTML(
        filename=str(html_path),
        url_fetcher=_local_file_fetcher,
        base_url=str(html_path.parent),
    ).write_pdf(str(out_path))
    return out_path


def _local_file_fetcher(url: str):
    """Restrictive local fetcher: only file:// URLs inside the project tree."""
    parsed = urlparse(url)
    if parsed.scheme not in ("", "file"):
        raise ValueError(f"Refusing non-file URL: {url}")
    target = Path(url2pathname(parsed.path)).resolve()
    root_resolved = ROOT.resolve()
    if not target.is_relative_to(root_resolved):
        raise ValueError(f"Refusing to fetch outside project root: {url}")
    if not target.is_file():
        raise ValueError(f"File not found: {target}")
    return URLFetcherResponse(_file_url(target), target.read_bytes(), {}, 200)


def main(argv: list[str]) -> int:
    if not SHEETS_DIR.is_dir():
        print(f"No sheets/ directory found at {SHEETS_DIR}", file=sys.stderr)
        return 1

    wanted = {a.removesuffix(".html").removesuffix(".pdf") for a in argv[1:] or []}
    sheets = sorted(p for p in SHEETS_DIR.glob("*.html"))
    if wanted:
        sheets = [p for p in sheets if p.stem in wanted]
        missing = wanted - {p.stem for p in sheets}
        if missing:
            print(f"Unknown sheet(s): {', '.join(sorted(missing))}", file=sys.stderr)
            return 1

    OUT_DIR.mkdir(exist_ok=True)
    failures = []
    for sheet in sheets:
        try:
            out = build_sheet(sheet)
            print(f"built {out.relative_to(ROOT)}")
        except Exception as exc:  # keep building the rest, report at the end
            failures.append((sheet.stem, exc))
            print(f"FAILED {sheet.stem}: {exc}", file=sys.stderr)

    if failures:
        print(f"\n{len(failures)} sheet(s) failed to build.", file=sys.stderr)
        return 1
    print(f"\nDone. {len(sheets)} PDF(s) in {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
