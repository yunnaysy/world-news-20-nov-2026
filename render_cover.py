from PIL import Image, ImageDraw, ImageFont
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


def panel(box, fill="#0d1d2b", outline="#284050", radius=14):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=1)


def paint_translucent(draw_scene):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_scene(ImageDraw.Draw(layer, "RGBA"))
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
text(749, 116, "THE DAY IN FOCUS", 13, "#9fb4bd", FONT_SANS)

# Hero landscape — a painted monsoon coast with a broad storm eye and shelter lights.
hy, hh = 162, 366
for y in range(hy, hy + hh):
    t = (y - hy) / hh
    c1 = (17, 47, 66)
    c2 = (5, 24, 36)
    c = tuple(round(a * (1 - t) + b * t) for a, b in zip(c1, c2))
    d.line((0, y, W, y), fill=c)

# Layered cloud banks and a visible, spiral-shaped storm structure.
def draw_clouds(layer):
    for i in range(22):
        x0 = random.randint(150, 810)
        y0 = random.randint(190, 310)
        length = random.randint(150, 360)
        phase = random.random() * math.tau
        amplitude = random.randint(7, 18)
        pts = [(x0+j, y0 + math.sin(j/53 + phase)*amplitude)
               for j in range(0, length, 8)]
        shade = random.choice([(126,161,171,29),(74,120,139,37),(37,84,105,42)])
        layer.line(pts, fill=shade, width=random.randint(12, 31), joint="curve")
    for i in range(9):
        x0 = 470 + i * 45
        y0 = 255 + (i % 4) * 17
        pts = [(x0+j, y0 + math.sin(j/62+i*.41)*18)
               for j in range(0, 265, 8)]
        layer.line(pts, fill=(5,25,38,95), width=23, joint="curve")
paint_translucent(draw_clouds)
cx, cy = 764, 302
for phase, color, width in [(0, "#82abb2", 7), (1.7, "#d0d5c7", 5), (3.2, "#5e929f", 4)]:
    spiral = []
    for step in range(230):
        t = step / 229
        angle = -2.3 + t * math.tau * 1.72 + phase
        radius = 27 + t * 155
        spiral.append((cx + math.cos(angle)*radius,
                       cy + math.sin(angle)*radius*.56))
    line(spiral, color, width)
d.ellipse((cx-43, cy-25, cx+43, cy+25), fill=(9, 30, 43, 210))
d.ellipse((cx-18, cy-10, cx+18, cy+10), fill=(151, 185, 185, 125))

# Rain veils.
def draw_rain(layer):
    for i in range(250):
        x = random.randint(0, W)
        y = random.randint(hy+20, hy+300)
        layer.line([(x, y), (x-9, y+22)],
                   fill=(179, 209, 211, random.randint(25, 82)), width=1)
paint_translucent(draw_rain)

# Sea bands, foam, and wave crests.
d.polygon([(0, 408), (180, 388), (370, 419), (555, 396), (735, 419), (1024, 388),
           (1024, 528), (0, 528)], fill="#092b3c")
for row in range(18):
    y = 418 + row * 7
    for j in range(9):
        x = j * 132 + (row % 2) * 42 + random.randint(-14, 14)
        length = random.randint(24, 74)
        line([(x, y), (x+length, y-random.randint(0, 4))],
             (113, 174, 181, random.randint(28, 104)), random.choice([1, 1, 2]))

# Ganjam shore, rain-dark palms and a low-lit shelter.
d.polygon([(465, 528), (510, 496), (544, 475), (562, 452), (613, 454),
           (680, 445), (758, 458), (837, 444), (918, 451), (1024, 438), (1024, 528)],
          fill="#182f31")
d.polygon([(506, 509), (554, 481), (587, 466), (651, 466), (712, 462),
           (781, 471), (855, 461), (942, 466), (1024, 462), (1024, 528), (477, 528)],
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
    line([(x, 487), (x+33, 484)], (214, 198, 155, 80), 1)

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
text(25, 489, "IMD: landfall 7:30–8:30 a.m. IST  •  Patrapur rain: 209 mm", 14, "#c8d7d9", FONT_REG)

# Two independent, cinematic lead panels.
panel((20, 540, 504, 768), "#0b1725")
panel((520, 540, 1004, 768), "#111722")

# Kyiv: river, damaged bridge, skyline, fire glow and emergency lamps.
for y in range(548, 760):
    t=(y-548)/212
    col=(14, 29, 49)
    d.line((28,y,496,y), fill=tuple(int(c*(1-t*.27)) for c in col))
d.ellipse((300, 584, 494, 727), fill=(217, 91, 56, 30))
# distant building silhouettes
for bx, bw, top in [(285,38,601),(326,48,578),(377,35,612),(417,52,593),(463,28,622)]:
    d.rectangle((bx, top, bx+bw, 704), fill="#16293a")
    for wx in range(bx+7, bx+bw-4, 13):
        for wy in range(top+14, 690, 18):
            if random.random() > .53:
                d.rectangle((wx,wy,wx+4,wy+7), fill=(226,156,98,random.randint(70,170)))
# River reflections
d.rectangle((28, 703, 496, 755), fill="#071c2a")
for _ in range(45):
    x=random.randint(265,490); y=random.randint(710,752)
    line([(x,y),(x+random.randint(5,32),y)],(111,157,166,random.randint(20,90)),1)
# Bridge deck and battered piers
line([(272, 660), (490, 687)], "#687987", 8)
line([(272, 654), (490, 681)], "#aab5b6", 2)
for bx in [316, 405, 470]:
    line([(bx, 665), (bx-6, 723)], "#526473", 8)
    line([(bx-17, 725), (bx+8, 725)], "#526473", 4)
line([(375, 671), (361, 680), (373, 690), (358, 699)], "#f17b52", 4)
# low emergency light
d.ellipse((429, 678, 441, 690), fill="#fa815a")
d.ellipse((426, 675, 444, 693), outline=(249,128,89,130), width=2)
# left-side fade behind copy
blend_left_fade(548, 756, 315, (5, 15, 26))
text(36, 557, "UKRAINE  /  OVERNIGHT", 12, "#ff9a76", FONT_SANS)
text(36, 579, "KYIV UNDER FIRE", 28, "#f1f3f1", FONT_COND)
text(36, 617, "3 bridges damaged", 18, "#e1e9e9", FONT_SANS)
text(36, 642, "At least 3 utility workers killed", 14, "#c9d7dc", FONT_REG)
text(36, 666, "≈15 civilians injured", 15, "#c9d7dc", FONT_REG)
text(36, 735, "Power, heat & water disrupted", 13, "#b7c8ce", FONT_REG)

# Asian markets: a physical-looking quote wall and a sharply falling index trace.
for y in range(548, 760):
    t=(y-548)/212
    d.line((528,y,996,y), fill=(20-int(7*t),24-int(5*t),34-int(6*t)))
for x in range(818, 988, 34):
    line([(x, 618), (x, 744)], (103,115,128,40), 1)
for y in range(620, 744, 24):
    line([(808,y),(988,y)],(103,115,128,40),1)
points=[(817,625),(838,634),(859,628),(880,650),(900,644),(919,674),(939,668),(958,704),(980,715)]
line(points, "#ef655b", 4)
for x,y in points:
    d.ellipse((x-3,y-3,x+3,y+3),fill="#ffd2b4")
# dark tint keeps the chart legible behind labels.
d.rectangle((528,548,996,768), fill=(3,11,20,78))
text(540, 557, "ASIA  /  AP FRIDAY CLOSE", 12, "#ff8978", FONT_SANS)
text(540, 579, "CHIP & AI SELLOFF", 26, "#f4f4ef", FONT_COND)
text(540, 617, "NIKKEI 225", 14, "#d4dde1", FONT_SANS)
text(692, 611, "−5.1%", 24, "#ff8171", FONT_SANS)
text(540, 644, "KOSPI", 14, "#d4dde1", FONT_SANS)
text(692, 638, "−5.2%", 24, "#ff8171", FONT_SANS)
text(540, 678, "Nikkei 56,436.65  •  Kospi 4,869.12", 12, "#dce4e4", FONT_SANS)
text(540, 701, "Hang Seng −2.2%  •  ASX −1.6%", 12, "#b8c8ce", FONT_REG)
text(540, 735, "Shanghai −1.3%  •  AI shares slide", 12, "#c5d2d7", FONT_REG)

# COP31 gets a clear, factual supporting headline and a visual negotiation-room cue.
panel((20, 780, 1004, 868), "#10222d", "#34515c", 12)
d.rectangle((20, 780, 27, 868), fill="#71aaa5")
text(42, 789, "ANTALYA  /  COP31 • SCHEDULED FINAL DAY", 12, "#a9d8d0", FONT_SANS)
text(42, 808, "NO DEAL YET", 25, "#f3f5f0", FONT_COND)
text(210, 814, "Fossil fuels absent from Thursday's draft; talks may run long.", 16, "#d3e0df", FONT_REG)
# Simple lit summit-room silhouette, not a generic climate icon.
d.rectangle((833, 840, 987, 868), fill="#183644")
for i in range(5):
    x=844+i*29
    d.ellipse((x, 823, x+16, 841), fill="#b9c9b9")
    d.rectangle((x+3, 840, x+13, 858), fill="#426775")
d.rectangle((823, 858, 994, 863), fill="#d7a866")

# Compact but legible briefs: one line each, with estimates and expectations attributed.
panel((20, 872, 1004, 946), "#0b1a26", "#253b47", 10)
text(36, 879, "TOKYO", 12, "#91c5cf", FONT_SANS)
text(36, 897, "Core CPI 2.2%", 19, "#f0f3ef", FONT_COND)
text(36, 923, "Market expects Dec. BoJ hike", 11, "#bac9cf", FONT_REG)
line([(260,879),(260,938)],"#2e4550",1)
text(280, 879, "BEIJING", 12, "#91c5cf", FONT_SANS)
text(280, 897, "LPR held for 18th month", 17, "#f0f3ef", FONT_COND)
text(280, 923, "1-year 3.0%  /  5-year 3.5%", 11, "#bac9cf", FONT_REG)
line([(512,879),(512,938)],"#2e4550",1)
text(532, 879, "WELLINGTON", 12, "#91c5cf", FONT_SANS)
text(532, 897, "Phillips makes 118", 18, "#f0f3ef", FONT_COND)
text(532, 923, "First India treble in one year", 11, "#bac9cf", FONT_REG)
line([(754,879),(754,938)],"#2e4550",1)
text(773, 879, "GTA VI  /  SENSOR TOWER EST.", 11, "#91c5cf", FONT_SANS)
text(773, 897, ">24.5m sales  •  $2.36bn", 15, "#f0f3ef", FONT_COND)
text(773, 923, "Thursday launch; unofficial", 11, "#bac9cf", FONT_REG)

# A readable date-check footer separates Thursday context from today's leads.
d.rectangle((0, 952, W, H), fill="#e3e9e7")
text(24, 958, "DATE CHECK", 16, "#142b35", FONT_SANS)
text(140, 958, "NOT TODAY: APEC close • Anthropic IPO • ICJ ruling • GTA VI launch • Kerch strike.", 15, "#263e48", FONT_REG)
text(24, 981, "Thu: Bukele registered; Iran remarks. Kerch strike earlier this week; BepiColombo due Saturday.", 15, "#263e48", FONT_REG)
text(24, 1008, "Sources: The Hindu / IMD · Kyiv Independent · AP · CNA · Reuters · AA · ICC · BBC", 10, "#43575f", FONT_REG)

im.save("entry.png", format="PNG", optimize=True)
