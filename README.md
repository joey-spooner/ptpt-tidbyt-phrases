# 🇵🇹 PT-PT Tidbyt Phrases

A Tidbyt app that teaches you one European Portuguese phrase at a time — because Brazilian Portuguese is a different vibe and this household has standards.

## What it does

Every hour, your Tidbyt display shows a practical PT-PT phrase in large green text alongside its English translation in blue. Every two seconds the display dramatically flips to a green background with white text, because subtlety is overrated.

50 phrases included. Enough to survive Lisbon, confuse a taxi driver, and order a pastel de nata with confidence.

## Usage

**Add or edit phrases:**

```
data/phrases.csv
```

Two columns: `pt` (the phrase, in caps) and `en` (the English gloss, lowercase — it gets uppercased at render time because consistency matters).

**Rebuild the app:**

```bash
python3 tools/build_app.py
```

This generates `app/app.star`. Do not edit that file by hand. It will not end well.

**Preview it:**

```bash
pixlet render app/app.star
```

**Push to your Tidbyt:**

```bash
pixlet push --api-token <token> <device-id> app/app.star
```

## Project structure

```
data/phrases.csv      ← source of truth
tools/build_app.py    ← generates the Starlark app from CSV
app/app.star          ← generated, do not touch
```

## Notes

- European Portuguese only. PT-PT. Not BR-PT. The ç's are non-negotiable.
- Phrase rotation is currently set to every 3 seconds for testing. Production target is hourly.
- The validator will warn you if your phrases are too long for the screen. It is not judging you. Much.

## Requirements

- [Pixlet](https://github.com/tidbyt/pixlet)
- Python 3
- A Tidbyt (obviously)
- A passing interest in the Portuguese language
