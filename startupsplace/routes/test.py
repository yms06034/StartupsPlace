import urllib.request
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from konlpy.tag import Okt

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

def getresult(client_id,client_secret,query,display=10,start=1,sort='sim'):
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + \
    "&display=" + str(display) + "&start=" + str(start) + "&sort=" + sort

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_json = json.loads(response_body)
        # print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    return pd.DataFrame(response_json['items'])

client_id = "Riuyt2wGnc_hO61T8yg9"
client_secret = "JwLjweTgNq"
query = '치킨창업'
display=100
start=1
sort='sim'

result_blog= getresult(client_id,client_secret,query,display,start,sort)
result_blog = result_blog.astype('string')

result_blog = result_blog.replace(r'<b>', '', regex=True)
result_blog = result_blog.replace(r'</b>', '', regex=True)
result_blog

ls = []
for i in range(len(result_blog['description'])):
    ls.append(result_blog['description'][i])

Okt = Okt()

for i in range(len(ls)):
    clear = Okt.nouns(ls[i])
    ls[i] = ' '.join(clear)


vect = CountVectorizer()
matrix = vect.fit_transform(ls)
matrix.toarray()

ta = vect.vocabulary_

wordcloud = WordCloud(font_path = 'C://Windows//Fonts//ONE Mobile Title.ttf',
    max_font_size=200, max_words=100, background_color="white", width=800, height=800).generate_from_frequencies(ta)

fig = plt.figure(figsize=(10, 10))
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud)
plt.tight_layout(pad=0)
plt.axis('off')
plt.show()