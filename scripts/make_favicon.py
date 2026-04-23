"""Generate WDfavicon.png — white W on red background."""
import os
from PIL import Image, ImageDraw, ImageFont

SIZE = 512
RED = (220, 27, 27)   # #dc1b1b — matches site palette
WHITE = (255, 255, 255)

font_path = None
for path in [
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/Arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
]:
    if os.path.exists(path):
        font_path = path
        break
if font_path is None:
    raise SystemExit("No suitable bold font found")

img = Image.new("RGB", (SIZE, SIZE), RED)
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(font_path, int(SIZE * 0.72))
bbox = draw.textbbox((0, 0), "W", font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (SIZE - tw) // 2 - bbox[0]
y = (SIZE - th) // 2 - bbox[1]
draw.text((x, y), "W", font=font, fill=WHITE)

out = os.path.join(os.path.dirname(__file__), "..", "images", "WDfavicon.png")
out = os.path.normpath(out)
img.save(out, "PNG", optimize=True)
print(f"wrote {out} using {font_path}")
