# -*- coding: utf-8 -*-
"""
마무리 작업:
  1) 전 페이지 공통 푸터에 사이트맵성 링크(게시판·회사소개·약관 등) 주입
  2) sitemap.xml 생성 (canonical 기준, noindex 제외)
  3) robots.txt 생성
"""
import os, re, glob, io, sys, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
BASE = "https://anigamemate.com"

FOOTLINKS = """  <div class="wrap">
    <nav aria-label="푸터 링크" style="display:flex;gap:16px 18px;flex-wrap:wrap;padding-bottom:22px;margin-bottom:22px;border-bottom:1px solid var(--line);font-size:14px;font-weight:600;color:var(--brand)">
      <a href="index.html">홈</a>
      <a href="retro-games.html">레트로게임</a>
      <a href="character-goods.html">캐릭터굿즈</a>
      <a href="doujin.html">자가출판물</a>
      <a href="anime-goods.html">애니굿즈</a>
      <a href="board.html">게시판</a>
      <a href="about.html">회사소개</a>
      <a href="terms.html">이용약관</a>
      <a href="privacy.html">개인정보처리방침</a>
      <a href="https://blog.naver.com/tryforyou" target="_blank" rel="noopener noreferrer">네이버 블로그 ↗</a>
      <a href="https://anigamemate.tistory.com/" target="_blank" rel="noopener noreferrer">티스토리 ↗</a>
      <a href="https://smartstore.naver.com/anigamemate" target="_blank" rel="noopener noreferrer">스마트스토어 ↗</a>
    </nav>
  </div>
"""


def inject_footer():
    inj = skip = 0
    for f in glob.glob("*.html"):
        s = open(f, encoding="utf-8").read()
        if 'aria-label="푸터 링크"' in s:
            skip += 1
            continue
        if '<div class="wrap foot">' in s:
            s = s.replace('<div class="wrap foot">', FOOTLINKS + '  <div class="wrap foot">', 1)
            open(f, "w", encoding="utf-8").write(s)
            inj += 1
    print(f"푸터 링크 주입: {inj}개 · 이미 있음/미대상 {skip}개")


def build_sitemap():
    rows = []
    for f in sorted(glob.glob("*.html")):
        s = open(f, encoding="utf-8").read()
        mc = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        mr = re.search(r'<meta name="robots" content="([^"]+)"', s)
        if not mc:
            continue
        robots = mr.group(1) if mr else "index"
        if "noindex" in robots:
            continue
        loc = mc.group(1)
        lastmod = datetime.date.fromtimestamp(os.path.getmtime(f)).isoformat()
        # 우선순위: 홈 1.0, 상단 카테고리 0.9, 상품 0.6, 그 외 0.7
        if loc.rstrip("/") == BASE:
            pr = "1.0"
        elif "/p/" in loc:
            pr = "0.6"
        elif loc.count("/") <= 3:  # https://host/xxx
            pr = "0.9"
        else:
            pr = "0.7"
        rows.append((loc, lastmod, pr))
    body = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n    <priority>{pr}</priority>\n  </url>"
        for loc, lm, pr in rows)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + body + "\n</urlset>\n")
    open("sitemap.xml", "w", encoding="utf-8").write(xml)
    print(f"sitemap.xml 생성: {len(rows)}개 URL (noindex 제외)")


def build_robots():
    txt = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /cart/\n"
        "Disallow: /board/write\n"
        "Disallow: /*?type=\n"
        "\n"
        f"Sitemap: {BASE}/sitemap.xml\n"
    )
    open("robots.txt", "w", encoding="utf-8").write(txt)
    print("robots.txt 생성")


if __name__ == "__main__":
    inject_footer()
    build_sitemap()
    build_robots()
