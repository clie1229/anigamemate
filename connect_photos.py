# -*- coding: utf-8 -*-
"""실제 사진 연결 도구.
사용법
  1) photos/ 폴더에 실제 사진을 넣는다. 파일명은  <sku>-<번호>.jpg  형식.
       예) fc-smb3-1.jpg  fc-smb3-2.jpg  cg-sanrio-cinnamoroll-key-1.png
       (번호 1 = 대표/카드 썸네일, 2·3·4 = 갤러리 추가 컷)
  2)  python connect_photos.py   실행.
       → photos/의 사진을 img/로 복사하고, 해당 상품 페이지·카드의
         플레이스홀더(.svg)를 실제 사진(.jpg/.png/...)으로 자동 교체.
       → 사진이 없는 컷은 기존 일러스트 플레이스홀더가 그대로 유지됨.
  3) git add -A && git commit && git push  로 배포.

  python connect_photos.py guide   → photos/사진-파일이름-가이드.md 재생성.
"""
import os, re, glob, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("photos", exist_ok=True)
os.makedirs("img", exist_ok=True)
EXTS = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif")


def connect():
    photos = [f for f in glob.glob("photos/*") if os.path.splitext(f)[1].lower() in EXTS]
    if not photos:
        print("photos/ 폴더에 사진이 없습니다. <sku>-<번호>.jpg 형식으로 넣어주세요.")
        print("파일명은  photos/사진-파일이름-가이드.md  참고.")
        return
    connected = skipped = 0
    htmls = glob.glob("*.html")
    cache = {h: open(h, encoding="utf-8").read() for h in htmls}
    changed = set()
    for f in sorted(photos):
        base = os.path.basename(f)
        stem, ext = os.path.splitext(base)
        ext = ext.lower()
        m = re.match(r"^(.+)-(\d+)$", stem)
        if not m:
            print(f"  건너뜀(형식이 <sku>-<번호>가 아님): {base}")
            skipped += 1
            continue
        sku, idx = m.group(1), m.group(2)
        dst = f"img/{sku}-{idx}{ext}"
        shutil.copyfile(f, dst)
        old = f'img/{sku}-{idx}.svg'
        new = f'img/{sku}-{idx}{ext}'
        hit = 0
        for h in htmls:
            if old in cache[h]:
                cache[h] = cache[h].replace(old, new)
                changed.add(h); hit += 1
        print(f"  연결: {base}  → {dst}  (HTML {hit}곳 교체)")
        connected += 1
    for h in changed:
        open(h, "w", encoding="utf-8").write(cache[h])
    print(f"\n완료: 사진 {connected}장 연결 · 파일 {len(changed)}개 수정 · 건너뜀 {skipped}")
    if connected:
        print("다음: git add -A && git commit -m \"실제 사진 연결\" && git push")


def guide():
    from platforms import PLATFORMS
    from shop import CATEGORIES
    rows = []
    LAB = {  # 유형별 컷 라벨(참고용)
        "retro": "1 대표(정면) / 2 후면 / 3 단자 / 4 구동화면(디스크는 디스크·케이스 앞·뒤·구동)",
        "goods": "1 대표(정면) / 2 후면 / 3 디테일 / 4 구성(유형에 따라 박스·사이즈 등)",
    }
    def add(sku, name, cat):
        rows.append(f"| `{sku}` | {name} | `{sku}-1.jpg` … `{sku}-4.jpg` |")
    rows_r, rows_g = [], []
    for p in PLATFORMS:
        for (name, sku, *_ ) in ((t[0], t[1]) for t in p["products"]):
            pass
    lines = ["# 실제 사진 파일 이름 가이드", "",
             "photos/ 폴더에 아래 파일명으로 사진을 넣고 `python connect_photos.py` 실행.",
             "- `-1` = 대표 이미지(카드 썸네일+갤러리 첫 컷), `-2`~`-4` = 갤러리 추가 컷",
             "- 확장자는 .jpg .png .webp 등 가능. 일부 컷만 넣어도 됩니다(나머지는 기존 이미지 유지).", "",
             "## 레트로게임", "", "| SKU | 상품명 | 넣을 파일명 |", "|---|---|---|"]
    for p in PLATFORMS:
        for t in p["products"]:
            name, sku = t[0], t[1]
            lines.append(f"| `{sku}` | {name} | `{sku}-1.jpg` ~ `{sku}-4.jpg` |")
    lines += ["", "## 캐릭터굿즈 · 자가출판물 · 애니굿즈", "", "| SKU | 상품명 | 넣을 파일명 |", "|---|---|---|"]
    for c in CATEGORIES:
        for s in c["subs"]:
            for t in s["products"]:
                name, sku = t[0], t[1]
                lines.append(f"| `{sku}` | {name} | `{sku}-1.jpg` ~ `{sku}-4.jpg` |")
    open("photos/사진-파일이름-가이드.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("guide 생성: photos/사진-파일이름-가이드.md")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "guide":
        guide()
    else:
        connect()
