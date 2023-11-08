# -*- coding: utf-8 -*-
"""라쏘1030.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rojelIDrCeEgaKbdLKFHJbInYpv0SHN5
"""



import pandas as pd

file_path = '/content/drive/My Drive/Colab Notebooks/tesla2101.csv'
df = pd.read_csv(file_path)
# 'media'와 'url' 열 삭제
df = df.drop(['media', 'url'], axis=1)
df
# 또는
# df = df.drop(columns=['media', 'url'])

import re, unicodedata
from string import whitespace
pattern_whitespace = re.compile(f'[{whitespace}]+')

# NaN 값을 빈 문자열로 대체
df['content'] = df['content'].fillna('').astype(str)
# df['subtitle'] = df['subtitle'].fillna('').astype(str)

# 공백 처리 및 정규화
pattern_whitespace = re.compile(f'[{whitespace}]+')

df['content'] = df['content'].str.replace(
    pattern_whitespace, ' ', regex = True
).map(lambda x: unicodedata.normalize('NFC', x)).str.strip()

# 바이라인 제거
'''
...했다. 지역=ㅇㅇㅇ 기자, 이메일 주소, ⓒ©, www.example.com
'''
def clean_byline(text):
    # byline
    pattern_email = re.compile(r'[-_0-9a-z]+@[-_0-9a-z]+(?:\.[0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_url = re.compile(r'(?:https?:\/\/)?[-_0-9a-z]+(?:\.[-_0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_others = re.compile(r'\.([^\.]*(?:기자|특파원|교수|작가|대표|논설|고문|주필|부문장|팀장|장관|원장|연구원|이사장|위원|실장|차장|부장|에세이|화백|사설|소장|단장|과장|기획자|큐레이터|저작권|평론가|©|©|ⓒ|\@|\/|=|:앞쪽_화살표:|무단|전재|재배포|금지|\[|\]|\(\))[^\.]*)$')
    result = pattern_email.sub('', text)
    result = pattern_url.sub('', result)
    result = pattern_others.sub('.', result)
    # 본문 시작 전 꺽쇠로 쌓인 바이라인 제거
    pattern_bracket = re.compile(r'^((?:\[.+\])|(?:【.+】)|(?:<.+>)|(?:◆.+◆)\s)')
    result = pattern_bracket.sub('', result).strip()
    return result
df['content'] = df['content'].map(clean_byline)

df

# 날짜 열을 Datetime 형식으로 변환
df['date'] = pd.to_datetime(df['date'])

# 주말을 각각 금요일과 월요일로 합치기
daily_news_count = df.groupby(pd.Grouper(key='date', freq='B'))['content'].count()

# 결과 출력
daily_news_count_df = daily_news_count.reset_index()
daily_news_count_df.columns = ['Date', 'News Count']

# 결과 출력
total_news = daily_news_count_df['News Count'].sum()
print(total_news)

total_news = total_news.astype(str)

pip install konlpy

from sklearn.feature_extraction.text import TfidfVectorizer

# 'News Count' 열을 문자열로 변환
daily_news_count_df['News Count'] = daily_news_count_df['News Count'].astype(str)

# TfidfVectorizer를 사용하여 'News Count' 열을 Tfidf로 변환
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(daily_news_count_df['News Count'])

# 결과 확인
print(X)

# '날짜' 열을 Datetime 형식으로 변환
df_volume['날짜'] = pd.to_datetime(df_volume['날짜'])

# 1월 데이터만 필터링
january_data = df_volume[(df_volume['날짜'].dt.month == 1)]

# 거래량을 모두 더함
total_volume = january_data['거래량'].sum()

# 결과 출력
print("1월 전체 거래량:", total_volume)

import pandas as pd
# 엑셀 파일 경로
excel_file_path = r'/content/drive/MyDrive/Colab Notebooks/data/2101거래량.xlsx'

# 엑셀 파일을 데이터프레임으로 읽기
df_volume = pd.read_excel(excel_file_path)
# df_volume['거래량'] = pd.to_numeric(df_volume['거래량'], errors='coerce')

# 거래량 열에서 'M'을 제거하고 숫자로 변환
df_volume['거래량'] = pd.to_numeric(df_volume['거래량'].str.replace('M', ''))

# 거래량 열의 값을 모두 더함
total_volume = df_volume['거래량'].sum()



print(total_volume)

import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer

# 'News Count' 열을 문자열로 변환

# TfidfVectorizer를 사용하여 'News Count' 열을 Tfidf로 변환
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(total_news)

# 데이터프레임에서 독립변수(X)와 종속변수(y) 선택
# 'content' 열의 텍스트 데이터를 독립변수로 사용하고,
# 어떤 종속변수를 예측하려는지에 따라 해당 열을 선택해야 합니다.
y = total_volume  # target_column을 실제 종속변수 열로 바꿔야 합니다.

# 데이터를 훈련 세트와 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 라쏘 회귀 모델 생성
lasso_model = Lasso(alpha=1.0)  # alpha는 규제 강도를 조절하는 매개변수입니다.

# 모델을 훈련 데이터에 적합
lasso_model.fit(X_train, y_train)

# 테스트 세트로 예측
y_pred = lasso_model.predict(X_test)

# 모델의 성능 평가
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")

import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer

# 데이터프레임에서 독립변수(X)와 종속변수(y) 선택
# 여기서는 'content' 열의 텍스트 데이터를 독립변수로 사용하고,
# 어떤 종속변수를 예측하려는지에 따라 해당 열을 선택해야 합니다.
X = daily_news_count_df['News Count']
y = df_volume['거래량']  # target_column을 실제 종속변수 열로 바꿔야 합니다.

# 텍스트 데이터를 숫자 데이터로 변환 (텍스트 피처 벡터화, TF-IDF 사용)
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(X)

# 데이터를 훈련 세트와 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 라쏘 회귀 모델 생성
lasso_model = Lasso(alpha=1.0)  # alpha는 규제 강도를 조절하는 매개변수입니다.

# 모델을 훈련 데이터에 적합
lasso_model.fit(X_train, y_train)

# 테스트 세트로 예측
y_pred = lasso_model.predict(X_test)

# 모델의 성능 평가
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")

from konlpy.tag import Okt
from gensim import corpora
from gensim.models import LdaModel, TfidfModel


# 형태소 분석기 초기화
okt = Okt()

# 텍스트 데이터를 리스트로 변환
documents = df['content'].tolist()

# 불용어 리스트 정의
stop_words = ['월', '위', '일', '억', '년', '원', '지난해', '를', '것', '등','차','올해','챗'
              '위', '가', '조', '의', '및','약','수','주','기자','만','이','중','말','마하','미','거','게','고','분','때문','때','더','점','씨',
              '전','개','디','은','론','닉','키','김','책','그',
              '팀','스케','용','닉스', '이번', '그룹', '현지', '로이터', '전국', '하나', '루', '중이', '경찰', '자기', '확인', '운동', '남성',
              '확', '집', '전달', '토크', '륜', '의학', '거주', '곳', '소', '기', '재', '하이', '초', '공간', '배포', '총',
              '무단', '이마트', '대구', '저작권', '강동', '수다', '뉴스', '줌', '텍사스', '헬', '대신', '이름', '텍', '텍사스주',
              '플로리다', '캘리포니아주', '약관', '본사', '건', '장기', '감염증', '캐릭터', '달이', '김혜민', '청원', '창',
              '마스터', '산', '강원도', '부분', '주인', '알렉스', '제', '좀', '네', '보', '로직', '루다', '중산', '생수', '엠씨',
              '선', '타이', '커피', '에브리싱', '명의', '베이커', '크루', '스프링', '완', '타고', '세션', '순', '발', '스틱'
              '개사', '만점', '대성', '데일리안', '킥', '수단', '부문', '플라잉', '별', '날', '장', '대한', '기업', '뉴욕', '가장',
              '로', '달', '대표', '업체', '사업', '미래','계획', '세계', '회사', '업계',
              '기존', '통해', '관련', '현재', '지난', '시장', '카','그룹', '차량', '협업', '행차', '기록', '백화점', '대비',
              '대로', '전체', '고객', '공개', '서울', '이상', '아이오', '적용', '예정', '시간', '예상', '사', '로',
              '예스', '교수', '게임', '아이', '선', '대비', '며', '업종', '뉴시스', '서명', '바이', '산', '파이낸셜 뉴스',
              '이후', '보도', '제','총', '가장', '제프', '억만장자', '최고', '부자','창업', '조스', '최대', '지급',
              '국고', '차등', '위해', '미만', '이상', '경우', '개편', '일부', '지금', '생각', '우리', '요', '또', '앵커',
              '상황', '얘기', '정도', '안', '사실', '사람', '하나', '좀', '경우', '재개', '부분', '가지', '계속', '오늘',
              '볼', '걸', '수도', '저','왜', '회장', '박', '대해', '며', '영상', '자신', '에스', '명', '이메일', '사업자',
              '최근', '응답', '리움', '정부', '대표', '대통령', '국민', '면', '부산', '정치', '후보', '오늘', '안',
              '문', '장관', '회의', '사회', '주택', '제', '힘', '민주당', '오', '최근', '요', '와이드', '지리', '목표']

# 각 문서를 형태소 분석 및 토큰화하고 불용어 제거
tokenized_documents = []

for document in documents:
    # 형태소 분석 수행 후 명사만 선택 (원하는 형태소 선택 가능)
    tokens = [word for word, pos in okt.pos(document) if pos in ['Noun'] and word not in stop_words]
    tokenized_documents.append(tokens)

# 사전 (Dictionary) 생성
dictionary = corpora.Dictionary(tokenized_documents)

# Tfidf 모델 생성
tfidf = TfidfModel(dictionary=dictionary)
corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_documents]

# LDA 모델 생성
lda_model = LdaModel(corpus, num_topics=30, id2word=dictionary, passes=15)

# LDA 모델 출력
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic #{idx}: {topic}")

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

# 시각화 준비
vis = gensimvis.prepare(lda_model, corpus, dictionary)

# 시각화를 HTML 파일로 저장
pyLDAvis.save_html(vis, 'lda_visualization.html')

# from konlpy.tag import Okt
# from gensim import corpora
# from gensim.models import LdaModel, TfidfModel
# import pyLDAvis
# import pyLDAvis.gensim

# # 형태소 분석기 초기화
# okt = Okt()

# # 텍스트 데이터를 리스트로 변환
# documents = df['content'].tolist()

# # 불용어 리스트 정의
# stop_words = ['월', '위', '일', '억', '년', '원', '지난해', '를', '것', '등','차','올해','챗'
#               '위', '가', '조', '의', '및','약','수','주','기자','만','이','중','말','마하','미','거','게','고','분','때문','때','더','점','씨','전','개','디','은','론','닉','키','김','책','그',
#               '팀','스케','용','닉스']

# # 각 문서를 형태소 분석 및 토큰화하고 불용어 제거
# tokenized_documents = []

# for document in documents:
#     # 형태소 분석 수행 후 명사만 선택 (원하는 형태소 선택 가능)
#     tokens = [word for word, pos in okt.pos(document) if pos in ['Noun'] and word not in stop_words]
#     tokenized_documents.append(tokens)

# # 사전 (Dictionary) 생성
# dictionary = corpora.Dictionary(tokenized_documents)

# # Tfidf 모델 생성
# tfidf = TfidfModel(dictionary=dictionary)
# corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_documents]

# # LDA 모델 생성
# lda_model = LdaModel(corpus, num_topics=30, id2word=dictionary, passes=15)

# # LDA 모델 출력
# for idx, topic in lda_model.print_topics(-1):
#     print(f"Topic #{idx}: {topic}")

# # pyLDAvis 시각화
# pyLDAvis.enable_notebook()
# vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
# pyLDAvis.display(vis)

# pyLDAvis 시각화
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis)

pip install pyLDAvis==3.4.1

!pip install --upgrade gensim
!pip install --upgrade pyLDAvis joblib

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
pyLDAvis.enable_notebook()
vis = gensimvis.prepare(lda_model, corpus, dictionary, mds='tsne')
pyLDAvis.display(vis)