#coding:utf-8

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import MovieItem

class DyttSpider(CrawlSpider):
    name = 'Dytt'
    allowed_domains = ['ygdy8.net', 'ygdy8.com']
    start_urls = [
        'http://www.ygdy8.net/html/gndy/china/index.html',
        'http://www.ygdy8.net/html/gndy/rihan/index.html',
        'http://www.ygdy8.net/html/gndy/oumei/index.html',
        'http://www.ygdy8.net/html/gndy/dyzz/index.html',
        'http://www.ygdy8.net/html/gndy/jddy/index.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=('list_\d+_\d+.html'), restrict_xpaths=('//td[@bgcolor="#F4FAE2"]/a[last()-1]'))),
        Rule(LinkExtractor(allow=('/html/gndy/(?:dyzz|jddy)/\d+/\d+.html')), callback='parse_item')
    )

    def parse_item(self, response):
        item = MovieItem()
        item['website'] = u'电影天堂'
        item['description'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract_first()
        item['link'] = repr(response.xpath('//td[@bgcolor="#fdfddf"]/font[@color="#ff0000"]/a/@href|//td[@bgcolor="#fdfddf"]/a/@href').extract())
        return item
