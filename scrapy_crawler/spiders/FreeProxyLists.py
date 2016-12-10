# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
import urllib

class FreeproxylistsSpider(scrapy.Spider):
    name = "FreeProxyLists"
    allowed_domains = ["freeproxylists.net"]
    start_urls = ['http://www.freeproxylists.net/']

    def parse(self, response):
        for ipdata in response.css('table.DataGrid').css('tr.Odd, tr.Even'):
            try:
                yield {
                    'ip' : Selector(text=urllib.unquote(ipdata.css('td script::text').re('"(.*)"')[0])).css('a::text').extract_first(),
                    'port' : ipdata.css('td::text').extract_first(),
                    'protocol' : ipdata.css('td::text')[1].extract(),
                    'anonimity' : ipdata.css('td::text')[2].extract(),
                    'country' : ipdata.css('td::text')[3].extract().strip(),
                }
            except:
            	self.logger.error('Error parsing %s' % ipdata.extract())