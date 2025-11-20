# 🎬 Netflix 콘텐츠 데이터 분석 프로젝트

![Netflix Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/1280px-Netflix_2015_logo.svg.png)

---

## 📌 1. 데이터 분석 프로젝트 설명

본 프로젝트는 Netflix의 영화 및 TV 프로그램 데이터를 기반으로  
**장르, 제작연도, 국가, 평점 등 다양한 기준으로 콘텐츠 패턴을 분석**하는 데이터 분석 프로젝트입니다.  

데이터셋(titles.csv)을 활용하여  
- 데이터 전처리  
- 시각적 분석  
- 장르 및 국가별 트렌드 파악  
등의 과정을 수행하였으며, 분석 코드는 `netflix_analysis.py`에 포함되어 있습니다.

---

## 🎯 2. 프로젝트 주제

**Netflix 콘텐츠 데이터의 다각적 분석을 통한 트렌드 및 특성 파악**

---

## 💡 3. 주제 선택 이유

1. **OTT 시장의 빠른 성장**  
   Netflix는 글로벌 시장에서 가장 많이 사용되는 스트리밍 플랫폼으로,  
   콘텐츠 소비 트렌드를 분석하기에 최적의 데이터임.

2. **데이터의 다양성**  
   장르, 국가, 연도, 평점 등 다양한 변수를 포함하여  
   여러 관점의 분석이 가능함.

3. **실전 데이터 분석 경험**  
   Pandas, Matplotlib 등 기본적인 데이터 분석 도구를 활용하여  
   전처리 → 분석 → 시각화 과정을 직접 수행할 수 있음.

---

## 📊 4. 데이터 분석 내용

### 1️⃣ 장르 & 연령등급 분석
- 장르별 콘텐츠 수 시각화
- 연령등급별 콘텐츠 분포
- 연령등급별 인기 장르 Top 3
- 연도별 장르 트렌드 분석

### 2️⃣ 시간대 & 트렌드 분석
- 연도별 제작 콘텐츠 수 변화
- 연도별 IMDb 평균 점수 변화
- 시대별 Top 장르 분석
- 사용자 정의 필터(연도 범위, 콘텐츠 유형) 적용

### 3️⃣ 제작국가 & 글로벌 분석
- 국가별 콘텐츠 제작량 분석
- 콘텐츠 제작 국가 Top 10
- 국가별 평점 통계(IMDb, TMDB)
- 국가별 TMDB 인기도 분석

### 4️⃣ 평점 & 인기도 분석
- 장르별 평균 IMDb/TMDB 점수 분석
- 장르별 TMDB 인기도 순위
- 그룹별(장르·연도·국가) 점수 비교 기능
- 사용자 선택형 커스텀 분석 제공

---

## 🎥 5. 시연 동영상 (YouTube)

> 📺 **[시연 영상 보러가기](https://youtu.be/OX5ns-QHptE?si=0_FWmKHMJXCHCPY0)**  

---

## 👥 6. 팀원 소개

| 이름 | 역할 |
|------|----------------------------|

| 한재현 | 시간대 & 트렌드 분석 |

| 박도훈 | 장르 & 연령등급 분석 |

| 진선정 | 평점 & 인기도 분석 |

| 정현지 | 제작국가 & 글로벌 분석 |

---

## 🔗 7. 외부 URL

- Netflix 공식 사이트: https://www.netflix.com  
- 데이터 출처: Kaggle  
- Python 공식문서: https://docs.python.org  
- Matplotlib: https://matplotlib.org  

---

## 💻 8. 코드 Push 안내

본 프로젝트에서 사용된 전체 분석 코드는 아래 파일에 포함되어 있습니다.

- `netflix_analysis.py` : Netflix 데이터 전처리 및 시각화 분석 코드
- `titles.csv` : Netflix 콘텐츠 데이터셋

위 두 파일은 본 GitHub Repository에 모두 Push 완료하였습니다.

코드를 수정하거나 분석을 재현하려면 다음과 같이 실행할 수 있습니다:

### ▶️ 로컬에서 프로젝트 실행 방법

1. 레포지토리 클론
```bash
git clone https://github.com/yourID/netflix_analysis.git
'''
2.라이브러리 설치
'''
pip install pandas matplotlib seaborn
'''
3.분석 코드 실행
'''
python netflix_analysis.py
'''

