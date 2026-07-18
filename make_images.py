# -*- coding: utf-8 -*-
"""상품별 이미지 파일(img/<sku>.svg) 생성 + 썸네일을 <img>로 연결.
   카테고리 색상 그라데이션 + 이모지 + 상품명 라벨 = 디자인 플레이스홀더.
   실물 사진으로 교체 시 img/<sku>.svg 를 같은 이름의 이미지로 바꾸면 됨."""
import os, re, glob, io, sys, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from platforms import PLATFORMS
from shop import CATEGORIES

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

STYLE = {
    "retro":     ("🎮", "#ece5ff", "#d6c9ff", "#3b2f8f"),
    "character": ("🧸", "#ffe3f0", "#ffccdf", "#b83280"),
    "doujin":    ("📖", "#e6f0ff", "#cfe0ff", "#2b4c8f"),
    "anime":     ("✨", "#fff1dc", "#ffdcb0", "#a15a1e"),
}

def cat_of_sku(sku):
    if sku.startswith("cg-"): return "character"
    if sku.startswith("dj-"): return "doujin"
    if sku.startswith("ag-"): return "anime"
    return "retro"

# sku -> 상품명
data = {}
for p in PLATFORMS:
    for t in p["products"]:
        data[t[1]] = t[0]
for c in CATEGORIES:
    for s in c["subs"]:
        for t in s["products"]:
            data[t[1]] = t[0]
# HTML에서 참조되는 상품 sku도 포함(데이터에 없는 것 대비)
for f in glob.glob("*.html"):
    for sku in re.findall(r'href="product-([a-z0-9-]+)\.html"', open(f, encoding="utf-8").read()):
        data.setdefault(sku, None)

os.makedirs("img", exist_ok=True)

def make_svg(sku, name):
    emoji, c1, c2, tc = STYLE[cat_of_sku(sku)]
    label = ""
    if name:
        short = name if len(name) <= 18 else name[:17] + "…"
        label = (f'<text x="200" y="214" font-size="17" text-anchor="middle" fill="{tc}" '
                 f'font-family="Pretendard,Apple SD Gothic Neo,Malgun Gothic,sans-serif" '
                 f'font-weight="700">{H.escape(short)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" '
            f'aria-label="{H.escape(name or "상품 이미지")}">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<rect width="400" height="300" fill="url(#g)"/>'
            f'<text x="200" y="138" font-size="86" text-anchor="middle" dominant-baseline="central">{emoji}</text>'
            f'{label}'
            f'<text x="200" y="282" font-size="13" text-anchor="middle" fill="{tc}" opacity="0.45" '
            f'font-family="sans-serif" letter-spacing="1">AnigameMate</text>'
            f'</svg>\n')

made = 0
for sku, name in data.items():
    open(os.path.join("img", f"{sku}.svg"), "w", encoding="utf-8").write(make_svg(sku, name))
    made += 1

# 썸네일/대표이미지를 <img>로 배선
CARD = re.compile(r'(<a class="prod" href="product-([a-z0-9-]+)\.html">\s*)<div class="thumb"[^>]*>(?:(?!</div>).)*</div>', re.S)
MAIN = re.compile(r'<div class="main"[^>]*>(?:(?!</div>).)*</div>', re.S)
IMG_STYLE = 'style="width:100%;height:100%;object-fit:cover"'
wired = 0
for f in glob.glob("*.html"):
    s = open(f, encoding="utf-8").read(); o = s
    s = CARD.sub(lambda m: m.group(1) + f'<img class="thumb" src="img/{m.group(2)}.svg" alt="상품 대표 이미지" loading="lazy" {IMG_STYLE}>', s)
    base = os.path.basename(f)
    if base.startswith("product-") and base not in ("product-template.html", "product-detail-template.html"):
        sku = base[len("product-"):-len(".html")]
        if os.path.exists(os.path.join("img", f"{sku}.svg")):
            s = MAIN.sub(f'<img class="main" src="img/{sku}.svg" alt="대표 이미지" {IMG_STYLE}>', s, count=1)
    if s != o:
        open(f, "w", encoding="utf-8").write(s); wired += 1

print(f"SVG 이미지 생성 {made}개 · HTML 배선 {wired}개")
