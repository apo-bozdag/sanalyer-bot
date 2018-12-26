# -*- coding: utf-8 -*-
import scrapy


class SdnSpider(scrapy.Spider):
    name = 'sdn'
    allowed_domains = ['shiftdelete.net']
    start_urls = ['http://shiftdelete.net/']

    def parse(self, response):
        pass
