#coding:utf-8

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import MovieItem

class DoubanxSpider(CrawlSpider):
    name = 'Doubanx'
    allowed_domains = ['doubanx.com']
    start_urls = [
        'http://www.doubanx.com/category/ai-qing-pian',
        'http://www.doubanx.com/category/ke-huan-pian',
        'http://www.doubanx.com/category/xi-ju-pian',
        'http://www.doubanx.com/category/ju-qing-pian',
        'http://www.doubanx.com/category/dong-zuo-pian',
        'http://www.doubanx.com/category/xuan-yi-pian',
        'http://www.doubanx.com/category/kong-bu-pian',
        'http://www.doubanx.com/category/fan-zui-pian',
        'http://www.doubanx.com/category/zhan-zheng-pian',
        'http://www.doubanx.com/category/dong-hua-pian',
        'http://www.doubanx.com/category/jing-song-pian',
        'http://www.doubanx.com/category/mao-xian-pian',
        'http://www.doubanx.com/category/jia-ting-pian',
        'http://www.doubanx.com/category/ji-lu-pian',
    ]

    rules = (
        Rule(LinkExtractor(allow=('http://www.doubanx.com/category/[\w-]+/page/\d+'), restrict_xpaths=('//a[@class="page_btn cur_page"]/following-sibling::*[1]'))),
        Rule(LinkExtractor(allow=('http://www.doubanx.com/movie/[\w-]+/\d+')), callback='parse_item')
    )

    def parse_item(self, response):
        item = MovieItem()
        item['website'] = u'豆瓣X'
	name = response.xpath('//a[@class="poster_info_wrapper poster_title"]/span/strong/text()').extract()[0]
	try:
	    cname = response.xpath('//a[@class="poster_info_wrapper poster_title"]/span/strong/text()').extract()[1]
        except:
            cname = ''
        item['description'] = name + cname
        item['link'] = repr(response.xpath('//a[@class="magnet_link"][contains(@href,"thunder")]/@href').extract())
        return item
