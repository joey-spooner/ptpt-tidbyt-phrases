# PT-PT Tidbyt Phrase App Rules

This repository contains a simple Tidbyt/Pixlet phrase-of-the-day app.

## Goal
Show one PT-PT phrase per hour on a Tidbyt display.

## Constraints
- European Portuguese only (PT-PT), not Brazilian Portuguese
- Keep phrases short enough for a 64x32 Tidbyt screen
- Keep English glosses short (max ~15 chars for tom-thumb font)
- Keep PT phrases short (max ~10 chars for 6x13 font; some intentionally exceed this)
- No external APIs in V1
- Source of truth is `data/phrases.csv` (columns: `pt`, `en`)
- Generated file is `app/app.star`
- Do not hand-edit `app/app.star`; regenerate it from CSV

## Preferred workflow
- Update `data/phrases.csv`
- Run `python3 tools/build_app.py`
- Render with Pixlet
- Push manually to Tidbyt

## Display design
- Two columns in CSV: `pt` (Portuguese phrase, stored ALL CAPS) and `en` (English gloss, stored lowercase)
- No example sentences — only the phrase and its English gloss are shown
- Both PT and EN are displayed uppercase
- Text is horizontally and vertically centered on the display
- Animation alternates between two frames (2 seconds each):
  - Frame 1 — dark background: PT in green (`#00CC00`), EN in blue (`#5BC8F5`)
  - Frame 2 — green background (`#006600`): PT and EN in white (`#FFF`)
- Phrase rotation: currently `unix // 3` (every 3 seconds, for testing); production target is hourly

## Style guidance
- Prioritize practical everyday phrases
- Prefer high-frequency PT-PT usage
- Avoid slang that is obscure or too region-specific
