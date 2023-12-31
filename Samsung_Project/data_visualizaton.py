import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from wordcloud import WordCloud, STOPWORDS
import os
from dotenv import load_dotenv

load_dotenv()
font_path = os.environ.get('FONT_PATH')

#파일 불려오기
saveMerge = './data/samsung_merge.csv'
saveReactivity = './data/reactivity.csv'
saveCategory = './data/category.csv'

mergeData = pd.read_csv(saveMerge)
reactivity = pd.read_csv(saveReactivity)
category = pd.read_csv(saveCategory)

#폰트 설정
font = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font)
plt.rcParams['font.size'] = 10

# 기사 버즈량 및 주가 비교 시각화
plt.figure(figsize=(8, 8))
plt.title("기사 버즈량 및 주가 비교", fontsize=20)
plt.xticks(rotation=75)

dates = list(map(lambda n: pd.to_datetime(n).strftime('%Y-%m-%d'), mergeData['날짜']))

#날짜
plt.plot(dates, mergeData['본문백분위'].values, label='버즈량', color ='dodgerblue')
plt.plot(dates, mergeData['삼성전자 주가백분위'].values, label='주가',color='darkorange')

#범례를 그래프의 오른쪽 상단
plt.legend(loc=1)
#plt.show()

#일자별 기사 관심도
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.xticks(rotation=75)

plt.plot(reactivity['날짜'], reactivity['반응갯수'].values, label='반응수', marker = 'o', linestyle = 'solid', color='limegreen')
plt.legend(loc=0)
plt.tight_layout() 

#카테고리별 기사량
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.bar(category['분야'], category['count'], color='lightskyblue')
plt.tight_layout() 

#결과 출력
#plt.show()
noun_data = pd.read_csv('./data/okt.csv', encoding='utf-8')

noun_data['명사'] = noun_data

#text_data = ' '.join(noun_data['명사'].dropna())

text_data = ' '.join(noun_data['명사'].astype(str).dropna())

# wordcloud = WordCloud(max_font_size=200,
#                       font_path=font_path,
#                       #stopwords=STOPWORDS,
#                       background_color='#FFFFFF',
#                       width=1200,
#                       height=800,
#                       max_words=70).generate(text_data)

# plt.figure(figsize=(20,20))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.tight_layout(pad=0)
# plt.axis('off')
plt.show()

#버즈량이 많은 날짜만 워드클라우드 만들기
content_data = pd.read_csv('./data/wordcloud.csv', encoding='utf-8')
print(content_data.index)

wordcloud = WordCloud(max_font_size=200,
                      font_path=font_path,
                      background_color='#FFFFFF',
                      width=800,
                      height=600,
                      max_words=80).generate(' '.join(content_data[content_data['날짜']=='2023-08-16']['내용'].values)) #2023년 8월 16일자 기사본문 합치기!

plt.figure(figsize=(15,15))
plt.imshow(wordcloud)
plt.tight_layout(pad=0)
plt.axis('off')
plt.show()