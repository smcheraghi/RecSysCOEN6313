# RecSysCOEN6313
Recommendation system

## Build setup

``` bash
# install front-end
cd frontend
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production/Flask with minification
# Creates the dist folder in the root of application.
# The production flask application use this folder
npm run build


# install back-end
cd ../backend
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
cd ..

# serve back-end at localhost:5000
FLASK_APP=run.py flask run
# or
python3 run.py
```
## Data Source Introduction
https://tianchi.aliyun.com/datalab/dataSet.html?spm=5176.100073.0.0.583d3ea7v2AdZk&dataId=649

## Data link on Google Drive
https://drive.google.com/open?id=1oWW5DNOCmgqooILF6CavPxPTdJVY-J_c
https://drive.google.com/open?id=1wpcxDkKKUE-e56kucRwxGZQXEyHuYkFA

## Learning Tree-based Deep Model for Recommender Systems
https://arxiv.org/pdf/1801.02294.pdf

## Real-Time Personalized Recommendation System - Alibaba Cloud Community
https://www.alibabacloud.com/blog/real-time-personalized-recommendation-system_115904

## 推荐系统主要算法总结及Youtube深度学习推荐算法实例概括
https://www.jiqizhixin.com/articles/2017-07-09-5

## 一文综述用于推荐系统的所有深度学习方法 - CSDN博客
https://blog.csdn.net/kingzone_2008/article/details/80692113