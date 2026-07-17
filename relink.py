# -*- coding: utf-8 -*-
"""
페이지 상호 연동(링크 배선) 정리 + 상단 내비 플레이스홀더 생성.
  A) 상품 카드 절대경로  href="/p/<sku>"          → href="product-<sku>.html"
  B) 미존재 상품유형 페이지 retro-games-<slug>-<type>.html
        → retro-games-<slug>.html?type=<type>   (같은 카테고리 필터뷰 · 404 제거)
  C) 상단 내비 미구현 카테고리 3종 플레이스홀더('준비 중') 생성
     : anime-goods.html / character-goods.html / doujin.html
"""
import sys, io, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

RE_P = re.compile(r'href="/p/([a-z0-9-]+)"')
RE_TYPE = re.compile(r'retro-games-([a-z0-9-]+?)-(software|console|accessories|parts)\.html')

def relink():
    changed = 0
    for f in glob.glob("*.html"):
        s = open(f, encoding="utf-8").read()
        orig = s
        s = RE_P.sub(r'href="product-\1.html"', s)
        s = RE_TYPE.sub(r'retro-games-\1.html?type=\2', s)
        if s != orig:
            open(f, "w", encoding="utf-8").write(s)
            changed += 1
            print(f"  배선 수정: {f}")
    print(f"링크 재배선 완료: {changed}개 파일")

PLACEHOLDER = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | AnigameMate</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://anigamemate.com/{slug}">
<style>
  :root{{--bg:#fbf7f0;--surface:#fff;--ink:#1b1a2e;--muted:#5d5b78;--brand:#3b2f8f;
    --brand-dark:#241c63;--accent:#e8543f;--line:#e6e0d6;--radius:14px}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
    color:var(--ink);background:var(--bg);line-height:1.7}}
  .wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
  a{{color:inherit;text-decoration:none}}
  .btn{{display:inline-block;background:var(--brand);color:#fff;font-weight:600;
    padding:14px 26px;border-radius:10px;font-size:16px;transition:background .2s}}
  .btn:hover{{background:var(--brand-dark)}}
  .btn-ghost{{background:#fff;color:var(--brand);border:2px solid var(--brand)}}
  header{{position:sticky;top:0;z-index:50;background:rgba(251,247,240,.94);
    backdrop-filter:blur(8px);border-bottom:2px solid var(--ink)}}
  .nav{{display:flex;align-items:center;justify-content:space-between;height:66px;gap:16px}}
  .logo{{font-weight:800;font-size:20px;color:var(--brand);letter-spacing:-.02em}}
  .logo span{{color:var(--accent)}}
  .nav-links{{display:flex;gap:18px;align-items:center;font-size:15px}}
  .nav-links a[aria-current="page"]{{color:var(--brand);font-weight:700}}
  .nav .btn{{padding:10px 18px;font-size:15px}}
  .crumb{{padding:18px 0 0;font-size:14px;color:var(--muted)}}
  .hero{{text-align:center;padding:96px 0 90px;max-width:640px;margin:0 auto}}
  .tag{{display:inline-block;background:#eee9f7;color:var(--brand);font-weight:700;font-size:13px;
    padding:6px 14px;border-radius:999px;margin-bottom:20px}}
  h1{{font-size:clamp(28px,5vw,40px);letter-spacing:-.03em;font-weight:800;margin-bottom:14px}}
  .hero p{{color:var(--muted);font-size:17px;margin-bottom:28px}}
  .cta{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
  footer{{border-top:2px solid var(--ink);padding:40px 0;color:var(--muted);font-size:14px}}
  @media(max-width:600px){{.nav-links{{display:none}}}}
</style>
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="logo" href="index.html">Anigame<span>Mate</span></a>
    <nav class="nav-links" aria-label="주요 메뉴">
      <a href="retro-games.html">레트로게임</a>
      <a href="character-goods.html"{cur_character}>캐릭터굿즈</a>
      <a href="doujin.html"{cur_doujin}>자가출판물</a>
      <a href="anime-goods.html"{cur_anime}>애니굿즈</a>
    </nav>
    <a class="btn" href="retro-games.html">레트로게임 보기</a>
  </div>
</header>
<main>
  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <span aria-current="page">{title}</span></nav>
    <section class="hero">
      <span class="tag">준비 중</span>
      <h1>{title} 카테고리는 준비 중입니다</h1>
      <p>{desc} 지금은 레트로게임 중고 카테고리가 먼저 열려 있어요. 오픈 알림을 원하시면 레트로게임 페이지에서 재입고·오픈 알림을 신청해 주세요.</p>
      <div class="cta">
        <a class="btn" href="retro-games.html">레트로게임 중고 둘러보기</a>
        <a class="btn btn-ghost" href="index.html">홈으로</a>
      </div>
    </section>
  </div>
</main>
<footer>
  <div class="wrap">
    <p>© 2026 AnigameMate. All rights reserved.</p>
    <p>사업자등록번호 000-00-00000 · 통신판매업신고 제0000-서울○○-0000호</p>
  </div>
</footer>
</body>
</html>
"""

PLACEHOLDERS = [
    ("character-goods.html", "캐릭터굿즈", "산리오·짱구 등 캐릭터 굿즈를 정품 기준으로 준비하고 있습니다."),
    ("doujin.html", "자가출판물", "동인지·자가출판물 카테고리를 준비하고 있습니다."),
    ("anime-goods.html", "애니굿즈", "애니메이션 피규어·굿즈 카테고리를 준비하고 있습니다."),
]

def make_placeholders():
    for slug, title, desc in PLACEHOLDERS:
        html = PLACEHOLDER.format(
            title=title, desc=desc, slug=slug.replace(".html", ""),
            cur_character=' aria-current="page"' if slug == "character-goods.html" else "",
            cur_doujin=' aria-current="page"' if slug == "doujin.html" else "",
            cur_anime=' aria-current="page"' if slug == "anime-goods.html" else "",
        )
        open(slug, "w", encoding="utf-8").write(html)
        print(f"  플레이스홀더 생성: {slug}")

if __name__ == "__main__":
    make_placeholders()
    relink()
