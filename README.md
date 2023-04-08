

# Startups Place
키워드 하나로 찾는 신규 창업자를 위한 창업 관련 DATA &amp; DashBorad 개발

## Description
본 프로젝트는 신규 창업자를 위해 원하는 창업 관련 키워드 하나로 찾는 정보 사이트

## Project INFO


## PIPELINE


## Environment

> Python Version 3.8
> Docker Mysql 5


## Prerequisite
> pip install -r requirements.txt
> 
> export FLASK_APP=startupsplace
>
> flask run


## Files
`models/bertdataset.py` Kobert data

`models/classifier.py` Kobert classifier

`models/predict.py` Kobert predict

`routes/sing_route.py` Web Page of Predict Value & Crawling

## RETROSPECTIVE
##### 이전  회사에서 DA 진행을 할 때는 sklearn으로 ML만 진행 하였는데 이번 프로젝트를 통해 Deep learning을 조금이 나마 알게 되었다.
##### 챗봇이 아닌 Classifiter를 사용할 계획이라 Bert를 사용해서 진행했다.
##### Bert 논문을 보면서 모델 구조부터 천천히 익히면서 공부하였는데 확실한건 CNN보다 NLP 에 더 잘 맞는다는 것 이였다.
##### 또한 왜 NVIDIA가 큰 성공을 할 수 있는지 알 수 있던 계기가 되었다... (내 GPU...)

