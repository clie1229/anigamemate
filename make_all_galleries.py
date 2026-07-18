# -*- coding: utf-8 -*-
"""모든 상품 페이지에 멀티 사진 갤러리 일괄 적용.
   상품을 유형별로 분류해 유형별 4장 일러스트(img/<sku>-1~4.svg) 생성,
   상세페이지 갤러리 연결 + 카드 썸네일을 대표 이미지(-1)로 통일.
   이미 수작업한 5종(fc-smb3/ps1-ff7/fc-console/ag-figure-scale17/cg-sanrio-cinnamoroll-key)은 보존."""
import os, re, glob, html as H
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("img", exist_ok=True)
from platforms import PLATFORMS
from shop import CATEGORIES

DONE = {"fc-smb3", "ps1-ff7", "fc-console", "ag-figure-scale17", "cg-sanrio-cinnamoroll-key"}

# ---------- helpers ----------
def badge(label, dark=True):
    fill, tc = ("#1b1a2e", "#fff") if dark else ("#fff", "#1b1a2e")
    w = 30 + len(label) * 15
    return (f'<rect x="14" y="14" width="{w}" height="28" rx="14" fill="{fill}" opacity="0.9"/>'
            f'<text x="{14 + w/2}" y="33" text-anchor="middle" fill="{tc}" font-size="14" '
            f'font-family="sans-serif" font-weight="700">{H.escape(label)}</text>')

def wm(dark=False):
    c = "#fff" if dark else "#000"
    return (f'<text x="200" y="290" text-anchor="middle" font-family="sans-serif" font-size="11" '
            f'fill="{c}" opacity="0.3" letter-spacing="1">AnigameMate · 예시 이미지</text>')

def S(inner):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img">' + inner + '</svg>\n'

def two_lines(name, n=10):
    name = re.sub(r"\s*\([^)]*\)\s*", " ", name).strip()
    if len(name) <= n:
        return [name]
    # 공백 기준 2줄
    parts = name.split()
    if len(parts) >= 2:
        mid = len(parts) // 2
        a, b = " ".join(parts[:mid]), " ".join(parts[mid:])
    else:
        a, b = name[:n], name[n:2 * n]
    return [a[:14], b[:14]]

def title_text(name, x, y, fill, size=15):
    out = []
    for i, ln in enumerate(two_lines(name)):
        out.append(f'<text x="{x}" y="{y + i * 20}" text-anchor="middle" font-family="sans-serif" '
                   f'font-weight="800" font-size="{size}" fill="{fill}">{H.escape(ln)}</text>')
    return "".join(out)

def hue(sku):
    palette = ["#7C5CFF", "#e8543f", "#2b9d6b", "#e0a800", "#3b6fd4", "#c0468f", "#d4772a"]
    return palette[sum(map(ord, sku)) % len(palette)]

# ---------- 유형별 4장 ----------
def cartridge(sku, name):
    front = S(f'<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6f3ec"/><stop offset="1" stop-color="#e7e1d5"/></linearGradient></defs>'
        f'<rect width="400" height="300" fill="url(#b)"/>'
        f'<rect x="120" y="46" width="160" height="208" rx="14" fill="#d7d1c4" stroke="#b3aa98" stroke-width="2"/>'
        f'<path d="M120 60 q0-14 14-14 h132 q14 0 14 14 v34 h-160 z" fill="{hue(sku)}"/>'
        f'<rect x="138" y="106" width="124" height="100" rx="4" fill="#fff" stroke="#cbc3b2"/>'
        f'{title_text(name,200,140,"#3b2f8f")}'
        f'<text x="200" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#8a8271" letter-spacing="2">CARTRIDGE</text>'
        f'<rect x="150" y="216" width="100" height="24" rx="3" fill="#cfc8b8"/>{badge("정면")}{wm()}')
    ribs = "".join(f'<rect x="140" y="{y}" width="120" height="6" rx="3" fill="#b9b1a0"/>' for y in range(120, 210, 16))
    back = S(f'<rect width="400" height="300" fill="#e9e3d7"/><rect x="120" y="46" width="160" height="208" rx="14" fill="#cfc9bb" stroke="#aca392" stroke-width="2"/>{ribs}'
        f'<circle cx="140" cy="238" r="5" fill="#9c927d"/><circle cx="260" cy="238" r="5" fill="#9c927d"/>{badge("후면")}{wm()}')
    pins = "".join(f'<rect x="{x}" y="150" width="10" height="90" rx="2" fill="#d4af37"/>' for x in range(96, 300, 20))
    conn = S(f'<rect width="400" height="300" fill="#2a2924"/><rect x="80" y="138" width="240" height="116" rx="6" fill="#33312c"/>{pins}'
        f'<text x="200" y="128" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#e6dfce">단자 세척 완료 · 구동 확인</text>{badge("단자",False)}{wm(True)}')
    game = S(f'<rect width="400" height="300" rx="14" fill="#12111c"/><rect x="26" y="26" width="348" height="228" rx="6" fill="#5c94fc"/>'
        f'<ellipse cx="110" cy="86" rx="26" ry="13" fill="#fff"/><ellipse cx="300" cy="72" rx="22" ry="11" fill="#fff"/>'
        f'<rect x="26" y="214" width="348" height="40" fill="#00a800"/><rect x="150" y="150" width="26" height="26" rx="3" fill="#e8a13f" stroke="#a9611a" stroke-width="2"/>'
        f'<rect x="196" y="196" width="20" height="20" rx="4" fill="#c23b22"/><circle cx="320" cy="150" r="9" fill="#ffd93b" stroke="#c99a12" stroke-width="2"/>{badge("구동 화면")}')
    return [("정면", front), ("후면", back), ("단자", conn), ("구동 화면", game)]

def disc(sku, name):
    d = S(f'<rect width="400" height="300" fill="#26252b"/><defs><radialGradient id="d" cx="0.4" cy="0.35"><stop offset="0" stop-color="#f3f3f6"/><stop offset="0.7" stop-color="#c9c9d2"/><stop offset="1" stop-color="#9a9aa6"/></radialGradient></defs>'
        f'<circle cx="200" cy="150" r="96" fill="url(#d)" stroke="#7b7b86" stroke-width="2"/><path d="M200 54 a96 96 0 0 1 68 28" stroke="#fff" stroke-width="6" fill="none" opacity="0.5"/>'
        f'<circle cx="200" cy="150" r="30" fill="#26252b" stroke="#8a8a95" stroke-width="2"/><circle cx="200" cy="150" r="12" fill="#3a3942"/>'
        f'<text x="200" y="272" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#e6e6ee">게임 디스크 · 로딩 확인</text>{badge("디스크",False)}{wm(True)}')
    cf = S(f'<rect width="400" height="300" fill="#eef0f4"/><rect x="128" y="40" width="150" height="220" rx="6" fill="#fff" stroke="#c3c7d0" stroke-width="2"/><rect x="128" y="40" width="16" height="220" rx="6" fill="{hue(sku)}"/>'
        f'<rect x="152" y="58" width="112" height="150" rx="3" fill="{hue(sku)}" opacity="0.85"/>{title_text(name,208,116,"#fff")}'
        f'<text x="208" y="234" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#7a7f8a">DISC · NTSC-J</text>{badge("케이스 앞")}{wm()}')
    lines = "".join(f'<rect x="150" y="{y}" width="150" height="5" rx="2" fill="#cfd3db"/>' for y in range(150, 210, 12))
    shots = "".join(f'<rect x="{x}" y="60" width="44" height="34" rx="3" fill="#b9c0cf"/>' for x in (150, 202, 254))
    cb = S(f'<rect width="400" height="300" fill="#e9ebef"/><rect x="112" y="40" width="200" height="220" rx="6" fill="#fff" stroke="#c3c7d0" stroke-width="2"/>{shots}{lines}{badge("케이스 뒤")}{wm()}')
    game = S(f'<rect width="400" height="300" rx="14" fill="#12111c"/><rect x="26" y="26" width="348" height="180" rx="4" fill="#0b1030"/>'
        f'<rect x="40" y="150" width="308" height="44" rx="6" fill="#1b2660" stroke="#3a56b0" stroke-width="2"/><rect x="52" y="162" width="200" height="6" rx="3" fill="#9fb0e6"/><rect x="52" y="176" width="150" height="6" rx="3" fill="#6d80c4"/>'
        f'<text x="200" y="285" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#fff" opacity="0.5">실기 구동 · 세이브 정상</text>{badge("구동 화면")}')
    return [("디스크", d), ("케이스 앞", cf), ("케이스 뒤", cb), ("구동 화면", game)]

def device(sku, name):
    vents = "".join(f'<rect x="{x}" y="150" width="6" height="60" rx="3" fill="#c9b8a0"/>' for x in range(120, 290, 14))
    front = S(f'<defs><linearGradient id="cb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4efe6"/><stop offset="1" stop-color="#e7e0d3"/></linearGradient></defs>'
        f'<rect width="400" height="300" fill="url(#cb)"/><rect x="70" y="120" width="260" height="120" rx="12" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>'
        f'<rect x="120" y="98" width="160" height="34" rx="6" fill="#3a352c"/>{vents}<circle cx="300" cy="150" r="9" fill="{hue(sku)}"/>{badge("정면")}{wm()}')
    back = S(f'<rect width="400" height="300" fill="#efe9dd"/><rect x="70" y="120" width="260" height="120" rx="12" fill="#d3c9b5" stroke="#a89d85" stroke-width="2"/>'
        f'<rect x="100" y="150" width="46" height="30" rx="4" fill="#3a352c"/><rect x="176" y="150" width="46" height="30" rx="4" fill="#3a352c"/><circle cx="280" cy="165" r="14" fill="#3a352c"/>{badge("후면")}{wm()}')
    cable = S(f'<rect width="400" height="300" fill="#33312c"/><rect x="150" y="90" width="100" height="60" rx="8" fill="#4a463d" stroke="#6b6456" stroke-width="2"/>'
        f'<path d="M200 150 C 200 200 300 200 300 250" stroke="#1e1c18" stroke-width="10" fill="none"/><path d="M200 150 C 200 200 100 200 100 250" stroke="#1e1c18" stroke-width="10" fill="none"/>'
        f'<rect x="86" y="248" width="28" height="18" rx="3" fill="#d4af37"/>{badge("단자·케이블",False)}{wm(True)}')
    def pad(x):
        return (f'<rect x="{x}" y="150" width="90" height="56" rx="10" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>'
                f'<rect x="{x+14}" y="168" width="10" height="26" fill="#3a352c"/><rect x="{x+9}" y="176" width="20" height="10" fill="#3a352c"/><circle cx="{x+66}" cy="178" r="7" fill="{hue(sku)}"/>')
    sset = S(f'<rect width="400" height="300" fill="#efe9dd"/><rect x="130" y="60" width="140" height="66" rx="10" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>{pad(70)}{pad(240)}'
        f'<text x="200" y="250" text-anchor="middle" font-size="12" fill="#7d7563" font-family="sans-serif">본체 + 구성품</text>{badge("구성품")}{wm()}')
    return [("정면", front), ("후면", back), ("단자·케이블", cable), ("구성품", sset)]

def accessory(sku, name):
    c = hue(sku)
    item = S(f'<rect width="400" height="300" fill="#efe9dd"/><rect x="110" y="120" width="180" height="80" rx="20" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>'
        f'<rect x="140" y="145" width="14" height="34" fill="#3a352c"/><rect x="133" y="156" width="28" height="12" fill="#3a352c"/>'
        f'<circle cx="248" cy="162" r="9" fill="{c}"/><circle cx="226" cy="162" r="9" fill="{c}"/>{title_text(name,200,238,"#7d7563",13)}{badge("정면")}{wm()}')
    detail = S(f'<rect width="400" height="300" fill="#33312c"/><circle cx="160" cy="150" r="34" fill="{c}"/><circle cx="240" cy="150" r="34" fill="{c}"/>'
        f'<text x="200" y="230" text-anchor="middle" fill="#e6dfce" font-size="12" font-family="sans-serif">버튼 반응 정상</text>{badge("버튼·상태",False)}{wm(True)}')
    conn = S(f'<rect width="400" height="300" fill="#2a2924"/><path d="M200 60 C 200 150 200 150 200 220" stroke="#1e1c18" stroke-width="12" fill="none"/>'
        f'<rect x="182" y="216" width="36" height="26" rx="4" fill="#d4af37"/>{badge("단자",False)}{wm(True)}')
    sset = S(f'<rect width="400" height="300" fill="#efe9dd"/><rect x="90" y="150" width="90" height="50" rx="16" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/><rect x="220" y="150" width="90" height="50" rx="16" fill="#ddd3bf" stroke="#b7ab92" stroke-width="2"/>'
        f'<text x="200" y="240" text-anchor="middle" font-size="12" fill="#7d7563" font-family="sans-serif">구성품 일체</text>{badge("구성")}{wm()}')
    return [("정면", item), ("버튼·상태", detail), ("단자", conn), ("구성", sset)]

def figure(sku, name):
    c = hue(sku)
    def body(view):
        base = '<ellipse cx="200" cy="252" rx="70" ry="16" fill="#d8d2ea"/>'
        if view == 0:
            b = (f'<circle cx="200" cy="96" r="30" fill="#f2d3b0"/><path d="M170 92 q30-40 60 0 q4 24-30 24 q-34 0-30-24z" fill="#5b3a2e"/>'
                 f'<rect x="176" y="126" width="48" height="86" rx="18" fill="{c}"/><rect x="150" y="132" width="20" height="66" rx="10" fill="{c}"/><rect x="230" y="132" width="20" height="66" rx="10" fill="{c}"/>'
                 f'<rect x="182" y="208" width="14" height="44" rx="7" fill="#3b3350"/><rect x="204" y="208" width="14" height="44" rx="7" fill="#3b3350"/><circle cx="190" cy="94" r="3" fill="#333"/><circle cx="210" cy="94" r="3" fill="#333"/>')
        elif view == 1:
            b = (f'<circle cx="200" cy="96" r="30" fill="#f2d3b0"/><path d="M172 96 q28-44 56 -2 q-2 26-40 22 q-20-2-16-20z" fill="#5b3a2e"/>'
                 f'<rect x="184" y="126" width="40" height="86" rx="18" fill="{c}"/><rect x="196" y="208" width="16" height="44" rx="8" fill="#3b3350"/><circle cx="216" cy="94" r="3" fill="#333"/>')
        else:
            b = (f'<circle cx="200" cy="96" r="30" fill="#5b3a2e"/><rect x="176" y="126" width="48" height="86" rx="18" fill="{c}"/>'
                 f'<rect x="182" y="208" width="14" height="44" rx="7" fill="#3b3350"/><rect x="204" y="208" width="14" height="44" rx="7" fill="#3b3350"/>')
        return (f'<defs><linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3f0fb"/><stop offset="1" stop-color="#e2dcf3"/></linearGradient></defs><rect width="400" height="300" fill="url(#fg)"/>{base}{b}')
    box = S(f'<rect width="400" height="300" fill="#efe9dd"/><rect x="120" y="46" width="160" height="208" rx="8" fill="#2b2740" stroke="#1b1830" stroke-width="2"/><rect x="138" y="90" width="124" height="130" rx="4" fill="#cfe6ff" opacity="0.9"/>'
        f'<circle cx="200" cy="130" r="18" fill="#f2d3b0"/><rect x="186" y="150" width="28" height="46" rx="10" fill="{c}"/>{title_text(name,200,74,"#fff",13)}{badge("박스")}{wm()}')
    return [("정면", S(body(0) + badge("정면") + wm())), ("측면", S(body(1) + badge("측면") + wm())),
            ("후면", S(body(2) + badge("후면") + wm())), ("박스", box)]

def plush(sku, name):
    ring = '<circle cx="200" cy="52" r="20" fill="none" stroke="#c9a24a" stroke-width="6"/><rect x="196" y="70" width="8" height="26" rx="4" fill="#c9a24a"/>'
    c = hue(sku)
    fr = S(f'<rect width="400" height="300" fill="#fff2f8"/>{ring}<ellipse cx="200" cy="180" rx="66" ry="58" fill="#fff" stroke="#e6d9ef" stroke-width="2"/>'
        f'<ellipse cx="152" cy="152" rx="15" ry="28" fill="#fff" stroke="#e6d9ef" stroke-width="2"/><ellipse cx="248" cy="152" rx="15" ry="28" fill="#fff" stroke="#e6d9ef" stroke-width="2"/>'
        f'<circle cx="184" cy="176" r="5" fill="#5a4a6a"/><circle cx="216" cy="176" r="5" fill="#5a4a6a"/><ellipse cx="200" cy="192" rx="9" ry="5" fill="{c}"/>{badge("정면")}{wm()}')
    bk = S(f'<rect width="400" height="300" fill="#fbeff6"/>{ring}<ellipse cx="200" cy="180" rx="66" ry="58" fill="#f3ecf7" stroke="#e0d3ea" stroke-width="2"/><rect x="182" y="200" width="36" height="14" rx="5" fill="#e6d9ef"/>{badge("후면")}{wm()}')
    bars = "".join(f'<rect x="{x}" y="150" width="{3 if i%2 else 2}" height="40" fill="#222"/>' for i, x in enumerate(range(150, 250, 5)))
    tag = S(f'<rect width="400" height="300" fill="#fbf1f6"/><path d="M160 60 h120 v170 h-120 z" fill="#fff" stroke="#e2c9d6" stroke-width="2"/><circle cx="200" cy="76" r="7" fill="none" stroke="#c98aa8" stroke-width="3"/>'
        f'<text x="220" y="112" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="13" fill="#b83280">정품 택</text>{bars}{badge("정품 택")}{wm()}')
    size = S(f'<rect width="400" height="300" fill="#fff2f8"/><ellipse cx="170" cy="170" rx="54" ry="50" fill="#fff" stroke="#e6d9ef" stroke-width="2"/><rect x="250" y="70" width="30" height="190" fill="#fff7c2" stroke="#e0c96a"/>'
        + "".join(f'<line x1="250" y1="{y}" x2="{264 if i%5 else 280}" y2="{y}" stroke="#c9a24a" stroke-width="2"/>' for i, y in enumerate(range(80, 262, 10)))
        + f'<text x="300" y="180" font-family="sans-serif" font-size="12" fill="#8a6a1a" font-weight="700">사이즈</text>{badge("사이즈")}{wm()}')
    return [("정면", fr), ("후면", bk), ("정품 택", tag), ("사이즈", size)]

def book(sku, name):
    c = hue(sku)
    cover = S(f'<rect width="400" height="300" fill="#efe9e2"/><rect x="132" y="46" width="140" height="208" rx="4" fill="{c}"/><rect x="132" y="46" width="10" height="208" fill="#00000022"/>'
        f'<rect x="152" y="150" width="100" height="4" fill="#ffffffcc"/>{title_text(name,206,120,"#fff")}<text x="206" y="230" text-anchor="middle" font-size="10" fill="#ffffffcc" font-family="sans-serif">자가출판 · 초판</text>{badge("표지")}{wm()}')
    lines = "".join(f'<rect x="{x1}" y="{y}" width="70" height="4" rx="2" fill="#c9c3b8"/>' for x1 in (70, 226) for y in range(110, 200, 14))
    spread = S(f'<rect width="400" height="300" fill="#e7e1d5"/><rect x="60" y="80" width="280" height="150" rx="4" fill="#fff" stroke="#cbc3b2"/><line x1="200" y1="80" x2="200" y2="230" stroke="#d8d0c0" stroke-width="2"/>'
        f'<rect x="80" y="98" width="90" height="60" rx="3" fill="#dfe6d6"/>{lines}{badge("펼침면")}{wm()}')
    detail = S(f'<rect width="400" height="300" fill="#fff"/><rect x="60" y="60" width="280" height="180" rx="4" fill="#f4efe6"/>'
        + "".join(f'<rect x="90" y="{y}" width="220" height="5" rx="2" fill="#cbc3b2"/>' for y in range(90, 210, 16))
        + f'{badge("디테일")}{wm()}')
    stack = S(f'<rect width="400" height="300" fill="#efe9e2"/>'
        + "".join(f'<rect x="{110+i*6}" y="{70+i*26}" width="180" height="20" rx="3" fill="{c}" opacity="{0.6+i*0.12}"/>' for i in range(3))
        + f'<text x="200" y="250" text-anchor="middle" font-size="12" fill="#7d7563" font-family="sans-serif">소량 발행</text>{badge("여러 권")}{wm()}')
    return [("표지", cover), ("펼침면", spread), ("디테일", detail), ("여러 권", stack)]

def media(sku, name):
    c = hue(sku)
    cf = S(f'<rect width="400" height="300" fill="#e9ebef"/><rect x="130" y="46" width="140" height="200" rx="4" fill="#12111c"/><rect x="146" y="64" width="108" height="120" rx="3" fill="{c}"/>{title_text(name,200,120,"#fff")}'
        f'<text x="200" y="210" text-anchor="middle" font-size="11" fill="#cfcfd8" font-family="sans-serif">BLU-RAY · 초회한정</text>{badge("케이스 앞")}{wm()}')
    d = S(f'<rect width="400" height="300" fill="#26252b"/><defs><radialGradient id="m" cx="0.4" cy="0.35"><stop offset="0" stop-color="#eef"/><stop offset="1" stop-color="#99a"/></radialGradient></defs><circle cx="200" cy="150" r="92" fill="url(#m)" stroke="#7b7b86"/><circle cx="200" cy="150" r="26" fill="#26252b"/>{badge("디스크",False)}{wm(True)}')
    cb = S(f'<rect width="400" height="300" fill="#dfe1e6"/><rect x="120" y="46" width="160" height="200" rx="4" fill="#fff" stroke="#c3c7d0"/>'
        + "".join(f'<rect x="140" y="{y}" width="120" height="5" rx="2" fill="#cfd3db"/>' for y in range(150, 210, 12))
        + f'{badge("케이스 뒤")}{wm()}')
    book_ = S(f'<rect width="400" height="300" fill="#efeae0"/><rect x="120" y="70" width="160" height="160" rx="4" fill="#fff" stroke="#cbc3b2"/><rect x="140" y="90" width="120" height="70" rx="3" fill="{c}" opacity="0.7"/>'
        + "".join(f'<rect x="140" y="{y}" width="120" height="4" rx="2" fill="#cbc3b2"/>' for y in range(172, 214, 12))
        + f'<text x="200" y="255" text-anchor="middle" font-size="11" fill="#7d7563" font-family="sans-serif">특전 부클릿</text>{badge("부클릿")}{wm()}')
    return [("케이스 앞", cf), ("디스크", d), ("케이스 뒤", cb), ("부클릿", book_)]

def goods(sku, name):
    c = hue(sku)
    fr = S(f'<rect width="400" height="300" fill="#f3eef7"/><rect x="120" y="50" width="160" height="200" rx="10" fill="#fff" stroke="#e0d6ea" stroke-width="2"/><rect x="120" y="50" width="160" height="46" rx="10" fill="{c}"/>'
        f'<rect x="146" y="118" width="108" height="80" rx="6" fill="{c}" opacity="0.18"/>{title_text(name,200,166,"#3b2f8f",13)}<text x="200" y="82" text-anchor="middle" font-size="12" fill="#fff" font-weight="700" font-family="sans-serif">OFFICIAL</text>{badge("정면")}{wm()}')
    bk = S(f'<rect width="400" height="300" fill="#efe9f3"/><rect x="120" y="50" width="160" height="200" rx="10" fill="#f6f1fa" stroke="#ddd2e8" stroke-width="2"/>'
        + "".join(f'<rect x="146" y="{y}" width="108" height="5" rx="2" fill="#d8cee6"/>' for y in range(90, 200, 16))
        + f'{badge("후면")}{wm()}')
    detail = S(f'<rect width="400" height="300" fill="{c}"/><rect x="90" y="90" width="220" height="120" rx="10" fill="#ffffff33"/><circle cx="200" cy="150" r="42" fill="#ffffff55"/>{badge("디테일",False)}{wm(True)}')
    sset = S(f'<rect width="400" height="300" fill="#f3eef7"/>'
        + "".join(f'<rect x="{80+i*70}" y="{110+(i%2)*20}" width="56" height="80" rx="8" fill="{c}" opacity="{0.5+i*0.15}"/>' for i in range(3))
        + f'<text x="200" y="240" text-anchor="middle" font-size="12" fill="#7d5b9a" font-family="sans-serif">구성 일체</text>{badge("구성")}{wm()}')
    return [("정면", fr), ("후면", bk), ("디테일", detail), ("구성", sset)]

# ---------- 분류 ----------
def kind_of(sku, name, chips, cat):
    txt = name + " " + " ".join(chips)
    if cat == "retro":
        pref = sku.split("-")[0]
        if "본체" in txt:
            return device
        if ("기판" in name or "하네스" in name or "주변기기" in txt or sku.startswith("ac-")
                or any(k in name for k in ("컨트롤러", "어댑터", "컨버터", "메모리카드", "패드"))):
            return accessory
        if pref in ("ps1", "ps2", "ss", "dc", "gc") or (pref == "pce" and "CD" in txt):
            return disc
        return cartridge
    if cat in ("anime", "character"):
        if "figure" in sku or "피규어" in name:
            return figure
        if any(k in name for k in ("인형", "키링", "쿠션", "플러시")):
            return plush
        if any(k in name for k in ("블루레이", "OST", "CD")):
            return media
        return goods
    if cat == "doujin":
        return book
    return goods

# ---------- 상품 수집 ----------
items = {}  # sku -> (name, chips, cat)
for p in PLATFORMS:
    for (name, sku, price, grade, chips, meta, stock) in p["products"]:
        items[sku] = (name, chips, "retro")
CATMAP = {"character-goods": "character", "doujin": "doujin", "anime-goods": "anime"}
for c in CATEGORIES:
    cat = CATMAP[c["slug"]]
    for s in c["subs"]:
        for (name, sku, price, cond, chips, meta, stock) in s["products"]:
            items[sku] = (name, chips, cat)

# ---------- 이미지 생성 ----------
labels_by_sku = {}
made = 0
for sku, (name, chips, cat) in items.items():
    fn = kind_of(sku, name, chips, cat)
    scenes = fn(sku, name)
    labels_by_sku[sku] = [lab for lab, _ in scenes]
    if sku in DONE:
        continue  # 이미 수작업본 보존
    for i, (lab, s) in enumerate(scenes, 1):
        open(os.path.join("img", f"{sku}-{i}.svg"), "w", encoding="utf-8").write(s)
        made += 1

# ---------- 갤러리 배선 ----------
JS = ('<style>.thumbs img,.gthumbs img{aspect-ratio:1;width:100%;object-fit:cover;border:1px solid var(--line);'
      'border-radius:8px;cursor:pointer;background:#efe9dd}.thumbs img.on,.gthumbs img.on{border:2px solid var(--brand)}'
      '.thumbs img:hover,.gthumbs img:hover{border-color:var(--brand)}</style>'
      '<script>function pmset(el){var m=document.getElementById("pmain");m.src=el.src;m.alt=el.alt;'
      'document.querySelectorAll(".thumbs img,.gthumbs img").forEach(function(i){i.classList.remove("on")});el.classList.add("on")}</script>')
wired = 0
for sku, labs in labels_by_sku.items():
    if sku in DONE:
        continue
    f = f"product-{sku}.html"
    if not os.path.exists(f):
        continue
    s = open(f, encoding="utf-8").read()
    s = s.replace(f'src="img/{sku}.svg"', f'src="img/{sku}-1.svg"', 1)
    s = s.replace('<img class="main" ', '<img class="main" id="pmain" ', 1)
    m = re.search(r'<div class="(g?thumbs)">((?:\s*<div>[^<]*</div>)+)\s*</div>', s)
    if m:
        cls = m.group(1)
        imgs = []
        for i, lab in enumerate(labs, 1):
            on = ' class="on"' if i == 1 else ''
            imgs.append(f'<img src="img/{sku}-{i}.svg" alt="{H.escape(lab)}"{on} onclick="pmset(this)">')
        new = f'<div class="{cls}">\n          ' + "\n          ".join(imgs) + "\n        </div>"
        s = s[:m.start()] + new + s[m.end():]
    if "function pmset" not in s:
        s = s.replace("</main>", JS + "\n</main>", 1)
    open(f, "w", encoding="utf-8").write(s)
    wired += 1

# ---------- 카드 썸네일을 대표(-1)로 통일 ----------
repointed = 0
for f in glob.glob("*.html"):
    s = open(f, encoding="utf-8").read(); o = s
    for sku in items:
        s = s.replace(f'src="img/{sku}.svg"', f'src="img/{sku}-1.svg"')
    if s != o:
        open(f, "w", encoding="utf-8").write(s); repointed += 1

print(f"이미지 생성 {made}개 · 갤러리 배선 {wired}개 · 카드 통일 {repointed}개 파일")
