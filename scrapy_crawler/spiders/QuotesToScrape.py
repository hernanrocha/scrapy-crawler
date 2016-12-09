# -*- coding: utf-8 -*-
import scrapy

# Generated from 'scrapy genspider QuotesToScrape quotes.toscrape.com'
# Test: run 'scrapy crawl QuotesToScrape -o quotes.jl'

class QuotestoscrapeSpider(scrapy.Spider):
    name = "QuotesToScrape"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)