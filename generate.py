#!/usr/bin/env python3
"""Draw the news-image-20261127 front page (1024x1024 PNG) from stories.json.

Layout, top to bottom: masthead, lead story with a drawn Gulf illustration,
a world map with 12 numbered flashpoints, a markets strip, a 3x4 grid of
the day's stories, and a wire ticker. Everything is drawn with PIL from
the JSON data; no network, no randomness, so repeated runs are identical.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "stories.json").read_text())

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 25, 38)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GOLD = (184, 134, 11)
GREY = (90, 92, 98)
LIGHT = (233, 228, 216)
SEA = (168, 196, 210)
LAND = (216, 208, 182)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


# Simplified continent outlines in (lon, lat); equirectangular projection.
CONTINENTS = [
    # North America
    [(-168, 65), (-150, 70), (-130, 71), (-110, 73), (-95, 80), (-85, 73),
     (-75, 72), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-84, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-124, 48), (-135, 58), (-155, 58), (-168, 65)],
    # South America
    [(-80, 10), (-75, 11), (-70, 12), (-60, 8), (-52, 5), (-50, 0),
     (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -40),
     (-70, -50), (-73, -53), (-70, -40), (-72, -20), (-78, -5), (-80, 10)],
    # Africa
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -27), (12, -18), (9, 4), (-8, 5), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (5, 60), (-5, 58), (-10, 52), (-10, 36)],
    # Asia
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (162, 58),
     (158, 52), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35),
     (122, 38), (120, 32), (115, 23), (109, 18), (105, 10), (100, 8),
     (97, 15), (92, 21), (88, 22), (80, 15), (77, 8), (75, 12), (72, 20),
     (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (44, 29), (40, 31),
     (36, 36), (30, 36), (30, 62)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (136, -12), (132, -12),
     (126, -14), (122, -17), (118, -20), (113, -22)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (-1, 51), (-5, 50)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (144, 44),
     (142, 42), (140, 36), (136, 33), (131, 31), (130, 31)],
]


def project(lon, lat, box):
    """Map lon/lat into the map box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (90.0 - lat) / 150.0 * (y1 - y0)
    return x, y


def draw_masthead(d):
    d.rectangle([0, 0, W, 72], fill=NAVY)
    d.rectangle([0, 72, W, 76], fill=GOLD)
    text(d, (24, 14), "THE WORLD TODAY", font(FONTB, 40), (250, 247, 238))
    text(d, (1000, 20), DATA["dateline"], font(FONTB, 17), (214, 196, 150),
         anchor="ra")
    text(d, (1000, 44), "ONE DAY  •  ONE PICTURE  •  MAKE.FUN",
         font(FONT, 12), (170, 180, 200), anchor="ra")


def draw_lead(d):
    lead = DATA["lead"]
    # Kicker + headline, left column.
    text(d, (24, 92), lead["kicker"], font(FONTB, 15), RED)
    y = 114
    for line in wrap(d, lead["headline"], font(FONTB, 30), 590):
        text(d, (24, y), line, font(FONTB, 30), INK)
        y += 36
    y += 6
    for line in wrap(d, lead["deck"], font(FONT, 15), 590):
        text(d, (24, y), line, font(FONT, 15), (52, 54, 62))
        y += 20
    y += 8
    d.line([24, y, 614, y], fill=GOLD, width=2)
    y += 10
    for line in wrap(d, lead["detail"], font(FONTB, 14), 590):
        text(d, (24, y), line, font(FONTB, 14), (70, 60, 40))
        y += 19
    # Illustration panel: dusk over a Gulf oil terminal.
    x0, y0, x1, y1 = 636, 88, 1000, 318
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0 - 1)
        r = int(58 + (24 - 58) * t)
        g = int(58 + (33 - 58) * t)
        b = int(74 + (61 - 74) * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    # Low sun and its reflection.
    d.ellipse([x0 + 250, y0 + 28, x0 + 296, y0 + 74], fill=(232, 164, 62))
    d.rectangle([x0, 236, x1, y1], fill=(38, 62, 84))  # sea
    for yy in range(240, y1, 12):
        d.line([(x0 + 20, yy), (x1 - 20, yy)], fill=(58, 88, 112), width=2)
    # Refinery silhouettes on the shore.
    shore = 236
    d.rectangle([x0, shore - 4, x1, shore + 2], fill=(30, 30, 34))
    for bx, bw, bh in [(x0 + 28, 34, 96), (x0 + 70, 26, 128), (x0 + 104, 30, 84),
                       (x0 + 142, 22, 110), (x0 + 210, 30, 92), (x0 + 248, 24, 118)]:
        d.rectangle([bx, shore - bh, bx + bw, shore], fill=(24, 26, 32))
    for bx, bw, bh in [(x0 + 70, 26, 128), (x0 + 248, 24, 118)]:
        mast_top = max(y0 + 4, shore - bh - 26)
        d.rectangle([bx + bw // 2 - 2, mast_top, bx + bw // 2 + 2,
                     shore - bh], fill=(24, 26, 32))
        d.ellipse([bx + bw // 2 - 7, shore - bh - 15, bx + bw // 2 + 7,
                   shore - bh - 1], fill=(240, 140, 40))  # flare
    # Smoke plumes drifting up from two stacks (panel-relative coords,
    # kept inside the panel: centre minus radius stays below y0).
    for cx, cy, rad in [(x0 + 83, y0 + 52, 20), (x0 + 110, y0 + 38, 22),
                        (x0 + 142, y0 + 30, 20), (x0 + 260, y0 + 52, 18),
                        (x0 + 286, y0 + 38, 20)]:
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(52, 52, 58))
    # A small drone silhouette in the sky.
    dx, dy = x0 + 300, y0 + 30
    d.line([(dx - 14, dy), (dx + 14, dy)], fill=(220, 220, 220), width=3)
    d.line([(dx, dy - 8), (dx, dy + 8)], fill=(220, 220, 220), width=3)
    d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(220, 220, 220))
    # Caption strip naming the three Gulf flashpoints.
    d.rectangle([x0, y1 - 26, x1, y1], fill=(20, 25, 38))
    text(d, (x0 + 10, y1 - 21), "KUWAIT  •  JAZAN  •  RAS TANURA",
         font(FONTB, 13), (240, 200, 120))
    d.rectangle([x0, y0, x1, y1], outline=(20, 25, 38), width=2)


# Per-pin label offsets (dx, dy) to keep labels off each other and off the sea.
LABEL_DXDY = {1: (10, -8), 2: (10, 6), 3: (10, -28), 4: (-70, 18), 5: (-58, 14),
              6: (-66, 4), 7: (10, -6), 8: (-58, -24), 9: (14, 2),
              10: (-100, 14), 11: (10, -20), 12: (10, -6)}


def draw_map(d):
    box = (24, 368, 1000, 560)
    text(d, (24, 332), "FLASHPOINTS — 12 PLACES THAT MADE THE NEWS",
         font(FONTB, 16), INK)
    text(d, (1000, 334), "27 NOVEMBER 2026", font(FONTB, 13), GREY,
         anchor="ra")
    d.rectangle(box, fill=(226, 236, 240))
    d.rectangle(box, outline=(180, 186, 190), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(150, 146, 128))
    for pin in DATA["pins"]:
        px, py = project(pin["lon"], pin["lat"], box)
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=RED,
                  outline=(255, 255, 255), width=2)
        text(d, (px, py - 1), str(pin["n"]), font(FONTB, 12),
             (255, 255, 255), anchor="mm")
        dx, dy = LABEL_DXDY[pin["n"]]
        lx, ly = px + dx, py + dy
        lab = f"{pin['n']}. {pin['label']}"
        text(d, (lx + 1, ly + 1), lab, font(FONTB, 12), (255, 255, 255))
        text(d, (lx, ly), lab, font(FONTB, 12), INK)


def draw_markets(d):
    y0, y1 = 576, 622
    d.rectangle([0, y0, W, y1], fill=NAVY)
    items = DATA["markets"]
    cw = W // len(items)
    for i, (name, val) in enumerate(items):
        cx = i * cw + cw // 2
        down = "-" in val
        col = (235, 120, 110) if down else (120, 220, 150)
        text(d, (cx, y0 + 5), name, font(FONTB, 12), (200, 208, 220),
             anchor="ma")
        text(d, (cx, y0 + 22), val, font(FONTB, 14), col, anchor="ma")
        if i:
            d.line([(i * cw, y0 + 6), (i * cw, y1 - 6)], fill=(70, 84, 110))


def draw_grid(d):
    stories = DATA["stories"]
    x0, y0 = 24, 640
    cw, ch, gap = 315, 76, 8
    for idx, s in enumerate(stories):
        r, c = divmod(idx, 3)
        x, y = x0 + c * (cw + gap), y0 + r * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=(255, 255, 255),
                    outline=(205, 200, 188), width=1)
        d.rectangle([x, y, x + 5, y + ch], fill=RED)
        text(d, (x + 14, y + 8), f"{idx + 1:02d}", font(FONTB, 15), RED)
        text(d, (x + 46, y + 9), s["tag"], font(FONTB, 11), GOLD)
        lines = wrap(d, s["headline"], font(FONTB, 14), cw - 28)
        ly = y + 27
        for line in lines[:2]:
            text(d, (x + 14, ly), line, font(FONTB, 14), INK)
            ly += 16
        det = wrap(d, s["detail"], font(FONT, 11), cw - 28)
        text(d, (x + 14, y + ch - 16), det[0] if det else "",
             font(FONT, 11), GREY)


def draw_ticker(d):
    y0, y1 = 968, H
    d.rectangle([0, y0, W, y1], fill=INK)
    text(d, (24, y0 + 8), "WIRE", font(FONTB, 15), (240, 200, 120))
    items = "   •   ".join(DATA["ticker"])
    lines = wrap(d, items, font(FONT, 12), W - 110)
    ly = y0 + 5
    for line in lines[:3]:
        text(d, (96, ly), line, font(FONT, 12), (235, 235, 230))
        ly += 16


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_map(d)
    draw_markets(d)
    draw_grid(d)
    draw_ticker(d)
    img.save(HERE / "entry.png", optimize=True)


if __name__ == "__main__":
    main()
