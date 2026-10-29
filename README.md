# Free Sick-Day Kit

Free printables for the sick-day scramble. When a kid wakes up feverish and the
whole morning unravels, these sheets help you slow it down: track medicine
times, keep drinks and rest happening, hand a fever-free "well day" a clear
menu, and make returning to daycare or work one less thing to remember.

Plain, friendly, tested — like a friend would explain it. Everything is
education-only, **not medical advice**. Always follow your doctor's and
medicine-label instructions.

## What's inside

| PDF (in `printables/`) | What it's for |
| --- | --- |
| `symptom-medicine-log.pdf` | Write-in log of symptoms, temperatures, and medicine times for each sick day. |
| `drink-rest-menu-cards.pdf` | Cut-out "menu" cards that make sips and rest feel like ordering off a real menu. |
| `well-day-menus.pdf` | TV-time and quiet-play menus for the fever-free, 24-hour-on-the-mend kid. |
| `get-well-bingo.pdf` | Two 5x5 bingo boards played by spotting kind things — resting, sipping, cheering each other on. |
| `get-well-note.pdf` | A note a kid can color and send to a sick friend or sibling. |
| `no-cook-dinner-cards.pdf` | No-cook, no- energy dinner idea cards for the cooked-by-now grown-up. |
| `return-day-work-card.pdf` | One small summary card: symptoms, last medicine and time, fever-free stretch — hand it to daycare, school, or your shift lead. |

## Requirements

- Python 3.10+
- WeasyPrint (`pip install weasyprint`)
- pypdf (used by the tests to validate output)

No signups, no accounts, no network calls. Everything runs locally.

## Build

```bash
python3 build.py
```

That reads every HTML file in `sheets/`, renders it, and writes an
unbranded, print-ready PDF to `printables/`. Re-run any time you edit a sheet.

## Test

```bash
python3 -m pytest
```

The tests verify every HTML sheet builds a valid PDF (correct `%PDF` header,
real page objects, page sizes, endstream close-out) and that every source file
has a matching PDF.

## Printing tips

- Print at 100% (no "fit to page") so the write-in lines land where expected.
- Cards print on the same sheet they were designed for — cut on the dashed lines.
- Cardstock makes the bingo and menu cards last through the week.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

Made by Asdale Dynamics, LLC. More beginner-friendly tools and guides at
[dylanasdale.github.io](https://dylanasdale.github.io).

*Education only. Not medical advice.*
