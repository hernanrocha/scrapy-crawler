# -*- coding: utf-8 -*-
import scrapy


class ThepiratebaySpider(scrapy.Spider):
    name = "ThePirateBay"
    allowed_domains = ["thepiratebay.org"]
    start_urls = ['https://thepiratebay.org/browse/200']

    def parse(self, response):
        # Warning: Using xpath because table/thead/tr is not parseable
        #          Chrome and Firefox add table/tbody and scrapy don't
        for torrent in response.xpath('//table[@id="searchResult"]/tr[position() < last()]'):
            try:
            	yield {
                    'category': torrent.css('td.vertTh a::text')[1].extract(),
                    'title': torrent.css('div.detName a::text').extract_first(),
                    'magnet': torrent.css('a::attr("href")').re(r'magnet:.*')[0],
                    'uploader': torrent.css('a.detDesc::text').extract_first(),
                    'size' : torrent.css('font.detDesc::text').re('Size(.*[MG]iB)'),
                }
            except:
            	self.logger.error('Error parsing %s' % torrent.extract())

    	# Find 'Next' link
        for link in response.css('a'):
            if link.css('img::attr("alt")').re('Next'):
                next_link = link.css('::attr("href")').extract_first()
                self.logger.info('Next page: %s' % next_link)
                yield scrapy.Request(response.urljoin(next_link))