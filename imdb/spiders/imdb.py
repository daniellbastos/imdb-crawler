# -*- coding: utf-8 -*-
import scrapy


class IMDbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/search/title?user_rating=7.0,10.0&count=250']

    def parse(self, response):
        for row in response.css('div.lister-item'):
            yield self.sanitize(row)

        next_page = response.css('div.desc a.lister-page-next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def sanitize(self, row):
        data = {}
        data['name'] = row.css('h3 a::text').extract_first()
        data['year'] = row.css('h3 span.lister-item-year::text').extract_first()
        data['duration'] = row.css('p.text-muted span.runtime::text').extract_first()
        data['gender'] = row.css('p.text-muted span.genre::text').extract_first()

        if data['gender']:
            data['gender'] = data['gender'].rstrip().replace('\n', '').replace(', ', ',')

        data['ratings_imdb'] = row.css('div.ratings-bar div.ratings-imdb-rating strong::text').extract_first()
        data['description'] = ' '.join([i.strip() for i in row.css('p.text-muted::text').extract() if i.replace('\n','').strip()])
        data['image'] = row.css('div.lister-item-image a img::attr(src)').extract_first()
        return data
