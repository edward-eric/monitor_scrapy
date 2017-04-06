# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "benz"
    allowed_domains = ["mercedes-benz.com"]
    start_urls = ['https://me-cn.secure.mercedes-benz.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        login_url = response.xpath('//a[@id="loginButtonLandingpage"]/@href').extract_first()
        if login_url:
            return scrapy.Request(url=login_url, callback=self.click_login)

    def click_login(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={'username': 'leiming.chen@daimler.com',
                                                                                'password': 'Welcome2016'},
                                                callback=self.after_login)
    def after_login(self, response):
        return scrapy.FormRequest.from_response(response, callback=self.goto_landing)

    def goto_landing(self, response):
        return scrapy.Request(url='https://me-cn.secure.mercedes-benz.com/wps/myportal', callback=self.parse_text)

    def parse_text(self, response):
        self.logger.info(response.text)