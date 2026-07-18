# -*- coding: utf-8 -*-
"""PS1 크로노 트리거 상품을 실물 사진으로 신규 생성.
   product-ps1-ff7.html을 복제·수정해 product-ps1-ct.html 생성,
   PS1 카테고리(전체/소프트)에 카드 추가, sitemap 등록."""
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PRICE_DISP = "129,000원"
PRICE_NUM = "129000"
COND = "디스크·케이스 양호 · 스퀘어소프트 정품"

src = open("product-ps1-ff7.html", encoding="utf-8").read()

# 1) 갤러리 블록 교체 (실물 사진 + 예시 3컷)
gal_old = '''      <div class="gallery">
        <img class="main" id="pmain" src="img/ps1-ff7-1.svg" alt="대표 이미지" style="width:100%;height:100%;object-fit:cover">
        <div class="thumbs">
          <img src="img/ps1-ff7-1.svg" alt="디스크" class="on" onclick="pmset(this)">
          <img src="img/ps1-ff7-2.svg" alt="케이스 앞" onclick="pmset(this)">
          <img src="img/ps1-ff7-3.svg" alt="케이스 뒤" onclick="pmset(this)">
          <img src="img/ps1-ff7-4.svg" alt="구동 화면" onclick="pmset(this)">
        </div>
        <p class="shot-note">
          모든 사진은 보정 없이 실제 판매 상품을 촬영한 것입니다. 흠집이나 변색도 그대로 담습니다.
        </p>
      </div>'''
gal_new = '''      <div class="gallery">
        <img class="main" id="pmain" src="img/ps1-ct-1.png" alt="크로노 트리거 (PS1) 실물 케이스" style="width:100%;height:100%;object-fit:cover">
        <div class="thumbs">
          <img src="img/ps1-ct-1.png" alt="실물 케이스" class="on" onclick="pmset(this)">
          <img src="img/ps1-ct-2.svg" alt="디스크" onclick="pmset(this)">
          <img src="img/ps1-ct-3.svg" alt="케이스 뒤" onclick="pmset(this)">
          <img src="img/ps1-ct-4.svg" alt="구동 화면" onclick="pmset(this)">
        </div>
        <p class="shot-note">
          1번은 실제 판매 상품을 촬영한 사진입니다. 2~4번은 예시 이미지이며, 추후 실물 사진으로 교체합니다.
        </p>
      </div>'''
assert gal_old in src, "갤러리 블록 매칭 실패"
s = src.replace(gal_old, gal_new)

# 2) 텍스트 치환
s = s.replace("ps1-ff7", "ps1-ct").replace("PS1-FF7", "PS1-CT")
s = s.replace("파이널 판타지 VII", "크로노 트리거")
s = s.replace("디스크 3장 · 케이스 양호", COND)
s = s.replace("45,000원", PRICE_DISP).replace('"45000"', f'"{PRICE_NUM}"')
s = s.replace('content="45000"', f'content="{PRICE_NUM}"')
# og:image / JSON-LD image[0] → 실제 png
s = s.replace("img/ps1-ct-1.jpg", "img/ps1-ct-1.png")

open("product-ps1-ct.html", "w", encoding="utf-8").write(s)
print("생성: product-ps1-ct.html")

# 3) 카테고리 카드 삽입 (전체 + 소프트)
card = '''          <a class="prod" href="product-ps1-ct.html">
            <img class="thumb" src="img/ps1-ct-1.png" alt="크로노 트리거 (PS1) 실물" loading="lazy" style="width:100%;height:100%;object-fit:cover">
            <div class="prod-body">
              <div class="chips"><span class="chip g">A등급</span><span class="chip">동작 확인</span><span class="chip">NTSC-J</span></div>
              <h3>크로노 트리거 (PS1)</h3>
              <p class="meta">''' + COND + '''</p>
              <p class="price">''' + PRICE_DISP + '''</p>
              <span class="btn btn-sm btn-accent" style="text-align:center">바로 구매</span>
            </div>
          </a>

'''
for f in ("retro-games-ps1.html", "retro-games-ps1-software.html"):
    try:
        h = open(f, encoding="utf-8").read()
    except FileNotFoundError:
        print("  없음:", f); continue
    if "product-ps1-ct.html" in h:
        print("  이미 있음:", f); continue
    m = re.search(r'(<div class="prods">\s*\n)', h)
    if m:
        h = h[:m.end()] + "\n" + card + h[m.end():]
        open(f, "w", encoding="utf-8").write(h)
        print("  카드 추가:", f)
    else:
        print("  prods 그리드 못 찾음:", f)

# 4) sitemap 등록
sm = open("sitemap.xml", encoding="utf-8").read()
if "/p/ps1-ct<" not in sm:
    entry = ("  <url>\n    <loc>https://anigamemate.com/p/ps1-ct</loc>\n"
             "    <lastmod>2026-07-18</lastmod>\n    <priority>0.6</priority>\n  </url>\n")
    sm = sm.replace("</urlset>", entry + "</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("sitemap 등록: /p/ps1-ct")
