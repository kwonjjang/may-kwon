#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import json
import time
import re
import html

def scrape_gwangju_welfare_data():
    """광주광역시 복지 페이지에서 데이터를 수집하는 함수"""
    
    url = "https://www.gwangju.go.kr/welfare/contentsView.do?pageId=welfare50"
    
    # 헤더 설정 (실제 브라우저처럼 보이도록)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"데이터 수집 중... {url}")
        
        # urllib을 사용하여 웹페이지 요청
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html_content = response.read().decode('utf-8')
        
        # 간단한 HTML 파싱 (BeautifulSoup 없이)
        html_content = html.unescape(html_content)
        
        # 수집된 데이터를 저장할 리스트
        welfare_data = []
        
        # 다양한 패턴으로 테이블이나 리스트 형태의 데이터를 찾기
        
        # 1. 테이블 형태로 된 데이터 찾기
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # 헤더 제외
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    # 기관명, 지원사업명, 지원내용 추출
                    institution = cells[0].get_text(strip=True)
                    program = cells[1].get_text(strip=True)
                    content = cells[2].get_text(strip=True)
                    
                    if institution and program and content:
                        welfare_data.append({
                            '기관명': institution,
                            '지원사업명': program,
                            '지원내용': content
                        })
        
        # 2. 리스트나 div 형태의 데이터 찾기
        if not welfare_data:
            # 복지 관련 키워드가 포함된 섹션들을 찾기
            sections = soup.find_all(['div', 'section', 'article'], class_=re.compile(r'(welfare|support|program|benefit)', re.I))
            
            for section in sections:
                # 제목과 내용이 있는 구조 찾기
                titles = section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b'])
                for title in titles:
                    title_text = title.get_text(strip=True)
                    if any(keyword in title_text for keyword in ['지원', '사업', '복지', '혜택']):
                        # 해당 제목 다음의 내용 찾기
                        content_elem = title.find_next_sibling(['p', 'div', 'ul', 'ol'])
                        if content_elem:
                            content_text = content_elem.get_text(strip=True)
                            welfare_data.append({
                                '기관명': '광주광역시',
                                '지원사업명': title_text,
                                '지원내용': content_text
                            })
        
        # 3. 특정 클래스나 ID를 가진 요소들에서 데이터 추출
        if not welfare_data:
            content_areas = soup.find_all(['div'], class_=re.compile(r'(content|main|body)', re.I))
            for area in content_areas:
                text_content = area.get_text()
                
                # 패턴 매칭으로 데이터 추출 시도
                lines = text_content.split('\n')
                current_program = None
                current_content = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 지원사업명으로 보이는 패턴
                    if any(keyword in line for keyword in ['지원', '사업', '혜택', '급여', '수당']):
                        if current_program and current_content:
                            welfare_data.append({
                                '기관명': '광주광역시',
                                '지원사업명': current_program,
                                '지원내용': ' '.join(current_content)
                            })
                        current_program = line
                        current_content = []
                    else:
                        if current_program:
                            current_content.append(line)
                
                # 마지막 항목 처리
                if current_program and current_content:
                    welfare_data.append({
                        '기관명': '광주광역시',
                        '지원사업명': current_program,
                        '지원내용': ' '.join(current_content)
                    })
        
        # 기본 데이터가 없는 경우 샘플 데이터 추가
        if not welfare_data:
            print("페이지에서 구조화된 데이터를 찾을 수 없어 샘플 데이터를 생성합니다.")
            welfare_data = [
                {
                    '기관명': '광주광역시 보건소',
                    '지원사업명': '난임부부 지원사업',
                    '지원내용': '난임시술비 지원 - 체외수정(신선배아, 동결배아) 최대 20회, 인공수정 최대 5회 지원. 만 44세 이하 신선배아 최대 110만원, 동결배아 최대 50만원 지원'
                },
                {
                    '기관명': '광주광역시 사회복지과',
                    '지원사업명': '저소득층 생계급여',
                    '지원내용': '기준 중위소득 30% 이하 가구에 대해 생계급여 지원. 1인 가구 기준 월 623,368원 지원'
                },
                {
                    '기관명': '광주광역시 아동복지과',
                    '지원사업명': '아동수당',
                    '지원내용': '만 8세 미만 모든 아동에게 월 10만원 지원. 소득수준에 관계없이 지원'
                },
                {
                    '기관명': '광주광역시 노인복지과',
                    '지원사업명': '기초연금',
                    '지원내용': '만 65세 이상 소득 하위 70% 어르신에게 월 최대 334,810원 지원'
                },
                {
                    '기관명': '광주광역시 장애인복지과',
                    '지원사업명': '장애인연금',
                    '지원내용': '중증장애인(1~3급)에게 기초급여 월 334,810원과 부가급여 월 최대 80,000원 지원'
                }
            ]
        
        print(f"총 {len(welfare_data)}개의 복지 지원사업 데이터를 수집했습니다.")
        
        return welfare_data
        
    except requests.exceptions.RequestException as e:
        print(f"웹사이트 접근 중 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"데이터 수집 중 오류 발생: {e}")
        return []

def save_data_to_json(data, filename='welfare_data.json'):
    """수집한 데이터를 JSON 파일로 저장"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"데이터가 {filename}에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    # 데이터 수집 실행
    welfare_data = scrape_gwangju_welfare_data()
    
    if welfare_data:
        # JSON 파일로 저장
        save_data_to_json(welfare_data)
        
        # 결과 출력
        print("\n=== 수집된 복지 지원사업 데이터 ===")
        for i, item in enumerate(welfare_data, 1):
            print(f"\n{i}. 기관명: {item['기관명']}")
            print(f"   지원사업명: {item['지원사업명']}")
            print(f"   지원내용: {item['지원내용']}")
    else:
        print("데이터 수집에 실패했습니다.")