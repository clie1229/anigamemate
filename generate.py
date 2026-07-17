#!/usr/bin/env python3
"""
AnigameMate — 레트로게임 기종 페이지 생성기

사용법:
    python3 generate.py

platforms.py의 PLATFORMS 데이터를 읽어 retro-games-<slug>.html 19개를 생성합니다.
기종을 추가하거나 문구를 고치려면 platforms.py만 수정하고 다시 실행하세요.

생성물에 포함되는 것
  - title/description/canonical/OG/Twitter
  - BreadcrumbList + ItemList(Product·Offer) + FAQPage JSON-LD
  - AEO 답변 블록, 상품유형 탭, 필터 사이드바, 상품 그리드
  - 상태 등급표, 기종 소개, FAQ, 관련 기종 내부링크
"""

import html
import json
import re
from pathlib import Path

from platforms import PLATFORMS, PLATFORM_BY_SLUG

BASE = "https://anigamemate.com"
OUT = Path(__file__).parent

GRADE_ROWS = [
    ("S", "미개봉 또는 사용감 거의 없음", "박스·설명서 완비", "확인 완료"),
    ("A", "경미한 사용감, 라벨 온전", "박스 또는 설명서 일부", "확인 완료"),
    ("B", "흠집·변색 있음, 플레이 지장 없음", "본품만", "확인 완료"),
    ("부품용", "상태 무관", "본품만", "미동작 (제목에 명시)"),
]

FILTERS = [
    ("상태 등급", "grade", [("S", "S · 미개봉/최상"), ("A", "A · 경미한 사용감"),
                          ("B", "B · 흠집 있음"), ("parts", "부품용 (미동작)")]),
    ("구성품", "set", [("full", "박스풀셋"), ("box", "박스만"), ("rom", "본품만")]),
    ("지역코드", "region", [("ntsc-j", "NTSC-J (일본판)"), ("ntsc-u", "NTSC-U (북미판)"),
                          ("kr", "한글판 / 국내판")]),
    ("동작 확인", "work", [("ok", "확인 완료"), ("no", "부품용(미동작)")]),
    ("장르", "genre", [("action", "액션"), ("rpg", "RPG"), ("shooting", "슈팅"),
                      ("sports", "스포츠"), ("puzzle", "퍼즐")]),
    ("가격대", "price", [("0-30000", "~3만원"), ("30000-100000", "3~10만원"),
                       ("100000-300000", "10~30만원"), ("300000-", "30만원~")]),
]

TYPE_TABS = [("software", "소프트"), ("console", "본체"),
             ("accessories", "주변기기"), ("parts", "부품·수리용")]

CSS = """  :root{
    --bg:#fbf7f0; --surface:#ffffff; --ink:#1b1a2e; --muted:#5d5b78;
    --brand:#3b2f8f; --brand-dark:#241c63; --accent:#e8543f; --accent-soft:#fdeeea;
    --line:#e6e0d6; --radius:14px;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
    color:var(--ink);background:var(--bg);line-height:1.7;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px}
  a{color:inherit;text-decoration:none}
  .mono{font-family:ui-monospace,SFMono-Regular,"D2Coding",Consolas,monospace}
  .btn{display:inline-block;background:var(--brand);color:#fff;font-weight:600;
    padding:15px 30px;border-radius:10px;font-size:17px;border:none;cursor:pointer;transition:background .2s}
  .btn:hover{background:var(--brand-dark)}
  .btn-accent{background:var(--accent)}
  .btn-accent:hover{background:#c8412e}
  .btn-sm{padding:9px 16px;font-size:14px;border-radius:8px}
  header{position:sticky;top:0;z-index:50;background:rgba(251,247,240,.94);
    backdrop-filter:blur(8px);border-bottom:2px solid var(--ink)}
  .nav{display:flex;align-items:center;justify-content:space-between;height:66px;gap:16px}
  .logo{font-weight:800;font-size:20px;color:var(--brand);letter-spacing:-.02em;white-space:nowrap}
  .logo span{color:var(--accent)}
  .nav-links{display:flex;gap:18px;align-items:center;font-size:15px}
  .nav .btn{padding:10px 18px;font-size:15px}
  .crumb{padding:18px 0 0;font-size:14px;color:var(--muted)}
  .crumb a:hover{color:var(--brand)}
  .head{padding:30px 0 8px}
  h1{font-size:clamp(28px,5vw,42px);line-height:1.2;letter-spacing:-.03em;font-weight:800;margin-bottom:10px}
  .lead{font-size:17px;color:var(--muted);max-width:680px}
  .answer{background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);
    padding:24px 26px;margin:26px 0 0;max-width:820px}
  .answer h2{font-size:18px;margin-bottom:8px;color:var(--brand)}
  .answer p{color:var(--muted)}
  .tabs{display:flex;gap:10px;flex-wrap:wrap;margin:34px 0 0}
  .tab{background:var(--surface);border:2px solid var(--ink);border-radius:10px;
    padding:11px 20px;font-weight:600;font-size:15px}
  .tab[aria-current="true"]{background:var(--ink);color:#fff}
  .tab:hover{border-color:var(--brand)}
  section{padding:40px 0}
  h2.title{font-size:clamp(21px,3.2vw,28px);letter-spacing:-.02em;margin-bottom:6px;font-weight:800}
  .sub{color:var(--muted);margin-bottom:26px}
  .layout{display:grid;grid-template-columns:250px 1fr;gap:28px;align-items:start}
  .filters{background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);padding:22px;
    position:sticky;top:86px}
  .filters h3{font-size:16px;margin-bottom:4px}
  .filters .hint{font-size:12px;color:var(--muted);margin-bottom:18px;line-height:1.5}
  fieldset{border:none;margin-bottom:18px;padding-bottom:16px;border-bottom:1px solid var(--line)}
  fieldset:last-of-type{border-bottom:none;margin-bottom:8px}
  legend{font-size:13px;font-weight:700;color:var(--brand);margin-bottom:8px;letter-spacing:.02em}
  .opt{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--muted);padding:3px 0;cursor:pointer}
  .opt input{width:15px;height:15px;accent-color:var(--brand);cursor:pointer}
  .prods{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  .prod{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden;
    display:flex;flex-direction:column;transition:border-color .15s,transform .15s}
  .prod:hover{border-color:var(--brand);transform:translateY(-2px)}
  .thumb{aspect-ratio:4/3;background:#efe9dd;display:flex;align-items:center;justify-content:center;
    border-bottom:1px solid var(--line);color:#a89f8d;font-size:12px;letter-spacing:.06em}
  .prod-body{padding:16px 16px 18px;display:flex;flex-direction:column;flex:1}
  .chips{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px}
  .chip{font-size:11px;font-weight:700;padding:3px 7px;border-radius:5px;background:#eee9f7;color:var(--brand)}
  .chip.g{background:var(--accent-soft);color:var(--accent)}
  .chip.off{background:#eceaf0;color:var(--muted)}
  .prod h3{font-size:15px;line-height:1.45;margin-bottom:6px;flex:1}
  .meta{font-size:12px;color:var(--muted);margin-bottom:10px;line-height:1.6}
  .price{font-size:19px;font-weight:800;letter-spacing:-.02em;margin-bottom:12px}
  .price.soldout{color:var(--muted)}
  table{width:100%;border-collapse:collapse;background:var(--surface);border:2px solid var(--ink);
    border-radius:var(--radius);overflow:hidden}
  caption{caption-side:top;text-align:left;color:var(--muted);font-size:14px;padding-bottom:10px}
  th,td{padding:13px 16px;text-align:left;border-bottom:1px solid var(--line);font-size:14px}
  thead th{background:var(--ink);color:#fff;font-weight:600}
  tbody tr:last-child td{border-bottom:none}
  .grade{font-weight:800;color:var(--accent)}
  .about{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:28px 30px;
    max-width:820px}
  .about h2{font-size:20px;margin-bottom:10px}
  .about p{color:var(--muted);font-size:15px;margin-bottom:10px}
  .about p:last-child{margin-bottom:0}
  .about a{color:var(--brand);font-weight:600}
  .faq{max-width:820px}
  details{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:4px 22px;margin-bottom:12px}
  summary{cursor:pointer;font-weight:600;padding:17px 0;list-style:none;position:relative;font-size:15px}
  summary::after{content:"+";position:absolute;right:0;color:var(--accent);font-size:22px}
  details[open] summary::after{content:"\\2212"}
  details p{padding:0 0 17px;color:var(--muted);font-size:15px}
  .related{display:flex;gap:10px;flex-wrap:wrap}
  .rel{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:9px 18px;font-size:14px}
  .rel:hover{border-color:var(--brand);color:var(--brand)}
  .cta-band{background:var(--brand-dark);color:#fff;border-radius:20px;text-align:center;padding:48px 30px}
  .cta-band h2{font-size:clamp(21px,3.2vw,28px);margin-bottom:12px;font-weight:800}
  .cta-band p{color:#c7c2e8;margin-bottom:22px}
  .form{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;max-width:470px;margin:0 auto}
  .form input{flex:1;min-width:210px;padding:14px 18px;border-radius:10px;border:none;font-size:16px;
    font-family:inherit;color:var(--ink)}
  .note{margin-top:14px;color:#a9a3d4;font-size:13px}
  footer{border-top:2px solid var(--ink);padding:44px 0;color:var(--muted);font-size:14px;margin-top:20px}
  .foot{display:flex;justify-content:space-between;flex-wrap:wrap;gap:20px}
  address{font-style:normal;line-height:1.9}
  @media(max-width:900px){
    .layout{grid-template-columns:1fr}
    .filters{position:static}
    .prods{grid-template-columns:repeat(2,1fr)}
  }
  @media(max-width:600px){
    .prods{grid-template-columns:1fr}
    .nav-links{display:none}
    section{padding:34px 0}
    table{display:block;overflow-x:auto}
  }"""


def esc(s):
    """JSON-LD·meta에 넣기 위해 HTML 태그를 제거하고 이스케이프."""
    return html.escape(re.sub(r"<[^>]+>", "", s), quote=True)


def ld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>")


def related_slugs(p):
    """같은 그룹의 다른 기종 최대 4개 + 국내 유통 연결고리."""
    same = [q["slug"] for q in PLATFORMS if q["group"] == p["group"] and q["slug"] != p["slug"]]
    extra = {"famicom": ["comboy"], "comboy": ["famicom"],
             "mega-drive": ["gamboy"], "gamboy": ["mega-drive"]}
    return (same[:4] + extra.get(p["slug"], []))[:5]


def build_head(p):
    url = f"{BASE}/retro-games/{p['slug']}"
    title = f"{p['name']} 중고 | 소프트·본체·주변기기 | AnigameMate"
    desc = (f"{p['name']} 중고 소프트·본체·주변기기. {p['keywords']}. "
            "모든 상품은 실기 동작 확인 후 S·A·B 등급으로 등록합니다.")
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "레트로게임 중고", "item": f"{BASE}/retro-games"},
            {"@type": "ListItem", "position": 3, "name": p["name"], "item": url},
        ],
    }
    items = []
    for i, (name, sku, price, grade, chips, meta, stock) in enumerate(p["products"], 1):
        items.append({
            "@type": "ListItem", "position": i,
            "item": {
                "@type": "Product", "name": name,
                "url": f"{BASE}/p/{sku}", "sku": sku.upper(),
                "itemCondition": "https://schema.org/UsedCondition",
                "offers": {
                    "@type": "Offer", "price": str(price), "priceCurrency": "KRW",
                    "availability": ("https://schema.org/InStock" if stock
                                     else "https://schema.org/OutOfStock"),
                    "itemCondition": "https://schema.org/UsedCondition",
                },
            },
        })
    itemlist = {"@context": "https://schema.org", "@type": "ItemList",
                "name": f"{p['name']} 중고 상품", "numberOfItems": len(items),
                "itemListElement": items}
    faqpage = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in p["faqs"]
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="AnigameMate">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(p['lead'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og-{p['slug']}.jpg">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">

{ld(breadcrumb)}
{ld(itemlist)}
{ld(faqpage)}

<style>
{CSS}
</style>
</head>"""


def build_filters(p):
    out = []
    for legend, name, opts in FILTERS:
        rows = "\n".join(
            f'            <label class="opt"><input type="checkbox" name="{name}" '
            f'value="{v}"> {label}</label>'
            for v, label in opts)
        out.append(f"""          <fieldset>
            <legend>{legend}</legend>
{rows}
          </fieldset>""")
    return "\n".join(out)


def build_products(p):
    cards = []
    for name, sku, price, grade, chips, meta, stock in p["products"]:
        chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
        grade_chip = (f'<span class="chip g">{grade}등급</span>'
                      if grade in ("S", "A", "B") else f'<span class="chip g">{grade}</span>')
        if stock:
            cta = '<span class="btn btn-sm btn-accent" style="text-align:center">바로 구매</span>'
            price_cls, lead_chip = "price", grade_chip
        else:
            cta = ('<span class="btn btn-sm" style="text-align:center;background:var(--muted)">'
                   '재입고 알림</span>')
            price_cls, lead_chip = "price soldout", '<span class="chip off">품절</span>'
        cards.append(f"""          <a class="prod" href="product-{sku}.html">
            <div class="thumb">실물 사진</div>
            <div class="prod-body">
              <div class="chips">{lead_chip}{chip_html}</div>
              <h3>{name}</h3>
              <p class="meta">{meta}</p>
              <p class="{price_cls}">{price:,}원</p>
              {cta}
            </div>
          </a>""")
    return "\n\n".join(cards)


def build_page(p):
    tabs = "\n".join(
        f'        <a class="tab" href="retro-games-{p["slug"]}-{slug}.html">{label}</a>'
        for slug, label in TYPE_TABS)
    grade_rows = "\n".join(
        f'          <tr><td><span class="grade mono">{g}</span></td><td>{a}</td>'
        f"<td>{b}</td><td>{c}</td></tr>"
        for g, a, b, c in GRADE_ROWS)
    about = "\n".join(f"        <p>{para}</p>" for para in p["about"])
    faqs = "\n".join(
        f"""        <details{' open' if i == 0 else ''}>
          <summary>{q}</summary>
          <p>{a}</p>
        </details>"""
        for i, (q, a) in enumerate(p["faqs"]))
    rels = "\n".join(
        f'        <a class="rel" href="retro-games-{s}.html">{PLATFORM_BY_SLUG[s]["name"]}</a>'
        for s in related_slugs(p))
    in_stock = sum(1 for x in p["products"] if x[6])

    return f"""{build_head(p)}
<body>

<header>
  <div class="wrap nav">
    <a class="logo" href="index.html">Anigame<span>Mate</span></a>
    <nav class="nav-links" aria-label="주요 메뉴">
      <a href="retro-games.html">레트로게임</a>
      <a href="character-goods.html">캐릭터굿즈</a>
      <a href="doujin.html">자가출판물</a>
      <a href="anime-goods.html">애니굿즈</a>
    </nav>
    <a class="btn" href="#alert">재입고 알림</a>
  </div>
</header>

<main>
  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼">
      <a href="index.html">홈</a> › <a href="retro-games.html">레트로게임 중고</a> › <span aria-current="page">{p['name']}</span>
    </nav>

    <div class="head">
      <h1>{p['name']} 중고</h1>
      <p class="lead">{p['lead']}</p>

      <div class="answer">
        <h2>{p['aeo_q']}</h2>
        <p>{p['aeo_a']}</p>
      </div>

      <nav class="tabs" aria-label="상품 유형">
        <a class="tab" href="retro-games-{p['slug']}.html" aria-current="true">전체</a>
{tabs}
      </nav>
    </div>
  </div>

  <section id="list">
    <div class="wrap layout">

      <aside class="filters">
        <h3>필터</h3>
        <p class="hint">필터 결과 페이지는 색인되지 않고 이 카테고리로 canonical 처리됩니다.</p>
        <form action="retro-games-{p['slug']}.html" method="get">
{build_filters(p)}
          <button type="submit" class="btn btn-sm" style="width:100%">필터 적용</button>
        </form>
      </aside>

      <div>
        <h2 class="title">{p['name']} 중고 상품</h2>
        <p class="sub">전체 {len(p['products'])}개 · 재고 {in_stock}개 · 실기 동작 확인 완료</p>
        <div class="prods">

{build_products(p)}

        </div>
      </div>
    </div>
  </section>

  <section id="grade" style="background:#f4efe5">
    <div class="wrap">
      <h2 class="title">상태 등급 기준</h2>
      <p class="sub">모든 기종에 같은 기준을 적용합니다</p>
      <table>
        <caption>등급은 외관 기준이며, 동작 확인 결과는 등급과 별도로 표기합니다.</caption>
        <thead>
          <tr><th scope="col">등급</th><th scope="col">외관 상태</th><th scope="col">구성품</th><th scope="col">동작</th></tr>
        </thead>
        <tbody>
{grade_rows}
        </tbody>
      </table>
    </div>
  </section>

  <section id="about">
    <div class="wrap">
      <div class="about">
        <h2>{p['name']}이란</h2>
{about}
      </div>
    </div>
  </section>

  <section id="faq" style="background:#f4efe5">
    <div class="wrap">
      <h2 class="title">{p['name']} 자주 묻는 질문</h2>
      <p class="sub">구매 전 가장 많이 확인하시는 내용입니다</p>
      <div class="faq">
{faqs}
      </div>
    </div>
  </section>

  <section id="related">
    <div class="wrap">
      <h2 class="title">함께 보는 기종</h2>
      <p class="sub">{p['group']} 계열과 관련 기종</p>
      <nav class="related" aria-label="관련 기종">
{rels}
        <a class="rel" href="retro-games.html">전체 기종 보기</a>
      </nav>
    </div>
  </section>

  <section id="alert">
    <div class="wrap">
      <div class="cta-band">
        <h2>찾는 {p['name']} 상품이 없나요?</h2>
        <p>입고되면 가장 먼저 알려드립니다.</p>
        <form class="form" action="/subscribe" method="post">
          <label for="email" style="position:absolute;left:-9999px">이메일 주소</label>
          <input id="email" name="email" type="email" required placeholder="이메일 주소를 입력하세요">
          <button type="submit" class="btn btn-accent">알림 신청</button>
        </form>
        <p class="note">광고성 정보 수신에 동의하게 되며, 언제든 무료로 수신거부할 수 있습니다.</p>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot">
    <div>
      <p class="logo" style="font-size:18px;margin-bottom:8px">Anigame<span>Mate</span></p>
      <address>
        서울 ○○구 ○○로 00, 0층<br>
        문의 <a href="mailto:help@anigamemate.com">help@anigamemate.com</a> · 평일 10:00–18:00
      </address>
    </div>
    <div>
      <p>© 2026 AnigameMate. All rights reserved.</p>
      <p>사업자등록번호 000-00-00000 · 통신판매업신고 제0000-서울○○-0000호</p>
      <p>{p['name']} 및 각 게임 타이틀의 상표권과 저작권은 해당 권리자에게 있습니다.</p>
    </div>
  </div>
</footer>

</body>
</html>
"""


def main():
    for p in PLATFORMS:
        path = OUT / f"retro-games-{p['slug']}.html"
        path.write_text(build_page(p), encoding="utf-8")
        print(f"  생성 {path.name}  ({p['group']} · 상품 {len(p['products'])}개 · FAQ {len(p['faqs'])}개)")
    print(f"\n총 {len(PLATFORMS)}개 기종 페이지 생성 완료")


if __name__ == "__main__":
    main()
