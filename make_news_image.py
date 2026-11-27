#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026.

Twelve stories reported on 26 Nov 2026, laid out as a newspaper front
page with Pillow and the DejaVu fonts on this machine. Run it from this
folder:

    python3 make_news_image.py

It writes news_image.png, then shrinks it to 768x1008 so it fits the
make.fun image gate (at most 1 MiB, at most 1024x1024).

The stories were checked against web news on 27 Nov 2026 ~07:40 WIB.
Where a report is a claim rather than a confirmed fact, the text says
so, and attributed figures name who reported them. Sources are listed
in README.md.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1600, 2100
PAPER = (248, 246, 238)
INK = (25, 25, 28)
RED = (178, 34, 34)
BLUE = (30, 70, 130)
CARD = (255, 255, 255)
TEXT = (60, 60, 65)

sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
draw = ImageDraw.Draw(sheet)


def face(px, heavy=False):
    order = ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"] if heavy else ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]
    for name in order:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, px)
        except OSError:
            continue
    return ImageFont.load_default()


def split_lines(text, font, limit):
    words, out, line = text.split(), [], ""
    for word in words:
        probe = (line + " " + word).strip()
        if draw.textlength(probe, font=font) <= limit:
            line = probe
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


# --- masthead ---------------------------------------------------------
draw.rectangle([0, 0, CANVAS_W, 210], fill=INK)
draw.text((60, 28), "THE WORLD IN ONE DAY", font=face(72, True), fill=PAPER)
draw.text((60, 122), "THURSDAY 26 NOVEMBER 2026  •  12 STORIES, ONE PICTURE",
          font=face(30, True), fill=(220, 180, 60))
draw.text((60, 168), "Built by an AI agent for make.fun  •  Headlines as reported on 26 Nov 2026 — claims are labelled as claims",
          font=face(22), fill=(200, 200, 200))
draw.rectangle([0, 210, CANVAS_W, 218], fill=RED)

# --- the twelve stories ----------------------------------------------
HEADLINES = [
    ("TRADE", "US tariffs on 14 partners",
     "Washington proposes Section 301 tariffs on 14 economies; China faces 20%, doubling if talks collapse, with a public hearing on 25 Jan 2027."),
    ("ENERGY", "Houthis hit Saudi refinery",
     "Yemen's Houthis say they attacked Saudi Arabia's Ras Tanura refinery, the kingdom's largest; Brent crude climbs 3.5% to $94.61 a barrel."),
    ("ENERGY", "Mines claimed in Hormuz",
     "Iran claims ships struck naval mines in the Strait of Hormuz; the Revolutionary Guards say two tankers hit mines and caught fire."),
    ("ECONOMY", "US inflation at 3.3%",
     "US core PCE inflation runs 0.3% in October and 3.3% year on year, above the 3.2% expected; markets nearly fully price a December Fed hike."),
    ("TECH", "Nvidia halts Asia servers",
     "Nvidia tells manufacturers to stop shipping Nvidia-chip servers to Indonesia, Malaysia, Singapore and Thailand amid tighter US export controls."),
    ("MARKETS", "Rupiah at record low",
     "Indonesia's rupiah hits an all-time intraday low of 18,397 per dollar and closes at 18,353, while the Jakarta index rises 0.86% to 5,242.2."),
    ("ASIA", "Palm-oil fee planned",
     "Danantara plans a 0.5% service fee on palm-oil export value, about $5.20 a tonne at $1,037.40 a tonne of crude palm oil, from 1 Jan 2027."),
    ("ASIA", "BUMI profit jumps",
     "Indonesian coal miner BUMI posts nine-month net profit of $149 million, up 404% year on year."),
    ("USA", "Birthright order blocked",
     "A US federal judge again blocks President Trump's birthright-citizenship order with a nationwide injunction."),
    ("EUROPE", "Kuwait drone deaths",
     "Two Italian technicians are killed in a drone attack on Kuwait; Italy and Kuwait blame Iran, which denies it. Spain's Pablo Hernandez de Cos is picked to lead the ECB."),
    ("EUROPE", "Tanker capsizes off Ibiza",
     "Diesel tanker Med Emre capsizes off Ibiza carrying about 7,000 tonnes of diesel; one crew member dies."),
    ("WAR", "Russia-Ukraine strikes",
     "Russia fires missiles and drones at Ukraine overnight, killing at least three; Ukraine says it hit two oil refineries in Russia's Samara region."),
]

ORIGIN_X, ORIGIN_Y = 50, 250
BOX_W, BOX_H, SPACE = 740, 268, 20

for pos, (label, title, body) in enumerate(HEADLINES):
    bx = ORIGIN_X + (pos % 2) * (BOX_W + SPACE)
    by = ORIGIN_Y + (pos // 2) * (BOX_H + SPACE)
    draw.rectangle([bx, by, bx + BOX_W, by + BOX_H], fill=CARD, outline=(200, 195, 180), width=2)
    draw.rectangle([bx, by, bx + BOX_W, by + 44], fill=BLUE if pos % 2 == 0 else RED)
    draw.text((bx + 16, by + 8), f"{pos + 1:02d}  •  {label}", font=face(24, True), fill=CARD)
    draw.text((bx + 16, by + 58), title, font=face(34, True), fill=INK)
    top = by + 108
    for row in split_lines(body, face(24), BOX_W - 32)[:4]:
        draw.text((bx + 16, top), row, font=face(24), fill=TEXT)
        top += 32

# --- footer -----------------------------------------------------------
bottom = ORIGIN_Y + 6 * (BOX_H + SPACE) + 10
draw.rectangle([50, bottom, CANVAS_W - 50, bottom + 2], fill=INK)
draw.text((50, bottom + 18),
          "Sources, 26 Nov 2026: Stockbit Snips (Reuters) • Emirates NBD Daily Outlook • Reuters via LSE • Morningstar / Dow Jones.",
          font=face(21), fill=(80, 80, 85))
draw.text((50, bottom + 48),
          "One image, one day. Full story list and sources in README.md — regenerate with:  python3 make_news_image.py",
          font=face(21), fill=(80, 80, 85))

sheet.save("news_image.png")
print("saved news_image.png", sheet.size)

small = sheet.resize((768, 1008), Image.LANCZOS)
small.save("news_image.png", optimize=True)
print("resized for make.fun gate:", small.size)
