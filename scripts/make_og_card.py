"""Generate og-card.png — 1200x630 social share image for wilddeals.ca.

Layout: WDicon on the left, headline + trust strip on the right,
dark background with a subtle red radial glow.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.normpath(os.path.join(HERE, "..", "images"))

W, H = 1200, 630
BG = (10, 10, 10)
RED = (220, 27, 27)
WHITE = (255, 255, 255)
MUTED = (170, 170, 170)
CREAM = (246, 244, 238)


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit(f"No font found in: {candidates}")


# Background with soft red radial glow on the left (behind the icon)
canvas = Image.new("RGB", (W, H), BG)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy = 320, H // 2
for r in range(520, 0, -10):
    alpha = int(38 * (1 - r / 520) ** 2)
    gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(RED[0], RED[1], RED[2], alpha))
glow = glow.filter(ImageFilter.GaussianBlur(70))
canvas.paste(glow, (0, 0), glow)

# Subtle top-right cool shadow to add depth
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shade)
for r in range(480, 0, -10):
    alpha = int(28 * (1 - r / 480))
    sd.ellipse((W - 100 - r, -200 - r, W - 100 + r, -200 + r), fill=(0, 0, 0, alpha))
shade = shade.filter(ImageFilter.GaussianBlur(90))
canvas.paste(shade, (0, 0), shade)

# Paste WDicon on the left, 460px tall, centered vertically
icon = Image.open(os.path.join(IMG_DIR, "WDicon.png")).convert("RGBA")
ICON_SIZE = 460
icon = icon.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
icon_x = 70
icon_y = (H - ICON_SIZE) // 2
canvas.paste(icon, (icon_x, icon_y), icon)

# Text column on the right
draw = ImageDraw.Draw(canvas)
bold = load_font(
    ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 78
)
semibold = load_font(
    ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 40
)
reg = load_font(
    ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"], 26
)
title = load_font(
    ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 48
)

tx = icon_x + ICON_SIZE + 60  # start x for text column

# Title — red WildDeals wordmark
draw.text((tx, 130), "WILDDEALS", font=title, fill=RED)

# Main headline
draw.text((tx, 210), "40,000+ Deals.", font=bold, fill=WHITE)
draw.text((tx, 300), "Hours before", font=semibold, fill=CREAM)
draw.text((tx, 348), "other forums.", font=semibold, fill=CREAM)

# Divider line
draw.rectangle((tx, 440, tx + 340, 442), fill=RED)

# Trust strip
draw.text((tx, 462), "100% Free   ·   Made in Canada", font=reg, fill=MUTED)
draw.text((tx, 500), "Now on iPhone   ·   Android May 5", font=reg, fill=MUTED)

out = os.path.join(IMG_DIR, "og-card.png")
canvas.save(out, "PNG", optimize=True)
print(f"wrote {out}  ({W}x{H})")
