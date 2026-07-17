# AnigameMate

애니굿즈·캐릭터 굿즈·자가출판물·레트로게임 중고를 다루는 정적 쇼핑몰 사이트입니다.
네이버·구글·AI검색(GEO/AEO) 노출을 겨냥해 구조화 데이터(JSON-LD)와 온페이지 SEO를 갖춘 순수 HTML/CSS 사이트입니다.

## 구성

| 영역 | 페이지 |
|------|--------|
| 홈 | `index.html` |
| 레트로게임 | `retro-games.html` + 기종 19 (`retro-games-<slug>.html`) + 기종×유형 76 (`retro-games-<slug>-<type>.html`) + 상품 59 (`product-<sku>.html`) |
| 캐릭터굿즈·자가출판물·애니굿즈 | 허브 3 + 하위분류 12 + 굿즈 상품 25 |
| 게시판 | `board.html` + 게시글(`board-<id>.html`) + 글쓰기(`board-write.html`) |
| 회사 정보 | `about.html` · `terms.html` · `privacy.html` |
| SEO | `sitemap.xml` · `robots.txt` |

총 208개 HTML 페이지. 모든 페이지가 상단 내비·공통 푸터·브레드크럼으로 상호 연결됩니다.
외부 채널(네이버 블로그·티스토리·스마트스토어)은 내비·푸터·`sameAs` 구조화 데이터로 연동돼 있습니다.

## 재생성 (데이터 → HTML)

데이터 파일만 고치고 아래 스크립트를 순서대로 실행하면 사이트 전체가 재생성됩니다. (Python 3.9+)

```bash
python gen_pages.py      # 기종 카테고리 페이지
python gen_products.py   # 레트로 상품 페이지
python gen_types.py      # 기종×유형 페이지
python gen_shop.py       # 캐릭터/자가출판/애니 카테고리 + 게시판
python gen_info.py       # 회사소개·약관·개인정보
python relink.py         # 링크 배선 + 플레이스홀더
python finalize.py       # 공통 푸터 링크 + sitemap.xml + robots.txt
python add_blog.py; python add_tistory.py; python add_store.py   # 외부 채널 링크
```

- 데이터: `platforms.py`(레트로 기종·상품), `shop.py`(굿즈 카테고리·게시판)
- 기획: `CLAUDE.md`, `IA-레트로게임중고.md`

## 로컬 미리보기

```bash
python -m http.server 5500
# http://localhost:5500
```

## 배포 (GitHub Pages)

정적 사이트이므로 저장소 루트를 GitHub Pages로 지정하면 그대로 서비스됩니다.
(Settings → Pages → Branch: `main` / `/root`)

## 참고 (배포 전 교체 필요)

- 가격·시세는 예시(placeholder)입니다. 실제 시세로 교체하세요.
- 사업자등록번호·주소 등 회사 정보는 예시 값입니다.
- 장바구니·구독·게시판 등록(`/cart/add`, `/subscribe`, `/board/*`)은 백엔드가 필요한 데모 엔드포인트입니다.
