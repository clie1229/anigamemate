# -*- coding: utf-8 -*-
"""
AnigameMate — 비-레트로 카테고리 + 게시판 생성기.
생성물:
  <cat>.html                 카테고리 허브 3개 (character-goods/doujin/anime-goods)
  <cat>-<sub>.html           하위분류 12개
  product-<sku>.html         굿즈 상품 페이지 24개
  board.html / board-<id>.html / board-write.html   게시판
디자인/토큰은 사이트 공통과 동일. 상단 내비에 '게시판' 포함.
"""
import sys, io, os, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from shop import CATEGORIES, BOARD_CATS, BOARD_POSTS

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://anigamemate.com"
NL = ",\n"
CAT_BY_SLUG = {c["slug"]: c for c in CATEGORIES}
BOARD_LABEL = dict(BOARD_POSTS and BOARD_CATS)


def esc(s):
    return html.escape(re.sub(r"<[^>]+>", "", str(s)), quote=True) if False else html.escape(str(s), quote=True)


import re
def esc(s):
    return html.escape(re.sub(r"<[^>]+>", "", str(s)), quote=True)


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


CSS = """<style>
  :root{
    --bg:#fbf7f0; --surface:#ffffff; --ink:#1b1a2e; --muted:#5d5b78;
    --brand:#3b2f8f; --brand-dark:#241c63; --accent:#e8543f; --accent-soft:#fdeeea;
    --line:#e6e0d6; --radius:14px; --ok:#1f7a52; --ok-soft:#e8f4ee;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
    color:var(--ink);background:var(--bg);line-height:1.7;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px}
  a{color:inherit;text-decoration:none}
  .mono{font-family:ui-monospace,SFMono-Regular,"D2Coding",Consolas,monospace}
  .btn{display:inline-block;background:var(--brand);color:#fff;font-weight:600;
    padding:14px 26px;border-radius:10px;font-size:16px;border:none;cursor:pointer;transition:background .2s;text-align:center}
  .btn:hover{background:var(--brand-dark)}
  .btn-accent{background:var(--accent)}.btn-accent:hover{background:#c8412e}
  .btn-ghost{background:var(--surface);color:var(--brand);border:2px solid var(--brand)}
  .btn-ghost:hover{background:var(--brand);color:#fff}
  .btn-sm{padding:9px 16px;font-size:14px;border-radius:8px}
  .btn-muted{background:var(--muted)}
  header{position:sticky;top:0;z-index:50;background:rgba(251,247,240,.94);
    backdrop-filter:blur(8px);border-bottom:2px solid var(--ink)}
  .nav{display:flex;align-items:center;justify-content:space-between;height:66px;gap:16px}
  .logo{font-weight:800;font-size:20px;color:var(--brand);letter-spacing:-.02em;white-space:nowrap}
  .logo span{color:var(--accent)}
  .nav-links{display:flex;gap:18px;align-items:center;font-size:15px}
  .nav-links a[aria-current="page"]{color:var(--brand);font-weight:700}
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
  .tabs{display:flex;gap:10px;flex-wrap:wrap;margin:30px 0 0}
  .tab{background:var(--surface);border:2px solid var(--ink);border-radius:10px;padding:10px 18px;font-weight:600;font-size:15px;cursor:pointer}
  .tab[aria-current="true"],.tab.on{background:var(--ink);color:#fff}
  .tab:hover{border-color:var(--brand)}
  section{padding:40px 0}
  h2.title{font-size:clamp(21px,3.2vw,28px);letter-spacing:-.02em;margin-bottom:6px;font-weight:800}
  .sub{color:var(--muted);margin-bottom:26px}
  .subcats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .subcat{background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);padding:22px 20px;display:block;transition:transform .15s}
  .subcat:hover{transform:translateY(-3px)}
  .subcat h3{font-size:18px;margin-bottom:6px}
  .subcat p{font-size:13px;color:var(--muted)}
  .prods{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  .prod{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;transition:border-color .15s,transform .15s}
  .prod:hover{border-color:var(--brand);transform:translateY(-2px)}
  .thumb{aspect-ratio:4/3;background:#efe9dd;display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line);color:#a89f8d;font-size:12px}
  .prod-body{padding:16px;display:flex;flex-direction:column;flex:1}
  .chips{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px}
  .chip{font-size:11px;font-weight:700;padding:3px 7px;border-radius:5px;background:#eee9f7;color:var(--brand)}
  .chip.g{background:var(--accent-soft);color:var(--accent)}
  .chip.off{background:#eceaf0;color:var(--muted)}
  .chip.ok{background:var(--ok-soft);color:var(--ok)}
  .prod h3{font-size:15px;line-height:1.45;margin-bottom:6px;flex:1}
  .meta{font-size:12px;color:var(--muted);margin-bottom:10px}
  .price{font-size:19px;font-weight:800;margin-bottom:12px}
  .price.soldout{color:var(--muted)}
  .about{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:28px 30px;max-width:820px}
  .about h2{font-size:20px;margin-bottom:10px}
  .about p{color:var(--muted);font-size:15px;margin-bottom:10px}.about p:last-child{margin-bottom:0}
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
  /* 상품 상세 */
  .hero{display:grid;grid-template-columns:1fr 1fr;gap:36px;padding:28px 0 12px;align-items:start}
  .gallery .main{aspect-ratio:4/3;background:#efe9dd;border:2px solid var(--ink);border-radius:var(--radius);display:flex;align-items:center;justify-content:center;color:#a89f8d;font-size:13px}
  .gthumbs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px}
  .gthumbs div{aspect-ratio:1;background:#efe9dd;border:1px solid var(--line);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#a89f8d;font-size:10px}
  .price-box{background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);padding:22px 24px;margin:12px 0 16px}
  .price-box .big{font-size:32px;font-weight:800}
  .price-box .big.soldout{color:var(--muted);text-decoration:line-through;font-size:24px}
  .buy{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
  .buy .btn{width:100%}
  table{width:100%;border-collapse:collapse;background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);overflow:hidden}
  caption{caption-side:top;text-align:left;color:var(--muted);font-size:14px;padding-bottom:10px}
  th,td{padding:13px 16px;text-align:left;border-bottom:1px solid var(--line);font-size:14px;vertical-align:top}
  tbody th{background:#f4efe5;font-weight:600;width:150px;white-space:nowrap}
  thead th{background:var(--ink);color:#fff;font-weight:600}
  tbody tr:last-child td,tbody tr:last-child th{border-bottom:none}
  /* 게시판 */
  .board{width:100%;border-collapse:collapse;background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);overflow:hidden}
  .board th,.board td{padding:13px 14px;border-bottom:1px solid var(--line);font-size:14px;text-align:left}
  .board thead th{background:var(--ink);color:#fff}
  .board td.num,.board td.cat,.board td.date,.board td.views{color:var(--muted);white-space:nowrap;font-size:13px}
  .board tr:last-child td{border-bottom:none}
  .board a:hover{color:var(--brand)}
  .pin{display:inline-block;background:var(--accent-soft);color:var(--accent);font-weight:700;font-size:11px;padding:2px 7px;border-radius:5px;margin-right:6px}
  .btag{display:inline-block;background:#eee9f7;color:var(--brand);font-weight:700;font-size:11px;padding:2px 7px;border-radius:5px}
  .board-top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:16px}
  .post{background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);padding:28px 30px;max-width:860px}
  .post h1{font-size:clamp(22px,3.4vw,30px);margin-bottom:10px}
  .post .pmeta{color:var(--muted);font-size:14px;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:18px;display:flex;gap:14px;flex-wrap:wrap}
  .post .pbody p{color:#33314a;font-size:15.5px;margin-bottom:12px}
  .comments{max-width:860px;margin-top:22px}
  .comment{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin-bottom:10px}
  .comment .cwho{font-weight:700;font-size:13px;margin-bottom:4px}
  .comment p{color:var(--muted);font-size:14px}
  .cform,.wform{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px;max-width:860px;margin-top:14px}
  .wform{border:2px solid var(--ink)}
  .field{margin-bottom:14px}
  .field label{display:block;font-weight:700;font-size:14px;margin-bottom:6px}
  .field input,.field select,.field textarea{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:8px;font-size:15px;font-family:inherit;color:var(--ink);background:#fff}
  .field textarea{min-height:180px;resize:vertical}
  .postnav{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;max-width:860px;margin-top:18px}
  .cta-band{background:var(--brand-dark);color:#fff;border-radius:20px;text-align:center;padding:48px 30px}
  .cta-band h2{font-size:clamp(21px,3.2vw,28px);margin-bottom:12px;font-weight:800}
  .cta-band p{color:#c7c2e8;margin-bottom:22px}
  .form{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;max-width:470px;margin:0 auto}
  .form input{flex:1;min-width:210px;padding:14px 18px;border-radius:10px;border:none;font-size:16px;font-family:inherit;color:var(--ink)}
  .note{margin-top:14px;color:#a9a3d4;font-size:13px}
  footer{border-top:2px solid var(--ink);padding:44px 0;color:var(--muted);font-size:14px;margin-top:20px}
  .foot{display:flex;justify-content:space-between;flex-wrap:wrap;gap:20px}
  address{font-style:normal;line-height:1.9}
  @media(max-width:900px){.subcats{grid-template-columns:repeat(2,1fr)}.prods{grid-template-columns:repeat(2,1fr)}.hero{grid-template-columns:1fr}}
  @media(max-width:600px){.nav-links{display:none}.subcats,.prods,.buy{grid-template-columns:1fr}section{padding:34px 0}
    table,.board{display:block;overflow-x:auto}.board td.views{display:none}}
</style>"""


def header(current=None):
    items = [("retro-games.html", "레트로게임", "retro-games"),
             ("character-goods.html", "캐릭터굿즈", "character-goods"),
             ("doujin.html", "자가출판물", "doujin"),
             ("anime-goods.html", "애니굿즈", "anime-goods"),
             ("board.html", "게시판", "board")]
    links = ""
    for href, label, key in items:
        cur = ' aria-current="page"' if key == current else ""
        links += f'      <a href="{href}"{cur}>{label}</a>\n'
    return f"""<header>
  <div class="wrap nav">
    <a class="logo" href="index.html">Anigame<span>Mate</span></a>
    <nav class="nav-links" aria-label="주요 메뉴">
{links.rstrip()}
    </nav>
    <a class="btn" href="#alert">재입고 알림</a>
  </div>
</header>"""


FOOTER = """<footer>
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
      <p>각 캐릭터·작품의 상표권과 저작권은 해당 권리자에게 있습니다.</p>
    </div>
  </div>
</footer>"""


def alert_band(label):
    return f"""  <section id="alert">
    <div class="wrap">
      <div class="cta-band">
        <h2>찾는 {label} 상품이 없나요?</h2>
        <p>신상 입고와 재입고를 가장 먼저 알려드립니다.</p>
        <form class="form" action="/subscribe" method="post">
          <label for="email" style="position:absolute;left:-9999px">이메일 주소</label>
          <input id="email" name="email" type="email" required placeholder="이메일 주소를 입력하세요">
          <button type="submit" class="btn btn-accent">알림 신청</button>
        </form>
        <p class="note">광고성 정보 수신에 동의하게 되며, 언제든 무료로 수신거부할 수 있습니다.</p>
      </div>
    </div>
  </section>"""


def page(title, desc, canon, jsonld, body, current=None, robots="index, follow"):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AnigameMate">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">

{jsonld}

{CSS}
</head>
<body>

{header(current)}

<main>
{body}
</main>

{FOOTER}

</body>
</html>
"""


def cond_avail(cond, stock):
    if cond == "예약":
        return "https://schema.org/PreOrder"
    return "https://schema.org/InStock" if stock else "https://schema.org/OutOfStock"


def cond_item(cond):
    return "https://schema.org/UsedCondition" if "중고" in cond else "https://schema.org/NewCondition"


def origin_of(chips):
    for k in ("정발", "병행수입", "자가출판"):
        if k in chips:
            return k
    return "표기 참조"


def product_card(pr):
    name, sku, price, cond, chips, meta, stock = pr
    if stock:
        first = f'<span class="chip g">{cond}</span>'
        pcls, btn = "price", '<span class="btn btn-sm btn-accent" style="text-align:center">바로 구매</span>'
    else:
        first = '<span class="chip off">품절</span>'
        pcls, btn = "price soldout", '<span class="btn btn-sm" style="text-align:center;background:var(--muted)">재입고 알림</span>'
    ch = first + "".join(f'<span class="chip">{c}</span>' for c in chips)
    return f"""          <a class="prod" href="product-{sku}.html">
            <div class="thumb">실물 사진</div>
            <div class="prod-body">
              <div class="chips">{ch}</div>
              <h3>{name}</h3>
              <p class="meta">{meta}</p>
              <p class="{pcls}">{price:,}원</p>
              {btn}
            </div>
          </a>"""


# ---------------- 카테고리 허브 ----------------
def render_hub(cat):
    slug, name = cat["slug"], cat["name"]
    canon = f"{BASE}/{slug}"
    subcards = "\n".join(
        f"""        <a class="subcat" href="{slug}-{s['slug']}.html"><h3>{s['name']}</h3><p>{s['desc']}</p></a>"""
        for s in cat["subs"])
    featured = []
    for s in cat["subs"]:
        featured.append(s["products"][0])
    feat_cards = "\n\n".join(product_card(pr) for pr in featured[:6])
    faqs = "\n".join(
        f"""        <details{' open' if i == 0 else ''}><summary>{q}</summary><p>{a}</p></details>"""
        for i, (q, a) in enumerate(cat["faqs"]))
    subitems = [{"@type": "ListItem", "position": i + 1, "name": s["name"],
                 "url": f"{BASE}/{slug}/{s['slug']}"} for i, s in enumerate(cat["subs"])]
    jsonld = "\n".join([
        ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{name}",
            "url": canon, "isPartOf": {"@type": "WebSite", "name": "AnigameMate", "url": f"{BASE}/"}}),
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": canon}]}),
        ld({"@context": "https://schema.org", "@type": "ItemList", "name": f"{name} 하위 분류",
            "itemListElement": subitems}),
        ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in cat["faqs"]]}),
    ])
    body = f"""  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <span aria-current="page">{name}</span></nav>
    <div class="head">
      <h1>{name}</h1>
      <p class="lead">{cat['lead']}</p>
      <div class="answer"><h2>{cat['aeo_q']}</h2><p>{cat['aeo_a']}</p></div>
    </div>
  </div>

  <section id="subcats">
    <div class="wrap">
      <h2 class="title">{name} 분류</h2>
      <p class="sub">원하는 분류에서 바로 찾아보세요</p>
      <div class="subcats">
{subcards}
      </div>
    </div>
  </section>

  <section style="background:#f4efe5">
    <div class="wrap">
      <h2 class="title">신상·추천 상품</h2>
      <p class="sub">분류별 대표 상품을 모았습니다</p>
      <div class="prods">

{feat_cards}

      </div>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <h2 class="title">{name} 자주 묻는 질문</h2>
      <p class="sub">구매 전 확인하세요</p>
      <div class="faq">
{faqs}
      </div>
    </div>
  </section>

{alert_band(name)}"""
    return page(f"{name} | AnigameMate", f"{name}. {cat['lead']}"[:150], canon, jsonld, body, current=slug)


# ---------------- 하위분류 ----------------
def render_sub(cat, sub):
    slug, name = cat["slug"], cat["name"]
    sslug, sname = sub["slug"], sub["name"]
    canon = f"{BASE}/{slug}/{sslug}"
    cards = "\n\n".join(product_card(pr) for pr in sub["products"])
    # 관련 하위분류
    rels = "\n        ".join(
        f'<a class="rel" href="{slug}-{s["slug"]}.html">{s["name"]}</a>'
        for s in cat["subs"] if s["slug"] != sslug)
    rels += f'\n        <a class="rel" href="{slug}.html">{name} 전체 보기</a>'
    items = []
    for i, (pn, sku, price, cond, chips, meta, stock) in enumerate(sub["products"], 1):
        items.append({"@type": "ListItem", "position": i, "item": {
            "@type": "Product", "name": pn, "url": f"{BASE}/p/{sku}", "sku": sku.upper(),
            "itemCondition": cond_item(cond),
            "offers": {"@type": "Offer", "price": str(price), "priceCurrency": "KRW",
                       "availability": cond_avail(cond, stock), "itemCondition": cond_item(cond)}}})
    jsonld = "\n".join([
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": f"{BASE}/{slug}"},
            {"@type": "ListItem", "position": 3, "name": sname, "item": canon}]}),
        ld({"@context": "https://schema.org", "@type": "ItemList", "name": f"{sname} 상품",
            "numberOfItems": len(sub["products"]), "itemListElement": items}),
    ])
    body = f"""  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <a href="{slug}.html">{name}</a> › <span aria-current="page">{sname}</span></nav>
    <div class="head">
      <h1>{sname}</h1>
      <p class="lead">{sub['desc']}. 정품 구분과 상태를 상품마다 표기합니다.</p>
    </div>
  </div>

  <section id="list">
    <div class="wrap">
      <h2 class="title">{sname} 상품</h2>
      <p class="sub">전체 {len(sub['products'])}개</p>
      <div class="prods">

{cards}

      </div>
    </div>
  </section>

  <section id="related" style="background:#f4efe5">
    <div class="wrap">
      <h2 class="title">{name} 다른 분류</h2>
      <p class="sub">함께 둘러보세요</p>
      <nav class="related" aria-label="관련 분류">
        {rels}
      </nav>
    </div>
  </section>

{alert_band(sname)}"""
    return page(f"{sname} | {name} | AnigameMate", f"{sname} {name}. {sub['desc']}"[:150], canon, jsonld, body, current=slug)


# ---------------- 굿즈 상품 페이지 ----------------
def render_product(cat, sub, pr):
    name, sku, price, cond, chips, meta, stock = pr
    slug, cname = cat["slug"], cat["name"]
    sslug, sname = sub["slug"], sub["name"]
    canon = f"{BASE}/p/{sku}"
    origin = origin_of(chips)
    others = [p for p in sub["products"] if p[1] != sku]

    if cond == "예약":
        stock_txt, price_cls = "예약 판매 · 입고 예정월 상세 참조", "big"
        buy = f'<a class="btn btn-accent" href="/cart/add?sku={sku}">예약 구매</a><a class="btn btn-ghost" href="/cart/add?sku={sku}&amp;mode=cart">장바구니</a>'
    elif stock:
        stock_txt, price_cls = "재고 있음", "big"
        buy = f'<a class="btn btn-accent" href="/cart/add?sku={sku}">바로 구매</a><a class="btn btn-ghost" href="/cart/add?sku={sku}&amp;mode=cart">장바구니</a>'
    else:
        stock_txt, price_cls = "품절 · 재입고 알림", "big soldout"
        buy = '<a class="btn btn-muted btn-block" href="#related" style="grid-column:1/-1">재입고 알림 · 다른 상품 보기</a>'

    chips_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    others_cards = "\n".join(
        f"""        <a class="prod" href="product-{o[1]}.html"><div class="thumb">실물 사진</div>
          <div class="prod-body"><div class="chips"><span class="chip g">{o[3]}</span></div><h3>{o[0]}</h3><p class="price">{o[2]:,}원</p></div></a>"""
        for o in others)
    others_cards += f"""\n        <a class="prod" href="{slug}-{sslug}.html"><div class="thumb">카테고리</div>
          <div class="prod-body"><div class="chips"><span class="chip">전체</span></div><h3>{sname} 전체 보기</h3><p class="price">더보기</p></div></a>"""

    product_ld = {
        "@context": "https://schema.org", "@type": "Product", "name": name,
        "description": f"{cname} {sname} - {name}. {meta}. 정품 구분: {origin}.",
        "sku": sku.upper(), "url": canon,
        "image": [f"{BASE}/img/{sku}-1.jpg", f"{BASE}/img/{sku}-2.jpg"],
        "itemCondition": cond_item(cond), "category": f"{cname} > {sname}",
        "offers": {"@type": "Offer", "url": canon, "price": str(price), "priceCurrency": "KRW",
                   "availability": cond_avail(cond, stock), "itemCondition": cond_item(cond),
                   "seller": {"@type": "Organization", "name": "AnigameMate"},
                   "priceValidUntil": "2026-12-31"}}
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": cname, "item": f"{BASE}/{slug}"},
        {"@type": "ListItem", "position": 3, "name": sname, "item": f"{BASE}/{slug}/{sslug}"},
        {"@type": "ListItem", "position": 4, "name": name, "item": canon}]}
    jsonld = ld(product_ld) + "\n" + ld(breadcrumb)

    body = f"""  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <a href="{slug}.html">{cname}</a> › <a href="{slug}-{sslug}.html">{sname}</a> › <span aria-current="page">{name}</span></nav>

    <div class="hero">
      <div class="gallery">
        <div class="main">대표 실물 사진</div>
        <div class="gthumbs"><div>정면</div><div>후면</div><div>디테일</div><div>구성</div></div>
      </div>
      <div id="buy">
        <div class="chips"><span class="chip g">{cond}</span>{chips_html}</div>
        <h1>{name}</h1>
        <p class="meta mono" style="margin-bottom:6px">SKU {sku.upper()} · {cname} &gt; {sname}</p>
        <div class="price-box">
          <p class="{price_cls}">{price:,}원</p>
          <p class="meta" style="margin-top:6px">배송비 3,500원 · 평일 14시 이전 결제 시 당일 출고</p>
          <p class="meta" style="margin-top:4px;font-weight:700;color:{'var(--accent)' if not stock else 'var(--ok)'}">{stock_txt}</p>
        </div>
        <div class="buy">{buy}</div>
        <p class="meta">정품 구분: <strong>{origin}</strong> · 상태·구성은 아래 상세표에서 확인하세요.</p>
      </div>
    </div>
  </div>

  <section id="spec">
    <div class="wrap">
      <h2 class="title">상품 정보</h2>
      <p class="sub">같은 항목을 같은 형식으로 표기합니다</p>
      <table>
        <tbody>
          <tr><th scope="row">상품 상태</th><td>{cond}</td></tr>
          <tr><th scope="row">정품 구분</th><td>{origin}</td></tr>
          <tr><th scope="row">구성·사양</th><td>{meta}</td></tr>
          <tr><th scope="row">분류</th><td><a href="{slug}-{sslug}.html" style="color:var(--brand);font-weight:600">{cname} &gt; {sname}</a></td></tr>
          <tr><th scope="row">상품번호(SKU)</th><td class="mono">{sku.upper()}</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section id="desc" style="background:#f4efe5">
    <div class="wrap">
      <div class="about">
        <h2>상품 설명</h2>
        <p>{cname} {sname} 카테고리의 <strong>{name}</strong>입니다. {meta}. 정품 구분은 {origin}이며, 상태와 구성은 실물 사진에 그대로 담았습니다.</p>
        <p>{'예약 상품은 입고 예정월에 순차 발송되며, 입고 전까지 취소·환불이 가능합니다.' if cond=='예약' else '재고 단일 상품이라 품절 시 재입고가 불확실합니다. 재입고 알림을 신청하시면 가장 먼저 안내드립니다.'} 궁금한 점은 <a href="board.html">게시판</a>이나 고객문의로 남겨주세요.</p>
      </div>
    </div>
  </section>

  <section id="policy">
    <div class="wrap">
      <h2 class="title">배송 · 교환 · 환불</h2>
      <p class="sub">전자상거래법 기준</p>
      <div class="about" style="max-width:none">
        <p><strong>배송</strong> — 배송비 3,500원(5만원 이상 무료), 평일 14시 이전 결제 시 당일 출고, 보통 1~2일 내 도착. 파손 주의 상품은 완충 포장합니다.</p>
        <p><strong>교환·환불</strong> — 수령 후 7일 이내 청약철회 가능(단순 변심 시 왕복 배송비 구매자 부담). 표기와 다른 하자는 배송비 판매자 부담으로 처리합니다.</p>
        <p><strong>병행수입 상품</strong>은 국내 공식 A/S가 제한될 수 있습니다. 자가출판물·개봉 굿즈 등 재판매가 어려운 상품은 반품이 제한될 수 있어 상세 표기를 확인해 주세요.</p>
      </div>
    </div>
  </section>

  <section id="related" style="background:#f4efe5">
    <div class="wrap">
      <h2 class="title">함께 보는 {sname} 상품</h2>
      <p class="sub">같은 분류의 다른 상품</p>
      <div class="prods">
{others_cards}
      </div>
    </div>
  </section>

{alert_band(name)}"""
    robots = "index, follow"
    return page(f"{name} | {sname} 중고·굿즈 | AnigameMate", f"{name}. {meta}. 정품 구분 {origin}."[:150], canon, jsonld, body, current=slug, robots=robots)


# ---------------- 게시판 ----------------
def render_board():
    canon = f"{BASE}/board"
    label = dict(BOARD_CATS)
    rows = ""
    posts = sorted(BOARD_POSTS, key=lambda p: (not p["pinned"], -p["id"]))
    for p in posts:
        pin = '<span class="pin">공지</span>' if p["pinned"] else ""
        rows += f"""          <tr data-cat="{p['cat']}">
            <td class="num">{p['id']}</td>
            <td class="cat"><span class="btag">{label[p['cat']]}</span></td>
            <td><a href="board-{p['id']}.html">{pin}{p['title']}</a></td>
            <td class="date">{p['author']}</td>
            <td class="date">{p['date']}</td>
            <td class="views">{p['views']:,}</td>
          </tr>\n"""
    tabs = '<button class="tab on" data-filter="all" type="button">전체</button>\n        '
    tabs += "\n        ".join(
        f'<button class="tab" data-filter="{c}" type="button">{l}</button>' for c, l in BOARD_CATS)
    jsonld = "\n".join([
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "게시판", "item": canon}]}),
        ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "AnigameMate 게시판", "url": canon}),
    ])
    body = f"""  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <span aria-current="page">게시판</span></nav>
    <div class="head">
      <h1>게시판</h1>
      <p class="lead">공지사항·구매후기·질문답변·자유게시판. 궁금한 점과 후기를 자유롭게 남겨주세요.</p>
      <nav class="tabs" id="btabs" aria-label="게시판 분류">
        {tabs}
      </nav>
    </div>
  </div>

  <section id="list">
    <div class="wrap">
      <div class="board-top">
        <p class="sub" style="margin:0">전체 {len(posts)}개 글</p>
        <a class="btn btn-sm" href="board-write.html">글쓰기</a>
      </div>
      <table class="board">
        <thead>
          <tr><th style="width:52px">번호</th><th style="width:96px">분류</th><th>제목</th><th style="width:96px">작성자</th><th style="width:104px">작성일</th><th style="width:72px">조회</th></tr>
        </thead>
        <tbody id="brows">
{rows.rstrip()}
        </tbody>
      </table>
    </div>
  </section>

  <section id="alert">
    <div class="wrap">
      <div class="cta-band">
        <h2>궁금한 점이 있으신가요?</h2>
        <p>질문답변 게시판에 남겨주시면 운영자가 확인 후 답변드립니다.</p>
        <a class="btn" href="board-write.html" style="background:#fff;color:var(--brand)">글쓰기</a>
      </div>
    </div>
  </section>

  <script>
  (function(){{
    var tabs=document.querySelectorAll('#btabs .tab');
    var rows=document.querySelectorAll('#brows tr');
    tabs.forEach(function(t){{
      t.addEventListener('click',function(){{
        tabs.forEach(function(x){{x.classList.remove('on')}});
        t.classList.add('on');
        var f=t.getAttribute('data-filter');
        rows.forEach(function(r){{
          r.style.display=(f==='all'||r.getAttribute('data-cat')===f)?'':'none';
        }});
      }});
    }});
  }})();
  </script>"""
    return page("게시판 | AnigameMate", "AnigameMate 게시판 — 공지사항·구매후기·질문답변·자유게시판.", canon, jsonld, body, current="board")


def render_post(p):
    label = dict(BOARD_CATS)
    canon = f"{BASE}/board/{p['id']}"
    body_html = "\n".join(f"        <p>{para}</p>" for para in p["body"])
    # 이전/다음 (id 기준)
    ids = sorted(x["id"] for x in BOARD_POSTS)
    idx = ids.index(p["id"])
    prev_id = ids[idx - 1] if idx > 0 else None
    next_id = ids[idx + 1] if idx < len(ids) - 1 else None
    prev_link = f'<a class="rel" href="board-{prev_id}.html">← 이전 글</a>' if prev_id else '<span></span>'
    next_link = f'<a class="rel" href="board-{next_id}.html">다음 글 →</a>' if next_id else '<span></span>'
    # 샘플 댓글 (후기/질답/자유에만)
    comments = ""
    if p["cat"] != "notice":
        comments = f"""
  <section>
    <div class="wrap">
      <div class="comments">
        <h2 class="title" style="font-size:19px">댓글</h2>
        <div class="comment"><p class="cwho">운영자</p><p>글 남겨주셔서 감사합니다. 문의 주신 내용은 확인 후 안내드리겠습니다.</p></div>
        <form class="cform" action="/board/{p['id']}/comment" method="post">
          <div class="field"><label for="cbody">댓글 쓰기</label>
            <textarea id="cbody" name="body" style="min-height:80px" placeholder="댓글을 입력하세요 (데모 · 실제 등록되지 않습니다)"></textarea></div>
          <button class="btn btn-sm" type="submit">등록</button>
        </form>
      </div>
    </div>
  </section>"""
    jsonld = "\n".join([
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "게시판", "item": f"{BASE}/board"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": canon}]}),
        ld({"@context": "https://schema.org", "@type": "DiscussionForumPosting",
            "headline": p["title"], "datePublished": p["date"],
            "author": {"@type": "Person", "name": p["author"]},
            "articleSection": label[p["cat"]], "url": canon,
            "interactionStatistic": {"@type": "InteractionCounter",
                                     "interactionType": "https://schema.org/ViewAction",
                                     "userInteractionCount": p["views"]}}),
    ])
    pin = '<span class="pin">공지</span>' if p["pinned"] else ""
    body = f"""  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <a href="board.html">게시판</a> › <span aria-current="page">{label[p['cat']]}</span></nav>

    <article class="post" style="margin-top:22px">
      <h1>{pin}{p['title']}</h1>
      <div class="pmeta">
        <span class="btag">{label[p['cat']]}</span>
        <span>작성자 {p['author']}</span>
        <span>{p['date']}</span>
        <span>조회 {p['views']:,}</span>
      </div>
      <div class="pbody">
{body_html}
      </div>
    </article>
{comments}

  <div class="wrap">
    <div class="postnav">
      {prev_link}
      <a class="rel" href="board.html">목록</a>
      {next_link}
    </div>
  </div>"""
    return page(f"{p['title']} | 게시판 | AnigameMate",
                f"{p['title']} - AnigameMate 게시판 {label[p['cat']]}", canon, jsonld, body, current="board")


def render_write():
    canon = f"{BASE}/board/write"
    opts = "\n".join(f'              <option value="{c}">{l}</option>' for c, l in BOARD_CATS)
    jsonld = ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "게시판", "item": f"{BASE}/board"},
        {"@type": "ListItem", "position": 3, "name": "글쓰기", "item": canon}]})
    body = f"""  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <a href="board.html">게시판</a> › <span aria-current="page">글쓰기</span></nav>
    <div class="head"><h1>글쓰기</h1><p class="lead">공지·후기·질문·자유 글을 남길 수 있습니다. (데모 화면 — 실제 등록되지 않습니다)</p></div>
  </div>

  <section>
    <div class="wrap">
      <form class="wform" action="/board/submit" method="post">
        <div class="field"><label for="wcat">분류</label>
          <select id="wcat" name="cat">
{opts}
          </select></div>
        <div class="field"><label for="wtitle">제목</label>
          <input id="wtitle" name="title" type="text" placeholder="제목을 입력하세요"></div>
        <div class="field"><label for="wauthor">작성자</label>
          <input id="wauthor" name="author" type="text" placeholder="닉네임"></div>
        <div class="field"><label for="wbody">내용</label>
          <textarea id="wbody" name="body" placeholder="내용을 입력하세요"></textarea></div>
        <div style="display:flex;gap:10px">
          <button class="btn" type="submit">등록</button>
          <a class="btn btn-ghost" href="board.html">취소</a>
        </div>
      </form>
    </div>
  </section>"""
    return page("글쓰기 | 게시판 | AnigameMate", "AnigameMate 게시판 글쓰기", canon, jsonld, body,
                current="board", robots="noindex, follow")


def main():
    n = 0
    for cat in CATEGORIES:
        open(os.path.join(HERE, f"{cat['slug']}.html"), "w", encoding="utf-8").write(render_hub(cat)); n += 1
        for sub in cat["subs"]:
            open(os.path.join(HERE, f"{cat['slug']}-{sub['slug']}.html"), "w", encoding="utf-8").write(render_sub(cat, sub)); n += 1
            for pr in sub["products"]:
                open(os.path.join(HERE, f"product-{pr[1]}.html"), "w", encoding="utf-8").write(render_product(cat, sub, pr)); n += 1
    # 게시판
    open(os.path.join(HERE, "board.html"), "w", encoding="utf-8").write(render_board()); n += 1
    for p in BOARD_POSTS:
        open(os.path.join(HERE, f"board-{p['id']}.html"), "w", encoding="utf-8").write(render_post(p)); n += 1
    open(os.path.join(HERE, "board-write.html"), "w", encoding="utf-8").write(render_write()); n += 1
    hubs = len(CATEGORIES)
    subs = sum(len(c["subs"]) for c in CATEGORIES)
    prods = sum(len(s["products"]) for c in CATEGORIES for s in c["subs"])
    print(f"생성 {n}개 · 허브 {hubs} · 하위분류 {subs} · 굿즈상품 {prods} · 게시판 {1 + len(BOARD_POSTS) + 1}")


if __name__ == "__main__":
    main()
