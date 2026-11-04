"""Builds assets/banner.svg: Arriero's Wealth, DwarfVault and Dragon Audio in one night scene.

Run: python assets/make_banner.py
"""

from __future__ import annotations

import base64
import io
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).parent
SRC = HERE / "src"
W, H = 1200, 320
GOLD = "#f5b82e"
GROUND = 262


def b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def arriero() -> Image.Image:
    img = Image.open(SRC / "arriero_abuelo.png").convert("RGBA")
    w, h = img.size
    edge = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
    edge += [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    for xy in edge:
        if img.getpixel(xy)[3] and min(img.getpixel(xy)[:3]) > 215:
            ImageDraw.floodfill(img, xy, (0, 0, 0, 0), thresh=40)
    px = img.load()
    for y in range(int(h * 0.88), h):
        for x in range(w):
            if min(px[x, y][:3]) > 200:
                px[x, y] = (0, 0, 0, 0)
    return img.crop(img.getbbox())


def chest() -> Image.Image:
    img = Image.open(SRC / "dwarf_icon.png").convert("RGBA")
    return img.crop(img.getbbox())


def dragon() -> Image.Image:
    img = Image.open(SRC / "dragon_emblem.png").convert("RGBA")
    img = img.crop(img.getbbox())
    return img.resize((260, round(260 * img.height / img.width)), Image.LANCZOS)


def stars(n: int = 46) -> str:
    rnd = random.Random(11)
    out = []
    for _ in range(n):
        x, y = rnd.randint(10, W - 10), rnd.randint(10, 190)
        r = rnd.choice([0.8, 1, 1.2, 1.6])
        out.append(
            f'<circle class="tw" cx="{x}" cy="{y}" r="{r}" '
            f'style="animation-delay:{rnd.uniform(0, 6):.2f}s;animation-duration:{rnd.uniform(3, 7):.2f}s"/>'
        )
    return "\n    ".join(out)


def wave() -> str:
    pts = []
    for x in range(0, W + 1, 6):
        mid = 600
        amp = 3 + 9 * max(0.0, 1 - abs(x - mid) / 520) ** 2
        y = GROUND + 18 + amp * math.sin(x / 17) * math.sin(x / 61)
        pts.append(f"{x},{y:.1f}")
    return "M" + " L".join(pts)


def build() -> str:
    a, c, d = arriero(), chest(), dragon()
    ah = 150
    aw = round(a.width * ah / a.height)
    cw = 74
    ch = round(c.height * cw / c.width)
    dw, dh = 210, round(d.height * 210 / d.width)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
     aria-label="David Salazar Saldarriaga — Arriero's Wealth, DwarfVault and Dragon Audio">
  <style>
    .tw {{ fill:#fff; animation: tw 5s ease-in-out infinite; }}
    @keyframes tw {{ 0%,100% {{ opacity:.15 }} 50% {{ opacity:.9 }} }}
    .walk {{ animation: walk 1.6s steps(2) infinite; }}
    @keyframes walk {{ 50% {{ transform: translateY(-2px) }} }}
    .coin {{ animation: coin 4.8s ease-out infinite; opacity:0; }}
    @keyframes coin {{ 0% {{ opacity:0; transform:translate(0,0) }} 15% {{ opacity:1 }}
                       100% {{ opacity:0; transform:translate(10px,-46px) }} }}
    .glow {{ animation: glow 4s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }}
    @keyframes glow {{ 0%,100% {{ opacity:.25; transform:scale(.9) }} 50% {{ opacity:.6; transform:scale(1.08) }} }}
    .spark {{ animation: spark 4s ease-in-out infinite; opacity:0; transform-box: fill-box; transform-origin:center; }}
    @keyframes spark {{ 0%,70%,100% {{ opacity:0; transform:scale(.3) }} 80% {{ opacity:1; transform:scale(1) }} }}
    .float {{ animation: float 7s ease-in-out infinite; }}
    @keyframes float {{ 0%,100% {{ transform: translateY(0) rotate(0deg) }} 50% {{ transform: translateY(-6px) rotate(-1.2deg) }} }}
    .ring {{ animation: ring 6s ease-out infinite; opacity:0; transform-box: fill-box; transform-origin:center; }}
    @keyframes ring {{ 0% {{ opacity:.55; transform:scale(.55) }} 100% {{ opacity:0; transform:scale(1.5) }} }}
    .flow {{ stroke-dasharray: 2 10; animation: flow 3s linear infinite; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -120 }} }}
    .fade {{ animation: fade 1.6s ease-out both; }}
    @keyframes fade {{ from {{ opacity:0; transform:translateY(6px) }} to {{ opacity:1; transform:none }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .coin,.spark,.ring {{ opacity:0 }} }}
  </style>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d0a24"/><stop offset=".65" stop-color="#1d1450"/><stop offset="1" stop-color="#33206b"/>
    </linearGradient>
    <radialGradient id="moon" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="chestGlow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{GOLD}" stop-opacity=".8"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="line" x1="0" x2="1">
      <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".15" stop-color="{GOLD}"/>
      <stop offset=".85" stop-color="#7c5cff"/><stop offset="1" stop-color="#7c5cff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
    <path id="star4" d="M0,-6 L1.4,-1.4 L6,0 L1.4,1.4 L0,6 L-1.4,1.4 L-6,0 L-1.4,-1.4 Z"/>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    {stars()}

    <circle cx="1040" cy="120" r="150" fill="url(#moon)"/>

    <path d="M0,{GROUND-40} L90,{GROUND-95} L170,{GROUND-55} L270,{GROUND-120} L380,{GROUND-60} L470,{GROUND-90} L560,{GROUND-50}
             L660,{GROUND-105} L760,{GROUND-60} L860,{GROUND-130} L960,{GROUND-70} L1060,{GROUND-115} L1200,{GROUND-50} L1200,{H} L0,{H} Z"
          fill="#2a1c5e" opacity=".75"/>
    <path d="M0,{GROUND-10} L120,{GROUND-50} L230,{GROUND-20} L340,{GROUND-60} L450,{GROUND-18} L600,{GROUND-45}
             L740,{GROUND-15} L850,{GROUND-55} L980,{GROUND-20} L1100,{GROUND-48} L1200,{GROUND-15} L1200,{H} L0,{H} Z"
          fill="#1a1240"/>
    <rect y="{GROUND}" width="{W}" height="{H-GROUND}" fill="#120c30"/>

    <path class="flow" d="{wave()}" fill="none" stroke="url(#line)" stroke-width="2.2" stroke-linecap="round"/>

    <!-- Arriero's Wealth -->
    <g transform="translate(70,{GROUND - ah + 4})">
      <g class="walk"><image href="{b64(a)}" width="{aw}" height="{ah}" style="image-rendering:pixelated"/></g>
      <circle class="coin" cx="48" cy="40" r="5" fill="{GOLD}" stroke="#a8740c" stroke-width="1.5"/>
      <circle class="coin" cx="58" cy="44" r="4" fill="{GOLD}" stroke="#a8740c" stroke-width="1.5" style="animation-delay:1.6s"/>
      <circle class="coin" cx="40" cy="46" r="4.5" fill="{GOLD}" stroke="#a8740c" stroke-width="1.5" style="animation-delay:3.2s"/>
    </g>

    <!-- DwarfVault -->
    <g transform="translate({600 - cw // 2},{GROUND - ch + 6})">
      <ellipse class="glow" cx="{cw / 2}" cy="{ch / 2}" rx="{cw * .95}" ry="{ch * .9}" fill="url(#chestGlow)"/>
      <image href="{b64(c)}" width="{cw}" height="{ch}" style="image-rendering:pixelated"/>
      <use class="spark" href="#star4" x="{cw - 6}" y="2" fill="#fff6d6"/>
      <use class="spark" href="#star4" x="6" y="{ch * .35:.0f}" fill="#fff6d6" style="animation-delay:2s"/>
    </g>

    <!-- Dragon Audio -->
    <g transform="translate({1040 - dw // 2},{120 - dh // 2})">
      <circle class="ring" cx="{dw / 2}" cy="{dh / 2}" r="{dw * .55}" fill="none" stroke="{GOLD}" stroke-width="1.5"/>
      <circle class="ring" cx="{dw / 2}" cy="{dh / 2}" r="{dw * .55}" fill="none" stroke="{GOLD}" stroke-width="1.5" style="animation-delay:2s"/>
      <circle class="ring" cx="{dw / 2}" cy="{dh / 2}" r="{dw * .55}" fill="none" stroke="#7c5cff" stroke-width="1.5" style="animation-delay:4s"/>
      <g class="float"><image href="{b64(d)}" width="{dw}" height="{dh}"/></g>
    </g>

    <g class="fade" text-anchor="middle" font-family="Segoe UI, Inter, Helvetica, Arial, sans-serif">
      <text x="600" y="92" font-size="40" font-weight="700" fill="#ffffff" letter-spacing=".5">David Salazar Saldarriaga</text>
      <text x="600" y="128" font-size="15" font-weight="600" fill="{GOLD}" letter-spacing="4"
            font-family="Consolas, Menlo, monospace">DATA SCIENCE · AI · MUSIC</text>
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    out = HERE / "banner.svg"
    out.write_text(build(), encoding="utf-8")
    print(f"{out} — {out.stat().st_size / 1024:.0f} KB")
