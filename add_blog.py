# -*- coding: utf-8 -*-
"""네이버 블로그(anigamemate) 사이트 연동 — 상단 내비 + 푸터 링크 주입."""
import re, glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BLOG = "https://blog.naver.com/tryforyou"
NAV_LINK = f'<a href="{BLOG}" target="_blank" rel="noopener noreferrer">블로그 ↗</a>'
FOOT_LINK = f'<a href="{BLOG}" target="_blank" rel="noopener noreferrer">네이버 블로그 ↗</a>'

# 헤더 nav-links 끝(게시판 뒤 </nav>)에 블로그 링크
RE_HEAD = re.compile(r'(<a href="board\.html"[^>]*>게시판</a>)(\s*</nav>)')
# 푸터 링크 행 끝(개인정보처리방침 뒤)에 블로그 링크
RE_FOOT = re.compile(r'(<a href="privacy\.html">개인정보처리방침</a>)')

def main():
    head_n = foot_n = skip = 0
    for f in glob.glob("*.html"):
        s = open(f, encoding="utf-8").read()
        if BLOG in s:
            skip += 1
            continue
        o = s
        s, h = RE_HEAD.subn(r'\1\n      ' + NAV_LINK + r'\2', s, count=1)
        s, ft = RE_FOOT.subn(r'\1\n      ' + FOOT_LINK, s, count=1)
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
            head_n += h
            foot_n += ft
    print(f"블로그 링크 주입 — 헤더 {head_n}개 · 푸터 {foot_n}개 · 스킵(이미 있음) {skip}")

if __name__ == "__main__":
    main()
