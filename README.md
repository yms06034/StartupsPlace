


# Startups Place
키워드 하나로 찾는 신규 창업자를 위한 창업 관련 DATA &amp; DashBorad 개발

## Description
본 프로젝트는 신규 창업자를 위해 원하는 창업 관련 키워드 하나로 찾는 정보 사이트

## Service INFO
- **메인 페이지**

![1__메인페이지_AdobeExpress (1)](https://user-images.githubusercontent.com/98085184/230842608-ffe28991-12a2-4430-9c4d-1970dde97389.gif)

> 키워드 검색 기능 및 UI 구현

- **회원가입 및 로그인 페이지**
> 회원가입 기능 및 중복 회원 처리 기능 구현 \
> 로그인 기능

- **지역별 상권 정보 페이지**
  
![ezgif com-video-to-gif (1)](https://user-images.githubusercontent.com/98085184/230846334-1d385242-e41b-459b-95d6-99f66f88fdbb.gif)

> 원하는 브랜드 명을 검색하면 전국 지점에 있는 프렌차이즈 위치를 보여주는 페이지

- **키워드 정보 페이지**

![ezgif com-video-to-gif](https://user-images.githubusercontent.com/98085184/230844648-fbe65c20-e20c-4700-8722-7b7cff364e42.gif)
> 메인 페이지 상단에 있는 검색창을 통해 원하는 **창업정보**를 검색 하면 보여지는 페이지 \
> 블로그, 뉴스, 연간 검색어, 키워드 별 검색량, NLP처리, 유튜브 영상 등 다양한 창업 관련 정보블 보여주는 페이지

- **매장 정보 페이지**

![image](https://user-images.githubusercontent.com/98085184/230845598-3bd5b07b-f1ec-43c1-bb91-5ea3e4aa7bdc.png)

> 다양한 프렌차이즈 가게 정보를 보여주는 페이지




## PIPELINE
![Startupsplace_pipeling](https://user-images.githubusercontent.com/98085184/230840969-bb3e6f8b-37d2-4d0e-9358-cf539796e16a.png)

> 네이버, 카카오, 구글의 API를 가져와 데이터 전처리 후 DB에 담아주고 Flask로 넘겨주었습니다.
## Environment

> Python Version 3.8 \
> Docker Mysql 5.3


## Prerequisite
```
$ pip install -r requirements.txt
$ export FLASK_APP=startupsplace
$ flask run
```

## Troubleshooting
- 전국 지역 별 프렌차이즈 위치 정보를 보여주고 싶어서 위치 정보 관련 API를 찾고 있었는데 확실히 무료로 공유해주는 곳이 없었다...
그래서 처음에는 User가 원하는 프렌차이즈를 검색하면 네이버에서 크롤링을 진행해 위치 정보를 보여주려고 했으나 경도, 위도 값을 가져오는 것은 Json으로 가져올 수 있었으나, 속도가 너무 느릴 뿐더러 크롤링을 계속 시도하는 거 자체를 서비스화 하기에는 좀 불안했다. (크롤링 실패 시 큰일 이니깐... 안정화 작업도 해야하니...)
- 그래서 생각한 것이 카카오 MAP API를 활용해 진행하였다.
	- 속도도 더 빨라지고 안정성도 많이 올라갔다.
- 자세한 코드는 [여기](https://github.com/yms06034/StartupsPlace/blob/master/startupsplace/routes/chart_route.py)에서 확인이 가능합니다.


## RETROSPECTIVE
- 작업 기간이 3일 동안 진행했는데 시간이 더 있었다면 \
실제 가볍게 살펴볼 수 있는 페이지로 서비스 화를 진행해도 재밌겠다는 생각을 하게 된 프로젝트 였다.
- 또한 이 프로젝트를 진행하면서 컴퓨터가 강제 포맷이 되는 바람에 기간을 맞추려고 Docker로 환경 구성을 다시 진행할 수 있는 계기가 되었고 Docker에 대해 다시 한번 필요성에 대해 정말 깊이 깨달았다.

