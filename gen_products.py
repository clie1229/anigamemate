# -*- coding: utf-8 -*-
"""
AnigameMate — 개별 상품 상세페이지(product-<sku>.html) 일괄 생성기
- platforms.py 의 각 기종 products 로부터 상품 페이지를 만든다.
- 규격: product-fc-smb3.html / product-template.html (동일 디자인·리치 JSON-LD).
- 카테고리 카드가 product-<sku>.html 로 연결되도록 링크를 맞춘다.
- 이미 손질된 product-fc-smb3.html 은 기본 보존(--all 로 덮어쓰기).

⚠️ 가격·시세는 platforms.py 의 placeholder 예시. 실제 시세로 교체 필요.
"""
import sys, io, os, re, json, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from platforms import PLATFORMS, PLATFORM_BY_SLUG

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://anigamemate.com"
SAB = ("S", "A", "B")

GRADE_DESC = {
    "S": "미개봉 또는 사용감 거의 없음",
    "A": "경미한 사용감, 라벨/외관 온전",
    "B": "흠집·변색 있으나 사용 지장 없음",
    "부품용": "상태 무관 · 동작 보증 제외",
}
REGION_TOKENS = ("NTSC-J", "NTSC-U", "PAL", "한글판", "국내판")
BRAND = {"닌텐도": "Nintendo", "세가": "Sega", "소니": "Sony"}
BRAND_SLUG = {"comboy": "현대전자", "gamboy": "삼성전자", "zemmix": "대우전자",
              "pc-engine": "NEC · 허드슨", "neogeo": "SNK"}

# ---- 상품 페이지 CSS (product-fc-smb3.html 과 동일 + .warn 추가) ----
PCSS = """  :root{
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
    padding:15px 30px;border-radius:10px;font-size:17px;border:none;cursor:pointer;
    transition:background .2s;text-align:center}
  .btn:hover{background:var(--brand-dark)}
  .btn-accent{background:var(--accent)}
  .btn-accent:hover{background:#c8412e}
  .btn-ghost{background:transparent;color:var(--brand);border:2px solid var(--brand)}
  .btn-ghost:hover{background:var(--brand);color:#fff}
  .btn-muted{background:var(--muted)}
  header{position:sticky;top:0;z-index:50;background:rgba(251,247,240,.94);
    backdrop-filter:blur(8px);border-bottom:2px solid var(--ink)}
  .nav{display:flex;align-items:center;justify-content:space-between;height:66px;gap:16px}
  .logo{font-weight:800;font-size:20px;color:var(--brand);letter-spacing:-.02em;white-space:nowrap}
  .logo span{color:var(--accent)}
  .nav-links{display:flex;gap:18px;align-items:center;font-size:15px}
  .nav .btn{padding:10px 18px;font-size:15px}
  .crumb{padding:18px 0 0;font-size:14px;color:var(--muted)}
  .crumb a:hover{color:var(--brand)}
  .hero{display:grid;grid-template-columns:1fr 1fr;gap:36px;padding:28px 0 12px;align-items:start}
  .gallery .main{aspect-ratio:4/3;background:#efe9dd;border:2px solid var(--ink);border-radius:var(--radius);
    display:flex;align-items:center;justify-content:center;color:#a89f8d;font-size:13px;letter-spacing:.06em}
  .thumbs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px}
  .thumbs div{aspect-ratio:1;background:#efe9dd;border:1px solid var(--line);border-radius:8px;
    display:flex;align-items:center;justify-content:center;color:#a89f8d;font-size:10px}
  .shot-note{margin-top:12px;font-size:13px;color:var(--muted);background:var(--surface);
    border:1px solid var(--line);border-radius:8px;padding:10px 12px}
  .chips{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
  .chip{font-size:12px;font-weight:700;padding:4px 9px;border-radius:6px;background:#eee9f7;color:var(--brand)}
  .chip.g{background:var(--accent-soft);color:var(--accent)}
  .chip.ok{background:var(--ok-soft);color:var(--ok)}
  .chip.off{background:#eceaf0;color:var(--muted)}
  h1{font-size:clamp(24px,3.6vw,32px);line-height:1.3;letter-spacing:-.02em;font-weight:800;margin-bottom:8px}
  .sku{font-size:13px;color:var(--muted);margin-bottom:18px}
  .price-box{background:var(--surface);border:2px solid var(--ink);border-radius:var(--radius);
    padding:22px 24px;margin-bottom:16px}
  .price{font-size:34px;font-weight:800;letter-spacing:-.03em}
  .price.soldout{color:var(--muted);text-decoration:line-through;font-size:26px}
  .ship{font-size:14px;color:var(--muted);margin-top:6px}
  .stock{display:flex;align-items:center;gap:7px;font-size:14px;font-weight:600;color:var(--ok);margin-top:12px}
  .stock.out{color:var(--accent)}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--ok);display:inline-block}
  .stock.out .dot{background:var(--accent)}
  .buy{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
  .buy .btn{width:100%}
  .guard{background:var(--ok-soft);border:1px solid #bfe0cf;border-radius:10px;padding:14px 16px;
    font-size:14px;color:#17603f}
  .guard strong{display:block;margin-bottom:4px}
  section{padding:44px 0}
  h2.title{font-size:clamp(20px,3vw,26px);letter-spacing:-.02em;margin-bottom:6px;font-weight:800}
  .sub{color:var(--muted);margin-bottom:24px;font-size:15px}
  table{width:100%;border-collapse:collapse;background:var(--surface);border:2px solid var(--ink);
    border-radius:var(--radius);overflow:hidden}
  caption{caption-side:top;text-align:left;color:var(--muted);font-size:14px;padding-bottom:10px}
  th,td{padding:14px 16px;text-align:left;border-bottom:1px solid var(--line);font-size:15px}
  tbody th{background:#f4efe5;font-weight:600;width:180px;white-space:nowrap}
  tbody tr:last-child th,tbody tr:last-child td{border-bottom:none}
  .grade-badge{font-weight:800;color:var(--accent)}
  .warn{color:var(--accent);font-weight:700}
  .okk{color:var(--ok);font-weight:700}
  .desc{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    padding:28px 30px;max-width:860px}
  .desc h3{font-size:17px;margin:18px 0 8px}
  .desc h3:first-child{margin-top:0}
  .desc p,.desc li{color:var(--muted);font-size:15px}
  .desc ul{margin:0 0 0 18px}
  .desc li{padding:3px 0}
  .desc a{color:var(--brand);font-weight:600}
  .cols{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
  .card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:24px 26px}
  .card h3{font-size:17px;margin-bottom:10px}
  .card p,.card li{color:var(--muted);font-size:14px}
  .card ul{margin:0 0 0 18px}
  .faq{max-width:860px}
  details{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:4px 22px;margin-bottom:12px}
  summary{cursor:pointer;font-weight:600;padding:17px 0;list-style:none;position:relative;font-size:15px}
  summary::after{content:"+";position:absolute;right:0;color:var(--accent);font-size:22px}
  details[open] summary::after{content:"\\2212"}
  details p{padding:0 0 17px;color:var(--muted);font-size:15px}
  .prods{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .prod{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden;
    display:flex;flex-direction:column;transition:border-color .15s,transform .15s}
  .prod:hover{border-color:var(--brand);transform:translateY(-2px)}
  .thumb{aspect-ratio:4/3;background:#efe9dd;display:flex;align-items:center;justify-content:center;
    border-bottom:1px solid var(--line);color:#a89f8d;font-size:11px}
  .prod-body{padding:14px}
  .prod h3{font-size:14px;line-height:1.45;margin:6px 0}
  .prod .p{font-size:16px;font-weight:800}
  footer{border-top:2px solid var(--ink);padding:44px 0;color:var(--muted);font-size:14px;margin-top:20px}
  .foot{display:flex;justify-content:space-between;flex-wrap:wrap;gap:20px}
  address{font-style:normal;line-height:1.9}
  @media(max-width:900px){
    .hero{grid-template-columns:1fr;gap:24px}
    .prods{grid-template-columns:repeat(2,1fr)}
  }
  @media(max-width:600px){
    .cols{grid-template-columns:1fr}
    .nav-links{display:none}
    .buy{grid-template-columns:1fr}
    section{padding:34px 0}
    table{display:block;overflow-x:auto}
    tbody th{width:auto}
  }"""

HEADER = """<header>
  <div class="wrap nav">
    <a class="logo" href="index.html">Anigame<span>Mate</span></a>
    <nav class="nav-links" aria-label="주요 메뉴">
      <a href="retro-games.html">레트로게임</a>
      <a href="character-goods.html">캐릭터굿즈</a>
      <a href="doujin.html">자가출판물</a>
      <a href="anime-goods.html">애니굿즈</a>
    </nav>
    <a class="btn" href="#buy">바로 구매</a>
  </div>
</header>"""


def esc(s):
    return html.escape(re.sub(r"<[^>]+>", "", str(s)), quote=True)


def ld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>")


def grade_label(grade):
    return f"{grade}등급" if grade in SAB else grade


def short_name(name, pname):
    s = re.sub(r"\s*\([^)]*\)\s*", " ", name)   # (패미컴) 등 괄호 제거
    return re.sub(r"\s+", " ", s).strip()


def region_of(chips):
    for c in chips:
        if c in REGION_TOKENS:
            return c
    return None


def parts_of(grade, chips):
    return grade == "부품용" or any("미동작" in c for c in chips)


def compos_of(chips, meta):
    if any("박스풀셋" in c for c in chips):
        return "박스풀셋 (박스·설명서 포함)"
    if any("본체" in c for c in chips):
        return "본체 세트 · 상세 참조"
    if any(("주변기기" in c or "부품" in c or "하네스" in c) for c in chips):
        return "단품"
    return "본품만 (박스·설명서 없음)"


def brand_of(p):
    return BRAND.get(p["group"]) or BRAND_SLUG.get(p["slug"]) or p["name"]


def hero_chips(grade, chips, stock):
    out = []
    if stock:
        out.append(f'<span class="chip g">{grade_label(grade)}</span>')
    else:
        out.append('<span class="chip off">품절</span>')
        out.append(f'<span class="chip g">{grade_label(grade)}</span>')
    for c in chips:
        cls = "chip"
        if any(k in c for k in ("확인", "정상", "구동")):
            cls = "chip ok"
        elif "미동작" in c:
            cls = "chip off"
        out.append(f'<span class="{cls}">{c}</span>')
    return "".join(out)


def related_cards(p, cur_sku):
    """같은 기종 다른 상품 + 주변기기 필터뷰 + 카테고리."""
    cards = []
    for (name, sku, price, grade, chips, meta, stock) in p["products"]:
        if sku == cur_sku:
            continue
        gl = grade_label(grade)
        gchip = f'<span class="chip g">{gl}</span>' if stock else '<span class="chip off">품절</span>'
        cards.append(f"""        <a class="prod" href="product-{sku}.html">
          <div class="thumb">실물 사진</div>
          <div class="prod-body">
            <div class="chips">{gchip}</div>
            <h3>{name}</h3>
            <p class="p">{price:,}원</p>
          </div>
        </a>""")
    # 주변기기 필터뷰
    cards.append(f"""        <a class="prod" href="retro-games-{p['slug']}.html?type=accessories">
          <div class="thumb">주변기기</div>
          <div class="prod-body">
            <div class="chips"><span class="chip">주변기기</span></div>
            <h3>{p['name']} 주변기기 · 부품</h3>
            <p class="p">카테고리 보기</p>
          </div>
        </a>""")
    # 카테고리 전체
    cards.append(f"""        <a class="prod" href="retro-games-{p['slug']}.html">
          <div class="thumb">카테고리</div>
          <div class="prod-body">
            <div class="chips"><span class="chip">전체</span></div>
            <h3>{p['name']} 중고 전체 보기</h3>
            <p class="p">카테고리 보기</p>
          </div>
        </a>""")
    return "\n".join(cards[:4])


def render(p, product):
    name, sku, price, grade, chips, meta, stock = product
    slug, pname = p["slug"], p["name"]
    prod_url = f"{BASE}/p/{sku}"
    sku_code = sku.upper() + "-" + (grade if grade in SAB else "PARTS")
    gl = grade_label(grade)
    is_parts = parts_of(grade, chips)
    region = region_of(chips)
    compos = compos_of(chips, meta)
    leaf = short_name(name, pname)
    avail = "InStock" if stock else "OutOfStock"

    # ---- meta ----
    title = f"{name} {gl} 중고 | AnigameMate"
    desc = f"{pname} {leaf} 중고 {gl}. {meta}. " + (
        f"지역코드 {region}. " if region else "") + "7일 이내 구동 문제 시 교환·환불."

    # ---- JSON-LD ----
    addprops = [
        {"@type": "PropertyValue", "name": "상태 등급", "value": grade},
        {"@type": "PropertyValue", "name": "구성품", "value": compos},
        {"@type": "PropertyValue", "name": "동작 확인",
         "value": "부품용(미동작)" if is_parts else "실기 구동 확인 완료"},
    ]
    if region:
        addprops.append({"@type": "PropertyValue", "name": "지역코드", "value": region})
    product_ld = {
        "@context": "https://schema.org", "@type": "Product", "name": name,
        "description": f"{pname}용 중고 상품. {meta}. " + (
            "부품용(미동작)으로 동작을 보증하지 않습니다." if is_parts
            else "실기 구동을 확인한 뒤 등록했습니다."),
        "sku": sku_code, "url": prod_url,
        "image": [f"{BASE}/img/{sku}-1.jpg", f"{BASE}/img/{sku}-2.jpg", f"{BASE}/img/{sku}-3.jpg"],
        "itemCondition": "https://schema.org/UsedCondition",
        "category": f"레트로게임 중고 > {pname} > 상품",
        "brand": {"@type": "Brand", "name": brand_of(p)},
        "gamePlatform": pname,
        "additionalProperty": addprops,
        "offers": {
            "@type": "Offer", "url": prod_url, "price": str(price), "priceCurrency": "KRW",
            "availability": f"https://schema.org/{avail}",
            "itemCondition": "https://schema.org/UsedCondition",
            "seller": {"@type": "Organization", "name": "AnigameMate"},
            "priceValidUntil": "2026-12-31",
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {"@type": "MonetaryAmount", "value": "3500", "currency": "KRW"},
                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "KR"},
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                    "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 2, "unitCode": "DAY"},
                },
            },
            "hasMerchantReturnPolicy": {
                "@type": "MerchantReturnPolicy", "applicableCountry": "KR",
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                "merchantReturnDays": 7, "returnMethod": "https://schema.org/ReturnByMail",
                "returnFees": "https://schema.org/FreeReturn",
            },
        },
    }
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "레트로게임 중고", "item": f"{BASE}/retro-games"},
            {"@type": "ListItem", "position": 3, "name": pname, "item": f"{BASE}/retro-games/{slug}"},
            {"@type": "ListItem", "position": 4, "name": leaf, "item": prod_url},
        ],
    }
    faq_pairs = [
        (f"이 상품 {gl}은 어떤 상태인가요?",
         f"{gl}은 {GRADE_DESC.get(grade, '')}. 구성은 {compos}이며, " + (
             "부품용(미동작)이라 동작을 보증하지 않습니다." if is_parts
             else "실기 구동을 확인한 뒤 등록했습니다.")),
    ]
    if is_parts:
        faq_pairs.append(("부품용 상품도 교환·환불이 되나요?",
                          "부품용(미동작)은 동작을 보증하지 않아 미동작을 사유로 한 교환·환불 대상이 아닙니다. 다만 표기와 다른 하자가 있으면 수령 후 7일 이내 처리해 드립니다."))
    else:
        faq_pairs.append(("받고 나서 작동이 안 되면 어떻게 하나요?",
                          "수령 후 7일 이내 구동 문제가 확인되면 교환 또는 환불해 드립니다. 반품 배송비는 저희가 부담합니다."))
    faq_pairs.append((f"{pname} 관련 다른 상품도 있나요?",
                      f"네. 같은 기종의 소프트·본체·주변기기를 {pname} 카테고리에서 함께 보실 수 있습니다."))
    faqpage = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_pairs],
    }

    # ---- 본문 조각 ----
    if stock:
        buy_html = f"""        <div class="buy">
          <a class="btn btn-accent" href="/cart/add?sku={sku}">바로 구매</a>
          <a class="btn btn-ghost" href="/cart/add?sku={sku}&amp;mode=cart">장바구니</a>
        </div>"""
        stock_html = '<p class="stock"><span class="dot" aria-hidden="true"></span>재고 1개 · 중고 특성상 동일 상품 재입고는 불확실합니다</p>'
        price_html = f'<p class="price">{price:,}원</p>'
    else:
        buy_html = """        <div class="buy" style="grid-template-columns:1fr">
          <a class="btn btn-muted" href="#related">재입고 알림 · 다른 상품 보기</a>
        </div>"""
        stock_html = '<p class="stock out"><span class="dot" aria-hidden="true"></span>품절 · 동일 개체 재입고는 불확실합니다</p>'
        price_html = f'<p class="price soldout">{price:,}원</p>'

    work_cell = ('<span class="warn">부품용(미동작)</span> · 동작 보증 제외'
                 if is_parts else '<span class="okk">실기 구동 확인 완료</span>')
    region_cell = (f"{region} · 국내 유통 본체 호환 여부 상세 참조" if region else "해당 없음 / 상세 참조")
    faq_html = "\n".join(
        f"""        <details{' open' if i == 0 else ''}>
          <summary>{q}</summary>
          <p>{a}</p>
        </details>""" for i, (q, a) in enumerate(faq_pairs))

    insp_line = ("부품용(미동작) 상품으로, 외관과 표기 상태만 확인했습니다."
                 if is_parts else "매입 후 실기에 연결해 구동을 확인하고 등록했습니다.")

    doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{prod_url}">

<meta property="og:type" content="product">
<meta property="og:site_name" content="AnigameMate">
<meta property="og:title" content="{esc(name)} {gl} 중고">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:url" content="{prod_url}">
<meta property="og:image" content="{BASE}/img/{sku}-1.jpg">
<meta property="og:locale" content="ko_KR">
<meta property="product:price:amount" content="{price}">
<meta property="product:price:currency" content="KRW">
<meta name="twitter:card" content="summary_large_image">

{ld(product_ld)}
{ld(breadcrumb)}
{ld(faqpage)}

<style>
{PCSS}
</style>
</head>
<body>

{HEADER}

<main>
  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼">
      <a href="index.html">홈</a> › <a href="retro-games.html">레트로게임 중고</a> ›
      <a href="retro-games-{slug}.html">{pname}</a> › <span aria-current="page">{leaf}</span>
    </nav>

    <div class="hero">

      <div class="gallery">
        <div class="main">실물 사진 1 · 정면</div>
        <div class="thumbs">
          <div>정면</div>
          <div>후면</div>
          <div>{'단자·상태' if not is_parts else '상태'}</div>
          <div>{'구동 화면' if not is_parts else '외관'}</div>
        </div>
        <p class="shot-note">
          모든 사진은 보정 없이 실제 판매 상품을 촬영한 것입니다. 흠집이나 변색도 그대로 담습니다.
        </p>
      </div>

      <div id="buy">
        <div class="chips">{hero_chips(grade, chips, stock)}</div>

        <h1>{name}</h1>
        <p class="sku mono">SKU {sku_code} · {pname}</p>

        <div class="price-box">
          {price_html}
          <p class="ship">배송비 3,500원 · 평일 14시 이전 결제 시 당일 출고</p>
          {stock_html}
        </div>

{buy_html}

        <div class="guard">
          <strong>7일 이내 구동 문제 시 교환·환불</strong>
          오래된 기기 특성상 접촉 불량이 생길 수 있습니다. 수령 후 7일 이내 구동 문제가 확인되면
          반품 배송비를 저희가 부담하고 교환 또는 환불해 드립니다.
        </div>
      </div>

    </div>
  </div>

  <section id="spec">
    <div class="wrap">
      <h2 class="title">상품 상태표</h2>
      <p class="sub">모든 중고 상품에 같은 항목을 같은 형식으로 표기합니다</p>
      <table>
        <caption>등급은 외관 기준이며, 동작 확인 결과는 등급과 별도로 표기합니다.</caption>
        <tbody>
          <tr><th scope="row">상태 등급</th><td><span class="grade-badge mono">{grade}</span> · {GRADE_DESC.get(grade, '')}</td></tr>
          <tr><th scope="row">구성품</th><td>{compos}</td></tr>
          <tr><th scope="row">동작 확인</th><td>{work_cell}</td></tr>
          <tr><th scope="row">지역코드</th><td>{region_cell}</td></tr>
          <tr><th scope="row">외관 상태</th><td>{meta}</td></tr>
          <tr><th scope="row">기종</th><td><a href="retro-games-{slug}.html" style="color:var(--brand);font-weight:600">{pname}</a></td></tr>
          <tr><th scope="row">유통 구분</th><td>중고 · 개인 매입 후 자체 검수</td></tr>
          <tr><th scope="row">상품번호(SKU)</th><td class="mono">{sku_code}</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section id="desc" style="background:#f4efe5">
    <div class="wrap">
      <h2 class="title">상품 설명</h2>
      <p class="sub">검수 과정과 실제 상태를 그대로 적습니다</p>
      <div class="desc">
        <h3>이 상품에 대해</h3>
        <p>{pname}용 {leaf} 중고 상품입니다. {insp_line} 실제 상태는 <strong>{meta}</strong>이며, 이를 근거로 {gl}으로 분류했습니다.</p>

        <h3>검수 결과</h3>
        <ul>
          <li>{'외관·표기 상태 확인 (동작 미보증 부품용)' if is_parts else '전원 인가 후 정상 구동 확인'}</li>
          <li>구성: {compos}</li>
          <li>지역코드: {region if region else '상세 참조'}</li>
          <li>등급 근거: {meta}</li>
        </ul>

        <h3>구매 전 확인하세요</h3>
        <ul>
          <li>중고 단일 상품이라 동일 개체 재입고는 불확실합니다.</li>
          <li>본체·주변기기 호환은 <a href="retro-games-{slug}.html">{pname} 카테고리</a>에서 함께 확인하세요.</li>
          {'<li>부품용(미동작) 상품으로 동작을 보증하지 않으며, 수리·부품 용도로만 구매하세요.</li>' if is_parts else '<li>표기된 사용감은 반품 사유에 해당하지 않습니다. 추가 사진이 필요하면 문의해 주세요.</li>'}
        </ul>
      </div>
    </div>
  </section>

  <section id="policy">
    <div class="wrap">
      <h2 class="title">배송 · 교환 · 환불</h2>
      <p class="sub">전자상거래법에 따른 청약철회와 별개로, 구동 보증을 추가로 제공합니다</p>
      <div class="cols">
        <div class="card">
          <h3>배송 안내</h3>
          <ul>
            <li>배송비 3,500원 (5만원 이상 무료)</li>
            <li>평일 14시 이전 결제 시 당일 출고</li>
            <li>출고 후 보통 1~2일 내 도착</li>
            <li>파손에 약한 상품은 완충재로 개별 포장해 발송</li>
          </ul>
        </div>
        <div class="card">
          <h3>교환 · 환불</h3>
          <ul>
            <li>단순 변심: 수령 후 7일 이내, 왕복 배송비 구매자 부담</li>
            <li>구동 문제·표기 불일치: 7일 이내, 배송비 판매자 부담</li>
            <li>중고 특성상 표기된 사용감은 반품 사유에 해당하지 않습니다</li>
            <li>부품용(미동작) 상품은 구동 보증에서 제외됩니다</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section id="faq" style="background:#f4efe5">
    <div class="wrap">
      <h2 class="title">이 상품 자주 묻는 질문</h2>
      <p class="sub">구매 전 가장 많이 확인하시는 내용입니다</p>
      <div class="faq">
{faq_html}
      </div>
    </div>
  </section>

  <section id="related">
    <div class="wrap">
      <h2 class="title">함께 보는 {pname} 상품</h2>
      <p class="sub">같은 기종의 다른 상품</p>
      <div class="prods">
{related_cards(p, sku)}
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
      <p>{pname} 및 각 게임 타이틀의 상표권과 저작권은 해당 권리자에게 있습니다.</p>
    </div>
  </div>
</footer>

</body>
</html>
"""
    return doc


def main():
    overwrite_all = "--all" in sys.argv
    made, skipped = [], []
    for p in PLATFORMS:
        for product in p["products"]:
            sku = product[1]
            path = os.path.join(HERE, f"product-{sku}.html")
            if os.path.exists(path) and not overwrite_all:
                skipped.append(sku)
                continue
            with open(path, "w", encoding="utf-8") as f:
                f.write(render(p, product))
            made.append(sku)
    print(f"생성 {len(made)}개 · 보존(스킵) {len(skipped)}개")
    if skipped:
        print("  보존:", ", ".join(skipped))


if __name__ == "__main__":
    main()
