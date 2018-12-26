# -*- coding: utf-8 -*-
import scrapy
from .HomeSpider import HomeSpider
from Sybot.items import ContentItem
import html2text


class WebteknoSpider(scrapy.Spider):
    name = 'webtekno'
    allowed_domains = ['webtekno.com']
    start_urls = ['https://www.webtekno.com/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home = HomeSpider(**kwargs)
        self.source_url = 'https://www.webtekno.com'
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = True

    def parse(self, response):
        category_container = response.xpath('//div[contains(@class,"category-dropdown dropdown-container")]')
        if category_container:
            categories = category_container.xpath('//li[contains(@class,"dropdown-container__item ripple")]')
            for category in categories:
                link = category.css('li > a::attr(href)').extract_first()
                if link:
                    item = ContentItem()
                    item['category'] = category.css('li > a::text').extract_first()
                    request = scrapy.Request(link, callback=self.categoryDetailPage)
                    request.meta["item"] = item
                    yield request

    def categoryDetailPage(self, response):
        item = response.meta["item"]
        post_list_container = response.xpath('//div[contains(@class, "content-timeline__list")]')
        if post_list_container:
            posts = post_list_container.xpath('//div[contains(@class, "content-timeline__item")]')
            for post in posts:
                link = post.css('div > div.content-timeline--right > div > a::attr(href)').extract_first()
                item['title'] = post.css('div > div.content-timeline--right > div.content-timeline__detail > '
                                         'div.content-timeline__detail__container > a > h3 > span::text').extract_first().strip()
                item['news_url'] = link

                request = scrapy.Request(link, callback=self.postDetail)
                request.meta["item"] = item
                yield request

        next_page = response.css('li.pagination__box > a::text')[-1].extract()
        if next_page == '»':
            next_page = response.css('li.pagination__box > a::attr(href)')[-1].extract()
            request = scrapy.Request(url=self.source_url + next_page, callback=self.categoryDetailPage)
            request.meta["item"] = item
            yield request

    def postDetail(self, response):
        item = response.meta["item"]

        description = response.xpath('//div[contains(@class, "content-body__description")]/text()').extract_first().strip()
        content = response.xpath('//div[contains(@class, "content-body__detail")]/node()').extract()
        item['description'] = description
        item['content'] = "\n".join(content)

        print(item)

    def close(self, reason):
        print(self.home.getSourceUrls)
