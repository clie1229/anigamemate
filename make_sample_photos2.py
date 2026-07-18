# -*- coding: utf-8 -*-
"""예시 이미지 확장: 다른 상품 유형(디스크게임/본체/피규어/굿즈)에도
   멀티 사진 갤러리용 저작권 안전 일러스트 4종씩 생성하고 갤러리를 연결한다.
   실제 판매 시 같은 파일명(.svg→촬영본)으로 교체하면 됨."""
import os, re, html as H
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("img", exist_ok=True)

def badge(label, dark=True):
    fill, tc = ("#1b1a2e", "#fff") if dark else ("#fff", "#1b1a2e")
    w = 30 + len(label) * 15
    return (f'<rect x="14" y="14" width="{w}" height="28" rx="14" fill="{fill}" opacity="0.9"/>'
            f'<text x="{14 + w/2}" y="33" text-anchor="middle" fill="{tc}" font-size="14" '
            f'font-family="sans-serif" font-weight="700">{H.escape(label)}</text>')

def wm(dark=False):
    c = "#fff" if dark else "#000"
    return (f'<text x="200" y="290" text-anchor="middle" font-family="sans-serif" font-size="11" '
            f'fill="{c}" opacity="0.32" letter-spacing="1">AnigameMate · 예시 이미지</text>')

def svg(inner):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img">' + inner + '</svg>\n')

# ---------- 디스크 게임 (ps1-ff7) ----------
def disc(_):
    return svg(f'<rect width="400" height="300" fill="#26252b"/>'
        f'<defs><radialGradient id="d" cx="0.4" cy="0.35"><stop offset="0" stop-color="#f3f3f6"/>'
        f'<stop offset="0.7" stop-color="#c9c9d2"/><stop offset="1" stop-color="#9a9aa6"/></radialGradient></defs>'
        f'<circle cx="200" cy="150" r="96" fill="url(#d)" stroke="#7b7b86" stroke-width="2"/>'
        f'<path d="M200 54 a96 96 0 0 1 68 28" stroke="#fff" stroke-width="6" fill="none" opacity="0.5"/>'
        f'<circle cx="200" cy="150" r="30" fill="#26252b"/><circle cx="200" cy="150" r="30" fill="none" stroke="#8a8a95" stroke-width="2"/>'
        f'<circle cx="200" cy="150" r="12" fill="#3a3942"/>'
        f'<text x="200" y="270" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#e6e6ee">게임 디스크 · 로딩 확인 완료</text>'
        f'{badge("디스크", dark=False)}{wm(dark=True)}')

def case_front(_):
    return svg(f'<rect width="400" height="300" fill="#eef0f4"/>'
        f'<rect x="128" y="40" width="150" height="220" rx="6" fill="#fff" stroke="#c3c7d0" stroke-width="2"/>'
        f'<rect x="128" y="40" width="16" height="220" rx="6" fill="#2b3a67"/>'
        f'<defs><linearGradient id="cf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b5ba9"/><stop offset="1" stop-color="#7b3f8f"/></linearGradient></defs>'
        f'<rect x="152" y="58" width="112" height="150" rx="3" fill="url(#cf)"/>'
        f'<text x="208" y="120" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="15" fill="#fff">파이널</text>'
        f'<text x="208" y="142" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="15" fill="#fff">판타지 VII</text>'
        f'<text x="208" y="234" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#7a7f8a">DISC · NTSC-J</text>'
        f'{badge("케이스 앞")}{wm()}')

def case_back(_):
    lines = "".join(f'<rect x="150" y="{y}" width="150" height="5" rx="2" fill="#cfd3db"/>' for y in range(150, 210, 12))
    shots = "".join(f'<rect x="{x}" y="60" width="44" height="34" rx="3" fill="#b9c0cf"/>' for x in (150, 202, 254))
    bars = "".join(f'<rect x="{x}" y="222" width="{3 if i%2 else 2}" height="26" fill="#333"/>' for i, x in enumerate(range(258, 300, 4)))
    return svg(f'<rect width="400" height="300" fill="#e9ebef"/>'
        f'<rect x="112" y="40" width="200" height="220" rx="6" fill="#fff" stroke="#c3c7d0" stroke-width="2"/>'
        f'{shots}{lines}{bars}'
        f'<text x="160" y="240" font-family="sans-serif" font-size="10" fill="#7a7f8a">© 예시</text>'
        f'{badge("케이스 뒤")}{wm()}')

def rpg_screen(_):
    return svg(f'<rect width="400" height="300" rx="14" fill="#12111c"/>'
        f'<rect x="26" y="26" width="348" height="180" rx="4" fill="#0b1030"/>'
        f'<rect x="40" y="40" width="120" height="70" rx="4" fill="#20306a"/>'
        f'<circle cx="70" cy="75" r="14" fill="#e8a13f"/><rect x="92" y="62" width="56" height="8" rx="4" fill="#5fd06a"/><rect x="92" y="78" width="40" height="7" rx="3" fill="#4a5a9a"/>'
        f'<rect x="40" y="150" width="308" height="44" rx="6" fill="#1b2660" stroke="#3a56b0" stroke-width="2"/>'
        f'<rect x="52" y="162" width="200" height="6" rx="3" fill="#9fb0e6"/><rect x="52" y="176" width="150" height="6" rx="3" fill="#6d80c4"/>'
        f'<text x="200" y="285" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#fff" opacity="0.5">실기 구동 · 세이브 정상</text>'
        f'{badge("구동 화면")}')

# ---------- 본체 (fc-console) ----------
def console_front(_):
    vents = "".join(f'<rect x="{x}" y="150" width="6" height="60" rx="3" fill="#c9b8a0"/>' for x in range(120, 290, 14))
    return svg(f'<defs><linearGradient id="cb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4efe6"/><stop offset="1" stop-color="#e7e0d3"/></linearGradient></defs>'
        f'<rect width="400" height="300" fill="url(#cb)"/>'
        f'<rect x="70" y="120" width="260" height="120" rx="12" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>'
        f'<rect x="120" y="98" width="160" height="34" rx="6" fill="#3a352c"/>'
        f'{vents}<circle cx="300" cy="150" r="9" fill="#e8543f"/><circle cx="300" cy="180" r="9" fill="#c9b8a0"/>'
        f'<text x="110" y="150" font-family="sans-serif" font-size="10" fill="#8a8271">POWER</text>'
        f'{badge("정면")}{wm()}')

def console_back(_):
    return svg(f'<rect width="400" height="300" fill="#efe9dd"/>'
        f'<rect x="70" y="120" width="260" height="120" rx="12" fill="#d3c9b5" stroke="#a89d85" stroke-width="2"/>'
        f'<rect x="100" y="150" width="46" height="30" rx="4" fill="#3a352c"/><text x="123" y="200" text-anchor="middle" font-size="9" fill="#7d7563" font-family="sans-serif">RF OUT</text>'
        f'<rect x="176" y="150" width="46" height="30" rx="4" fill="#3a352c"/><text x="199" y="200" text-anchor="middle" font-size="9" fill="#7d7563" font-family="sans-serif">AV</text>'
        f'<circle cx="280" cy="165" r="14" fill="#3a352c"/><text x="280" y="200" text-anchor="middle" font-size="9" fill="#7d7563" font-family="sans-serif">DC IN</text>'
        f'{badge("후면")}{wm()}')

def console_cable(_):
    return svg(f'<rect width="400" height="300" fill="#33312c"/>'
        f'<rect x="150" y="90" width="100" height="60" rx="8" fill="#4a463d" stroke="#6b6456" stroke-width="2"/>'
        f'<text x="200" y="125" text-anchor="middle" font-size="12" fill="#e6dfce" font-family="sans-serif">RF 스위치</text>'
        f'<path d="M200 150 C 200 200 300 200 300 250" stroke="#1e1c18" stroke-width="10" fill="none"/>'
        f'<path d="M200 150 C 200 200 100 200 100 250" stroke="#1e1c18" stroke-width="10" fill="none"/>'
        f'<rect x="86" y="248" width="28" height="18" rx="3" fill="#d4af37"/><rect x="286" y="248" width="28" height="18" rx="3" fill="#c0c0c8"/>'
        f'{badge("단자·케이블", dark=False)}{wm(dark=True)}')

def console_set(_):
    def pad(x):
        return (f'<rect x="{x}" y="150" width="90" height="56" rx="10" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>'
                f'<rect x="{x+14}" y="168" width="10" height="26" fill="#3a352c"/><rect x="{x+9}" y="176" width="20" height="10" fill="#3a352c"/>'
                f'<circle cx="{x+66}" cy="178" r="7" fill="#e8543f"/><circle cx="{x+50}" cy="178" r="7" fill="#e8543f"/>')
    return svg(f'<rect width="400" height="300" fill="#efe9dd"/>'
        f'<rect x="130" y="60" width="140" height="66" rx="10" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>'
        f'<rect x="160" y="46" width="80" height="20" rx="4" fill="#3a352c"/>'
        f'{pad(70)}{pad(240)}'
        f'<text x="200" y="250" text-anchor="middle" font-size="12" fill="#7d7563" font-family="sans-serif">본체 + 컨트롤러 2개 구성</text>'
        f'{badge("구성품")}{wm()}')

# ---------- 피규어 (ag-figure-scale17) ----------
def figure(view, color="#7C5CFF"):
    # view: 'front','side','back'
    base = '<ellipse cx="200" cy="252" rx="70" ry="16" fill="#d8d2ea"/>'
    if view == "front":
        body = (f'<circle cx="200" cy="96" r="30" fill="#f2d3b0"/>'  # head
                f'<path d="M170 92 q30-40 60 0 q4 24-30 24 q-34 0-30-24z" fill="#5b3a2e"/>'  # hair
                f'<rect x="176" y="126" width="48" height="86" rx="18" fill="{color}"/>'  # body
                f'<rect x="150" y="132" width="20" height="66" rx="10" fill="{color}"/><rect x="230" y="132" width="20" height="66" rx="10" fill="{color}"/>'  # arms
                f'<rect x="182" y="208" width="14" height="44" rx="7" fill="#3b3350"/><rect x="204" y="208" width="14" height="44" rx="7" fill="#3b3350"/>'
                f'<circle cx="190" cy="94" r="3" fill="#333"/><circle cx="210" cy="94" r="3" fill="#333"/>')
        lab = "정면"
    elif view == "side":
        body = (f'<circle cx="200" cy="96" r="30" fill="#f2d3b0"/>'
                f'<path d="M172 96 q28-44 56 -2 q-2 26-40 22 q-20-2-16-20z" fill="#5b3a2e"/>'
                f'<rect x="184" y="126" width="40" height="86" rx="18" fill="{color}"/>'
                f'<rect x="196" y="208" width="16" height="44" rx="8" fill="#3b3350"/>'
                f'<circle cx="216" cy="94" r="3" fill="#333"/>')
        lab = "측면·후면"
    else:
        body = (f'<circle cx="200" cy="96" r="30" fill="#5b3a2e"/>'
                f'<rect x="176" y="126" width="48" height="86" rx="18" fill="{color}"/>'
                f'<rect x="182" y="208" width="14" height="44" rx="7" fill="#3b3350"/><rect x="204" y="208" width="14" height="44" rx="7" fill="#3b3350"/>')
        lab = "후면"
    return svg(f'<defs><linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3f0fb"/><stop offset="1" stop-color="#e2dcf3"/></linearGradient></defs>'
        f'<rect width="400" height="300" fill="url(#fg)"/>{base}{body}{badge(lab)}{wm()}')

def figure_box(_):
    return svg(f'<rect width="400" height="300" fill="#efe9dd"/>'
        f'<rect x="120" y="46" width="160" height="208" rx="8" fill="#2b2740" stroke="#1b1830" stroke-width="2"/>'
        f'<rect x="138" y="90" width="124" height="130" rx="4" fill="#cfe6ff" opacity="0.9"/>'
        f'<ellipse cx="200" cy="206" rx="34" ry="8" fill="#a9c0e0"/>'
        f'<circle cx="200" cy="130" r="18" fill="#f2d3b0"/><rect x="186" y="150" width="28" height="46" rx="10" fill="#7C5CFF"/>'
        f'<text x="200" y="76" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14" fill="#fff">1/7 SCALE</text>'
        f'<text x="200" y="240" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#cfc7e6">예약 · 미개봉 박스</text>'
        f'{badge("박스")}{wm()}')

# ---------- 굿즈 키링 (cg-sanrio-cinnamoroll-key) ----------
def plush(view):
    ring = '<circle cx="200" cy="52" r="20" fill="none" stroke="#c9a24a" stroke-width="6"/><rect x="196" y="70" width="8" height="26" rx="4" fill="#c9a24a"/>'
    if view == "front":
        body = ('<ellipse cx="200" cy="176" rx="66" ry="60" fill="#fff" stroke="#e6d9ef" stroke-width="2"/>'
                '<ellipse cx="150" cy="150" rx="16" ry="30" fill="#fff" stroke="#e6d9ef" stroke-width="2"/>'
                '<ellipse cx="250" cy="150" rx="16" ry="30" fill="#fff" stroke="#e6d9ef" stroke-width="2"/>'
                '<circle cx="182" cy="172" r="5" fill="#5a4a6a"/><circle cx="218" cy="172" r="5" fill="#5a4a6a"/>'
                '<ellipse cx="200" cy="190" rx="10" ry="6" fill="#ffb0c8"/>')
        lab = "정면"
    elif view == "back":
        body = ('<ellipse cx="200" cy="176" rx="66" ry="60" fill="#f3ecf7" stroke="#e0d3ea" stroke-width="2"/>'
                '<ellipse cx="150" cy="150" rx="16" ry="30" fill="#f3ecf7" stroke="#e0d3ea" stroke-width="2"/>'
                '<ellipse cx="250" cy="150" rx="16" ry="30" fill="#f3ecf7" stroke="#e0d3ea" stroke-width="2"/>'
                '<rect x="182" y="196" width="36" height="14" rx="5" fill="#e6d9ef"/>')
        lab = "후면"
    return svg(f'<rect width="400" height="300" fill="#ffeff6"/>{ring}{body}{badge(lab)}{wm()}')

def tag(_):
    bars = "".join(f'<rect x="{x}" y="150" width="{3 if i%2 else 2}" height="40" fill="#222"/>' for i, x in enumerate(range(150, 250, 5)))
    return svg(f'<rect width="400" height="300" fill="#fbf1f6"/>'
        f'<path d="M160 60 h120 v170 h-120 z" fill="#fff" stroke="#e2c9d6" stroke-width="2"/>'
        f'<circle cx="200" cy="76" r="7" fill="none" stroke="#c98aa8" stroke-width="3"/>'
        f'<text x="220" y="112" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="14" fill="#b83280">정품 택</text>'
        f'{bars}<text x="200" y="210" text-anchor="middle" font-size="10" fill="#888" font-family="sans-serif">8809 · OFFICIAL</text>'
        f'{badge("정품 택")}{wm()}')

def size(_):
    return svg(f'<rect width="400" height="300" fill="#fff2f8"/>'
        f'<ellipse cx="170" cy="170" rx="56" ry="52" fill="#fff" stroke="#e6d9ef" stroke-width="2"/>'
        f'<rect x="250" y="70" width="30" height="200" fill="#fff7c2" stroke="#e0c96a"/>'
        + "".join(f'<line x1="250" y1="{y}" x2="{264 if i%5 else 280}" y2="{y}" stroke="#c9a24a" stroke-width="2"/>' for i, y in enumerate(range(80, 265, 10)))
        + f'<text x="300" y="180" font-family="sans-serif" font-size="13" fill="#8a6a1a" font-weight="700">약 12cm</text>'
        f'{badge("사이즈")}{wm()}')


PRODUCTS = {
    "ps1-ff7":                     [("디스크", disc), ("케이스 앞", case_front), ("케이스 뒤", case_back), ("구동 화면", rpg_screen)],
    "fc-console":                  [("정면", console_front), ("후면", console_back), ("단자·케이블", console_cable), ("구성품", console_set)],
    "ag-figure-scale17":           [("정면", lambda _: figure("front")), ("측면·후면", lambda _: figure("side")), ("후면", lambda _: figure("back")), ("박스", figure_box)],
    "cg-sanrio-cinnamoroll-key":   [("정면", lambda _: plush("front")), ("후면", lambda _: plush("back")), ("정품 택", tag), ("사이즈", size)],
}

# 1) 이미지 생성
made = 0
for sku, scenes in PRODUCTS.items():
    for i, (lab, fn) in enumerate(scenes, 1):
        open(os.path.join("img", f"{sku}-{i}.svg"), "w", encoding="utf-8").write(fn(lab))
        made += 1

# 2) 갤러리 배선
JS = ('<style>.thumbs img,.gthumbs img{aspect-ratio:1;width:100%;object-fit:cover;border:1px solid var(--line);'
      'border-radius:8px;cursor:pointer;background:#efe9dd}.thumbs img.on,.gthumbs img.on{border:2px solid var(--brand)}'
      '.thumbs img:hover,.gthumbs img:hover{border-color:var(--brand)}</style>'
      '<script>function pmset(el){var m=document.getElementById("pmain");m.src=el.src;m.alt=el.alt;'
      'document.querySelectorAll(".thumbs img,.gthumbs img").forEach(function(i){i.classList.remove("on")});el.classList.add("on")}</script>')
wired = 0
for sku, scenes in PRODUCTS.items():
    f = f"product-{sku}.html"
    if not os.path.exists(f):
        print("건너뜀(없음):", f); continue
    s = open(f, encoding="utf-8").read()
    s = s.replace(f'src="img/{sku}.svg"', f'src="img/{sku}-1.svg"', 1)
    s = s.replace('<img class="main" ', '<img class="main" id="pmain" ', 1)
    m = re.search(r'<div class="(g?thumbs)">((?:\s*<div>[^<]*</div>)+)\s*</div>', s)
    if m:
        cls = m.group(1)
        imgs = []
        for i, (lab, _) in enumerate(scenes, 1):
            on = ' class="on"' if i == 1 else ''
            imgs.append(f'<img src="img/{sku}-{i}.svg" alt="{H.escape(lab)}"{on} onclick="pmset(this)">')
        new = f'<div class="{cls}">\n          ' + "\n          ".join(imgs) + "\n        </div>"
        s = s[:m.start()] + new + s[m.end():]
    if "function pmset" not in s:
        s = s.replace("</main>", JS + "\n</main>", 1)
    open(f, "w", encoding="utf-8").write(s)
    wired += 1

print(f"예시 이미지 {made}개 생성 · 갤러리 배선 {wired}개 상품")
