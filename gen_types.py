# -*- coding: utf-8 -*-
"""
기종 × 상품유형 정적 페이지 생성기  retro-games-<slug>-<type>.html
  유형: software(소프트) / console(본체) / accessories(주변기기) / parts(부품·수리용)
  - 상품 있는 조합: index,follow + 상품 목록 + ItemList JSON-LD
  - 빈 조합: noindex,follow + 빈 상태 안내 (IA 얇은 페이지 색인 방지)
  - 디자인/CSS/헤더/등급표/관련기종은 카테고리 페이지(gen_pages)와 동일 재사용
생성 후 relink_types.py 로 모든 ?type= 링크를 실제 파일로 되돌린다.
"""
import sys, os
from platforms import PLATFORMS
from gen_pages import CSS, HEADER, GRADE_SECTION, RELATED_SUB, related_for  # gen_pages가 stdout을 UTF-8로 래핑

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://anigamemate.com"
SAB = ("S", "A", "B")
NL = ",\n"

TYPES = ["software", "console", "accessories", "parts"]
TYPE_LABEL = {"software": "소프트", "console": "본체",
              "accessories": "주변기기", "parts": "부품·수리용"}
TYPE_COPY = {
    "software": dict(
        lead="{p} 중고 소프트(타이틀). 카트리지·디스크를 실기 구동과 세이브까지 확인한 뒤 등록합니다.",
        q="{p} 소프트 중고, 작동 확인은 하나요?",
        a="<strong>모든 타이틀을 실기에 넣어 구동과 세이브를 확인한 뒤 S·A·B 등급으로 등록합니다.</strong> 동작하지 않는 개체는 부품·수리용으로 따로 분류하고, 박스풀셋·지역코드를 상품마다 표기합니다.",
        about="{p}의 게임 타이틀(소프트) 카테고리입니다. 박스풀셋·본품만 구성과 지역코드를 상품마다 표기하며, 모든 소프트는 실기 구동을 확인해 등록합니다."),
    "console": dict(
        lead="{p} 중고 본체. 전원·영상 출력·구동을 확인하고 외관 상태를 실물 사진에 담습니다.",
        q="{p} 본체 중고, 어떤 점을 확인하나요?",
        a="<strong>전원·영상 출력·구동을 확인하고 변색과 외관 상태를 실물 사진으로 담습니다.</strong> 구성품(컨트롤러·케이블)과 모델 번호를 상품마다 표기합니다.",
        about="{p} 본체 카테고리입니다. 모델별 사양과 구성품, 변색·외관 상태를 표기하고 실기 구동을 확인해 등록합니다."),
    "accessories": dict(
        lead="{p} 주변기기. 컨트롤러·케이블·메모리카드·변환기 등을 동작 확인 후 등록합니다.",
        q="{p} 주변기기도 동작 확인을 하나요?",
        a="<strong>컨트롤러 버튼 반응, 케이블·메모리카드 동작을 확인해 등록합니다.</strong> 순정/서드파티 여부와 호환 정보를 함께 표기합니다.",
        about="{p} 주변기기(컨트롤러·케이블·메모리카드·변환기 등) 카테고리입니다. 순정/서드파티 여부와 동작 확인 결과를 표기합니다."),
    "parts": dict(
        lead="{p} 부품·수리용. 미동작 개체와 수리용 부품을 명확히 표기해 판매합니다.",
        q="{p} 부품용 상품은 작동하나요?",
        a="<strong>부품·수리용은 동작을 보증하지 않는 미동작 개체입니다.</strong> 제목과 상태표에 부품용(미동작)을 표기하며, 미동작을 사유로 한 교환·환불 대상이 아닙니다.",
        about="{p} 부품·수리용 카테고리입니다. 미동작 개체와 수리용 부품을 취급하며, 동작을 보증하지 않습니다. 수리·부품 용도로만 구매하세요."),
}


def classify(name, sku, price, grade, chips, meta, stock):
    if grade == "부품용" or any("미동작" in c for c in chips):
        return "parts"
    if any("본체" in c for c in chips) or "본체" in name:
        return "console"
    if (any(("주변기기" in c or "부품" in c or "하네스" in c) for c in chips)
            or any(k in name for k in ("컨트롤러", "컨버터", "어댑터", "메모리카드", "하네스", "패드"))):
        return "accessories"
    return "software"


def sku_code(sku, grade):
    return sku.upper() + "-" + (grade if grade in SAB else "PARTS")


def grade_label(grade):
    return f"{grade}등급" if grade in SAB else grade


def card(product):
    name, sku, price, grade, chips, meta, stock = product
    if stock:
        first = f'<span class="chip g">{grade_label(grade)}</span>'
        price_cls = "price"
        btn = '<span class="btn btn-sm btn-accent" style="text-align:center">바로 구매</span>'
    else:
        first = '<span class="chip off">품절</span>'
        price_cls = "price soldout"
        btn = '<span class="btn btn-sm" style="text-align:center;background:var(--muted)">재입고 알림</span>'
    chip_html = first + "".join(f'<span class="chip">{c}</span>' for c in chips)
    return f"""          <a class="prod" href="product-{sku}.html">
            <div class="thumb">실물 사진</div>
            <div class="prod-body">
              <div class="chips">{chip_html}</div>
              <h3>{name}</h3>
              <p class="meta">{meta}</p>
              <p class="{price_cls}">{price:,}원</p>
              {btn}
            </div>
          </a>"""


def filters_block(slug, t):
    return f"""      <aside class="filters">
        <h3>필터</h3>
        <p class="hint">필터 결과 페이지는 색인되지 않고 이 카테고리로 canonical 처리됩니다.</p>
        <form action="retro-games-{slug}-{t}.html" method="get">
          <fieldset>
            <legend>상태 등급</legend>
            <label class="opt"><input type="checkbox" name="grade" value="S"> S · 미개봉/최상</label>
            <label class="opt"><input type="checkbox" name="grade" value="A"> A · 경미한 사용감</label>
            <label class="opt"><input type="checkbox" name="grade" value="B"> B · 흠집 있음</label>
            <label class="opt"><input type="checkbox" name="grade" value="parts"> 부품용 (미동작)</label>
          </fieldset>
          <fieldset>
            <legend>구성품</legend>
            <label class="opt"><input type="checkbox" name="set" value="full"> 박스풀셋</label>
            <label class="opt"><input type="checkbox" name="set" value="box"> 박스만</label>
            <label class="opt"><input type="checkbox" name="set" value="rom"> 본품(롬)만</label>
          </fieldset>
          <fieldset>
            <legend>지역코드</legend>
            <label class="opt"><input type="checkbox" name="region" value="ntsc-j"> NTSC-J (일본판)</label>
            <label class="opt"><input type="checkbox" name="region" value="ntsc-u"> NTSC-U (북미판)</label>
            <label class="opt"><input type="checkbox" name="region" value="kr"> 한글판 / 국내판</label>
          </fieldset>
          <fieldset>
            <legend>가격대</legend>
            <label class="opt"><input type="checkbox" name="price" value="0-30000"> ~3만원</label>
            <label class="opt"><input type="checkbox" name="price" value="30000-100000"> 3~10만원</label>
            <label class="opt"><input type="checkbox" name="price" value="100000-300000"> 10~30만원</label>
            <label class="opt"><input type="checkbox" name="price" value="300000-"> 30만원~</label>
          </fieldset>
          <button type="submit" class="btn btn-sm" style="width:100%">필터 적용</button>
        </form>
      </aside>"""


def json_ld(p, t, prods):
    slug, name = p["slug"], p["name"]
    label = TYPE_LABEL[t]
    url = f"{BASE}/retro-games/{slug}/{t}"
    breadcrumb = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "홈", "item": "{BASE}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "레트로게임 중고", "item": "{BASE}/retro-games" }},
    {{ "@type": "ListItem", "position": 3, "name": "{name}", "item": "{BASE}/retro-games/{slug}" }},
    {{ "@type": "ListItem", "position": 4, "name": "{label}", "item": "{url}" }}
  ]
}}
</script>"""
    if not prods:
        return breadcrumb
    items = []
    for i, (pn, sku, price, grade, chips, meta, stock) in enumerate(prods, 1):
        avail = "InStock" if stock else "OutOfStock"
        items.append(f"""    {{ "@type": "ListItem", "position": {i}, "item": {{
      "@type": "Product", "name": "{pn}",
      "url": "{BASE}/p/{sku}", "sku": "{sku_code(sku, grade)}",
      "itemCondition": "https://schema.org/UsedCondition",
      "offers": {{ "@type": "Offer", "price": "{price}", "priceCurrency": "KRW",
        "availability": "https://schema.org/{avail}", "itemCondition": "https://schema.org/UsedCondition" }} }} }}""")
    itemlist = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "{name} {label} 중고 상품",
  "numberOfItems": {len(prods)},
  "itemListElement": [
{NL.join(items)}
  ]
}}
</script>"""
    return breadcrumb + "\n" + itemlist


def render(p, t, prods):
    slug, name = p["slug"], p["name"]
    label = TYPE_LABEL[t]
    copy = TYPE_COPY[t]
    has = len(prods) > 0
    url = f"{BASE}/retro-games/{slug}/{t}"
    title = f"{name} {label} 중고 | AnigameMate"
    desc = (f"{name} 중고 {label}. " + copy["about"].format(p=name))[:150]
    robots = "index, follow" if has else "noindex, follow"

    tabs = f'<a class="tab" href="retro-games-{slug}.html">전체</a>\n'
    for tt in TYPES:
        cur = ' aria-current="true"' if tt == t else ""
        tabs += f'        <a class="tab" href="retro-games-{slug}-{tt}.html"{cur}>{TYPE_LABEL[tt]}</a>\n'

    # 본문(상품 목록 또는 빈 상태)
    if has:
        body = f"""  <section id="list">
    <div class="wrap layout">

{filters_block(slug, t)}

      <div>
        <h2 class="title">{name} {label} 중고 상품</h2>
        <p class="sub">전체 {len(prods)}개 · 실기 동작 확인 완료</p>
        <div class="prods">

{chr(10).join(card(pr) for pr in prods)}

        </div>
      </div>
    </div>
  </section>"""
    else:
        body = f"""  <section id="list">
    <div class="wrap">
      <div class="about" style="max-width:none;text-align:center;padding:44px 30px">
        <h2 style="margin-bottom:8px">아직 등록된 {name} {label} 상품이 없습니다</h2>
        <p style="margin-bottom:20px">입고되는 대로 이 페이지에 등록합니다. 재입고·입고 알림을 신청하시면 가장 먼저 알려드립니다.</p>
        <p><a class="rel" href="retro-games-{slug}.html" style="display:inline-block">{name} 전체 상품 보기</a>
           <a class="rel" href="#alert" style="display:inline-block">입고 알림 신청</a></p>
      </div>
    </div>
  </section>"""

    about_html = f"""  <section id="about">
    <div class="wrap">
      <div class="about">
        <h2>{name} {label} 안내</h2>
        <p>{copy['about'].format(p=name)}</p>
      </div>
    </div>
  </section>"""

    rels = related_for(p)
    rel_links = "\n        ".join(
        f'<a class="rel" href="retro-games-{q["slug"]}.html">{q["name"]}</a>' for q in rels)
    rel_links += f'\n        <a class="rel" href="retro-games-{slug}.html">{name} 전체 보기</a>'
    related_html = f"""  <section id="related">
    <div class="wrap">
      <h2 class="title">함께 보는 기종</h2>
      <p class="sub">{RELATED_SUB.get(p['group'], '함께 보는 기종')}</p>
      <nav class="related" aria-label="관련 기종">
        {rel_links}
      </nav>
    </div>
  </section>"""

    alert_html = f"""  <section id="alert">
    <div class="wrap">
      <div class="cta-band">
        <h2>찾는 {name} {label} 상품이 없나요?</h2>
        <p>입고되면 가장 먼저 알려드립니다.</p>
        <form class="form" action="/subscribe" method="post">
          <label for="email" style="position:absolute;left:-9999px">이메일 주소</label>
          <input id="email" name="email" type="email" required placeholder="이메일 주소를 입력하세요">
          <button type="submit" class="btn btn-accent">알림 신청</button>
        </form>
        <p class="note">광고성 정보 수신에 동의하게 되며, 언제든 무료로 수신거부할 수 있습니다.</p>
      </div>
    </div>
  </section>"""

    footer = f"""<footer>
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
      <p>{name} 및 각 게임 타이틀의 상표권과 저작권은 해당 권리자에게 있습니다.</p>
    </div>
  </div>
</footer>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="AnigameMate">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{name} 중고 {label} · 실기 동작 확인 · S·A·B 등급 표기.">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og-{slug}.jpg">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">

{json_ld(p, t, prods)}

{CSS}
</head>
<body>

{HEADER}

<main>
  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼">
      <a href="index.html">홈</a> › <a href="retro-games.html">레트로게임 중고</a> › <a href="retro-games-{slug}.html">{name}</a> › <span aria-current="page">{label}</span>
    </nav>

    <div class="head">
      <h1>{name} {label} 중고</h1>
      <p class="lead">{copy['lead'].format(p=name)}</p>

      <div class="answer">
        <h2>{copy['q'].format(p=name)}</h2>
        <p>{copy['a'].format(p=name)}</p>
      </div>

      <nav class="tabs" aria-label="상품 유형">
        {tabs.rstrip()}
      </nav>
    </div>
  </div>

{body}

{GRADE_SECTION}

{about_html}

{related_html}

{alert_html}
</main>

{footer}

</body>
</html>
"""


def main():
    made = empty = 0
    for p in PLATFORMS:
        buckets = {t: [] for t in TYPES}
        for pr in p["products"]:
            buckets[classify(*pr)].append(pr)
        for t in TYPES:
            prods = buckets[t]
            path = os.path.join(HERE, f"retro-games-{p['slug']}-{t}.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(render(p, t, prods))
            made += 1
            if not prods:
                empty += 1
    print(f"유형 페이지 생성: {made}개 (상품 있음 {made - empty} · 빈 상태 {empty})")


if __name__ == "__main__":
    main()
