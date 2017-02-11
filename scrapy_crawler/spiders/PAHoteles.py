# -*- coding: utf-8 -*-
import scrapy
from scrapy_crawler.items import PAHotelesItem

class PahotelesSpider(scrapy.Spider):
    name = "PAHoteles"
    allowed_domains = ["hoteles.com.ar"]
    start_urls = ['http://www.hoteles.com.ar/b/hoteles/cordoba/m']

    def parse(self, response):
        for item in response.xpath('//div[@id="resultList"]/div[contains(@class, "advertiseBlock")]'):
            paItem = PAHotelesItem()
            paItem['nombre'] = item.css('h2.advertise-name a::text').extract_first()
            paItem['link'] = item.css('h2.advertise-name a::attr("href")').extract_first()
            paItem['links_titles'] = item.css('div.advertiseBlockFooter ul li span::text').extract()
            paItem['links_links'] = item.css('div.advertiseBlockFooter ul li a::attr("href")').extract()
            yield paItem

        for link in response.xpath('//a[contains(@class, "friendlySearchLink")]'):
            if link.xpath('text()').re(">"):
                next_link = link.css('::attr("href")').extract_first()
                self.logger.info('Next page: %s' % next_link)
                yield scrapy.Request(response.urljoin(next_link))