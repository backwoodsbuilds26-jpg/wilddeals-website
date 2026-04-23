"""Generate wild-deals-banner-email.png — 1200x400 red-themed header
banner for all outbound WildDeals emails (newsletters + transactional).

Drop-in replacement for the existing green banner — same filename, same
dimensions, so no template edits required beyond pointing refs at the
new file (if the filename changes) or just overwriting it in place.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, "..", "images"))

W, H = 1200, 400
BG = (10, 10, 10)
RED = (220, 27, 27)
WHITE = (255, 255, 255)
CREAM = (246, 244, 238)
MUTED = (190, 190, 190)


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("No font found")


# Dark canvas with subtle red radial glow behind the logo
canvas = Image.new("RGB", (W, H), BG)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy = 220, H // 2
for r in range(360, 0, -8):
    alpha = int(40 * (1 - r / 360) ** 2)
    gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*RED, alpha))
glow = glow.filter(ImageFilter.GaussianBlur(60))
canvas.paste(glow, (0, 0), glow)

# Place WDicon on left, 320px tall, vertically centered
icon = Image.open(os.path.join(IMG, "WDicon.png")).convert("RGBA")
ICON = 320
icon = icon.resize((ICON, ICON), Image.LANCZOS)
icon_x, icon_y = 50, (H - ICON) // 2
canvas.paste(icon, (icon_x, icon_y), icon)

# Text column on right
draw = ImageDraw.Draw(canvas)
title = load_font(
    ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 88
)
tagline = load_font(
    ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"], 30
)

tx = icon_x + ICON + 50
draw.text((tx, 90), "WildDeals", font=title, fill=WHITE)
# Red divider
draw.rectangle((tx, 200, tx + 320, 203), fill=RED)
draw.text((tx, 220), "40,000+ deals daily", font=tagline, fill=CREAM)
draw.text((tx, 262), "Hours before other forums", font=tagline, fill=MUTED)

out = os.path.join(IMG, "wild-deals-banner-email-preview.png")
canvas.save(out, "PNG", optimize=True)
print(f"wrote preview: {out}  ({W}x{H})")
