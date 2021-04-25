import scrapy
from ..items import BlogscraperItem
class Googleai_spider(scrapy.Spider):
    name = 'blogs'
    start_urls = ['https://ai.googleblog.com/']

    def parse(self, response):

        items = BlogscraperItem()
        all_blogs = response.css('div.post')
        for blog in all_blogs:
            title = blog.css('.title a::text').extract()
            author = blog.css('.byline-author::text').extract()
            abstract = ''.join(blog.css('p::text').extract())
            date = blog.css('.publishdate::text').extract()

            items['title'] = title
            items['author'] = author
            items['abstract'] = abstract
            items['date'] = date

            yield items


        next_page = response.css('#Blog1_blog-pager-older-link::attr(href)').get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)




