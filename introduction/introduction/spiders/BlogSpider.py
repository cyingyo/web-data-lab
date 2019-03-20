import scrapy

from ..items import BlogItem


class BlogSpider(scrapy.Spider):
    name = 'blog'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            item = BlogItem()
            item['title'] = title.css('a ::text').get()
            yield item

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, callback=self.parse)
