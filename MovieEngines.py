#!/usr/bin/env python
#coding=utf-8

import time
import urllib2
from urllib import quote
import re
import sys
import threading
reload(sys)
sys.setdefaultencoding('utf-8')

def taskThread(method, taskList, maxThread=6, **args):
    for ts in range(0, len(taskList), maxThread):
        threads = []
        task = [taskList[ts+i] for i in range(maxThread) if ts+i < len(taskList)]
        for t in task:
            new_thread = threading.Thread(target=method, args=(t, args))
            threads.append(new_thread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
 



class GaoqingMp4(object):
    def __init__(self, ):
        self.baseURL = 'http://www.mp4ba.com/search.php?keyword='
        self.siteName = '高清MP4吧'
        self.result = []
        self.count = 0
        self.keyword = None

    def search(self, keyword):
        self.keyword = keyword
        searchURL = self.baseURL + keyword
        sourceHTML = urllib2.urlopen(searchURL).read()
        movieInfoRegx = r'<tr class="alt\d"(.*?)</tr>'
        movieInfos = re.findall(movieInfoRegx, sourceHTML, re.S)
        if movieInfos == []: return

        for movieInfo in re.findall(movieInfoRegx, sourceHTML, re.S):
            infoDict = {}
            detailsURL = 'http://www.mp4ba.com/' + re.findall(r'href="(show.php.*?)"',movieInfo)[0]
            infoDict['name'] = ''.join(re.findall(r'target="_blank">(.*?)<span class="keyword">(.*?)</span>(.*?)</a>',movieInfo,re.S)[0]).replace('\r\n','').replace(' ','')
            infoDict['downloadURL'] = self.getDownurl(detailsURL)
            infoDict['fileSize'] = re.findall(r'<td>(.*[M|G]B?)</td>',movieInfo)[0]
            self.result.append(infoDict)
        self.count = len(self.result)

    def getDownurl(self, detailsURL):
        page = urllib2.urlopen(detailsURL)
        html = page.read()
        return re.findall(r'<a id="magnet" href="(.*?)">',html)


    def __repr__(self, ):
        return '<{}:{}>'.format(self.siteName, str(self.keyword))



class Dytt(object):
    def __init__(self, ):
        self.baseURL = 'http://s.kujian.com/plus/search.php?kwtype=0&searchtype=title&keyword='
        self.siteName = '电影天堂'
        self.result = []
        self.count = 0
        self.keyword = None
        self.pageInfoURLs = []

    def pageSearch(self, page, args):
        pageURLBase = args['pageURLBase']
        movieURLRegx = args['movieURLRegx']
        pageURL = 'http://s.kujian.com/' + pageURLBase + str(page)
        pageHTML = urllib2.urlopen(pageURL).read()
        pageInfoURL = movieURLRegx.findall(pageHTML)
        self.pageInfoURLs.extend(pageInfoURL)

    def movieInfoSearch(self, infoURL, args):
        infoDict = {}
        downloadURLRegx = args['downloadURLRegx']
        movieTitleRegx = args['movieTitleRegx']
        infoHTML = urllib2.urlopen(infoURL).read()
        try: infoDict['name'] = movieTitleRegx.findall(infoHTML)[0].decode('gb2312')
        except UnicodeDecodeError,e: return
        infoDict['downloadURL'] = [url.decode('gb2312') for url in downloadURLRegx.findall(infoHTML)]
        self.result.append(infoDict) 

    def search(self, keyword):
        self.keyword = keyword
        searchURL = self.baseURL + quote(keyword.encode('gb2312'))
        sourceHTML = urllib2.urlopen(searchURL).read()

        movieURLRegx = re.compile(r'(?<=<td width=\'55%\'><b><a href=\')(/html/gndy/dyzz.*?|/html/tv/oumeitv.*?|/html/gndy/jddy.*?)\'>', re.S)
        pageCountRegx = r'PageNo=(\d+?)\'>{}</a></td>'.format('末页'.encode('gb2312'))
        pageCount = re.findall(pageCountRegx, sourceHTML, re.S)

        if pageCount != []:
            pageCount = int(pageCount[0])
            pageList = range(2, pageCount+1)
            pageURLRegx = r'<td><a href=\'(.*?)2\'>\[2\]</a>&nbsp;</td>'
            pageURLBase = re.findall(pageURLRegx, sourceHTML, re.S)[0]
            taskThread(self.pageSearch, pageList, pageURLBase=pageURLBase, movieURLRegx=movieURLRegx)
            
        infoURLs = movieURLRegx.findall(sourceHTML) + self.pageInfoURLs
        infoURLs = ['http://www.ygdy8.com'+url for url in infoURLs]
        movieTitleRegx = re.compile(r'<div class="title_all"><h1><font color=#07519a>(.*?)</font>', re.S)
        downloadURLRegx = re.compile(r'(?:"#fdfddf">|{}:<br />).*?<a href="(.*?)">'.format('下载地址'.encode('gb2312')), re.S)
        taskThread(self.movieInfoSearch, infoURLs, movieTitleRegx=movieTitleRegx, downloadURLRegx=downloadURLRegx)
        self.count = len(self.result)
 
    def __repr__(self, ):
        return '<{}:{}>'.format(self.siteName, str(self.keyword))

if __name__=='__main__':
    mname = raw_input('请输入要搜索的电影名:')
    movieEngines = [GaoqingMp4, Dytt, ]
    startTime = time.time()
    for engine in movieEngines:
        engine = engine()
        engine.search(mname)
        print engine.siteName
        if engine.result != []:
            for movie in engine.result:
                for k, v in movie.iteritems():
                    print '-'*20
                    print k, v
        else:
            print '搜索结果为空'
    costtime = time.time() - startTime
    print '搜索用时{}s'.format(costtime)
