#!/usr/bin/env python3
"""Draw the UK-NOC emblem (v1, 26 Nov 2026).

The Council seal: the name round the rim, LONDON at the foot, and in the middle
three coloured seats (government, UK industry, overseas suppliers) round one table.
The middle on its own is the small mark, used in the website header and browser tab.

Writes (run from anywhere):  python3 tools/make_emblem.py
  assets/uknoc-seal.svg   the seal (the home page shows it beside the title)
  assets/uknoc-mark.svg   the small mark for the website header
  favicon.svg             the browser-tab icon

With  --render <folder>  it also uses Chrome (Playwright) to make
  favicon.ico and apple-touch-icon.png in the site folder, and in <folder>:
  UK-NOC_seal_2000px.png (transparent), UK-NOC_seal.pdf (vector, for printers),
  UK-NOC_mark_1000px.png (for white backgrounds).
build_noc.py only reads the two files in assets/; it never runs this script.
"""
import math
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
TEAL, DEEP, INK, SAFF, SKY, CORAL, PAPER = "#0b4a55", "#0d3a43", "#f4f8f8", "#ffcf5c", "#8ab4ff", "#ff8f6b", "#eef5f6"
SEATS = ((0, SKY), (120, CORAL), (240, SAFF))  # government, UK industry, overseas suppliers
FONT_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700'
             '&family=Newsreader:opsz,wght@6..72,600;6..72,700&display=swap">')


def pt(cx, cy, r, deg):  # deg: 0 = straight up, clockwise
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def arc(cx, cy, r, d0, d1, clockwise=True):
    x0, y0 = pt(cx, cy, r, d0)
    x1, y1 = pt(cx, cy, r, d1)
    large = 1 if abs(d1 - d0) > 180 else 0
    return f"M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} {1 if clockwise else 0} {x1:.2f},{y1:.2f}"


def seats(c, r, width):
    return "".join(f'<path d="{arc(c, c, r, d - 52, d + 52)}" fill="none" stroke="{col}" stroke-width="{width}"/>'
                   for d, col in SEATS)


def seal():
    c = 120
    top = arc(c, c, 93, -108, 108)
    bot = arc(c, c, 101, 236, 124, clockwise=False)
    dots = "".join(f'<circle cx="{pt(c, c, 97, d)[0]:.2f}" cy="{pt(c, c, 97, d)[1]:.2f}" r="3.1" fill="{col}"/>'
                   for d, col in ((-118, SAFF), (-126, CORAL), (-134, SKY), (118, SKY), (126, CORAL), (134, SAFF)))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" aria-label="UK National Offset Council seal">'
            f'<defs><path id="sealtop" d="{top}"/><path id="sealbot" d="{bot}"/></defs>'
            f'<circle cx="{c}" cy="{c}" r="118" fill="{TEAL}"/>'
            f'<circle cx="{c}" cy="{c}" r="113" fill="none" stroke="{SAFF}" stroke-width="1.6"/>'
            f'<circle cx="{c}" cy="{c}" r="82" fill="{DEEP}" stroke="{SAFF}" stroke-width="1.6"/>'
            f'<text font-family="Newsreader,Georgia,serif" font-weight="700" font-size="14.6" letter-spacing="1.9" fill="{INK}">'
            '<textPath href="#sealtop" startOffset="50%" text-anchor="middle">UK NATIONAL OFFSET COUNCIL</textPath></text>'
            f'<text font-family="Newsreader,Georgia,serif" font-weight="700" font-size="13" letter-spacing="4" fill="{INK}">'
            f'<textPath href="#sealbot" startOffset="50%" text-anchor="middle">LONDON</textPath></text>{dots}'
            f'<circle cx="{c}" cy="{c}" r="40" fill="{PAPER}"/>{seats(c, 58, 14)}'
            f'<text x="{c}" y="{c + 6.5}" text-anchor="middle" font-family="Newsreader,Georgia,serif" font-weight="700" '
            f'font-size="18.5" fill="{TEAL}">UK-NOC</text></svg>')


def mark(table=PAPER, rim=TEAL):
    """The seal's middle on its own: light table for dark grounds, teal table for white paper."""
    c = 60
    ring = f'<circle cx="{c}" cy="{c}" r="19" fill="none" stroke="{rim}" stroke-opacity=".25" stroke-width="1.4"/>' if rim else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="UK-NOC">'
            f'<circle cx="{c}" cy="{c}" r="27" fill="{table}"/>{ring}{seats(c, 43, 15)}</svg>')


def tab_icon():
    """Browser tab: the mark on a teal disc, so it shows on light and dark tab bars."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">'
            f'<circle cx="60" cy="60" r="60" fill="{TEAL}"/><circle cx="60" cy="60" r="20" fill="{PAPER}"/>{seats(60, 38, 17)}</svg>')


def home_icon():
    """Phone home screen (the phone rounds the corners itself)."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180">'
            f'<rect width="180" height="180" fill="{TEAL}"/><circle cx="90" cy="90" r="25" fill="{PAPER}"/>{seats(90, 47, 20)}</svg>')


def write_svgs():
    (SITE / "assets").mkdir(exist_ok=True)
    for path, svg in (("assets/uknoc-seal.svg", seal()), ("assets/uknoc-mark.svg", mark()), ("favicon.svg", tab_icon())):
        (SITE / path).write_text(svg + "\n", encoding="utf-8")
        print("wrote", path)


def render(outdir):
    from io import BytesIO
    from PIL import Image
    from playwright.sync_api import sync_playwright
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    def page_html(svg, px):
        svg = svg.replace("<svg ", f'<svg width="{px}" height="{px}" style="display:block" ', 1)
        return f'<!doctype html><html><head><meta charset="utf-8">{FONT_LINK}</head><body style="margin:0;background:transparent">{svg}</body></html>'

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)

        def png(svg, px):
            pg = browser.new_page(viewport={"width": px, "height": px}, device_scale_factor=1)
            pg.set_content(page_html(svg, px), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            data = pg.screenshot(omit_background=True)
            pg.close()
            return Image.open(BytesIO(data)).convert("RGBA")

        icons = [png(tab_icon(), s) for s in (48, 32, 16)]
        icons[0].save(SITE / "favicon.ico", sizes=[(48, 48), (32, 32), (16, 16)], append_images=icons[1:])
        png(home_icon(), 180).convert("RGB").save(SITE / "apple-touch-icon.png")
        png(seal(), 2000).save(outdir / "UK-NOC_seal_2000px.png")
        png(mark(table=TEAL, rim=None), 1000).save(outdir / "UK-NOC_mark_1000px.png")
        pg = browser.new_page()  # a 100 mm seal on a 110 mm page, so nothing is trimmed at the edges
        pdf_svg = seal().replace("<svg ", '<svg style="display:block;width:100mm;height:100mm" ', 1)
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8">{FONT_LINK}</head>'
                       f'<body style="margin:0"><div style="padding:5mm">{pdf_svg}</div></body></html>', wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(outdir / "UK-NOC_seal.pdf"), width="110mm", height="110mm", print_background=True,
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, page_ranges="1")
        browser.close()
    print("wrote favicon.ico, apple-touch-icon.png and the print files in", outdir)


if __name__ == "__main__":
    write_svgs()
    if len(sys.argv) == 3 and sys.argv[1] == "--render":
        render(sys.argv[2])
