# -*- coding: utf-8 -*-
"""세가 새턴 실물 재고를 실제 상품으로 생성 (PS1 파일럿과 동일 방식)."""
import os, re, io, sys, html as H
from pathlib import Path
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SRC = Path(r"C:/Business/Goods/Sell/Retro Game/Sega Seturn")
STORE = "https://smartstore.naver.com/anigamemate"
CAT_SLUG = "saturn"
CAT_NAME = "세가 새턴"
BRAND = "Sega"
PLATFORM = "세가 새턴"
SKUP = "sat"
CAT_FILE = f"retro-games-{CAT_SLUG}.html"
CAT_SW = f"retro-games-{CAT_SLUG}-software.html"

GAMES = [
    ("3x3 eyes", "sat-3x3eyes", "3x3 eyes"),
    ("Gun Blaze S", "sat-gunblaze", "Gun Blaze S"),
    ("King Of Fighters 95", "sat-kof95", "King of Fighters '95"),
    ("Slayers Royal 2", "sat-slayers2", "Slayers Royal 2"),
    ("가디언 히어로즈", "sat-guardian", "가디언 히어로즈"),
    ("나이츠", "sat-nights", "나이츠"),
    ("노노무라 병원", "sat-nonomura", "노노무라 병원"),
    ("데이토나 USA", "sat-daytona", "데이토나 USA"),
    ("도키메키 메모리얼", "sat-tokimemo", "도키메키 메모리얼"),
    ("동급생 2", "sat-doukyusei2", "동급생 2"),
    ("동급생 if", "sat-doukyusei-if", "동급생 if"),
    ("디자이어 프리미엄", "sat-desire", "디자이어 프리미엄"),
    ("루나 2", "sat-lunar2", "루나 2"),
    ("마법기사 레이어스", "sat-rayearth", "마법기사 레이어스"),
    ("뱀파이어 헌터", "sat-vampire", "뱀파이어 헌터"),
    ("스내쳐", "sat-snatcher", "스내쳐"),
    ("아스카 120%", "sat-asuka120", "아스카 120%"),
    ("은하 아가씨 전설 유나", "sat-yuna", "은하 아가씨 전설 유나"),
    ("킹오브 파이터즈", "sat-kof", "킹 오브 파이터즈"),
    ("탄생S", "sat-tanjyo", "탄생 S"),
    ("통곡 그리고 파이널 에디션", "sat-tsuukoku", "통곡 그리고 파이널 에디션"),
    ("팬저 드래곤", "sat-panzer", "팬저 드래곤"),
    ("하급생", "sat-kakyusei", "하급생"),
]

ff7 = open("product-ps1-ff7.html", encoding="utf-8").read()
CSS = re.search(r"<style>.*?</style>", ff7, re.S).group(0)
HEADER = re.search(r"<header>.*?</header>", ff7, re.S).group(0)
FOOTER = re.search(r"<footer>.*?</footer>", ff7, re.S).group(0)
FOOTER = FOOTER.replace("플레이스테이션 및 각 게임 타이틀의", f"{PLATFORM} 및 각 게임 타이틀의")

GALLERY_JS = ('<style>.thumbs img{aspect-ratio:1;width:100%;object-fit:cover;border:1px solid var(--line);'
              'border-radius:8px;cursor:pointer;background:#efe9dd}.thumbs img.on{border:2px solid var(--brand)}'
              '.thumbs img:hover{border-color:var(--brand)}</style>'
              '<script>function pmset(el){var m=document.getElementById("pmain");m.src=el.src;m.alt=el.alt;'
              'document.querySelectorAll(".thumbs img").forEach(function(i){i.classList.remove("on")});el.classList.add("on")}</script>')


def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def current_photos(folder):
    dated = sorted([d for d in folder.iterdir() if d.is_dir() and re.fullmatch(r"\d{8}", d.name)], key=lambda d: d.name)
    base = dated[-1] if dated else folder
    files = [f for f in base.iterdir() if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png")]
    numeric = sorted([f for f in files if re.fullmatch(r"\d+(_\d+)?", f.stem)], key=lambda f: natkey(f.stem))
    others = sorted([f for f in files if f not in numeric], key=lambda f: natkey(f.stem))
    return (numeric + others)[:6]


def save_resized(src_path, dst_path, maxside=1100, q=82):
    im = Image.open(src_path)
    if im.mode in ("RGBA", "P", "LA"):
        im = im.convert("RGB")
    w, h = im.size
    if max(w, h) > maxside:
        r = maxside / max(w, h)
        im = im.resize((round(w * r), round(h * r)), Image.LANCZOS)
    im.save(dst_path, "JPEG", quality=q, optimize=True)
    return os.path.getsize(dst_path)


def gallery_html(sku, name, n):
    parts = []
    for i in range(1, n + 1):
        on = ' class="on"' if i == 1 else ''
        parts.append(f'          <img src="img/{sku}-{i}.jpg" alt="{H.escape(name)} 사진 {i}"{on} onclick="pmset(this)">')
    thumbs = "\n".join(parts)
    return f'''      <div class="gallery">
        <img class="main" id="pmain" src="img/{sku}-1.jpg" alt="{H.escape(name)} 실물" style="width:100%;height:100%;object-fit:cover">
        <div class="thumbs">
{thumbs}
        </div>
        <p class="shot-note">실제 판매 상품을 촬영한 사진입니다. 상태·구성은 사진으로 확인하시고, 가격·재고는 문의해 주세요.</p>
      </div>'''


def product_page(sku, name, n):
    url = f"https://anigamemate.com/p/{sku}"
    img0 = f"https://anigamemate.com/img/{sku}-1.jpg"
    title = f"{name} ({PLATFORM}) 중고 | AnigameMate"
    desc = f"{PLATFORM} {name} 중고. 실물 사진으로 상태 확인. 가격·재고는 문의(스마트스토어). 일본판(NTSC-J)."
    images = ",\n    ".join(f'"https://anigamemate.com/img/{sku}-{i}.jpg"' for i in range(1, n + 1))
    ld_product = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{H.escape(name)} ({PLATFORM})",
  "description": "{PLATFORM}용 중고 게임. 실물 사진으로 상태를 확인하실 수 있습니다. 가격·재고는 문의 바랍니다.",
  "sku": "{sku.upper()}",
  "url": "{url}",
  "image": [
    {images}
  ],
  "itemCondition": "https://schema.org/UsedCondition",
  "category": "레트로게임 중고 > {PLATFORM} > 소프트",
  "brand": {{ "@type": "Brand", "name": "{BRAND}" }},
  "gamePlatform": "{PLATFORM}",
  "offers": {{
    "@type": "Offer",
    "url": "{url}",
    "priceCurrency": "KRW",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/UsedCondition",
    "seller": {{ "@type": "Organization", "name": "AnigameMate" }}
  }}
}}
</script>'''
    ld_crumb = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "홈", "item": "https://anigamemate.com/" }},
    {{ "@type": "ListItem", "position": 2, "name": "레트로게임 중고", "item": "https://anigamemate.com/retro-games" }},
    {{ "@type": "ListItem", "position": 3, "name": "{PLATFORM}", "item": "https://anigamemate.com/retro-games/{CAT_SLUG}" }},
    {{ "@type": "ListItem", "position": 4, "name": "{H.escape(name)}", "item": "{url}" }}
  ]
}}
</script>'''
    body = f'''<main>
  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼">
      <a href="index.html">홈</a> › <a href="retro-games.html">레트로게임 중고</a> ›
      <a href="{CAT_FILE}">{PLATFORM}</a> › <span aria-current="page">{H.escape(name)}</span>
    </nav>

    <div class="hero">

{gallery_html(sku, name, n)}

      <div id="buy">
        <div class="chips"><span class="chip">중고</span><span class="chip ok">실물 사진</span><span class="chip">NTSC-J</span></div>

        <h1>{H.escape(name)} ({PLATFORM})</h1>
        <p class="sku mono">SKU {sku.upper()} · {PLATFORM}</p>

        <div class="price-box">
          <p class="price" style="font-size:26px">가격문의</p>
          <p class="ship">배송비 3,500원 · 가격·재고는 스마트스토어 또는 문의로 확인해 주세요</p>
          <p class="stock"><span class="dot" aria-hidden="true"></span>중고 단일 상품 · 실물 사진 기준</p>
        </div>

        <div class="buy">
          <a class="btn btn-accent" href="{STORE}" target="_blank" rel="noopener noreferrer">스마트스토어에서 구매</a>
          <a class="btn btn-ghost" href="board.html">문의하기</a>
        </div>

        <div class="guard">
          <strong>실물 사진 그대로</strong>
          보정 없이 실제 판매 상품을 촬영했습니다. 상태·구성은 사진으로 확인하시고, 궁금한 점은 문의해 주세요.
        </div>
      </div>

    </div>
  </div>

  <section id="spec">
    <div class="wrap">
      <h2 class="title">상품 정보</h2>
      <p class="sub">정확한 상태·구성은 실물 사진과 문의로 확인해 주세요</p>
      <table>
        <tbody>
          <tr><th scope="row">상품 상태</th><td>중고 · 실물 사진 참조</td></tr>
          <tr><th scope="row">구성품</th><td>실물 사진 참조</td></tr>
          <tr><th scope="row">동작 확인</th><td>구매 전 문의</td></tr>
          <tr><th scope="row">지역코드</th><td>NTSC-J (일본판)</td></tr>
          <tr><th scope="row">기종</th><td><a href="{CAT_FILE}" style="color:var(--brand);font-weight:600">{PLATFORM}</a></td></tr>
          <tr><th scope="row">유통 구분</th><td>중고 · 개인 매입</td></tr>
          <tr><th scope="row">상품번호(SKU)</th><td class="mono">{sku.upper()}</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section id="desc" style="background:#f4efe5">
    <div class="wrap">
      <div class="desc">
        <h2 style="font-size:20px;margin-bottom:10px">상품 설명</h2>
        <p>{PLATFORM}용 <strong>{H.escape(name)}</strong> 중고입니다. 위 갤러리는 보정 없이 실제 판매 상품을 촬영한 사진입니다.</p>
        <p>상태·구성품은 사진으로 확인하시고, 가격과 재고는 <a href="{STORE}" target="_blank" rel="noopener noreferrer">스마트스토어</a> 또는 <a href="board.html">문의 게시판</a>으로 확인해 주세요. 일본판(NTSC-J)으로 국내 유통 본체 호환 여부는 문의 바랍니다.</p>
      </div>
    </div>
  </section>

  <section id="related">
    <div class="wrap">
      <h2 class="title">함께 보는 {PLATFORM}</h2>
      <nav class="related" style="display:flex;gap:10px;flex-wrap:wrap">
        <a class="rel" href="{CAT_FILE}" style="background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:9px 18px;font-size:14px">{PLATFORM} 전체 보기</a>
        <a class="rel" href="{CAT_SW}" style="background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:9px 18px;font-size:14px">{PLATFORM} 소프트</a>
      </nav>
    </div>
  </section>
{GALLERY_JS}
</main>'''
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="AnigameMate">
<meta property="og:title" content="{H.escape(name)} ({PLATFORM}) 중고">
<meta property="og:description" content="실물 사진으로 상태 확인 · 가격/재고 문의">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img0}">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">

{ld_product}
{ld_crumb}

{CSS}
</head>
<body>

{HEADER}

{body}

{FOOTER}

</body>
</html>
'''


def card_html(sku, name):
    return f'''          <a class="prod" href="product-{sku}.html">
            <img class="thumb" src="img/{sku}-1.jpg" alt="{H.escape(name)} 실물" loading="lazy" style="width:100%;height:100%;object-fit:cover">
            <div class="prod-body">
              <div class="chips"><span class="chip">중고</span><span class="chip">실물 사진</span><span class="chip">NTSC-J</span></div>
              <h3>{H.escape(name)} ({PLATFORM})</h3>
              <p class="meta">실물 사진 · 일본판</p>
              <p class="price" style="font-size:15px">가격문의</p>
              <span class="btn btn-sm btn-accent" style="text-align:center">보기</span>
            </div>
          </a>'''


def upsert_card(fname, sku, name):
    if not os.path.exists(fname):
        print("  카테고리 파일 없음:", fname); return
    h = open(fname, encoding="utf-8").read()
    card = card_html(sku, name)
    pat = re.compile(r'          <a class="prod" href="product-' + re.escape(sku) + r'\.html">.*?</a>\n', re.S)
    if pat.search(h):
        h = pat.sub(card + "\n", h, count=1)
    else:
        m = re.search(r'(<div class="prods">\s*\n)', h)
        if not m:
            print("  prods 그리드 못 찾음:", fname); return
        h = h[:m.end()] + "\n" + card + "\n\n" + h[m.end():]
    open(fname, "w", encoding="utf-8").write(h)


def main():
    total = 0; made = []
    for folder, sku, name in GAMES:
        gdir = SRC / folder
        if not gdir.is_dir():
            print("  폴더 없음:", folder); continue
        photos = current_photos(gdir)
        if not photos:
            print("  사진 없음(건너뜀):", folder); continue
        n = 0
        for i, p in enumerate(photos, 1):
            total += save_resized(str(p), os.path.join("img", f"{sku}-{i}.jpg")); n = i
        open(f"product-{sku}.html", "w", encoding="utf-8").write(product_page(sku, name, n))
        upsert_card(CAT_FILE, sku, name)
        upsert_card(CAT_SW, sku, name)
        made.append((sku, name, n))
        print(f"  ✓ {name}  ({n}장, sku={sku})")

    sm = open("sitemap.xml", encoding="utf-8").read()
    add = "".join(
        f"  <url>\n    <loc>https://anigamemate.com/p/{sku}</loc>\n    <lastmod>2026-07-19</lastmod>\n    <priority>0.6</priority>\n  </url>\n"
        for sku, name, n in made if f"/p/{sku}<" not in sm)
    if add:
        open("sitemap.xml", "w", encoding="utf-8").write(sm.replace("</urlset>", add + "</urlset>"))
    print(f"\n생성 {len(made)}개 상품 · 이미지 총 {total//1024}KB · sitemap 갱신")


if __name__ == "__main__":
    main()
