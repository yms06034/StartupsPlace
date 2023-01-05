import requests
import pandas as pd
from pandas import json_normalize
import json
import urllib.request
from sqlalchemy import create_engine 

start = []
for n in range(0, 485000, 1000):
    start.append(n + 1)

end = []
for i in range(1000, 486000, 1000):
    end.append(i)

url = f'http://openapi.seoul.go.kr:8088/704f6a4477736a6b3936594c697761/json/LOCALDATA_072404/{start[0]}/{end[0]}/'

text = urllib.request.urlopen(url).read().decode('utf-8')
json_return = json.loads(text)
df = json_normalize(json_return['LOCALDATA_072404']['row'])
df = df[['MGTNO', 'RDNWHLADDR', 'RDNPOSTNO', 'BPLCNM', 'UPTAENM', 'X', 'Y', 'SNTUPTAENM']]



for i in range(1, 485):
    url_1 = f'http://openapi.seoul.go.kr:8088/704f6a4477736a6b3936594c697761/json/LOCALDATA_072404/{start[i]}/{end[i]}/'

    text_1 = urllib.request.urlopen(url_1).read().decode('utf-8')
    json_return = json.loads(text_1)
    df_1 = json_normalize(json_return['LOCALDATA_072404']['row'])
    df_1 = df_1[['MGTNO','RDNWHLADDR', 'RDNPOSTNO', 'BPLCNM', 'UPTAENM', 'X', 'Y', 'SNTUPTAENM']]
    df = df.append(df_1)
    
df.reset_index(inplace=True)
print("중복치 : ", df.duplicated().sum().sum())

df = df.drop('index', axis=1)

# DATA PREPROCESS

df.duplicated('MGTNO').sum()
df.isnull().sum()

df_drop = df.query('(X  == "") & (Y == "")')
df_drop.index

df = df.drop(df_drop.index, axis=0)

df['UPTAENM'].replace('?ㅑ?대포집/소주방', '정종/대포집/소주방', inplace=True)

df_drop_2 = df.query('UPTAENM == ""').index
df_1 = df.drop(df_drop_2, axis=0)

DB_CONNECT_PATH = 'mysql+pymysql://root:password@localhost:3307/gokaap?charset=utf8'

engine = create_engine(DB_CONNECT_PATH)
conn = engine.connect()

df.to_sql(name='seoul_restaurant_info', con=engine, if_exists='replace')