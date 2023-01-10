from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import json, requests, collections
import folium


NAME = 'foodindustry'

DB_CONNECT_PATH = 'mysql+pymysql://root:password@localhost:3307/gokaap?charset=utf8'

engine = create_engine(DB_CONNECT_PATH)
conn = engine.connect()

# Chart Area
SQL = """SELECT * FROM ecnmctrnds"""

df = pd.read_sql(SQL, engine)

SQL2 = """SELECT  
 'TOTAL',
 'KOREAN_RESTAURANT',
 'KOREAN_NOODLE_RESTAURANT',
 'KOREAN_MEAT_RESTAURANT',
 'KOREAN_SEAFOOD_RESTAURANT',
 'CHINESE_RESTAURANT',
 'JAPANESE_RESTAURANT',
 'WESTERN_RESTAURANT',
 'OTHER_FOREIGN_RESTAURANT',
 'BAKERY_BUSINESS',
 'FAST_FOOD',
 'CHICKEN',
 'KOREAN_SNACK_RESTAURANT',
 'SNACK_SHOP',
 'GENERAL_ENTERTAINMENT_BAR',
 'ENTERTAINMENT_BUSINESS',
 'DRAUGHT_BEER_SHOP',
 'OTHER_PUBS',
 'COFFEE_SHOP',
 'OTHER_NON_ALCOHOLIC_BEVERAGE_STORES' FROM ecnmctrnds"""

df = pd.read_sql(SQL, engine)
df2 = pd.read_sql(SQL2, engine)

food_list = list(np.array(df['TOTAL'].tolist()))

food_index = list(np.array(df['brnch'].tolist()))

df3 = df.transpose()
df3.drop(['index', 'brnch'], axis=0, inplace=True)

mean = []
for s in range(0, 10 + 1):
    m = list(np.array(df3[s].tolist()))
    mean.append(m)

year = list(np.array(df.brnch.tolist())) # 분기
col = list(np.array(df2.columns.tolist())) # 컬럼


# place map (kakao API & REST API(Search))
# 전국 or 수도권 프랜차이즈 데이터 크롤링 함수
def Location_function_kwd(query='19티'):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={query}'

    def get_store_list(start_x,start_y,end_x,end_y): 
        app_key = 'KakaoAK 95149feb7be63a078b25c8f8121a8ed4'
        offset = 0.01
        cnt = 1
        resp_list = []

        while True:
            jump_x = 0.5 # 지도 사각형 증가 값
            jump_y = 0.5
            params = {
                'query': query,
                'page': cnt,
                'rect': f'{start_x-offset},{start_y-offset},{end_x+offset},{end_y+offset}'
            }
            headers  = {
                'Authorization': app_key
            }

            resp = requests.get(url, params=params, headers=headers)
            search_count = resp.json()['meta']['total_count'] # 총 데이터 수 확인

            # 45개 이상이면 해당 지점 4분할 해서 지점 재확인
            if search_count > 45:
                dividing_x = (start_x + end_x) / 2
                dividing_y = (start_y + end_y) / 2
                # 1
                resp_list.extend(get_store_list(start_x,start_y,dividing_x,dividing_y))
                # 2 x만 이동
                resp_list.extend(get_store_list(dividing_x,start_y,end_x,dividing_y))
                # 3 y만 이동
                resp_list.extend(get_store_list(start_x,dividing_y,dividing_x,end_y))
                # 4 x,y 전부 이동
                resp_list.extend(get_store_list(dividing_x,dividing_y,end_x,end_y))
                return resp_list
            else:
                if resp.json()['meta']['is_end']:
                    resp_list.extend(resp.json()['documents'])
                    return resp_list
                else:
                    cnt += 1 # 페이지 이동
                    resp_list.extend(resp.json()['documents'])

    # 위도, 경도 찾아오는 함수          
    def getLatLng(addr):
        app_key = 'KakaoAK 95149feb7be63a078b25c8f8121a8ed4'
        url = 'https://dapi.kakao.com/v2/local/search/address.json'
        params = {
            'query': addr,
            'page': '',
            'AddressSize': ''
        }
        headers  = {
            'Authorization': app_key
        }
        resp = requests.get(url, params=params, headers=headers)

        if resp.json()['documents'] != []:
            json = resp.json()['documents'][0]
            return (json['x'], json['y'])
        else: 
            fixed_addr = addr.replace(addr.split(' ')[-1], '').strip()
            if fixed_addr == '':
                return (0, 0)
            else:
                return getLatLng(fixed_addr)

    # 시작 x 좌표 및 증가값
    start_x = 126 # ~ 129.7, 3.4 // 전국 시작 위치 (x)
    # start_x = 126.734086 # ~ 129.7, 3.4 // 수도권 시작 위치 (x)
    jump_x = 0.5
    jump_y = 0.5

    hosik2_list = []

    # 지도를 사각형으로 나누면서 데이터 받아옴
    for i in range(1,10):
        end_x = start_x + jump_x
        start_y = 33 # ~ 38.3, 4.9 // 전국 시작 위치 (y)
    #     start_y = 37.413294 # ~ 38.3, 4.9 // 수도권 시작 위치 (y)
        for j in range(1,13):
            end_y = start_y + jump_y
            hosik2_list_one = get_store_list(start_x,start_y,end_x,end_y)
            hosik2_list.extend(hosik2_list_one)
            start_y = end_y
        start_x = end_x

    hosik2_list = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in hosik2_list)))

    place_road_name = []
    for i in hosik2_list:
        place_road_name.append({'title':i['place_name'],'address': i['road_address_name'], 'url': i['place_url']})

    return place_road_name


chart_bp = Blueprint(NAME, __name__, url_prefix='/foodindustry')

@chart_bp.route('/place', methods=['GET', 'POST'])
def place_html():
    if request.method == "POST":
        query = request.form['input']
        place_road_name = Location_function_kwd(query)
        return render_template(f'{NAME}/place.html', place_road_name = place_road_name)

    # 전국 or 수도권 프랜차이즈 데이터 크롤링 함수
    # place_road_name = Location_function_kwd()
    return render_template(f'{NAME}/place.html', place_road_name = '19티')
                            # , place_road_name = json.dumps(place_road_name)

@chart_bp.route('/chart', methods=['GET', 'POST'])
def chart():
    q1_20 = {}
    for i in range(len(col)):
        q1_20[col[i]] = mean[0][i]
    q2_20 = {}
    for i in range(len(col)):
        q2_20[col[i]] = mean[1][i]
    q3_20 = {}
    for i in range(len(col)):
        q3_20[col[i]] = mean[2][i]
    q4_20 = {}
    for i in range(len(col)):
        q4_20[col[i]] = mean[3][i]
    q1_21 = {}
    for i in range(len(col)):
        q1_21[col[i]] = mean[4][i]
    q2_21 = {}
    for i in range(len(col)):
        q2_21[col[i]] = mean[5][i]
    q3_21 = {}
    for i in range(len(col)):
        q3_21[col[i]] = mean[6][i]
    q4_21 = {}
    for i in range(len(col)):
        q4_21[col[i]] = mean[7][i]
    q1_22 = {}
    for i in range(len(col)):
        q1_22[col[i]] = mean[8][i]
    q2_22 = {}
    for i in range(len(col)):
        q2_22[col[i]] = mean[9][i]
    q3_22 = {}
    for i in range(len(col)):
        q3_22[col[i]] = mean[10][i]

    return render_template(f'{NAME}/chart.html'
        , food_list = food_list
        , food_index = food_index
        , q1_20 = json.dumps(q1_20)
        , q2_20 = json.dumps(q2_20)
        , q3_20 = json.dumps(q3_20)
        , q4_20 = json.dumps(q4_20)
        , q1_21 = json.dumps(q1_21)
        , q2_21 = json.dumps(q2_21)
        , q3_21 = json.dumps(q3_21)
        , q4_21 = json.dumps(q4_21)
        , q1_22 = json.dumps(q1_22)
        , q2_22 = json.dumps(q2_22)
        , q3_22 = json.dumps(q3_22)
        )