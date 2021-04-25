import scrapy
import json
from ..items import BlogscraperItem

class Googleai_spider(scrapy.Spider):
    name = 'blog'
    with open(r'C:\Users\Chedvihas\PycharmProjects\Scraping\BlogScraper\BlogScraper\spiders\setup.json') as f:
        json_data = json.load(f)
    website = 'Cap-Gemini'
    start_urls = [json_data[website]['start_url']]



    def parse(self, response):

        items = BlogscraperItem()

        all_blogs = response.css(self.json_data[self.website]['all_blogs'])
        for blog in all_blogs:
            title = blog.css(self.json_data[self.website]['title']).extract_first()
            author = blog.css(self.json_data[self.website]['author']).extract()
            link = blog.css(self.json_data[self.website]['link']).extract_first()
            abstract = ''.join(blog.css(self.json_data[self.website]['abstract']).extract())
            date = blog.css(self.json_data[self.website]['date']).extract_first()
            items['website'] = self.website
            items['title'] = title
            items['author'] = author
            items['link'] = link
            if (self.json_data[self.website]['link_type'] == 'tail'):
                items['link'] = self.start_urls[0] + items['link']
            items['abstract'] = abstract.strip()
            items['date'] = date
            

            yield items



        try:
            next_page = response.xpath(self.json_data[self.website]['next_page_by_xpath']).get()
        except KeyError:
            next_page = response.css(self.json_data[self.website]['next_page']).get()


        if next_page is not None:
            if (self.json_data[self.website]['link_type'] == 'tail'):
                next_page = self.start_urls[0] + next_page
            yield response.follow(next_page,callback= self.parse)







