# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver import DesiredCapabilities
import time


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        print("设置代理")
        # if '127.0.0.1' not in request.url:
        #     request.meta['proxy'] = "http://proxy-sifi.rd.corpintra.net:3128"

class JavaScriptMiddleware(object):

    driver = None

    def __init__(self):
        print("PhantomJS is starting.....")
        self.desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        self.desired_capabilities['phantomjs.page.customHeaders.Accept-Language'] = 'zh-CN'
        self.driver = webdriver.PhantomJS(port=4444, desired_capabilities=self.desired_capabilities)

    def process_request(self, request, spider):
        if spider.name == "benz" and request.method != "POST" and "sm-legacy" not in request.url and "ciam" not in request.url\
                and "portal" not in request.url:

            # print("PhantomJS is starting.....")
            # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            # desired_capabilities['phantomjs.page.customHeaders.Accept-Language'] = 'zh-CN'
            # driver = webdriver.PhantomJS(port=4444, desired_capabilities=desired_capabilities)
            self.driver.get(request.url)
            time.sleep(1)
            self.driver.save_screenshot("screen.png")
            print("访问 " + request.url)
            body = self.driver.page_source
            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)
        elif "portal" in request.url:

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
                'cache-control':'max-age=0',
                # 'cookie': 'SMSESSION=/8ZuLd1QwQAtZxiZvOwE77nRcCy8x/t2SMJxQwSiCPhWoM8vzMBz1ARgljaxczzBVWETmpGNvVpC5j8fZRsnE1EYM/pI3vRxlTdLZpbEt4zPWfQL1EtT1iW7U09KaBlwDoWzz6bNugyNne1OCXK8yBenin8tUHDYlm2qTnzL0PAysivLbXP1zDUi9xykNy10KS9aUG/ju47pZUcYy62WlsmSCZduoTSYdr28GqIf/2JAOl8D3ZlD45JLbFINw1dSgQGBQYWNfwb4WQTc94Ufham9zp/xnjT+sHOFt4oKSowmiy9XajX65iyvpYa/9CjwKl2vQ7qGZCsGtZoiL8lMGCq4iHed8Mm24mmngO2byTg9WidorOGeAdVWdx0hVUfK0uEju9RD9EPmyutJkpX8Y0CiZ/GnCXzc+wlArsyHGVs2PbMs7nbcySqVZwt0CbM4yj8ZxxHHMlEmhGkfJptVZa1I+QH5NWkDJNXGbmsx9BPTUdrX+QTyTPp+LWYWH+S3TEOQl9SnkAu6c846Z79zP9SH+SBMV+8RIkkUW7kL1+57Az9uBRCOFGN8XpBncBM61gkOgoTDj/0vL0VEU1oTKNOb8E31dN94/6tF01FYOGrSxwfdZ831Pa5wU1MAghxXLDxK3cjM87U0A1sO1PMxD0mbRhwkRAmrStoWV1hOZRiZH3skoJpSu2W+nsh0o6/7lk0QXzs1w+s2Nc0TpkbAtKBNclGhd6O0ezyhyz5wYe6mRJokDhsUar039CpC3htfet30TlMqUPLL2AikJe29Wniq/Ht9eWH3T264KLEuJ/Nhoofg9PmUOIPL3jHRxQvhfpE7c83mxEX+qMvkzyeIvJ+obD0VN52w6+sflb/iz3cdz3/5TOnnySk2YQHSTff9IeiHggIV4QS3HQw07lAR5kXTsDavnx7XrPdTrqOHwcvcb/Y5rR6X/KRj19ur0R96hAiA2AMEiLzX06RSPcnz45Fwhi+MW9lAUtqRNsBOCKjGvdgEStCkoC8Ero9WUXD+ZIcpZmgzCwHAnOoa383xRBSPGPEGoC8wlWkw/+Y1oGRKcdzCCP8+5vzm1hI+hDdzGv1VKXHZCFjgpBcviV0o8G/jqUCGUjHeU3D/H+BegpxD7lJLavprE9y/gHt3O0gKlmbitiBlhquyoMn6Sz6lCCDSOKNigZJEHF+vnAXMwgKTyHcwmFb1ivLuMxdJyEa4QKS54pTlq+lNsoPXIoxUVAxiWFVCYyGi; LtpaToken2=lb5mH4+pxC+cAfx+xNO+6+7eeyYRsvrxfyr7I5ts475OEyzMxYYqSxCMRFnOZnE7iNQb/OBHMa0BNZ0Rlgr0MDSG+gGk/nWPbrGfe/qmpIQoLn8uCjbDhrd7rFoqDfMaESBQDRvumFqbrVr4nBpdT0UnU+Hp2cfMuwgmsdel2zlWOIMK4YOm++p/sMETC2/ESkZcUoepkFbe7ZIJd8aObRzWoeIO1mBgp9rS9uO0vc3NDC8f3FUBaios4qWeDP8E+Nj1Cdmop152FXfg1cy3x8I5LmGVTlyoJkvyxc6x7h+vrVBdSkCivMQmBKNTLL6/HccFBq5XbTphG6PoVAYksf60AbfyZaqYVI53NrB0uv0b1u4WrCXgmS8fqaXuJXFNzufOkWz+gR1OWnIcHV7v2ua0DhOHk9mk+1GvNmiCDNHnJl995Jr47ngTjdwgdUAS; JSESSIONID=0000l1VH-1uR8xaze_T-gsHVFXf:1b69a49n7;',
                'referer':'https://me-cn.secure.mercedes-benz.com/ciam/ciam-callback-auth?status=0',
                'upgrade-insecure-requests': '1'
            }

            for key, value in headers.items():
                self.desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value

            headers1 = request.headers
            newvalue = ''
            for key, value in headers1.items():
                if key.decode() == 'Set-Cookie':
                    for i in value:
                        newvalue = newvalue + i.decode() + ";"
                    self.desired_capabilities['phantomjs.page.customHeaders.cookie'] = newvalue

            self.driver = webdriver.PhantomJS(port=4444, desired_capabilities=self.desired_capabilities)
            self.driver.get(request.url)
            time.sleep(1)
            self.driver.save_screenshot("screen.png")
            print("访问 " + request.url)
            body = self.driver.page_source
            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return




class MonitorSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)