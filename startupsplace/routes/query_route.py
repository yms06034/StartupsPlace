from flask import Blueprint, render_template, request
import urllib.request
import json
import pandas as pd
import hashlib, hmac, base64, requests, time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


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

def get_count_days(query):
    now = datetime.now()
    fost = now - relativedelta(months=1)
    past = fost.strftime("%Y-%m-%d")
    now = now.strftime("%Y-%m-%d")
    
    client_id = "Riuyt2wGnc_hO61T8yg9"
    client_secret = "JwLjweTgNq"
    url = "https://openapi.naver.com/v1/datalab/search"
    body = "{\"startDate\":\""+past+"\",\"endDate\":\""+now+"\",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\""+query+"\",\"keywords\":[\""+query+"\"]}]}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data = json.loads(response_body.decode("utf-8"))
    else:
        return "Error Code:" + rescode
    
    d2 = data['results']
    for i in range(len(d2)):
        asc = d2[i]
        ds = asc['data']
    
    df = pd.DataFrame(ds)
    period = []
    ratio = []
    for i in range(0, len(df['period'])):
        period.append(df['period'][i])
        ratio.append(df['ratio'][i])

    preiod_fin = []
    for i in range(len(period)):
        pre = period[i]
        preiod_fin.append(pre[5:].replace('-','.'))
    preiod_fin
        
    return preiod_fin, ratio


def youtube_search(query):
    DEVELOPER_KEY='AIzaSyC086IVU7HuTYWRHile90XlZeMRrEsCkhs'
    YOUTUBE_API_SERVICE_NAME='youtube'
    YOUTUBE_API_VERSION='v3'

    youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    
    search_response=youtube.search().list(
        q=query,
        order='relevance',
        part='snippet',
        maxResults=10,
        ).execute()

    videoid = [] # 영상 ID
    publisne = [] # 영상 업로드 일자
    thumbnails = [] # 썸네일 이미지 링크
    videotitle = [] # 영상 타이틀
    channeltitle = [] # 채널 이름

    youtube = search_response['items']

    if youtube[0]['id'] == 'channelId':
        for c in range(1, 6):
            videoid.append(youtube[c]['id']['videoId'])           
    elif youtube[0]['id']['videoId']:
        for a in range(0, 5):
            videoid.append(youtube[a]['id']['videoId'])

    for y in range(0 ,5):
        publisn = youtube[y]['snippet']['publishedAt']
        publisne.append(publisn[:10])

        thumbnails.append(youtube[y]['snippet']['thumbnails']['medium']['url'])

        videotitle.append(youtube[y]['snippet']['title'])

        channeltitle.append(youtube[y]['snippet']['channelTitle'])
    
    return videoid, publisne, thumbnails, videotitle, channeltitle


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
    result.replace(r'&apos;', '', inplace=True, regex=True)

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

    # Word Cloud

    ls = []
    for i in range(len(result['description'])):
        ls.append(result['description'][i])

    word_ls = ','.join(ls)

    # Naver Datalab
    preiod_fin, ratio = get_count_days(query)

    # youtube data api
    videoid, publisne, thumbnails, videotitle, channeltitle = youtube_search(query)

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
                        , result_m_pc = result_m_pc
                        , word_ls = word_ls
                        , period = preiod_fin
                        , ratio = ratio
                        , kwd = query
                        , channeltitle = channeltitle
                        , videotitle = videotitle
                        , thumbnails = thumbnails
                        , publisne = publisne
                        , videoid = videoid)
