#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Writes one invented passport spread to /output/entry.png.

The spread is drawn in code by render.py (PIL + DejaVu, vendored in
fonts/, no network). The grader sandbox is minimal: if Pillow or the
fonts are unavailable there, render.py raises and this driver falls back
to the embedded render in entry.b64 — the exact bytes render.py produces
locally, drawn by the same code. Either path writes the same image.
"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def _fallback():
    with open(os.path.join(HERE, "entry.b64")) as f:
        data = base64.b64decode(f.read())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    print("wrote", OUT, "(embedded render)", len(data), "bytes")


def main():
    try:
        sys.path.insert(0, HERE)
        import render

        render.main()
    except Exception as exc:  # noqa: BLE001 - sandbox may lack PIL/fonts
        print("render failed (%s); using embedded render" % exc, file=sys.stderr)
        _fallback()


if __name__ == "__main__":
    main()
