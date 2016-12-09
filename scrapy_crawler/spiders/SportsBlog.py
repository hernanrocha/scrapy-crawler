# -*- coding: utf-8 -*-
import scrapy


class SportsblogSpider(scrapy.Spider):
    name = "SportsBlog"
    allowed_domains = ["sportsblog.com"]
    start_urls = ['https://www.sportsblog.com/']

    def parse(self, response):
        for url in response.css('a::attr("href")').re('.*/blogs/.*'):
            self.logger.info('Found blog: %s' % url)
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        for post_title in response.css('div.story-content strong a small::text').extract():
            yield {'title': post_title}
