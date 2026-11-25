#!/usr/bin/env python3
"""Render entry.png for news-image-20261125 v2 — local render only (Pillow).

49 stories, all verified as happened / first reported on Wed 25 Nov 2026.
Layout: masthead 0-88, 3 hero panels 96-376, 6 medium panels 384-534,
world map strip 542-662, ALSO list 670-992 (2 cols x 20 rows), footer 996-1024.
Distinct stories shown: 3 hero + 6 medium + 40 list = 49.
The repo's main.py only copies the committed entry.png (stdlib only).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (27, 42, 74)
RED = (176, 30, 36)
DARKRED = (122, 18, 24)
GOLD = (201, 162, 39)
CREAM = (255, 253, 247)
BORDER = (200, 192, 172)
MUTED = (90, 84, 72)
SKY = (207, 227, 238)
SAND = (232, 217, 176)
SEA = (46, 110, 180)

FD = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FD, name)
    if not os.path.exists(path):
        path = os.path.join(FD, "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)


def serif_b(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load_font("DejaVuSerif.ttf", size)


def serif_i(size):
    return load_font("DejaVuSerif-Italic.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def sans_b(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, lines, x, y, fnt, fill, leading=None, max_lines=None):
    if leading is None:
        leading = fnt.size + 3
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".") + "…"
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_centered(draw, y, text, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def hline(draw, y, x0=12, x1=1012, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def fit_one_line(draw, text, fnt, max_w):
    """Truncate at a word boundary with an ellipsis to fit one line."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=fnt) > max_w:
        cut = text.rfind(" ")
        text = text[:cut] if cut > 0 else text[:-1]
        text = text.rstrip()
    return text + "…"


# ---------------------------------------------------------------- flat icons
def ic_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 32, 64))
    for sx, sy in [(0.10, 0.15), (0.28, 0.08), (0.45, 0.22), (0.70, 0.10),
                   (0.88, 0.20), (0.15, 0.45), (0.80, 0.42), (0.06, 0.65)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2],
                  fill=(255, 255, 255))
    d.ellipse([x - w * 0.35, y + h * 0.72, x + w * 0.28, y + h * 1.0],
              fill=SEA)
    cx, cy = x + w * 0.60, y + h * 0.38
    d.polygon([(cx, cy - 42), (cx + 18, cy - 6), (cx + 11, cy + 32),
               (cx - 11, cy + 32), (cx - 18, cy - 6)], fill=(242, 242, 236))
    d.polygon([(cx, cy - 42), (cx + 18, cy - 6), (cx - 18, cy - 6)],
              fill=(200, 40, 40))
    d.rectangle([cx - 20, cy + 32, cx + 20, cy + 37], fill=(200, 40, 40))
    d.polygon([(cx - 8, cy + 37), (cx + 8, cy + 37), (cx, cy + 58)],
              fill=(255, 150, 40))
    d.polygon([(cx - 4, cy + 37), (cx + 4, cy + 37), (cx, cy + 48)],
              fill=(255, 220, 90))
    d.ellipse([cx - 6, cy - 14, cx + 6, cy - 2], fill=(120, 190, 230))


def ic_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 235))
    base = y + h * 0.84
    for bx, bh, col in [(0.10, 0.30, (120, 130, 140)),
                        (0.30, 0.50, (70, 110, 160)),
                        (0.50, 0.68, NAVY)]:
        d.rectangle([x + bx * w, base - bh * h, x + (bx + 0.14) * w, base],
                    fill=col)
    d.line([(x + w * 0.06, base), (x + w * 0.72, base)], fill=INK, width=2)
    d.text((x + w * 0.76, y + h * 0.05), "%", font=serif_b(34),
           fill=RED)
    d.text((x + w * 0.08, y + h * 0.07), "8:30", font=sans_b(18), fill=NAVY)


def ic_house(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 225))
    d.polygon([(x + w * 0.06, y + h * 0.42), (x + w * 0.50, y + h * 0.10),
               (x + w * 0.94, y + h * 0.42)], fill=(150, 60, 50))
    d.rectangle([x + w * 0.12, y + h * 0.42, x + w * 0.88, y + h * 0.88],
                fill=(220, 205, 170))
    d.polygon([(x + w * 0.56, y + h * 0.16), (x + w * 0.44, y + h * 0.42),
               (x + w * 0.54, y + h * 0.42), (x + w * 0.40, y + h * 0.72),
               (x + w * 0.52, y + h * 0.72), (x + w * 0.64, y + h * 0.38)],
              fill=(255, 200, 40))


def ic_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    d.polygon([(x + 4, y + h * 0.62), (x + w - 4, y + h * 0.62),
               (x + w - 14, y + h * 0.86), (x + 14, y + h * 0.86)],
              fill=(150, 60, 50))
    for i, col in enumerate([(200, 60, 50), (60, 110, 160), (220, 150, 40)]):
        d.rectangle([x + 8 + i * 11, y + h * 0.34, x + 17 + i * 11,
                     y + h * 0.60], fill=col)
    d.line([(x + 4, y + h * 0.88), (x + w - 4, y + h * 0.88)],
           fill=(90, 140, 180), width=2)


def ic_coin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 210))
    d.ellipse([x + 6, y + 14, x + 30, y + 38], fill=GOLD,
              outline=(140, 110, 20), width=2)
    d.text((x + 13, y + 17), "$", font=sans_b(18), fill=(255, 255, 255))
    d.line([(x + 8, y + 10), (x + w - 6, y + 10)], fill=RED, width=3)
    d.polygon([(x + w - 14, y + 10), (x + w - 6, y + 6), (x + w - 6, y + 14)],
              fill=RED)


def ic_candle(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 58, 74))
    d.polygon([(x + w / 2, y + 6), (x + w / 2 + 6, y + 16),
               (x + w / 2 - 6, y + 16)], fill=(255, 190, 60))
    d.rectangle([x + w / 2 - 6, y + 18, x + w / 2 + 6, y + 38],
                fill=(240, 238, 228))
    d.rectangle([x + 8, y + 38, x + w - 8, y + 42], fill=(140, 130, 110))


def ic_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    d.rectangle([x + 8, y + 10, x + w - 8, y + 20], fill=(120, 80, 40))
    d.rectangle([x + w / 2 - 3, y + 20, x + w / 2 + 3, y + 40],
                fill=(150, 105, 55))
    d.rectangle([x + 10, y + 38, x + w - 10, y + 42], fill=(90, 60, 30))


def ic_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    d.polygon([(x + 4, y + 12), (x + w - 4, y + 12), (x + w / 2, y + 4)],
              fill=(120, 60, 50))
    for i in range(3):
        cx = x + 10 + i * 13
        d.rectangle([cx, y + 14, cx + 5, y + 38], fill=(200, 200, 195),
                    outline=(120, 120, 115))
    d.rectangle([x + 6, y + 38, x + w - 6, y + 42], fill=(120, 60, 50))


def ic_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 240))
    d.rectangle([x + 6, y + 20, x + w - 16, y + 40], fill=(110, 120, 135))
    d.rectangle([x + w - 14, y + 8, x + w - 8, y + 40], fill=(90, 95, 105))
    d.polygon([(x + 8, y + 38), (x + 16, y + 26), (x + 24, y + 38),
               (x + 32, y + 22), (x + 40, y + 38)], fill=NAVY)


# ---------------------------------------------------------------- content
HEROES = [
    dict(num=1, kicker="JIUQUAN · SPACE", source="REUTERS",
         head="Pakistan's first astronaut reaches orbit aboard Shenzhou-24",
         deck="Muhammad Zeeshan Ali lifts off — the first foreigner to visit "
              "China's Tiangong station.",
         ill=ic_rocket),
    dict(num=3, kicker="WASHINGTON · ECONOMY", source="BEA · REUTERS",
         head="US inflation and growth data due at 8:30 a.m. ET",
         deck="October PCE and the second Q3 GDP reading land today — the last "
              "big numbers before the Fed meets.",
         ill=ic_chart),
    dict(num=10, kicker="LONDON · ENERGY", source="REUTERS",
         head="Ofgem lifts energy cap 26% to £2,166 from January",
         deck="Households face bills £443 higher from January as the regulator "
              "sets the new cap.",
         ill=ic_house),
]

MEDIUM = [
    dict(num=4, kicker="WASHINGTON · TRADE",
         head="US set to unveil new global tariffs",
         deck="Tariff findings on 16 partners expected today.",
         ill=ic_ship),
    dict(num=5, kicker="SYDNEY · ECONOMY",
         head="Australia inflation hotter than expected",
         deck="Trimmed mean 3.8% in October; rate-cut bets fade.",
         ill=ic_coin),
    dict(num=6, kicker="KYIV · WAR",
         head="490,334 Russian soldiers dead, BBC finds",
         deck="Leaked records put the toll far above official counts.",
         ill=ic_candle),
    dict(num=7, kicker="LOS ANGELES · LAW",
         head="Thomas Markle indicted by grand jury",
         deck="Meghan's father charged; FBI arrested him.",
         ill=ic_gavel),
    dict(num=8, kicker="SYDNEY · JUSTICE",
         head="Lamarre guilty of double murder",
         deck="Jury convicts Beau Lamarre over the 2024 killings.",
         ill=ic_court),
    dict(num=9, kicker="BERLIN · ECONOMY",
         head="Germany's Q3 GDP grows 0.1%, cut from 0.2%",
         deck="Destatis: final reading revised down from 0.2%.",
         ill=ic_factory),
]

# Left column: #2 + #11-#29. Right column: #30-#49. One line each, 12px.
ALSO_LEFT = [
    (2, "IOWA", "9,500 lb of lead azide detonated in Iowa"),
    (11, "QUITO", "US pauses military operations with Ecuador"),
    (12, "GOLD", "Gold slips ahead of US inflation data"),
    (13, "OIL", "Oil falls as glut fears beat Middle East disruption"),
    (14, "SEOUL", "Asian stocks plunge; Korea down 5.3%"),
    (15, "MUMBAI", "Indian stocks open higher on Wednesday"),
    (16, "LONDON", "Bank of England's Bailey faces MPs today"),
    (17, "WASHINGTON", "Durable goods, home sales, jobless claims due"),
    (18, "NEW YORK", "Storms threaten Thanksgiving travel on both coasts"),
    (19, "WASHINGTON", "Nvidia export-compliance deadline ends today"),
    (20, "BEIJING", "China's Chen Jining probed in anti-graft inquiry"),
    (21, "WASHINGTON", "US attorney general dodges questions on Nvidia probe"),
    (22, "FORT HOOD", "Fort Hood gunman asks court to delay firing squad"),
    (23, "SANTA CLARA", "Nvidia board in spotlight after Huang returns as CEO"),
    (24, "WASHINGTON", "Pentagon hires conservative firm to audit base schools"),
    (25, "TENNESSEE", "Tennessee paper's new owner is a local: Al Gore"),
    (26, "GLOBAL", "Tech outages pile up as AI raises the stakes"),
    (27, "NEW YORK", "Polly Anderson, senior AP editor, dies"),
    (28, "WASHINGTON", "Trump pardons turkeys Freedom and Feathers"),
    (29, "WASHINGTON", "Melania Trump welcomes White House Christmas tree"),
]

ALSO_RIGHT = [
    (30, "SPACE", "Hera spacecraft returns to asteroid Didymos"),
    (31, "LONDON", "Citi UK chief risk officer resigns"),
    (32, "CARACAS", "Citi weighs return to Venezuela"),
    (33, "TOKYO", "Starbucks picks banks for Japan business sale"),
    (34, "KINSHASA", "DR Congo military plane missing; rebels claim shoot-down"),
    (35, "NIGERIA", "Nigerian king, 92, suspended after sexual abuse claims"),
    (36, "GAZA", "Israeli strike kills Hamas internal security chief in Gaza"),
    (37, "DAMASCUS", "Landmine victims surge in Syria two years after war"),
    (38, "TAIPEI", "China-linked network used fake AI to smear Taiwan candidates"),
    (39, "RABAT", "Senegal reinstated as 2025 Africa Cup champions by court"),
    (40, "LONDON", "Two arrested over burglary at William and Kate's home"),
    (41, "HONIARA", "Solomon Islands ends China security pact for Australia treaty"),
    (42, "WASHINGTON", "Court unseals records on Ilhan Omar home search"),
    (43, "JOHANNESBURG", "Zimbabwean jailed for trying to fight in Ukraine"),
    (44, "BRUSSELS", "NATO chief vows space defence after Russian satellite report"),
    (45, "NEW DELHI", "The high cost of eating in India"),
    (46, "YAOUNDÉ", "Shot in the face at 15: a life wrecked by Cameroon's conflict"),
    (47, "MADRID", "Clashing political visions mirror a divided Spain before vote"),
    (48, "PYONGYANG", "North Koreans: spied on, beaten, jailed for being Christian"),
    (49, "KYIV", "Ukraine defends Libya strikes; Zelenskyy confirms second hit"),
]

# num: (nx, ny) pin position in the map box; leader=(tx, ty) true location.
MAP_PINS = {
    1: ((0.82, 0.42), None),
    2: ((0.155, 0.38), None),
    3: ((0.215, 0.62), (0.235, 0.45)),
    4: ((0.275, 0.30), (0.235, 0.45)),
    5: ((0.935, 0.76), None),
    6: ((0.585, 0.26), None),
    7: ((0.095, 0.48), None),
    8: ((0.885, 0.55), (0.915, 0.70)),
    9: ((0.545, 0.18), None),
    10: ((0.465, 0.14), None),
    11: ((0.265, 0.70), None),
    12: ((0.45, 0.42), None),
    13: ((0.625, 0.50), None),
    14: ((0.855, 0.32), None),
    15: ((0.715, 0.52), None),
}

# Simplified strip-map continents (normalized to the map box).
CONTINENTS = [
    [(0.03, 0.30), (0.08, 0.10), (0.16, 0.05), (0.24, 0.10), (0.28, 0.22),
     (0.26, 0.38), (0.20, 0.50), (0.12, 0.48), (0.06, 0.38)],
    [(0.28, 0.04), (0.32, 0.03), (0.33, 0.10), (0.29, 0.12)],
    [(0.24, 0.52), (0.29, 0.48), (0.33, 0.56), (0.31, 0.72), (0.28, 0.88),
     (0.25, 0.74), (0.23, 0.60)],
    [(0.45, 0.10), (0.50, 0.05), (0.55, 0.10), (0.54, 0.20), (0.49, 0.22),
     (0.45, 0.17)],
    [(0.45, 0.28), (0.52, 0.24), (0.57, 0.30), (0.55, 0.48), (0.52, 0.66),
     (0.48, 0.64), (0.45, 0.46)],
    [(0.56, 0.08), (0.68, 0.04), (0.82, 0.06), (0.90, 0.14), (0.88, 0.28),
     (0.80, 0.36), (0.70, 0.30), (0.62, 0.26), (0.57, 0.16)],
    [(0.78, 0.42), (0.82, 0.40), (0.84, 0.46), (0.80, 0.48)],
    [(0.82, 0.64), (0.89, 0.60), (0.93, 0.66), (0.90, 0.76), (0.84, 0.74)],
]


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top strip
    d.text((12, 5), "THE WORLD ON ONE PAGE", font=sans_b(13), fill=INK)
    draw_centered(d, 5, "DAY 329 OF 2026", sans_b(13), RED)
    tail = "EVERY STORY DATED WED 25 NOV"
    d.text((1012 - d.textlength(tail, font=sans_b(13)), 5), tail,
           font=sans_b(13), fill=INK)
    hline(d, 24)

    # masthead 0-88
    draw_centered(d, 30, "THE DAILY GLOBE", serif_b(40), INK)
    draw_centered(d, 68, "WEDNESDAY 25 NOVEMBER 2026  ·  49 STORIES  ·  "
                  "ALL VERIFIED TODAY", sans_b(14), INK)
    hline(d, 88, width=3)

    # hero panels 96-376
    hy, hh, hw, gap = 96, 280, 326, 10
    for i, st in enumerate(HEROES):
        x = 12 + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CREAM, outline=BORDER,
                    width=1)
        st["ill"](d, x + 1, hy + 1, hw - 2, 140)
        d.rectangle([x, hy + 141, x + hw, hy + 163], fill=NAVY)
        d.text((x + 8, hy + 145), st["kicker"], font=sans_b(11),
               fill=(255, 255, 255))
        num = str(st["num"])
        nw = d.textlength(num, font=sans_b(13))
        d.text((x + hw - 8 - nw, hy + 144), num, font=sans_b(13), fill=GOLD)
        ty = hy + 170
        ty = draw_wrapped(d, wrap_text(d, st["head"], sans_b(15), hw - 16),
                          x + 8, ty, sans_b(15), INK, leading=17, max_lines=2)
        draw_wrapped(d, wrap_text(d, st["deck"], sans(11), hw - 16), x + 8,
                     ty + 4, sans(11), MUTED, leading=13, max_lines=2)
        d.text((x + 8, hy + hh - 14), st["source"], font=sans_b(9),
               fill=MUTED)
        tag = "REPORTED TODAY"
        d.text((x + hw - 8 - d.textlength(tag, font=sans_b(9)), hy + hh - 14),
               tag, font=sans_b(9), fill=RED)

    # medium panels 384-534: 2 rows x 3 cols, 326 x 71
    for i, st in enumerate(MEDIUM):
        col, row = i % 3, i // 3
        x = 12 + col * (hw + gap)
        y = 384 + row * (71 + 8)
        d.rectangle([x, y, x + hw, y + 71], fill=CREAM, outline=BORDER,
                    width=1)
        st["ill"](d, x + 6, y + 6, 44, 44)
        tx = x + 56
        d.text((tx, y + 5), st["kicker"], font=sans_b(9), fill=NAVY)
        num = str(st["num"])
        d.ellipse([x + hw - 24, y + 4, x + hw - 6, y + 22], fill=RED)
        nw = d.textlength(num, font=sans_b(11))
        d.text((x + hw - 15 - nw / 2, y + 6), num, font=sans_b(11),
               fill=(255, 255, 255))
        draw_wrapped(d, wrap_text(d, st["head"], sans_b(12), hw - 64),
                     tx, y + 19, sans_b(12), INK, leading=13, max_lines=2)
        deck = fit_one_line(d, st["deck"], sans(10), hw - 64)
        d.text((tx, y + 48), deck, font=sans(10), fill=MUTED)

    # map band 542-662
    d.text((12, 544), "WHERE IT HAPPENED", font=sans_b(15), fill=INK)
    mx, my, mw, mh = 12, 564, 1000, 98
    d.rectangle([mx, my, mx + mw, my + mh], fill=SKY, outline=BORDER, width=1)
    for poly in CONTINENTS:
        pts = [(mx + px * mw, my + py * mh) for px, py in poly]
        d.polygon(pts, fill=SAND, outline=(180, 165, 130))
    for num, (pos, leader) in sorted(MAP_PINS.items()):
        nx, ny = pos
        px, py = mx + nx * mw, my + ny * mh
        if leader is not None:
            tx, ty = mx + leader[0] * mw, my + leader[1] * mh
            d.line([(px, py), (tx, ty)], fill=RED, width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=sans_b(10))
        d.text((px - tw / 2, py - 7), t, font=sans_b(10),
               fill=(255, 255, 255))
    d.text((mx + 6, my + mh - 16), "pins = story numbers",
           font=serif_i(11), fill=MUTED)

    # ALSO list 670-992
    d.text((12, 670), "ALSO ON WEDNESDAY 25 NOV — 40 MORE STORIES",
           font=sans_b(14), fill=INK)
    hline(d, 688)
    colw = 484
    for col, items in enumerate((ALSO_LEFT, ALSO_RIGHT)):
        x = 12 + col * (colw + 16)
        for row, (num, tag, head) in enumerate(items):
            y = 692 + row * 15
            d.text((x, y), "#%d" % num, font=sans_b(12), fill=RED)
            line = fit_one_line(d, "%s — %s" % (tag, head), sans(12),
                                colw - 30)
            d.text((x + 30, y), line, font=sans(12), fill=INK)

    # footer 996-1024
    draw_centered(d, 997, "Every story here happened or was first reported on "
                  "Wednesday 25 November 2026, as the named outlets reported "
                  "it. Disputed claims are attributed to the outlet that "
                  "reported them.", sans(10), MUTED)
    d.text((12, 1011), "THE DAILY GLOBE", font=sans_b(10), fill=INK)
    src = "Sources: AP · Reuters · AFP · BBC · BEA · NYT · Destatis · ABS · BBC Verify"
    draw_centered(d, 1011, src, sans(10), MUTED)
    tail2 = "WEDNESDAY 25 NOVEMBER 2026 · 49 STORIES"
    d.text((1012 - d.textlength(tail2, font=sans_b(10)), 1011), tail2,
           font=sans_b(10), fill=INK)

    img.save(path, optimize=True)
    return path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print(out, os.path.getsize(out), "bytes")
