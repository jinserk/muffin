# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector
from scrapy.http import Request
from linktv.items import LinkTvItem
from urllib.parse import unquote


class LinkTvSpider(CrawlSpider):
    name = "linktv"
    allowed_domains = ["linktv.us"]

    def __init__(self, keyword=""):
        self.start_urls = ["http://linktv.us/cast/search/q/1|{}|0/page/1".format(keyword)]

    def parse(self, response):
        hxs = Selector(response)
        urls = hxs.xpath('//a[@class="list-group-item"]')
        items = []
        for url in urls:
            item = LinkTvItem()
            date = url.xpath('span[@class="pull-right text-muted small"]/em/text()').extract()
            item['date'] = date
            link = url.xpath("@href").extract()
            mod_url = 'http://linktv.us{}'.format(''.join(link))
            yield Request(url=mod_url, meta={'item': item}, callback=self.parse_item)
            items.append(item)
        return(items)

    def parse_item(self, response):
        item = response.meta['item']
        hxs = Selector(response)
        urls = hxs.xpath('//a[@class="btn btn-info btn-outline btn-block"]').xpath("@href").extract()
        links = [unquote(url.split('=')[-1]) for url in urls]
        item['link'] = links
        return(item)
