from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import json

NAME = 'foodindustry'

DB_CONNECT_PATH = 'mysql+pymysql://root:password@localhost:3307/gokaap?charset=utf8'

engine = create_engine(DB_CONNECT_PATH)
conn = engine.connect()

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

chart_bp = Blueprint(NAME, __name__, url_prefix='/foodindustry')







@chart_bp.route('/place', methods=['GET', 'POST'])
def place_html():
    return render_template(f'{NAME}/place.html')

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