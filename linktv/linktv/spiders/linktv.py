# -*- coding: utf-8 -*-

from scrapy.spiders import Spider, Rule
from scrapy import Selector, Request
from linktv.items import LinkTvItem
from urllib.parse import unquote

programs = [
    { "name": "JTBC 뉴스룸",
      "keyword": "jtbc 뉴스룸",
    },
    { "name": "JTBC 이규연의 스포트라이트",
      "keyword": "이규연의 스포트라이트",
    },
    { "name": "JTBC 썰전",
      "keyword": "썰전",
    },
    { "name": "SBS 그것이 알고싶다",
      "keyword": "그것이 알고 싶다 -",
    },
]

class LinkTvSpider(Spider):
    name = "linktv"
    allowed_domains = ["linktv.us"]

    def start_requests(self):
        for program in programs:
            name = program["name"]
            url = "http://linktv.us/cast/search/q/1|{}|0/page/1".format(program["keyword"])
            yield Request(url=url, meta={'name': name}, callback=self.parse_program)
            
    def parse_program(self, response):
        name = response.meta['name']
        hxs = Selector(response)
        urls = hxs.xpath('//a[@class="list-group-item"]')
        for url in urls:
            date = url.xpath('span[@class="pull-right text-muted small"]/em/text()').extract()
            link = url.xpath("@href").extract()
            url = 'http://linktv.us{}'.format(''.join(link))
            yield Request(url=url, meta={'name': name, 'date':date}, callback=self.parse_link)

    def parse_link(self, response):
        name = response.meta['name']
        date = response.meta['date']
        hxs = Selector(response)
        urls = hxs.xpath('//a[@class="btn btn-info btn-outline btn-block"]').xpath("@href").extract()
        links = [unquote(url.split('=')[-1]) for url in urls]
        item = LinkTvItem()
        item['name'] = name
        item['date'] = date
        item['link'] = links
        return item
