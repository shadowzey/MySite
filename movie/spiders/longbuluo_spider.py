#coding:utf-8

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import MovieItem

class LongbuluoSpider(CrawlSpider):
    name = 'LongBuLuo'
    allowed_domains = ['lbldy.com']
    start_urls = [
        'http://www.lbldy.com/tag/dzp/',
        'http://www.lbldy.com/tag/xjp/',
        'http://www.lbldy.com/tag/kbp/',
        'http://www.lbldy.com/tag/khp/',
        'http://www.lbldy.com/tag/aqp/',
        'http://www.lbldy.com/tag/jqp/',
        'http://www.lbldy.com/tag/zzp/',
        'http://www.lbldy.com/tag/dhp/',
        'http://www.lbldy.com/tag/mxp/',
        'http://www.lbldy.com/tag/gfp/',
        'http://www.lbldy.com/tag/xyp/',
        'http://www.lbldy.com/tag/jsp/',
        'http://www.lbldy.com/tag/lzp/',
        'http://www.lbldy.com/tag/fzp/',
        'http://www.lbldy.com/tag/lsp/',
        'http://www.lbldy.com/tag/ssp/',
        'http://www.lbldy.com/tag/zjp/',
        'http://www.lbldy.com/tag/gzp/',
        'http://www.lbldy.com/tag/qhp/',
        'http://www.lbldy.com/tag/hxp/',
        'http://www.lbldy.com/tag/gwp/',
        'http://www.lbldy.com/tag/wxp/',
        'http://www.lbldy.com/tag/znp/',
        'http://www.lbldy.com/tag/smp/',
        'http://www.lbldy.com/tag/xbp/',
        'http://www.lbldy.com/tag/jfp/',
        'http://www.lbldy.com/tag/jtp/',
        'http://www.lbldy.com/tag/hsp/',
        'http://www.lbldy.com/tag/ydp/',
        'http://www.lbldy.com/tag/jlp/',
        'http://www.lbldy.com/tag/yyp/',
        'http://www.lbldy.com/tag/gfdy/',
    ]
    
    rules = (
        #Rule(LinkExtractor(allow=('www.lbldy.com/tag/.*/page/\d+/'), restrict_xpaths=('//div[@class="pagebar"]/a[last()]'))),
        Rule(LinkExtractor(allow=('www.lbldy.com/tag/.*/page/\d+/'), restrict_xpaths=('//a[@class="next page-numbers"]'))),
        Rule(LinkExtractor(allow=('www.lbldy.com/(?:movie|television|dongman|video)/\d+\.html')), callback='parse_item')
    )

    def parse_item(self, response):
        item = MovieItem()
        item['website'] = u'龙部落'
        item['description'] = response.xpath('//div[@class="post"]/h2/text()').extract_first()
        item['link'] = repr(response.xpath('//a[contains(@href, "ed2k") or contains(@href, "thunder") or contains(@href, "ftp") or contains(@href, "magnet")]/@href').extract())
        return item
