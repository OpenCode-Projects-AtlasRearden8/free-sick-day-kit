"""Tests for the Free Sick-Day Kit build.

Each test verifies that every HTML sheet in sheets/ builds a valid,
print-ready PDF: correct header/footer bytes, one Letter-size page,
real page objects, and expected text content.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from pypdf import PdfReader

import build as build_mod

ROOT = Path(build_mod.__file__).resolve().parent
SHEETS = sorted((ROOT / "sheets").glob("*.html"))

LETTER = (612.0, 792.0)

# Key phrases that must appear in the extracted text of each PDF.
EXPECTED_TEXT = {
    "symptom-medicine-log": ["Sick-Day Log", "Symptoms & temperature", "Medicine log"],
    "drink-rest-menu-cards": ["Adventure Water", "Blanket Fort Rest", "Crunchy Ice Chips"],
    "well-day-menus": ["TV Time Menu", "Quiet Play Menu"],
    "get-well-bingo": ["Get-Well Bingo", "Board A", "Board B"],
    "get-well-note": ["GET WELL SOON", "FEEL BETTER"],
    "no-cook-dinner-cards": ["Snack-Board Dinner", "Rotisserie Chicken", "CARD 09"],
    "return-day-work-card": ["Daycare / School / Babysitter", "Work / Your Own Shift"],
}


def test_expected_sheet_inventory():
    assert [p.stem for p in SHEETS] == sorted(EXPECTED_TEXT), (
        "sheets/ and the EXPECTED_TEXT inventory disagree")


@pytest.mark.parametrize("html_path", SHEETS, ids=lambda p: p.stem)
def test_sheet_builds_valid_pdf(html_path: Path, tmp_path: Path, monkeypatch):
    monkeypatch.setattr(build_mod, "OUT_DIR", tmp_path)
    out_pdf = build_mod.build_sheet(html_path)
    data = tmp_path / out_pdf.name
    assert out_pdf == data
    raw = data.read_bytes()

    # Valid, complete PDF file
    assert raw.startswith(b"%PDF-"), "missing %PDF header"
    assert b"%%EOF" in raw[-1024:], "missing %%EOF trailer"

    # Parses with pypdf: exactly one Letter-size, non-blank page
    reader = PdfReader(str(data))
    assert len(reader.pages) == 1, "sheet should print on a single page"
    box = reader.pages[0].mediabox
    assert (float(box.width), float(box.height)) == LETTER, (
        "page size should be US Letter (8.5x11in)")

    text = reader.pages[0].extract_text() or ""
    assert text.strip() != "", "page has no extractable text"
    for phrase in EXPECTED_TEXT[html_path.stem]:
        assert phrase.lower() in text.lower(), f"missing phrase: {phrase!r}"


@pytest.mark.parametrize("html_path", SHEETS, ids=lambda p: p.stem)
def test_source_is_html5_and_carries_disclaimer(html_path: Path):
    text = html_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in text
    assert 'charset="utf-8"' in text or "charset='utf-8'" in text
    assert "education" in text.lower(), "every sheet should say education-only"


def test_build_script_rejects_remote_urls(tmp_path: Path):
    pytest.importorskip("weasyprint")
    fetcher = build_mod._local_file_fetcher
    for bad in ("https://example.com/x.png", "http://example.com/x.css"):
        with pytest.raises(ValueError):
            fetcher(bad)


def test_no_secrets_in_repo():
    leak = re.compile(
        r"(sk-[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY)",
        re.M,
    )
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            if path.suffix in {".html", ".css", ".py", ".md", ".txt", ".toml", ".cfg"}:
                assert not leak.search(path.read_text(encoding="utf-8", errors="ignore")), (
                    f"possible secret in {path}")
