#!/usr/bin/env python3
"""Draw the iPhone app icon and launch logo from code (no game art, no fonts).

    python3 tools/ios/make_icon.py        (needs Pillow; writes into tools/ios/Assets.xcassets)

The icon is an original design: a 'TXRA' wordmark built from polygons over a night road
with neon edge lines. The output PNGs are committed, so building the app does not need Pillow.
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent / 'Assets.xcassets'
SS = 4  # supersampling for smooth edges

# Letters on a 200 x 280 grid: filled polygons, then counters cut out.
LETTERS = {
    'T': ([[(0, 0), (200, 0), (200, 62), (131, 62), (131, 280), (69, 280), (69, 62), (0, 62)]], []),
    'X': ([[(0, 0), (66, 0), (200, 280), (134, 280)], [(134, 0), (200, 0), (66, 280), (0, 280)]], []),
    'R': ([[(0, 0), (150, 0), (200, 42), (200, 118), (165, 152), (200, 280), (136, 280), (104, 164),
            (62, 164), (62, 280), (0, 280)]],
          [[(62, 56), (126, 56), (140, 70), (140, 96), (126, 110), (62, 110)]]),
    'A': ([[(73, 0), (127, 0), (200, 280), (140, 280), (127, 226), (73, 226), (60, 280), (0, 280)]],
          [[(100, 78), (120, 170), (80, 170)]]),
}


def wordmark_mask(text, height, slant=0.24, gap=34):
    """White-on-black mask of the wordmark, `height` pixels tall (already supersampled)."""
    scale = height / 280
    width = int((len(text) * 200 + (len(text) - 1) * gap + 280 * slant) * scale) + 4
    mask = Image.new('L', (width, height + 4), 0)
    draw = ImageDraw.Draw(mask)
    for i, ch in enumerate(text):
        x0 = i * (200 + gap)
        shapes, holes = LETTERS[ch]

        def place(poly):
            return [((x0 + x + (280 - y) * slant) * scale + 2, y * scale + 2) for x, y in poly]
        for poly in shapes:
            draw.polygon(place(poly), fill=255)
        for poly in holes:
            draw.polygon(place(poly), fill=0)
    return mask


def gradient(size, top, bottom):
    w, h = size
    img = Image.new('RGB', size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def glow(mask, radius, color, strength=1.0):
    layer = Image.new('RGB', mask.size, color)
    blurred = mask.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        blurred = blurred.point(lambda v: min(255, int(v * strength)))
    return layer, blurred


def icon(size=1024):
    S = size * SS
    horizon = int(S * 0.50)
    img = gradient((S, S), (8, 9, 22), (16, 10, 26))
    sky = gradient((S, horizon), (7, 8, 20), (58, 16, 62))
    img.paste(sky, (0, 0))
    draw = ImageDraw.Draw(img)
    vx = S // 2
    # Road: asphalt trapezoid to the vanishing point, darker than the sky glow.
    road = [(int(S * -0.05), S), (int(S * 1.05), S), (vx + S // 60, horizon), (vx - S // 60, horizon)]
    draw.polygon(road, fill=(18, 19, 26))
    # Horizon glow line.
    line = Image.new('L', (S, S), 0)
    ImageDraw.Draw(line).rectangle([0, horizon - S // 400, S, horizon + S // 400], fill=255)
    layer, m = glow(line, S // 60, (255, 64, 150), 2.2)
    img.paste(layer, (0, 0), m)
    img.paste((255, 120, 180), (0, 0), line)
    # Neon road edges (cyan) with glow, dashed centre line (amber) in perspective.
    edges = Image.new('L', (S, S), 0)
    ed = ImageDraw.Draw(edges)
    w = S // 90
    for side in (-1, 1):
        bottom_x = vx + side * int(S * 0.46)
        ed.polygon([(bottom_x - w, S), (bottom_x + w, S), (vx + side * S // 70 + 2, horizon),
                    (vx + side * S // 70 - 2, horizon)], fill=255)
    layer, m = glow(edges, S // 70, (40, 220, 255), 1.8)
    img.paste(layer, (0, 0), m)
    img.paste((150, 240, 255), (0, 0), edges)
    dash = Image.new('L', (S, S), 0)
    dd = ImageDraw.Draw(dash)
    for k in range(9):
        t0, t1 = (k + 0.15) / 9, (k + 0.6) / 9
        # perspective: distance from horizon grows quadratically toward the viewer
        y0, y1 = horizon + (S - horizon) * t0 ** 2, horizon + (S - horizon) * t1 ** 2
        h0, h1 = S / 300 * (1 + 9 * t0 ** 2), S / 300 * (1 + 9 * t1 ** 2)
        dd.polygon([(vx - h0, y0), (vx + h0, y0), (vx + h1, y1), (vx - h1, y1)], fill=255)
    layer, m = glow(dash, S // 120, (255, 177, 42), 1.6)
    img.paste(layer, (0, 0), m)
    img.paste((255, 196, 90), (0, 0), dash)
    # Wordmark across the horizon: dark shadow, cyan outline glow, warm white fill.
    mark = wordmark_mask('TXRA', int(S * 0.255))
    target_w = int(S * 0.86)
    mark = mark.resize((target_w, int(mark.height * target_w / mark.width)), Image.LANCZOS)
    full = Image.new('L', (S, S), 0)
    ox, oy = (S - mark.width) // 2, horizon - int(mark.height * 0.62)
    full.paste(mark, (ox, oy))
    shadow = full.filter(ImageFilter.GaussianBlur(S // 80)).point(lambda v: min(255, v * 2))
    img.paste((4, 4, 10), (S // 120, S // 60), shadow)
    outline = full.filter(ImageFilter.MaxFilter(2 * (S // 160) + 1))
    layer, m = glow(outline, S // 90, (40, 220, 255), 1.4)
    img.paste(layer, (0, 0), m)
    img.paste((30, 200, 255), (0, 0), outline)
    fill = gradient((S, S), (255, 252, 240), (255, 196, 110))
    img.paste(fill, (0, 0), full)
    return img.resize((size, size), Image.LANCZOS)


def launch_logo(width=900):
    """Transparent wordmark for the launch screen (3x scale)."""
    mark = wordmark_mask('TXRA', 300 * SS)
    w = width * SS
    mark = mark.resize((w, int(mark.height * w / mark.width)), Image.LANCZOS)
    pad = 12 * SS
    canvas = Image.new('L', (mark.width + 2 * pad, mark.height + 2 * pad), 0)
    canvas.paste(mark, (pad, pad))
    outline = canvas.filter(ImageFilter.MaxFilter(2 * (5 * SS) + 1))
    rgba = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    rgba.paste((30, 200, 255, 255), (0, 0), outline)
    rgba.paste((255, 239, 208, 255), (0, 0), canvas)
    return rgba.resize((rgba.width // SS, rgba.height // SS), Image.LANCZOS)


def main():
    out = ROOT / 'AppIcon.appiconset' / 'icon-1024.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    icon().save(out, optimize=True)
    logo = ROOT / 'LaunchLogo.imageset' / 'launch-logo@3x.png'
    logo.parent.mkdir(parents=True, exist_ok=True)
    launch_logo().save(logo, optimize=True)
    print(out, logo)


if __name__ == '__main__':
    main()
