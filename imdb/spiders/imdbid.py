# -*- coding: utf-8 -*-
import scrapy


class IMDbIDSpider(scrapy.Spider):
    name = 'imdbid'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/search/title?user_rating=7.0,10.0&count=250']

    def parse(self, response):
        for row in response.css('div.lister-item'):
            yield self.sanitize(row)

        next_page = response.css('div.desc a.lister-page-next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def sanitize(self, row):
        return {'imdbid': row.css('div.lister-item-image a img::attr(data-tconst)').extract_first()}
