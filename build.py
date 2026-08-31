import os
import json
import shutil
import random

# 15개의 타이틀 패턴 (출장과 마사지 분리 회피 구조)
TITLE_PATTERNS = [
    "{FULL_NAME} 출장 방문 마사지 · 1:1 홈케어 예약 │ S슬림홈케어",
    "{FULL_NAME} 출장 맞춤 힐링 마사지 코스 및 요금표 │ S슬림홈케어",
    "{FULL_NAME} 출장 전지역 안심 마사지 프로그램 안내 │ S슬림홈케어",
    "{FULL_NAME} 출장 릴렉싱 바디 마사지 제휴 예약 │ S슬림홈케어",
    "{FULL_NAME} 출장 홈테라피 힐링 마사지 코스 안내 │ S슬림홈케어",
    "{DONG} 출장 프라이빗 방문 마사지 서비스 │ S슬림홈케어",
    "{DONG} 출장 1:1 집중 힐링 마사지 예약 상담 │ S슬림홈케어",
    "{DONG} 출장 빠른 방문 케어 마사지 프로그램 │ S슬림홈케어",
    "{DONG} 출장 편안한 힐링 마사지 코스 안내 │ S슬림홈케어",
    "{DONG} 출장 맞춤 릴렉스 마사지 제휴 센터 │ S슬림홈케어",
    "{DISTRICT} {DONG} 출장 테라피 힐링 마사지 │ S슬림홈케어",
    "{DISTRICT} {DONG} 출장 전문 방문 마사지 요금 안내 │ S슬림홈케어",
    "{DISTRICT} {DONG} 출장 스트레스 해소 마사지 │ S슬림홈케어",
    "{DISTRICT} {DONG} 출장 프리미엄 홈케어 마사지 예약 │ S슬림홈케어",
    "{DISTRICT} {DONG} 출장 힐링 바디 마사지 코스 안내 │ S슬림홈케어"
]

# 15개의 디스크립션 패턴 (출장과 마사지 분리 회피 구조)
DESC_PATTERNS = [
    "{FULL_NAME} 전지역 출장 방문 케어 마사지 전문 S슬림홈케어입니다. 건식, 아로마, VIP스웨디시 코스 시간과 요금 확인. 문의: 0507-1280-3342",
    "{FULL_NAME} 일대 신속한 출장 1:1 홈 테라피 마사지 안내. 지친 하루를 달래주는 맞춤 힐링 케어 프로그램. 예약상담: 0507-1280-3342",
    "{FULL_NAME} 자택/오피스텔 출장 맞춤 릴렉싱 마사지 S슬림홈케어. 건식 지압부터 스페셜 아로마까지 완벽 케어. 문의: 0507-1280-3342",
    "{FULL_NAME} 어디서나 편안하게 받는 출장 전지역 힐링 마사지 서비스. 투명한 정찰제 가격표와 신속 배차. 예약: 0507-1280-3342",
    "{FULL_NAME} 일대 프리미엄 출장 전문 바디 마사지 예약 안내. 전문 힐러의 정성스러운 1:1 방문 관리. 상담: 0507-1280-3342",
    "{DONG} 인근 출장 프리미엄 바디 마사지 코스별 요금표 제공. 편안한 나만의 공간에서 즐기는 힐링. 상담: 0507-1280-3342",
    "{DONG} 지역 신속 방문 출장 1:1 맞춤 마사지 S슬림홈케어. 피로 회복을 위한 다양한 테라피 코스. 문의: 0507-1280-3342",
    "{DONG} 전지역 안심 출장 방문 힐링 마사지 안내. 건식, 아로마, 스웨디시 정찰제 코스 운영. 전화예약: 0507-1280-3342",
    "{DONG} 주민을 위한 출장 맞춤형 홈케어 마사지 프로그램. 뭉친 근육을 부드럽게 풀어드립니다. 상담: 0507-1280-3342",
    "{DONG} 일대 빠른 도착 출장 힐링 테라피 마사지. 호텔/자택 1:1 맞춤 방문 힐링 서비스. 예약: 0507-1280-3342",
    "{DISTRICT} {DONG} 출장 전문 힐링 마사지 서비스. 투명한 정찰제 코스 요금과 신속한 예약 안내: 0507-1280-3342",
    "{DISTRICT} {DONG} 일대 출장 방문 릴렉스 마사지 제휴점. 개운한 건식부터 촉촉한 아로마까지. 문의: 0507-1280-3342",
    "{DISTRICT} {DONG} 중심 출장 프라이빗 힐링 마사지 S슬림홈케어. 지친 일상 속 특별한 재충전. 상담: 0507-1280-3342",
    "{DISTRICT} {DONG} 전지역 출장 맞춤 홈바디 마사지 프로그램. 쾌적한 1:1 전담 케어 시스템. 예약: 0507-1280-3342",
    "{DISTRICT} {DONG} 신속 방문 출장 스트레스 해소 마사지. 꼼꼼한 관리와 정성스러운 서비스. 문의: 0507-1280-3342"
]

# 1. 템플릿 및 지역 데이터 읽기
with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

with open('regions.json', 'r', encoding='utf-8') as f:
    regions = json.load(f)

DIST_DIR = 'dist'
os.makedirs(DIST_DIR, exist_ok=True)

# 2. 메인 index.html 배포 (출장 키워드 제외된 청정 메인)
if os.path.exists('main_index.html'):
    shutil.copy('main_index.html', os.path.join(DIST_DIR, 'index.html'))
    print("[1/3] 메인 index.html 생성 완료")

sitemap_urls = ['https://poolim.netlify.app/']

# 3. 구·동 상세 페이지 일괄 생성 (15개 타이틀/디스크립션 무작위 배정)
for item in regions:
    city = item['city']
    city_slug = item['city_slug']
    district = item['district']
    district_slug = item['district_slug']
    dong = item['dong']
    dong_slug = item['dong_slug']
    
    full_name = f"{city} {district} {dong}"
    url_path = f"{city_slug}/{district_slug}/{dong_slug}"
    
    # 15개 패턴 중 무작위 선택 및 텍스트 치환
    selected_title = random.choice(TITLE_PATTERNS).format(FULL_NAME=full_name, CITY=city, DISTRICT=district, DONG=dong)
    selected_desc = random.choice(DESC_PATTERNS).format(FULL_NAME=full_name, CITY=city, DISTRICT=district, DONG=dong)
    
    page_html = template
    page_html = page_html.replace('{{PAGE_TITLE}}', selected_title)
    page_html = page_html.replace('{{PAGE_DESC}}', selected_desc)
    page_html = page_html.replace('{{FULL_NAME}}', full_name)
    page_html = page_html.replace('{{CITY}}', city)
    page_html = page_html.replace('{{CITY_SLUG}}', city_slug)
    page_html = page_html.replace('{{DISTRICT}}', district)
    page_html = page_html.replace('{{DISTRICT_SLUG}}', district_slug)
    page_html = page_html.replace('{{DONG}}', dong)
    page_html = page_html.replace('{{DONG_SLUG}}', dong_slug)
    page_html = page_html.replace('{{URL_PATH}}', url_path)
    
    # 로컬/웹 링크 호환
    page_html = page_html.replace('href="/"', 'href="../../../index.html"')
    page_html = page_html.replace('href="https://poolim.netlify.app/"', 'href="../../../index.html"')
    
    target_dir = os.path.join(DIST_DIR, city_slug, district_slug, dong_slug)
    os.makedirs(target_dir, exist_ok=True)
    
    target_file = os.path.join(target_dir, 'index.html')
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(page_html)
        
    sitemap_urls.append(f"https://poolim.netlify.app/{url_path}/")

print(f"[2/3] 총 {len(regions)}개 구·동 페이지 빌드 완료 (15종 랜덤 패턴 적용)")

# 4. sitemap.xml & robots.txt 작성
sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sitemap_urls:
    sitemap_content.append(f'  <url><loc>{u}</loc><priority>0.8</priority></url>')
sitemap_content.append('</urlset>')

with open(os.path.join(DIST_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(sitemap_content))

with open(os.path.join(DIST_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write("User-agent: *\nAllow: /\nSitemap: https://poolim.netlify.app/sitemap.xml\n")

print("[3/3] sitemap.xml 및 robots.txt 생성 완료")