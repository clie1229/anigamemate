# -*- coding: utf-8 -*-
"""예시: 특정 상품(fc-smb3)에 '여러 장 사진' 갤러리를 시연하기 위한
   저작권 안전 일러스트 이미지 4종 생성 (정면/후면/단자/구동화면).
   실제 판매 시 이 파일들을 실물 촬영본(같은 파일명)으로 교체하면 됨."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("img", exist_ok=True)

WM = ('<text x="200" y="290" text-anchor="middle" font-family="sans-serif" '
      'font-size="11" fill="#000" opacity="0.28" letter-spacing="1">AnigameMate · 예시 이미지</text>')

def badge(label, dark=True):
    fill = "#1b1a2e" if dark else "#ffffff"
    tc = "#ffffff" if dark else "#1b1a2e"
    w = 30 + len(label) * 15
    return (f'<rect x="14" y="14" width="{w}" height="28" rx="14" fill="{fill}" opacity="0.9"/>'
            f'<text x="{14 + w/2}" y="33" text-anchor="middle" fill="{tc}" font-size="14" '
            f'font-family="sans-serif" font-weight="700">{label}</text>')

# 1) 정면 — 카트리지 앞면
front = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-label="슈퍼마리오브라더스 3 (패미컴) 카트리지 정면">
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6f3ec"/><stop offset="1" stop-color="#e7e1d5"/></linearGradient></defs>
<rect width="400" height="300" fill="url(#bg)"/>
<rect x="120" y="46" width="160" height="208" rx="14" fill="#d7d1c4" stroke="#b3aa98" stroke-width="2"/>
<path d="M120 60 q0-14 14-14 h132 q14 0 14 14 v34 h-160 z" fill="#e8543f"/>
<rect x="138" y="106" width="124" height="100" rx="4" fill="#ffffff" stroke="#cbc3b2"/>
<text x="200" y="138" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="15" fill="#3b2f8f">슈퍼마리오</text>
<text x="200" y="160" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="15" fill="#3b2f8f">브라더스 3</text>
<text x="200" y="190" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#8a8271" letter-spacing="2">FAMICOM · HVC</text>
<rect x="150" y="216" width="100" height="24" rx="3" fill="#cfc8b8"/>
{badge("정면")}
{WM}
</svg>
'''

# 2) 후면 — 카트리지 뒷면(리브 패턴)
ribs = "".join(f'<rect x="140" y="{y}" width="120" height="6" rx="3" fill="#b9b1a0"/>' for y in range(120, 210, 16))
back = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-label="카트리지 후면">
<defs><linearGradient id="bg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#efeae0"/><stop offset="1" stop-color="#ddd6c8"/></linearGradient></defs>
<rect width="400" height="300" fill="url(#bg2)"/>
<rect x="120" y="46" width="160" height="208" rx="14" fill="#cfc9bb" stroke="#aca392" stroke-width="2"/>
{ribs}
<rect x="150" y="66" width="100" height="34" rx="4" fill="#c3bba9"/>
<text x="200" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#7d7563">MADE IN JAPAN</text>
<circle cx="140" cy="238" r="5" fill="#9c927d"/><circle cx="260" cy="238" r="5" fill="#9c927d"/>
{badge("후면")}
{WM}
</svg>
'''

# 3) 단자 — 핀 근접
pins = "".join(f'<rect x="{x}" y="150" width="10" height="90" rx="2" fill="#d4af37"/>' for x in range(96, 300, 20))
conn = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-label="카트리지 단자 근접">
<defs><linearGradient id="bg3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#33312c"/><stop offset="1" stop-color="#1f1e1a"/></linearGradient></defs>
<rect width="400" height="300" fill="url(#bg3)"/>
<rect x="80" y="138" width="240" height="116" rx="6" fill="#2a2924"/>
{pins}
<rect x="80" y="138" width="240" height="16" fill="#ffffff" opacity="0.06"/>
<text x="200" y="128" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#e6dfce">단자 세척 완료 · 산화 없음</text>
{badge("단자", dark=False)}
<text x="200" y="290" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#fff" opacity="0.3" letter-spacing="1">AnigameMate · 예시 이미지</text>
</svg>
'''

# 4) 구동 화면 — 일반 플랫포머 화면(특정 IP 아트 아님)
clouds = '<ellipse cx="110" cy="90" rx="26" ry="13" fill="#fff"/><ellipse cx="132" cy="86" rx="18" ry="11" fill="#fff"/><ellipse cx="300" cy="72" rx="22" ry="11" fill="#fff"/>'
qblocks = "".join(f'<rect x="{x}" y="150" width="26" height="26" rx="3" fill="#e8a13f" stroke="#a9611a" stroke-width="2"/><text x="{x+13}" y="169" text-anchor="middle" font-size="16" font-weight="800" fill="#7a3f10">?</text>' for x in (150, 224))
game = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-label="구동 화면 예시">
<rect width="400" height="300" rx="14" fill="#12111c"/>
<rect x="26" y="26" width="348" height="228" rx="6" fill="#5c94fc"/>
{clouds}
<rect x="26" y="214" width="348" height="40" fill="#00a800"/>
<rect x="26" y="214" width="348" height="8" fill="#54c454"/>
{qblocks}
<rect x="196" y="196" width="20" height="20" rx="4" fill="#c23b22"/>
<circle cx="201" cy="203" r="2.4" fill="#fff"/><circle cx="211" cy="203" r="2.4" fill="#fff"/>
<circle cx="320" cy="150" r="9" fill="#ffd93b" stroke="#c99a12" stroke-width="2"/>
{badge("구동 화면")}
<text x="200" y="285" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#fff" opacity="0.4" letter-spacing="1">AnigameMate · 예시 이미지</text>
</svg>
'''

files = {"fc-smb3-1.svg": front, "fc-smb3-2.svg": back, "fc-smb3-3.svg": conn, "fc-smb3-4.svg": game}
for name, svg in files.items():
    open(os.path.join("img", name), "w", encoding="utf-8").write(svg)
print("예시 사진 생성:", ", ".join(files))
