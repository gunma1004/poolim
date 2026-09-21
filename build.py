import os
import json
import shutil
import random

# 1. 기존 구·동 페이지용 패턴 (기존 유지)
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

DESC_PATTERNS = [
    "{FULL_NAME} 전지역 출장 방문 케어 마사지 전문 S슬림홈케어입니다. 건식, 아로마, VIP스웨디시 코스 시간과 요금 확인. 문의: 0507-1280-3342",
    "{FULL_NAME} 일대 신속한 출장 1:1 홈 테라피 마사지 안내. 지친 하루를 달래주는 맞춤 힐링 케어 프로그램. 예약상담: 0507-1280-3342",
    "{FULL_NAME} 자택/오피스텔 출장 맞춤 릴렉싱 마사지 S슬림홈케어. 건식 지압부터 스페셜 아로마까지 완벽 케어. 문의: 0507-1280-3342",
    "{FULL_NAME} 어디서나 편안하게 받는 출장 전지역 힐링 마사지 서비스. 투명한 정찰제 가격표와 신속 배차. 예약: 0507-1280-3342",
    "{FULL_NAME} 일대 프리미엄 출장 전문 바디 마사지 예약 안내. 전문 힐러의 정성스러운 1:1 방문 관리. 상담: 0507-1280-3342"
]

# 2. 상위 '시' 페이지 전용 패턴
CITY_TITLE_PATTERNS = [
    "{CITY} 전지역 홈케어 마사지 · 1:1 방문 힐링 센터 │ S슬림홈케어",
    "{CITY} 전지역 맞춤 마사지 코스 및 요금 안내 │ S슬림홈케어",
    "{CITY} 프리미엄 방문 마사지 서비스 총정리 │ S슬림홈케어",
    "{CITY} 전지역 24시 안심 테라피 마사지 예약 │ S슬림홈케어"
]

CITY_DESC_PATTERNS = [
    "{CITY} 전지역 어디든 신속하게 찾아가는 프리미엄 출장 마사지 S슬림홈케어입니다. 건식, 아로마, 스웨디시 전문 1:1 케어. ",
    "{CITY} 일대 자택, 오피스텔, 호텔 등 편안한 공간에서 즐기는 맞춤형 출장 힐링 마사지. 투명한 정찰제와 실시간 예약 시스템. ",
    "지친 일상의 피로를 말끔히 풀어드리는 {CITY} 전문 출장 마사지 서비스. 검증된 전문 테라피스트의 정성스런 1:1 맞춤 케어. "
]

# 3. 새로운 주소 체계에 맞춘 동별 홈스파·홈타이 패턴 리스트
EXTRA_TITLE_PATTERNS = [
    "{DONG} 홈스파 마사지·홈타이 │ {CITY} {DISTRICT} 안마 업체 S슬림홈타이",
    "{DONG} 프리미엄 홈타이 마사지 · 힐링 홈스파 예약 │ {CITY} {DISTRICT} 스파 샵 S슬림홈케어",
    "{DONG} 맞춤형 홈스파 마사지 및 아로마 홈타이 │ {DISTRICT} {CITY} 마사지 S슬림홈타이",
    "{DONG} 릴렉싱 스웨디시 마사지 서비스 │ {CITY} {DISTRICT} 마사지 센터 S슬림홈케어",
    "{DONG} 24시 안심 방문 홈스파 및 홈타이 테라피 │ {CITY} {DISTRICT} 전문 S슬림홈타이",
    "{DONG} 프라이빗 힐링 홈타이 · 맞춤 홈스파 │ {CITY}{DISTRICT} 마사지 S슬림홈케어",
    "{DONG} 스페셜 바디케어 홈스파 및 홈타이 │ {DISTRICT} {CITY} 업체 S슬림홈타이",
    "{DONG} 야간 심야 홈타이 마사지 · 힐링 홈ส파 │ {CITY} {DISTRICT} 업체 S슬림홈케어"
]

EXTRA_DESC_PATTERNS = [
    "{CITY} {DISTRICT} {DONG} 인근 신속 방문 출장 마사지 및 홈타이 마사지 서비스. 1:1 맞춤형 힐링 테라피 정찰제 요금 안내. ",
    "{CITY} 전지역 {DONG} 자택, 오피스텔, 호텔 전문 출장 마사지. 지친 일상의 피로를 풀어드리는 프리미엄 케어. ",
    "{DISTRICT} {DONG} 중심 24시간 언제나 편안하게 이용할 수 있는 출장 마사지 및 홈타이. 검증된 전문 관리사 배차. ",
    "{CITY} {DONG} 맞춤형 출장 방문 마사지 및 힐링 홈스파 전문 S슬림홈타이/홈케어. 뭉친 근육을 개운하게 케어해드립니다. "
]

with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

with open('regions.json', 'r', encoding='utf-8') as f:
    regions = json.load(f)

DIST_DIR = 'dist'
os.makedirs(DIST_DIR, exist_ok=True)

# 1. 메인 index.html 배포
if os.path.exists('main_index.html'):
    shutil.copy('main_index.html', os.path.join(DIST_DIR, 'index.html'))
    print("[1/5] 메인 index.html 복사 완료")

sitemap_urls = ['https://poolim.netlify.app/']

def clean_city_name(city_str):
    for suffix in ["광역시", "특별자치시", "시"]:
        if city_str.endswith(suffix):
            return city_str[:-len(suffix)]
    return city_str

# 2. 상위 광역 시/도 페이지 생성
city_map = {}
for r in regions:
    if r['city_slug'] not in city_map:
        city_map[r['city_slug']] = clean_city_name(r['city'])

for c_slug, c_name in city_map.items():
    full_name = f"{c_name} 전지역"
    selected_title = random.choice(CITY_TITLE_PATTERNS).format(CITY=c_name)
    selected_desc = random.choice(CITY_DESC_PATTERNS).format(CITY=c_name)
    
    c_html = template
    c_html = c_html.replace('{{PAGE_TITLE}}', selected_title)
    c_html = c_html.replace('{{PAGE_DESC}}', selected_desc)
    c_html = c_html.replace('{{FULL_NAME}}', full_name)
    c_html = c_html.replace('{{CITY}}', c_name)
    c_html = c_html.replace('{{CITY_SLUG}}', c_slug)
    c_html = c_html.replace('{{DISTRICT}}', '전지역')
    c_html = c_html.replace('{{DONG}}', f"{c_name} 전체")
    c_html = c_html.replace('{{URL_PATH}}', c_slug)
    c_html = c_html.replace('{{HOME_LINK}}', '../index.html')
    c_html = c_html.replace('{{CITY_LINK}}', './index.html')
    
    city_dir = os.path.join(DIST_DIR, c_slug)
    os.makedirs(city_dir, exist_ok=True)
    with open(os.path.join(city_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(c_html)
    sitemap_urls.append(f"https://poolim.netlify.app/{c_slug}/")

print(f"[2/5] 총 {len(city_map)}개 상위 광역 페이지 빌드 완료")

# 3. 구·동 세부 페이지 생성 (기존 페이지 그대로 유지)
for item in regions:
    city = item['city']
    city_slug = item['city_slug']
    district = item['district']
    district_slug = item['district_slug']
    dong = item['dong']
    dong_slug = item['dong_slug']
    
    full_name = f"{city} {district} {dong}"
    url_path = f"{city_slug}/{district_slug}/{dong_slug}"
    
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
    page_html = page_html.replace('{{HOME_LINK}}', '../../../index.html')
    page_html = page_html.replace('{{CITY_LINK}}', f'../../../{city_slug}/index.html')
    
    target_dir = os.path.join(DIST_DIR, city_slug, district_slug, dong_slug)
    os.makedirs(target_dir, exist_ok=True)
    
    with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page_html)
        
    sitemap_urls.append(f"https://poolim.netlify.app/{url_path}/")

print(f"[3/5] 총 {len(regions)}개 세부 구·동 페이지 빌드 완료")

# 4. [요청 반영] 대전·청주 지역에 대해 `/daejeon/massge/gayang/` 형태의 새로운 독립 페이지 생성
extra_dong_count = 0
target_cities = ['daejeon', 'cheongju']

for item in regions:
    if item['city_slug'] in target_cities:
        city = clean_city_name(item['city'])
        city_slug = item['city_slug']
        district = item['district']
        dong = item['dong']
        dong_slug = item['dong_slug']
        
        # 요청하신 주소 구조: {city_slug}/massge/{dong_slug}
        extra_slug = f"{city_slug}/massge/{dong_slug}"
        
        extra_title = random.choice(EXTRA_TITLE_PATTERNS).format(CITY=city, DISTRICT=district, DONG=dong)
        extra_desc = random.choice(EXTRA_DESC_PATTERNS).format(CITY=city, DISTRICT=district, DONG=dong)
        
        extra_html = template
        extra_html = extra_html.replace('{{PAGE_TITLE}}', extra_title)
        extra_html = extra_html.replace('{{PAGE_DESC}}', extra_desc)
        extra_html = extra_html.replace('{{FULL_NAME}}', f"{city} {district} {dong}")
        extra_html = extra_html.replace('{{CITY}}', city)
        extra_html = extra_html.replace('{{CITY_SLUG}}', city_slug)
        extra_html = extra_html.replace('{{DISTRICT}}', district)
        extra_html = extra_html.replace('{{DONG}}', dong)
        extra_html = extra_html.replace('{{URL_PATH}}', extra_slug)
        extra_html = extra_html.replace('{{HOME_LINK}}', '../../../index.html') # 상위 경로 조정
        extra_html = extra_html.replace('{{CITY_LINK}}', f'../../{city_slug}/index.html')
        
        # dist/daejeon/massge/gayang/ 폴더 생성
        target_dir = os.path.join(DIST_DIR, city_slug, 'massge', dong_slug)
        os.makedirs(target_dir, exist_ok=True)
        
        with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(extra_html)
            
        sitemap_urls.append(f"https://poolim.netlify.app/{extra_slug}/")
        extra_dong_count += 1

print(f"[4/5] 대전·청주 massge 경로 신규 동별 페이지 {extra_dong_count}개 생성 완료")

# 5. sitemap.xml & robots.txt 작성
sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sitemap_urls:
    sitemap_content.append(f'  <url><loc>{u}</loc><priority>0.8</priority></url>')
sitemap_content.append('</urlset>')

with open(os.path.join(DIST_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(sitemap_content))

with open(os.path.join(DIST_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write("User-agent: *\nAllow: /\nSitemap: https://poolim.netlify.app/sitemap.xml\n")

print("[5/5] sitemap.xml 및 robots.txt 작성 완료")

# 6. netlify.toml 작성
with open('netlify.toml', 'w', encoding='utf-8') as f:
    f.write('[build]\n  publish = "dist"\n\n[[redirects]]\n  from = "/*"\n  to = "/index.html"\n  status = 200\n')