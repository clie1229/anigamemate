# -*- coding: utf-8 -*-
"""네이버 스마트스토어(smartstore.naver.com/anigamemate) 연동 —
   헤더·푸터의 티스토리 링크 뒤(양쪽)에 '스마트스토어 ↗' 추가."""
import glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

STORE = "https://smartstore.naver.com/anigamemate"
TIST_LINK = '<a href="https://anigamemate.tistory.com/" target="_blank" rel="noopener noreferrer">티스토리 ↗</a>'
STORE_LINK = f'\n      <a href="{STORE}" target="_blank" rel="noopener noreferrer">스마트스토어 ↗</a>'


def main():
    n = skip = 0
    for f in glob.glob("*.html"):
        s = open(f, encoding="utf-8").read()
        if "smartstore.naver.com" in s:
            skip += 1
            continue
        if TIST_LINK in s:
            s = s.replace(TIST_LINK, TIST_LINK + STORE_LINK)   # 헤더+푸터 양쪽
            open(f, "w", encoding="utf-8").write(s)
            n += 1
    print(f"스마트스토어 링크 주입: {n}개 파일 · 스킵 {skip}")


if __name__ == "__main__":
    main()
