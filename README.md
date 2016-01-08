MySite
=====
说明
----
这是我的个人小网站，目前集成了一个电影爬虫和电影搜索的UI,并打包成了docker镜像，可以使用docker-compose快速部署。
需要环境
------
####
    1.docker
    2.docker-compose
构建步骤
----
####
    1.克隆我的代码到本地
        git clone https://github.com/shadowzey/MySite.git
    2.进入代码目录
        cd MySite
    3.构建需要的镜像
        docker-compose build
    4.启动容器
        docker-compose up -d
    5.初始化数据库
        docker-compose run web python manage.py db upgrade
    6.开始爬取电影数据
        docker-compose run web sh crawl_movie.sh
    7.等待爬取完成即可，未完成时也可通过http://ip:5000来查看页面

  
