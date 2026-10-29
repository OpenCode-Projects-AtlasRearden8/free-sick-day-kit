# STATUS.md — Free Sick-Day Kit

## What was built

A local, no-signup printable kit for surviving a sick day: HTML/CSS sources in
`sheets/` are rendered to unbranded, print-ready PDFs in `printables/` by one
build script. All content is education/organizing only, never medical advice.

Built by Asdale Dynamics, LLC (Dylan Asdale, RN — plain-English, beginner-first,
tested style).

The seven printables:

1. `symptom-medicine-log.pdf` — one-page-per-day write-in log: symptoms,
   temperatures, medicine times, "next dose okay at", and a call-the-doctor
   nudge strip.
2. `drink-rest-menu-cards.pdf` — 10 cut-out cards (6 " sip menu" + 4 rest
   menu) that turn fluids and lying down into ordering off a restaurant menu.
3. `well-day-menus.pdf` — TV-time and quiet-play menus gated behind a
   fever-free-24-hours rule.
4. `get-well-bingo.pdf` — two 5×5 "kindness spot" bingo boards (A and B) played
   beside the sick kid.
5. `get-well-note.pdf` — two half-page notes a kid can personalize and color.
6. `no-cook-dinner-cards.pdf` — nine zero-cook dinner rescue cards
   (snack-board, rotisserie pickup, sandwich bar, etc.).
7. `return-day-work-card.pdf` — two summary cards (daycare/school-side and
   work-side): symptoms, last dose & time, fever-free stretch, watch-fors.

## How to run it

```
python3 build.py          # build every sheet -> printables/*.pdf
python3 build.py bingo    # build a single sheet by short name
python3 -m pytest         # verify every sheet builds a valid PDF
```

Requirements: Python 3.10+, WeasyPrint (build), pypdf and pytest (tests).
Everything is local — no accounts, no network calls, no secrets, no personal
data in the repo.

## Verification results

- `python3 build.py`: all 7 sheets build cleanly (exit 0), each writes a
  ~12–29 KB PDF into `printables/`.
- `python3 -m pytest`: **17 passed** —
  - 7 × `test_sheet_builds_valid_pdf`: `%PDF` header, `%%EOF` trailer,
    parses with pypdf, exactly 1 page, exact US-Letter size (612×792 pt),
    non-blank extractable text, and expected sheet-specific phrases present.
  - 7 × `test_source_is_html5_and_carries_disclaimer`: HTML5 doctype, utf-8,
    education-only wording on every sheet.
  - remote-URL fetch rejection and a repo-wide secret-scan test.
- Visual pass at 60 DPI on all 7 pages: layouts fit on one page, cut lines and
  write-in fields land where expected.
- Fonts render with generic serif/sans fallbacks (DejaVu on Linux); only
  non-ASCII glyphs emitted are `—` and `→`.

## Known gaps

- Fonts: relies on system fallbacks; on a font-less minimal container the
  look shifts slightly (verified fine with DejaVu present).
- WeasyPrint 70 writes compressed object streams, so grep-for-`/Type /Page`
  on the raw bytes finds nothing in the output PDFs; the tests validate page
  structure via pypdf instead, which is the robust path.
- The kit says "education and organizing only, not medical advice" throughout,
  and defers to your doctor / program policy for anything clinical.
- No CI config yet; run `python3 -m pytest` after any sheet edit.
- The caret text uses "program's" in two spots; cards are US-English.
