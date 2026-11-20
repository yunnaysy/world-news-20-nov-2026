from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

random.seed(20)
W = H = 1024
im = Image.new("RGB", (W, H), "#081522")
d = ImageDraw.Draw(im, "RGBA")

FONT_SERIF = "/usr/share/fonts/truetype/sand-box/google/Playfair Display/PlayfairDisplay-VariableFont_wght.ttf"
FONT_SANS = "/usr/share/fonts/truetype/sand-box/google/IBM Plex Sans/IBMPlexSans-VariableFont_wdth,wght.ttf"
FONT_COND = "/usr/share/fonts/truetype/sand-box/google/Barlow Condensed/BarlowCondensed-Bold.ttf"
FONT_REG = FONT_SANS


def font(path, size):
    return ImageFont.truetype(path, size)


def text(x, y, value, size, fill="#f3f5f2", face=FONT_SANS, **kwargs):
    d.text((x, y), value, font=font(face, size), fill=fill, **kwargs)


def line(points, fill, width=1):
    d.line(points, fill=fill, width=width, joint="curve")


def panel(box, fill="#0d1d2b", outline="#284050", radius=6):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=1)


def paint_translucent(draw_scene, blur=0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_scene(ImageDraw.Draw(layer, "RGBA"))
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB"))


def blend_left_fade(y0, y1, end_x, color):
    pixels = im.load()
    for x in range(end_x):
        alpha = int(216 * max(0, 1 - x / (end_x * 1.08)) ** 1.65)
        if not alpha:
            continue
        for y in range(y0, y1):
            old = pixels[x, y]
            pixels[x, y] = tuple((color[i] * alpha + old[i] * (255 - alpha)) // 255
                                 for i in range(3))


# Masthead: restrained, cool white against the night desk.
d.rectangle((0, 0, W, 154), fill="#091622")
d.rectangle((24, 21, 33, 48), fill="#ef7455")
text(46, 20, "FIELDNOTES", 22, "#f5f6f2", FONT_COND)
text(176, 26, "WORLD / DAILY EDITION", 12, "#91a5b1", FONT_SANS)
text(793, 26, "FRIDAY  ·  20 NOVEMBER 2026", 14, "#dce6e8", FONT_SANS)
line([(24, 57), (1000, 57)], "#344956", 1)
text(24, 66, "FRIDAY,", 38, "#f3f5f2", FONT_SERIF)
text(24, 105, "20 NOVEMBER 2026", 43, "#f3f5f2", FONT_SERIF)
text(749, 114, "THE DAY IN FOCUS", 15, "#e1e9e9", FONT_SANS)

# Hero landscape — a painted monsoon coast with a broad storm eye and shelter lights.
hy, hh = 162, 326
for y in range(hy, hy + hh):
    t = (y - hy) / hh
    c1 = (17, 47, 66)
    c2 = (5, 24, 36)
    c = tuple(round(a * (1 - t) + b * t) for a, b in zip(c1, c2))
    d.line((0, y, W, y), fill=c)

# An irregular, low-contrast cyclone mass: broken cloud lobes rather than graphic rings.
def draw_clouds(layer):
    lobes = [
        (681, 222, 164, 52, 48), (762, 254, 121, 57, 55),
        (850, 213, 125, 43, 42), (901, 282, 106, 49, 39),
        (778, 331, 175, 36, 34), (626, 282, 94, 40, 31),
        (934, 346, 88, 31, 25), (713, 197, 81, 26, 22),
        (842, 301, 79, 29, 22),
    ]
    for i, (x, y, rx, ry, alpha) in enumerate(lobes):
        x += random.randint(-27, 24)
        y += random.randint(-15, 18)
        layer.ellipse((x-rx, y-ry, x+rx, y+ry),
                      fill=(91, 128, 145, alpha + (i % 3) * 5))
    for i in range(34):
        x = random.randint(625, 948)
        y = random.randint(199, 354)
        rx = random.randint(12, 72)
        ry = random.randint(7, 24)
        layer.ellipse((x-rx, y-ry, x+rx, y+ry),
                      fill=random.choice([(97,137,150,15),(49,91,108,25),(24,63,80,34)]))
    for points, width, shade in [
        ([(644,267),(665,243),(693,229),(721,225),(745,233),(763,250),(775,270)], 19, (35,75,91,91)),
        ([(787,324),(813,332),(837,327),(855,311)], 13, (48,87,101,74)),
    ]:
        layer.line(points, fill=shade, width=width, joint="curve")
paint_translucent(draw_clouds, blur=4)
cx, cy = 787, 281
d.ellipse((cx-22, cy-13, cx+22, cy+13), fill="#102c3b")
d.ellipse((cx-8, cy-5, cx+8, cy+5), fill="#506d77")

# Rain veils.
def draw_rain(layer):
    for i in range(170):
        x = random.randint(0, W)
        y = random.randint(hy+20, hy+300)
        layer.line([(x, y), (x-9, y+22)],
                   fill=(179, 209, 211, random.randint(25, 82)), width=1)
paint_translucent(draw_rain)

# Sea bands, foam, and wave crests.
d.polygon([(0, 408), (180, 388), (370, 419), (555, 396), (735, 419), (1024, 388),
           (1024, 488), (0, 488)], fill="#092b3c")
for row in range(7):
    y = 418 + row * 9
    for j in range(4):
        x = j * 260 + (row % 2) * 36 + random.randint(-14, 14)
        length = random.randint(24, 74)
        line([(x, y), (x+length, y-random.randint(0, 4))],
             (113, 174, 181, random.randint(28, 104)), random.choice([1, 1, 2]))

# Ganjam shore, rain-dark palms and a low-lit shelter.
d.polygon([(465, 488), (510, 476), (544, 465), (562, 452), (613, 454),
           (680, 445), (758, 458), (837, 444), (918, 451), (1024, 438), (1024, 488)],
          fill="#182f31")
d.polygon([(506, 485), (554, 474), (587, 466), (651, 466), (712, 462),
           (781, 471), (855, 461), (942, 466), (1024, 462), (1024, 488), (477, 488)],
          fill="#26372e")
for x in [600, 674, 913, 976]:
    # Leaning trunks and wind-flattened palm fronds.
    line([(x, 472), (x+14, 324)], "#182526", 7)
    for k in range(7):
        start = (x+14, 328 + k*2)
        end = (x + 14 + (k-3)*34, 312 + abs(k-3)*9)
        line([start, end], "#172526", 4)
        line([end, (end[0]+22, end[1]+4)], "#243630", 2)
# Shelter silhouette, with a warm but subtle lamp inside.
d.polygon([(818, 442), (890, 417), (960, 442), (960, 475), (818, 475)], fill="#101d22")
d.polygon([(810, 442), (890, 408), (968, 442)], fill="#0b171c")
d.rectangle((854, 445, 869, 473), fill="#d79a5a")
d.rectangle((896, 447, 911, 461), fill="#dfb678")
for x in range(811, 1000, 23):
    line([(x, 480), (x+33, 477)], (214, 198, 155, 80), 1)

# Smooth dark fade under the headline keeps the illustration visible and the type crisp.
blend_left_fade(hy, hy+hh, 630, (5, 18, 28))
d.rectangle((24, 182, 183, 207), fill="#e47759")
text(34, 184, "ODISHA  /  LANDFALL", 13, "#111e25", FONT_SANS)
text(24, 229, "AKVAN HITS", 41, "#f5f5ee", FONT_COND)
text(24, 270, "THE COAST", 41, "#f5f5ee", FONT_COND)
text(25, 321, "Gopalpur • Bay of Bengal", 19, "#d2e0e1", FONT_REG)
line([(25, 355), (380, 355)], "#a3bbc0", 1)
text(25, 369, "70–80 km/h", 23, "#ffffff", FONT_SANS)
text(195, 375, "gusts to 90 km/h", 17, "#d3dfe1", FONT_REG)
text(25, 407, "372,000 moved to 10,000 shelters", 17, "#dce8e7", FONT_SANS)
text(25, 467, "IMD: landfall 7:30–8:30 a.m. IST  •  Patrapur rain: 209 mm", 14, "#c8d7d9", FONT_REG)

# Expanded, squared editorial lead panels for Kyiv and the Asian close.
panel((20, 498, 504, 752), "#0b1725")
panel((520, 498, 1004, 752), "#111722")

# Kyiv: river, damaged bridge, skyline, fire glow and emergency lamps.
for y in range(506, 744):
    t=(y-506)/238
    col=(14, 29, 49)
    d.line((28,y,496,y), fill=tuple(int(c*(1-t*.27)) for c in col))
d.ellipse((330, 540, 494, 704), fill=(217, 91, 56, 27))
for bx, bw, top in [(316,34,558),(352,42,536),(398,34,570),(434,43,550),(478,22,580)]:
    d.rectangle((bx, top, bx+bw, 667), fill="#16293a")
    for wx in range(bx+7, bx+bw-4, 13):
        for wy in range(top+14, 657, 18):
            if random.random() > .53:
                d.rectangle((wx,wy,wx+4,wy+7), fill=(226,156,98,random.randint(70,170)))
d.rectangle((28, 666, 496, 739), fill="#071c2a")
for _ in range(33):
    x=random.randint(302,490); y=random.randint(672,734)
    line([(x,y),(x+random.randint(5,29),y)],(111,157,166,random.randint(20,75)),1)
line([(310, 628), (490, 651)], "#687987", 8)
line([(310, 622), (490, 645)], "#aab5b6", 2)
for bx in [350, 420, 477]:
    line([(bx, 633), (bx-6, 704)], "#526473", 8)
    line([(bx-17, 706), (bx+8, 706)], "#526473", 4)
line([(395, 638), (381, 647), (393, 656), (379, 665)], "#f17b52", 4)
d.ellipse((445, 645, 457, 657), fill="#fa815a")
d.ellipse((442, 642, 460, 660), outline=(249,128,89,130), width=2)
blend_left_fade(506, 744, 345, (5, 15, 26))
text(36, 507, "UKRAINE  /  OVERNIGHT", 13, "#ff9a76", FONT_SANS)
text(36, 529, "KYIV UNDER FIRE", 32, "#f1f3f1", FONT_COND)
text(36, 571, "3 bridges damaged", 19, "#e1e9e9", FONT_SANS)
text(36, 605, "At least 3 utility workers killed", 18, "#c9d7dc", FONT_REG)
text(36, 638, "≈15 civilians injured", 19, "#c9d7dc", FONT_REG)
text(36, 711, "Power, heat & water disrupted", 19, "#d3e0e1", FONT_REG)

# Asia's Friday close: restrained three-line grid, chart, and prominent index moves.
for y in range(506, 744):
    t=(y-506)/238
    d.line((528,y,996,y), fill=(20-int(7*t),24-int(5*t),34-int(6*t)))
for y in (578, 608, 638):
    line([(824,y),(989,y)], "#263642", 1)
for x in (824, 879, 934, 989):
    line([(x,570),(x,643)], "#202e39", 1)
points=[(827,575),(846,581),(865,574),(884,591),(903,586),(921,610),(941,602),(960,631),(982,637)]
line(points, "#6f9aa0", 3)
for x,y in points:
    d.ellipse((x-2,y-2,x+2,y+2),fill="#c9d9d5")
text(540, 507, "ASIA  /  AP FRIDAY CLOSE", 13, "#ff8978", FONT_SANS)
text(540, 529, "CHIP & AI SELLOFF", 32, "#f4f4ef", FONT_COND)
text(540, 574, "NIKKEI 225", 19, "#d4dde1", FONT_SANS)
text(690, 564, "−5.1%", 36, "#ff8171", FONT_SANS)
text(540, 612, "KOSPI", 19, "#d4dde1", FONT_SANS)
text(690, 602, "−5.2%", 36, "#ff8171", FONT_SANS)
text(540, 651, "Nikkei 56,436.65  •  Kospi 4,869.12", 18, "#dce4e4", FONT_REG)
text(540, 682, "Hang Seng −2.2%  •  ASX −1.6%", 19, "#b8c8ce", FONT_REG)
text(540, 713, "Shanghai −1.3%  •  AI shares slide", 19, "#c5d2d7", FONT_REG)

# COP31: muted teal diplomacy band with a single uncompleted agreement document.
panel((20, 760, 1004, 842), "#10222d", "#34515c", 5)
d.rectangle((20, 760, 27, 842), fill="#71aaa5")
text(42, 765, "ANTALYA  /  COP31 • SCHEDULED FINAL DAY", 13, "#a9d8d0", FONT_SANS)
text(42, 784, "NO DEAL YET", 28, "#f3f5f0", FONT_COND)
text(226, 791, "Fossil fuels absent from Thursday's draft; talks may run long.", 19, "#d3e0df", FONT_REG)
d.polygon([(887, 770), (960, 770), (978, 788), (978, 827), (887, 827)],
          fill="#193946", outline="#6c9e9f")
line([(960,770),(960,788),(978,788)], "#6c9e9f", 2)
for y, width in [(797,61),(807,72),(817,45)]:
    line([(899,y),(899+width,y)], "#80aaa6", 2)
line([(900,823),(915,823),(923,814),(935,819)], "#d6dfd7", 2)

# Four supporting briefs share one open, 106px ticker with thin dividing rules.
d.rectangle((20, 852, 1004, 958), fill="#0b1a26")
line([(20,852),(1004,852)],"#36505a",1)
text(36, 861, "TOKYO", 13, "#91c5cf", FONT_SANS)
text(36, 883, "Core CPI 2.2%", 20, "#f0f3ef", FONT_COND)
text(36, 921, "Market expects Dec. BoJ hike", 14, "#bac9cf", FONT_REG)
line([(260,861),(260,947)],"#2e4550",1)
text(280, 861, "BEIJING", 13, "#91c5cf", FONT_SANS)
text(280, 883, "LPR held for 18th month", 20, "#f0f3ef", FONT_COND)
text(280, 921, "1-year 3.0%  /  5-year 3.5%", 14, "#bac9cf", FONT_REG)
line([(512,861),(512,947)],"#2e4550",1)
text(532, 861, "WELLINGTON", 13, "#91c5cf", FONT_SANS)
text(532, 883, "Phillips makes 118", 20, "#f0f3ef", FONT_COND)
text(532, 921, "First India treble in one year", 14, "#bac9cf", FONT_REG)
line([(754,861),(754,947)],"#2e4550",1)
text(773, 861, "GTA VI  /  SENSOR TOWER EST.", 12, "#91c5cf", FONT_SANS)
text(773, 883, ">24.5m sales  •  $2.36bn", 19, "#f0f3ef", FONT_COND)
text(773, 921, "Thursday launch; unofficial", 14, "#bac9cf", FONT_REG)

# Cool date-check footer, spaced clear of the ticker.
d.rectangle((0, 966, W, H), fill="#e3e9e7")
text(24, 971, "DATE CHECK", 16, "#142b35", FONT_SANS)
text(140, 971, "NOT TODAY: APEC close • Anthropic IPO • ICJ ruling • GTA VI launch • Kerch strike.", 15, "#263e48", FONT_REG)
text(24, 989, "Thu: Bukele registered; Iran remarks. Kerch strike earlier this week; BepiColombo due Saturday.", 14, "#263e48", FONT_REG)
text(24, 1007, "Sources: The Hindu / IMD · Kyiv Independent · AP · CNA · Reuters · AA · ICC · BBC", 12, "#43575f", FONT_REG)

im.save("entry.png", format="PNG", optimize=True)
