#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Draws one invented passport spread (data page + visa page) for the
fictional Republic of Valtoria, deterministically, with no network.
Writes /output/entry.png (1024x640, under 1 MiB).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 640
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
HERE = os.path.dirname(os.path.abspath(__file__))


def font(name, size):
    vendored = os.path.join(HERE, "fonts", name)
    path = vendored if os.path.exists(vendored) else os.path.join(FD, name)
    return ImageFont.truetype(path, size)


F_SERIF = "DejaVuSerif.ttf"
F_SERIF_B = "DejaVuSerif-Bold.ttf"
F_SANS = "DejaVuSans.ttf"
F_SANS_B = "DejaVuSans-Bold.ttf"
F_MONO = "DejaVuSansMono.ttf"
F_MONO_B = "DejaVuSansMono-Bold.ttf"

# Palette
PAPER = (247, 244, 236)
PAPER2 = (242, 238, 226)
INK = (28, 32, 38)
TEAL = (31, 77, 74)
TEAL_DK = (20, 52, 50)
GOLD = (150, 112, 48)
BURG = (122, 46, 58)
BLUE = (43, 74, 122)
GREEN = (46, 93, 58)
GREY = (110, 110, 104)
LIGHT_LINE = (196, 188, 168)
SKIN = (232, 185, 141)
SKIN_DK = (214, 164, 120)
HAIR = (58, 38, 28)
JACKET = (46, 74, 90)
PHOTO_BG = (207, 224, 232)


def mrz_check(s):
    vals = {}
    for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = i
    vals["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    base1 = "P<VLTKOVAC<<ELENA<MARA"
    line1 = base1 + "<" * (44 - len(base1))
    assert len(line1) == 44
    doc = "VLT847291"
    nat = "VLT"
    dob = "940314"
    sex = "F"
    exp = "360601"
    pers = "<<<<<<<<<<<<<<"
    line2 = (
        doc + mrz_check(doc)
        + nat
        + dob + mrz_check(dob)
        + sex
        + exp + mrz_check(exp)
        + pers + mrz_check(pers)
    )
    line2 += mrz_check(line2)
    assert len(line2) == 44, len(line2)
    return line1, line2


def guilloche(d, x0, y0, x1, y1, color, step=7, amp=3.0):
    """Faint wavy security lines across a page region."""
    y = y0 + 4
    while y < y1:
        pts = []
        x = x0
        while x <= x1:
            pts.append((x, y + amp * math.sin((x - x0) / 26.0 + y / 9.0)))
            x += 4
        d.line(pts, fill=color, width=1)
        y += step


def coat_of_arms(d, cx, cy, s):
    """Small shield: mountain peaks under a star, on a teal roundel."""
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=TEAL, outline=GOLD, width=2)
    # mountains
    d.polygon([(cx - 0.62 * s, cy + 0.45 * s), (cx - 0.18 * s, cy - 0.35 * s),
               (cx + 0.12 * s, cy + 0.45 * s)], fill=(247, 244, 236))
    d.polygon([(cx - 0.05 * s, cy + 0.45 * s), (cx + 0.30 * s, cy - 0.10 * s),
               (cx + 0.62 * s, cy + 0.45 * s)], fill=(220, 214, 196))
    # star
    r1, r2 = 0.22 * s, 0.09 * s
    pts = []
    for i in range(10):
        r = r1 if i % 2 == 0 else r2
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy - 0.62 * s + r * math.sin(a)))
    d.polygon(pts, fill=GOLD)


def draw_portrait(d, x0, y0, x1, y1):
    """Flat passport-style portrait: woman, dark hair in a bun.
    Rendered on a temp layer so the backdrop arc cannot spill outside
    the photo box."""
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (w, h), PHOTO_BG + (255,))
    ld = ImageDraw.Draw(layer)
    # faint backdrop arc, clipped to the box
    ld.ellipse([-20, -60, w + 20, h - 40], fill=(190, 212, 222, 255))
    cx = w // 2
    # shoulders / jacket
    ld.polygon([(6, h), (cx - 52, h - 52), (cx - 30, h - 66),
                (cx + 30, h - 66), (cx + 52, h - 52), (w - 6, h)],
               fill=JACKET + (255,))
    # white shirt V
    ld.polygon([(cx - 16, h - 64), (cx + 16, h - 64), (cx, h - 34)],
               fill=(245, 245, 242, 255))
    # neck
    ld.rectangle([cx - 13, h - 96, cx + 13, h - 58], fill=SKIN_DK + (255,))
    # head
    ld.ellipse([cx - 34, 26, cx + 34, 104], fill=SKIN + (255,))
    # ears
    ld.ellipse([cx - 40, 58, cx - 30, 78], fill=SKIN + (255,))
    ld.ellipse([cx + 30, 58, cx + 40, 78], fill=SKIN + (255,))
    # hair: top cap + sides + bun
    ld.pieslice([cx - 36, 20, cx + 36, 92], 180, 360, fill=HAIR + (255,))
    ld.rectangle([cx - 36, 52, cx - 28, 96], fill=HAIR + (255,))
    ld.rectangle([cx + 28, 52, cx + 36, 96], fill=HAIR + (255,))
    ld.ellipse([cx - 14, 6, cx + 14, 30], fill=HAIR + (255,))
    # brows, eyes, nose, mouth
    ld.line([cx - 22, 62, cx - 8, 60], fill=HAIR + (255,), width=2)
    ld.line([cx + 8, 60, cx + 22, 62], fill=HAIR + (255,), width=2)
    ld.ellipse([cx - 20, 66, cx - 10, 72], fill=(30, 30, 30, 255))
    ld.ellipse([cx + 10, 66, cx + 20, 72], fill=(30, 30, 30, 255))
    ld.line([cx, 72, cx - 2, 84], fill=(170, 120, 90, 255), width=2)
    ld.arc([cx - 10, 86, cx + 10, 98], 15, 165, fill=(150, 70, 60, 255), width=2)
    img.paste(layer, (x0, y0))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def label_value(d, x, y, label, value, vfont, max_w=290):
    d.text((x, y), label, font=font(F_SANS, 10), fill=GREY)
    d.text((x, y + 13), value, font=vfont, fill=INK)


def stamp(d, x, y, w, h, color, lines, angle=-6):
    """A rectangular ink stamp, slightly rotated, double border."""
    st = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rectangle([20, 20, 20 + w, 20 + h], outline=color + (255,), width=3)
    sd.rectangle([24, 24, 20 + w - 4, 20 + h - 4], outline=color + (255,), width=1)
    cy = 20 + 16
    for i, (txt, fnt, col) in enumerate(lines):
        f = font(fnt[0], fnt[1])
        tw = sd.textlength(txt, font=f)
        sd.text((20 + (w - tw) / 2, cy), txt, font=f, fill=col + (235,))
        cy += fnt[1] + 3
    st = st.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(st, (x - 20, y - 20), st)


def main():
    global img
    img = Image.new("RGB", (W, H), (226, 220, 203))
    d = ImageDraw.Draw(img)

    # ---- outer cover edge + two pages ----
    d.rectangle([8, 8, W - 9, H - 9], fill=(58, 66, 60))  # cover rim
    d.rectangle([14, 14, 505, H - 15], fill=PAPER)
    d.rectangle([519, 14, W - 15, H - 15], fill=PAPER2)
    # gutter shadow
    for i in range(7):
        d.line([505 + i, 14, 505 + i, H - 15], fill=(200, 192, 172))
        d.line([519 - i, 14, 519 - i, H - 15], fill=(214, 206, 188))
    d.line([512, 14, 512, H - 15], fill=(120, 112, 96), width=1)

    guilloche(d, 16, 16, 503, H - 17, (228, 222, 202))
    guilloche(d, 521, 16, W - 17, H - 17, (224, 218, 198))

    # ================= LEFT PAGE: DATA PAGE =================
    d.text((30, 26), "REPUBLIC OF VALTORIA", font=font(F_SERIF_B, 24), fill=TEAL_DK)
    d.text((30, 56), "PASSPORT  ·  PASEPORT", font=font(F_SANS_B, 11), fill=GOLD)
    d.line([30, 76, 489, 76], fill=TEAL, width=2)
    coat_of_arms(d, 462, 48, 26)

    # photo
    draw_portrait(d, 30, 92, 180, 272)
    d.text((30, 278), "PHOTOGRAPH", font=font(F_SANS, 9), fill=GREY)

    # data fields, right of photo
    vx = 200
    vfb = font(F_SANS_B, 16)
    vfs = font(F_SANS_B, 14)
    label_value(d, vx, 92, "TYPE / TIP", "P", vfb)
    label_value(d, vx + 70, 92, "CODE / KOD", "VLT", vfb)
    label_value(d, vx + 150, 92, "PASSPORT No. / No. PASEPORT", "VLT 847 291", vfb)
    label_value(d, vx, 140, "SURNAME / NAMA KELUARGA", "KOVAC", vfb)
    label_value(d, vx, 188, "GIVEN NAMES / NAMA", "ELENA MARA", vfb)
    label_value(d, vx, 236, "NATIONALITY / KEWARGANEGARAAN", "VALTORIAN", vfb)
    label_value(d, vx + 215, 236, "SEX / JANTINA", "F", vfb)
    label_value(d, vx, 284, "DATE OF BIRTH / TARIKH LAHIR", "14 MAR 1994", vfb)
    label_value(d, vx, 332, "PLACE OF BIRTH / TEMPAT LAHIR", "MARENDOR", vfb)
    label_value(d, vx, 380, "DATE OF ISSUE / TARIKH KELUAR", "02 JUN 2026", vfs)
    label_value(d, vx + 170, 380, "DATE OF EXPIRY / TAMAT", "01 JUN 2036", vfs)
    label_value(d, vx, 428, "AUTHORITY / PIHAK BERKUASA",
                "MINISTRY OF THE INTERIOR — MARENDOR", font(F_SANS_B, 12))

    # signature
    d.line([30, 500, 240, 500], fill=INK, width=1)
    d.text((34, 474), "Elena Kovac", font=font(F_SERIF, 20), fill=(40, 50, 90))
    d.text((30, 504), "HOLDER'S SIGNATURE / TANDATANGAN", font=font(F_SANS, 9), fill=GREY)
    d.text((330, 478), "PAGE 1 OF 32", font=font(F_SANS_B, 10), fill=GREY)
    d.text((330, 496), "SEE PAGE 2 FOR VISAS", font=font(F_SANS, 10), fill=GREY)

    # MRZ
    d.rectangle([28, 528, 491, 600], fill=(255, 255, 255), outline=LIGHT_LINE)
    l1, l2 = mrz_lines()
    mf = font(F_MONO, 17)
    d.text((36, 536), l1, font=mf, fill=INK)
    d.text((36, 562), l2, font=mf, fill=INK)

    # ================= RIGHT PAGE: VISA PAGE =================
    d.text((538, 26), "VISAS", font=font(F_SERIF_B, 24), fill=TEAL_DK)
    d.text((538, 56), "VISA  ·  ENDORSEMENTS", font=font(F_SANS_B, 11), fill=GOLD)
    d.line([538, 76, 994, 76], fill=TEAL, width=2)
    coat_of_arms(d, 968, 48, 26)

    # Talvere tourist visa vignette (the telling detail)
    d.rectangle([538, 92, 800, 216], fill=(255, 255, 255), outline=BLUE, width=2)
    d.rectangle([542, 96, 796, 212], outline=BLUE, width=1)
    d.text((552, 102), "VISA — REPUBLIC OF TALVERE", font=font(F_SANS_B, 13), fill=BLUE)
    d.line([552, 124, 786, 124], fill=BLUE, width=1)
    d.text((552, 130), "TOURIST · SINGLE ENTRY · VALID 30 DAYS", font=font(F_SANS_B, 11), fill=INK)
    d.text((552, 148), "Issued 15 JUL 2026, Marendor", font=font(F_SANS, 11), fill=INK)
    d.text((552, 166), "CONDITION: holder must register with the", font=font(F_SANS, 11), fill=INK)
    d.text((552, 182), "local police within 72 hours of arrival.", font=font(F_SANS, 11), fill=INK)
    d.text((552, 198), "FEE PAID 12 DN", font=font(F_SANS_B, 11), fill=BURG)

    # stamps: all after issue date 02 JUN 2026
    stamp(d, 538, 236, 210, 96, BURG, [
        ("DRAVNOR", (F_SANS_B, 15), BURG),
        ("ARRIVAL  ·  18 JUN 2026", (F_SANS_B, 11), BURG),
        ("KESTREL PASS", (F_SANS, 10), BURG),
    ], angle=-5)
    stamp(d, 772, 236, 210, 96, BLUE, [
        ("DRAVNOR", (F_SANS_B, 15), BLUE),
        ("DEPARTURE  ·  25 JUN 2026", (F_SANS_B, 11), BLUE),
        ("KESTREL PASS", (F_SANS, 10), BLUE),
    ], angle=4)
    stamp(d, 538, 352, 210, 96, GREEN, [
        ("OSTMARK", (F_SANS_B, 15), GREEN),
        ("ARRIVAL  ·  03 JUL 2026", (F_SANS_B, 11), GREEN),
        ("OSTMARK GATE", (F_SANS, 10), GREEN),
    ], angle=5)
    stamp(d, 772, 352, 210, 96, BURG, [
        ("OSTMARK", (F_SANS_B, 15), BURG),
        ("DEPARTURE  ·  10 JUL 2026", (F_SANS_B, 11), BURG),
        ("OSTMARK GATE", (F_SANS, 10), BURG),
    ], angle=-4)
    stamp(d, 538, 468, 210, 96, BLUE, [
        ("TALVERE", (F_SANS_B, 15), BLUE),
        ("ARRIVAL  ·  22 JUL 2026", (F_SANS_B, 11), BLUE),
        ("NORTH HARBOUR", (F_SANS, 10), BLUE),
    ], angle=-6)
    # red fee stamp overlapping the last stamp corner
    stamp(d, 772, 468, 210, 96, BURG, [
        ("FEE PAID", (F_SANS_B, 16), BURG),
        ("12 DENARS", (F_SANS_B, 12), BURG),
        ("TALVERE · 22 JUL 2026", (F_SANS, 10), BURG),
    ], angle=7)

    d.text((538, 584), "THIS PASSPORT CONTAINS 32 PAGES  ·  PAGE 2",
           font=font(F_SANS, 10), fill=GREY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
