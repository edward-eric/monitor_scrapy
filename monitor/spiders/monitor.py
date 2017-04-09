# -*- coding: utf-8 -*-
import scrapy
from ..items import registerItem
from datetime import datetime


class ExampleSpider(scrapy.Spider):

    name = "scrapy.monitor.benz"

    allowed_domains = ["mercedes-benz.com"]

    start_urls = ['https://me-cn.secure.mercedes-benz.com/']

    def start_requests(self):
        for url in self.start_urls:
            self.logger.info("请求网页地址：%s", url)
            yield scrapy.Request(url=url, callback=self.parse_landing)

    def parse_landing(self, response):
        self.logger.info("分析返回的网页元素: %s", response.url)
        self.logger.info("查找注册按钮.....")
        self.logger.info("分析头文件注册按钮 vs 主题注册按钮.....")
        header_register_url = self.__locate__href(response, 'headernavigation-link-register')
        header_register_txt = self.__locate__text(response, 'headernavigation-link-register')

        main_register_url = self.__locate__href(response, 'registerButtonLandingpage')
        main_register_txt = self.__locate__text(response, 'registerButtonLandingpage')

        if header_register_url == main_register_url:
            self.logger.info("注册按钮全部符合要求, 链接为: %s", header_register_url)
            register_item = registerItem(id='headernavigation-link-register', href=header_register_url,
                                         val=header_register_txt, lastUpdated=datetime.now())
        else:
            self.logger.error("注册按钮分析错误， 请分析具体情况.....")

        header_login_url = self.__locate__href(response, 'loginLinkHeaderNavigation')
        header_login_txt = self.__locate__text(response, 'loginLinkHeaderNavigation')

        main_login_url = self.__locate__href(response, 'loginButtonLandingpage')
        main_login_txt = self.__locate__text(response, 'loginButtonLandingpage')

        if header_login_url == main_login_url:
            self.logger.info("登录按钮全部符合要求, 链接为: %s", header_login_url)
        else:
            self.logger.error("登录按钮分析错误， 请分析具体情况.....")

        if main_login_url:
            return scrapy.Request(url=main_login_url, callback=self.click_login)

    def click_login(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={'username': 'xxxxxxx',
                                                                                'password': 'xxxxxxx'},
                                                callback=self.after_login)
    def after_login(self, response):
        return scrapy.FormRequest.from_response(response, callback=self.goto_landing)

    def goto_landing(self, response):
        return scrapy.Request(url='https://me-cn.secure.mercedes-benz.com/wps/myportal',
                              headers=response.headers,
                              callback=self.parse_text)

    def parse_text(self, response):
        return

    def __locate__href(self, response, name):
        return response.xpath('//a[@id="' + name + '"]/@data-layer-url').extract_first()

    def __locate__text(self, response, name):
        return response.xpath('//a[@id="' + name + '"]/text()').extract_first()