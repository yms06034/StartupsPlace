from flask import Blueprint, render_template, request
import urllib.request
import json
import pandas as pd
import hashlib, hmac, base64, requests, time


# 블로그 크롤링 함수
def get_blog_result(query,display=50,start=1,sort='sim'):
    client_id = "Riuyt2wGnc_hO61T8yg9"
    client_secret = "JwLjweTgNq"
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
    else:
        return "Error Code:" + rescode

    return pd.DataFrame(response_json['items'])

# 뉴스 크롤링 함수
def get_news_result(query,display=50,start=1,sort='sim'):
    client_id = "Riuyt2wGnc_hO61T8yg9"
    client_secret = "JwLjweTgNq"
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText + \
    "&display=" + str(display) + "&start=" + str(start) + "&sort=" + sort

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_json = json.loads(response_body)
    else:
        return "Error Code:" + rescode

    return pd.DataFrame(response_json['items'])

# 연관 검색어 함수
BASE_URL = 'https://api.naver.com'
CUSTOMER_ID = '2429587'
API_KEY = '0100000000183abc2e61fb01bd7e71ec6f0b39650b32f1118985da8a7910a9304ce6943ec2'
SECRET_KEY = 'AQAAAAAYOrwuYfsBvX5x7G8LOWULjQX/5ZvbHUPo1843o9dYhw=='

def generate(timestamp, method, uri, secret_key):
    message = "{}.{}.{}".format(timestamp, method, uri)
    hash = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)

    hash.hexdigest()
    return base64.b64encode(hash.digest())

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(int(time.time() * 1000))
    signature = generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

def call_RelKwdStat(_kwds_string):
    dic_return_kwd = {}
    uri = '/keywordstool'
    method = 'GET'
    prm = {'hintKeywords' : _kwds_string , 'showDetail':1}
    r = requests.get(BASE_URL + uri, params=prm, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    r_data = r.json()
    
    return r_data


NAME = 'query'

query_bp = Blueprint(NAME, __name__)

@query_bp.route('/query', methods=['GET', 'POST'])
def query_html():
    query = request.form['input']
    query = query.replace(" ", "")

    result = get_blog_result(query)
    result_news = get_news_result(query)
    
    # blog
    result = result.astype('string')

    result.replace('<b>', '', inplace=True, regex=True)
    result.replace('</b>', '', inplace=True, regex=True)

    title = result['title']
    link = result['link']
    description = result['description']
    bloggername = result['bloggername']
    postdate = result['postdate']

    # news
    result_news = result_news.astype('string')

    result_news = result_news.replace(r'<b>', '', regex=True)
    result_news = result_news.replace(r'</b>', '', regex=True)
    result_news = result_news.replace(r'&quot;', '', regex=True)
    result_news = result_news.replace(r'&apos;', '', regex=True)

    n_title = result_news['title']
    n_link = result_news['link']
    n_description = result_news['description']

    # 연관 검색어
    search_terms = call_RelKwdStat(query)
    search_df = pd.DataFrame(search_terms['keywordList'])

    drop_index = search_df.query('monthlyMobileQcCnt == "< 10"').index
    search_df.drop(drop_index, axis=0, inplace=True)

    search_df = search_df.astype({'monthlyMobileQcCnt':'int'})
    search_df = search_df.sort_values(by='monthlyMobileQcCnt', ascending=False)[:20]
    search_df.reset_index(inplace=True)

    result_kwd = search_df['relKeyword']
    result_m_mo = search_df['monthlyMobileQcCnt']
    result_m_pc = search_df['monthlyPcQcCnt']

    return render_template('query.html' 
                        , title = title
                        , link = link
                        , description = description
                        , bloggername = bloggername
                        , postdate = postdate
                        , n_title = n_title
                        , n_link = n_link
                        , n_description = n_description
                        , result_kwd = result_kwd
                        , result_m_mo = result_m_mo
                        , result_m_pc = result_m_pc)