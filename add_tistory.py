# -*- coding: utf-8 -*-
"""티스토리 블로그(anigamemate.tistory.com) 연결 — 네이버 링크 옆에 나란히 주입.
   헤더 네이버 라벨을 '네이버 ↗'로 정리하고 '티스토리 ↗'를 추가한다."""
import glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TIST = "https://anigamemate.tistory.com/"
TIST_HEAD = f'<a href="{TIST}" target="_blank" rel="noopener noreferrer">티스토리 ↗</a>'
TIST_FOOT = f'<a href="{TIST}" target="_blank" rel="noopener noreferrer">티스토리 ↗</a>'

# 헤더: 네이버 링크(라벨 '블로그 ↗') → '네이버 ↗' 로 정리 + 티스토리 추가
OLD_HEAD = '<a href="https://blog.naver.com/tryforyou" target="_blank" rel="noopener noreferrer">블로그 ↗</a>'
NEW_HEAD = ('<a href="https://blog.naver.com/tryforyou" target="_blank" rel="noopener noreferrer">네이버 ↗</a>'
            '\n      ' + TIST_HEAD)
# 푸터: 네이버 블로그 링크 뒤에 티스토리 추가
OLD_FOOT = '<a href="https://blog.naver.com/tryforyou" target="_blank" rel="noopener noreferrer">네이버 블로그 ↗</a>'
NEW_FOOT = OLD_FOOT + '\n      ' + TIST_FOOT


def main():
    head_n = foot_n = skip = 0
    for f in glob.glob("*.html"):
        s = open(f, encoding="utf-8").read()
        if "anigamemate.tistory.com" in s:
            skip += 1
            continue
        o = s
        if OLD_HEAD in s:
            s = s.replace(OLD_HEAD, NEW_HEAD, 1); head_n += 1
        if OLD_FOOT in s:
            s = s.replace(OLD_FOOT, NEW_FOOT, 1); foot_n += 1
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
    print(f"티스토리 링크 주입 — 헤더 {head_n}개 · 푸터 {foot_n}개 · 스킵 {skip}")


if __name__ == "__main__":
    main()
