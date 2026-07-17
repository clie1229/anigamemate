# -*- coding: utf-8 -*-
"""회사소개·이용약관·개인정보처리방침 정적 페이지 생성 (gen_shop 디자인 재사용)."""
import os
from gen_shop import page, ld, BASE, HERE

def panel(title, sub, blocks):
    inner = "\n".join(f"        <h3 style=\"font-size:17px;margin:18px 0 8px\">{h}</h3>\n" +
                      "\n".join(f"        <p>{p}</p>" for p in ps) for h, ps in blocks)
    return f"""  <div class="wrap">
    <nav class="crumb" aria-label="브레드크럼"><a href="index.html">홈</a> › <span aria-current="page">{title}</span></nav>
    <div class="head"><h1>{title}</h1><p class="lead">{sub}</p></div>
  </div>
  <section>
    <div class="wrap">
      <div class="about" style="max-width:860px">
{inner}
      </div>
    </div>
  </section>"""

def crumb_ld(title, slug):
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": title, "item": f"{BASE}/{slug}"}]})

PAGES = {
    "about": ("회사소개", "AnigameMate는 애니굿즈·캐릭터 굿즈·자가출판물·레트로게임 중고를 취급하는 온라인 스토어입니다.", [
        ("우리가 하는 일", [
            "AnigameMate는 흩어져 있던 애니·게임 팬의 물건을 한 곳에서 안전하게 거래할 수 있도록 돕습니다. 레트로게임 중고를 중심으로 캐릭터 굿즈·자가출판물·애니굿즈까지 카테고리를 넓혀가고 있습니다."]),
        ("검수 원칙", [
            "모든 중고 게임은 실기에 연결해 구동과 세이브를 확인한 뒤 S·A·B 상태 등급으로 등록합니다. 동작하지 않는 개체는 부품·수리용으로 따로 분류합니다.",
            "굿즈는 정발·병행수입 여부를, 자가출판물은 창작자·발행 정보를 상품마다 표기합니다. 라이선스가 불분명하거나 진품 판단이 어려운 상품은 취급하지 않습니다."]),
        ("사업자 정보", [
            "상호 AnigameMate · 대표 ○○○ · 서울 ○○구 ○○로 00, 0층",
            "사업자등록번호 000-00-00000 · 통신판매업신고 제0000-서울○○-0000호",
            "고객문의 help@anigamemate.com · 평일 10:00–18:00"]),
    ]),
    "terms": ("이용약관", "AnigameMate 서비스 이용에 관한 기본 약관입니다. (예시 문안)", [
        ("제1조 (목적)", ["이 약관은 AnigameMate(이하 '회사')가 제공하는 온라인 쇼핑몰 서비스의 이용 조건과 절차, 회사와 이용자의 권리·의무를 규정함을 목적으로 합니다."]),
        ("제2조 (상품과 표기)", ["회사는 중고 상품의 상태 등급·동작 확인 결과·구성품을 상세페이지에 표기합니다. 표기된 사용감은 반품 사유에 해당하지 않으며, 표기와 다른 하자는 교환·환불 대상입니다."]),
        ("제3조 (청약철회 및 환불)", ["이용자는 수령 후 7일 이내 청약철회를 할 수 있습니다. 단순 변심 시 왕복 배송비는 이용자가 부담하며, 표기 불일치·구동 문제는 회사가 배송비를 부담합니다. 자가출판물·개봉 굿즈 등 재판매가 어려운 상품은 반품이 제한될 수 있습니다."]),
        ("제4조 (게시물)", ["이용자가 게시판에 등록한 게시물의 권리와 책임은 작성자에게 있습니다. 회사는 관련 법령이나 운영정책에 어긋나는 게시물을 사전 통지 없이 삭제할 수 있습니다."]),
        ("부칙", ["본 약관은 예시 문안이며, 실제 서비스 운영 시 관련 법령에 맞게 개정·공지됩니다."]),
    ]),
    "privacy": ("개인정보처리방침", "AnigameMate가 수집·이용하는 개인정보와 처리 방침입니다. (예시 문안)", [
        ("수집하는 개인정보", ["회원가입·주문 시 이름, 연락처, 배송지, 이메일, 결제 정보를 수집합니다. 재입고 알림 신청 시 이메일 주소를 수집합니다."]),
        ("이용 목적", ["주문 상품의 배송, 고객 문의 응대, 재입고·신상 알림 발송, 법령상 의무 이행을 위해 개인정보를 이용합니다."]),
        ("보유 및 파기", ["관련 법령이 정한 기간(전자상거래법상 계약·청약철회 기록 5년 등) 동안 보관 후 파기합니다. 알림 수신은 언제든 무료로 해지할 수 있습니다."]),
        ("이용자 권리", ["이용자는 자신의 개인정보 열람·정정·삭제·처리정지를 요청할 수 있습니다. 요청은 help@anigamemate.com으로 접수합니다."]),
        ("부칙", ["본 방침은 예시 문안이며, 실제 서비스 운영 시 관련 법령에 맞게 개정·공지됩니다."]),
    ]),
}

def main():
    for slug, (title, sub, blocks) in PAGES.items():
        canon = f"{BASE}/{slug}"
        body = panel(title, sub, blocks)
        html = page(f"{title} | AnigameMate", sub, canon, crumb_ld(title, slug), body, current=None)
        open(os.path.join(HERE, f"{slug}.html"), "w", encoding="utf-8").write(html)
        print("생성", slug + ".html")

if __name__ == "__main__":
    main()
