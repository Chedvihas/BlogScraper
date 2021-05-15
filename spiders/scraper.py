import scrapy
import json
from ..items import BlogscraperItem
import re
from bs4 import BeautifulSoup


class blogs_spider(scrapy.Spider):
    name = 'blog'
    page_number = 2
    with open(r'C:\Users\Chedvihas\PycharmProjects\Scraping\BlogScraper\BlogScraper\spiders\setup.json') as f:
        json_data = json.load(f)
    website = 'Stackoverflow'
    start_url = [json_data[website]['start_url']]

    def start_requests(self):
        yield scrapy.Request(url=self.start_url[0], callback=self.parse)

    def clean_abstract(self, text):
        text = ' '.join(text)
        soup = BeautifulSoup(text, "html.parser")
        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()

        # clean = re.compile('<.*?>')
        # text = re.sub(clean, ' ', text)
        # text = re.sub('\n', ' ', text)
        #return text
        return ' '.join(soup.stripped_strings)

    def get_data(self, response):

        items = BlogscraperItem()
        link = response.meta.get('link-item')
        title = response.css(self.json_data[self.website]['title']).extract_first()
        author = response.css(self.json_data[self.website]['author']).extract()
        abstract = self.clean_abstract(response.xpath(self.json_data[self.website]['abstract']).extract())
        date = response.css(self.json_data[self.website]['date']).extract_first()
        items['website'] = self.website
        items['title'] = title
        items['author'] = author
        items['link'] = link.strip()
        items['abstract'] = abstract
        items['date'] = date.strip()

        yield items

    def parse(self, response):

        all_blogs = response.css(self.json_data[self.website]['all_blogs'])

        for blog in all_blogs:
            link = blog.css(self.json_data[self.website]['link']).extract_first()
            link = response.urljoin(link)
            yield response.follow(link, callback=self.get_data, meta={'link-item': link})

        try:
            last_page = self.json_data[self.website]['next_page_by_count']
            next_page = self.json_data[self.website]['next_page_base_url'] + str(self.page_number) + '/'
            if self.page_number < last_page:
                self.page_number += 1
                yield response.follow(next_page, callback=self.parse)

        except KeyError:
            next_page = response.xpath(self.json_data[self.website]['next_page']).get()

            if next_page is not None:
                if self.json_data[self.website]['link_type'] == 'tail':
                    next_page = response.urljoin(next_page)
                yield response.follow(next_page, callback=self.parse)
