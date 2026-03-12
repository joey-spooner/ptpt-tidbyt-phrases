import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "phrases.csv"
OUT_PATH = ROOT / "app" / "app.star"

# Approximate character limits per font at 64px wide (no padding, centered)
PT_MAX_CHARS = 10   # 6x13: ~6px per char
EN_MAX_CHARS = 15   # tom-thumb: ~4px per char

APP_TEMPLATE = """\
load("render.star", "render")
load("time.star", "time")

# Generated from data/phrases.csv. Do not edit by hand.
PHRASES = [
{phrases_block}]

def _frame_colored(pt, en):
    return render.Box(
        child = render.Column(
            main_align = "center",
            cross_align = "center",
            expanded = True,
            children = [
                render.Text(content = pt, font = "6x13", color = "#00CC00"),
                render.Text(content = en, font = "tom-thumb", color = "#5BC8F5"),
            ],
        ),
    )

def _frame_green_bg(pt, en):
    return render.Box(
        color = "#006600",
        child = render.Column(
            main_align = "center",
            cross_align = "center",
            expanded = True,
            children = [
                render.Text(content = pt, font = "6x13", color = "#FFF"),
                render.Text(content = en, font = "tom-thumb", color = "#FFF"),
            ],
        ),
    )

def main(config):
    if len(PHRASES) == 0:
        return render.Root(
            child = render.Text(
                content = "No phrases",
                font = "5x7",
            ),
        )

    idx = (time.now().unix // 3) % len(PHRASES)
    p = PHRASES[idx]
    pt = p["pt"]
    en = p["en"].upper()

    return render.Root(
        delay = 2000,
        child = render.Animation(
            children = [
                _frame_colored(pt, en),
                _frame_green_bg(pt, en),
            ],
        ),
    )
"""


def escape_starlark(value: str) -> str:
    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    return value


def load_phrases():
    rows = []
    warnings = []

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # row 1 is the header
            pt = (row.get("pt") or "").strip()
            en = (row.get("en") or "").strip()

            if not pt or not en:
                continue

            if len(pt) > PT_MAX_CHARS:
                warnings.append(
                    f"Row {i}: pt={pt!r} ({len(pt)} chars) may overflow 6x13 font (max ~{PT_MAX_CHARS})"
                )
            if len(en) > EN_MAX_CHARS:
                warnings.append(
                    f"Row {i}: en={en!r} ({len(en)} chars) may overflow tom-thumb font (max ~{EN_MAX_CHARS})"
                )

            rows.append({"pt": pt, "en": en})

    return rows, warnings


def build_phrases_block(rows: list) -> str:
    lines = []
    for row in rows:
        lines.append("    {")
        lines.append(f'        "pt": "{escape_starlark(row["pt"])}",')
        lines.append(f'        "en": "{escape_starlark(row["en"])}",')
        lines.append("    },")
    return "\n".join(lines) + "\n"


def main() -> None:
    rows, warnings = load_phrases()

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    phrases_block = build_phrases_block(rows)
    app_star = APP_TEMPLATE.format(phrases_block=phrases_block)
    OUT_PATH.write_text(app_star, encoding="utf-8")
    print(f"Wrote {len(rows)} phrases to {OUT_PATH}")

    if warnings:
        print(f"{len(warnings)} length warning(s) — check stderr", file=sys.stderr)


if __name__ == "__main__":
    main()
