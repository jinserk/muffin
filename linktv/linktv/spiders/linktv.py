# -*- coding: utf-8 -*-

from scrapy.spiders import Spider, Rule
from scrapy import Selector, Request
from linktv.items import LinkTvItem, TitleItem
from urllib.parse import unquote

programs = [
    { "title": "JTBC 뉴스룸",
      "keyword": "jtbc 뉴스룸",
    },
    { "title": "JTBC 이규연의 스포트라이트",
      "keyword": "이규연의 스포트라이트",
    },
    { "title": "JTBC 썰전",
      "keyword": "썰전",
    },
    { "title": "SBS 그것이 알고싶다",
      "keyword": "그것이 알고 싶다 -",
    },
]

class LinkTvSpider(Spider):
    name = "linktv"
    allowed_domains = ["linktv.us"]

    def start_requests(self):
        items = []
        for program in programs:
            items.append(LinkTvItem())
            item = items[-1]
            item['title'] = program["title"]
            start_url = "http://linktv.us/cast/search/q/1|{}|0/page/1".format(program["keyword"])
            yield Request(url=start_url, meta={'items': items, 'item': item}, callback=self.parse)
            
    def parse(self, response):
        items = response.meta['items']
        item = response.meta['item']
        hxs = Selector(response)
        urls = hxs.xpath('//a[@class="list-group-item"]')
        item['data'] = []
        for url in urls:
            item['data'].append(TitleItem())
            subitem = item['data'][-1]
            date = url.xpath('span[@class="pull-right text-muted small"]/em/text()').extract()
            subitem['date'] = date
            link = url.xpath("@href").extract()
            mod_url = 'http://linktv.us{}'.format(''.join(link))
            yield Request(url=mod_url, meta={'items': items, 'subitem': subitem}, callback=self.parse_item)

    def parse_item(self, response):
        items = response.meta['items']
        subitem = response.meta['subitem']
        hxs = Selector(response)
        urls = hxs.xpath('//a[@class="btn btn-info btn-outline btn-block"]').xpath("@href").extract()
        links = [unquote(url.split('=')[-1]) for url in urls]
        subitem['link'] = links
        return items
