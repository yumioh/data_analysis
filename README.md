# 크롤링, 시각화 미니 프로젝트

## 1. 네이버 뉴스 크롤링
    - 2023년 8월 한달동안 연합뉴스 크롤링 
    - 크롤링 항목 : 날짜, 타이틀, 기사본문, 기사반응*, 카테고리
    - 기사내용 전차리
    - news.csv파일로 저장

     
####  기사반응은 비동기 방식으로 (단, 카테고리가 여러개로 분류 될 경우 가장 앞에 있는 카테고리로)
<br/>
<img src="https://github.com/yumioh/data_analysis/assets/38059057/8547f4ff-fd7f-478c-8ad4-dc66fc0c8475" width="50%" height="20%" />


## 2. 기사 데이터 정리 및 통계
    - 전체기사 일자별 카운트
    - 본문이 비어있는 기사를 제외하고 삼성전자글자가 들어간 뉴스들만 분류
    - 일자별로 분류한 카운트와 삼성 주가 데이터 합치기 (주가가 없는 날짜 제외)
    - 데이터 수치를 백분위로 변경 (날짜별합/전체합 * 100)

   
## 3. 관심도, 카테고리 데이터 통계
    - 삼성전자 날짜별 관심도 정리 (하지만, 2023년 8월은 관심도가 없어 반응이 전부 0으로 나옴)
    - 삼성전자 기사 카테고리별 합계


## 4. 정리한 데이터를 기반으로 그래프 작성(시각화)
    - 기사버즈량 및 주가 비교
    - 일자별 기사 관심도 
    - 카테고리별 기사량

## 5. 기사 버즈량이 가장 많은 날 워드 클라우드 만들기

## 6. 기사 버즈량이 가장 많은 날 댓글 수집 후 워드 클라우드 만들기


