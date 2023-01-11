from flask import Blueprint, render_template, request
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import random

DB_CONNECT_PATH = 'mysql+pymysql://root:password@localhost:3307/gokaap?charset=utf8'

engine = create_engine(DB_CONNECT_PATH)
conn = engine.connect()

def db_init():
    SQL = """ SELECT *
            FROM food_industry;"""

    SQL_d =   """ SELECT *
            FROM food_industry fi
            WHERE fi.cotegory REGEXP ('커피|디저트|제과제빵');
            """
    SQL_f =   """ SELECT *
            FROM food_industry fi
            WHERE fi.cotegory REGEXP ('한식|주점|별식|중식|일식|양식');
            """
    SQL_c =   """ SELECT *
            FROM food_industry fi
            WHERE fi.cotegory REGEXP ('치킨|피자');
            """
    SQL_a =   """ SELECT *
            FROM food_industry fi
            WHERE fi.cotegory REGEXP ('분식|패스트푸드');
            """
    df = pd.read_sql(SQL, engine)
    df_d = pd.read_sql(SQL_d, engine)
    df_f = pd.read_sql(SQL_f, engine)
    df_c = pd.read_sql(SQL_c, engine)
    df_a = pd.read_sql(SQL_a, engine)

    return df, df_f, df_c, df_a, df_d




NAME = 'info'
info_bp = Blueprint(NAME, __name__)

@info_bp.route('/info', methods=['GET', 'POST'])
def info():
    df, df_f, df_c, df_a, df_d = db_init()

    storename = df['storename']
    storeimg = df['storeimg']
    cotegory = df['cotegory']
    storecount = df['storecount']
    name = []
    img = []
    cote = []
    count = []
    num = []
    for _ in range(len(storename)):
       num.append(random.randrange(0, 400))

    for i in num:
        name.append(storename[i])
        img.append(storeimg[i])
        cote.append(cotegory[i])
        count.append(storecount[i])

    return render_template('info.html'
                        , name = name
                        , img = img
                        , cote = cote
                        , count = count)