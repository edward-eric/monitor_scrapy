import scrapy

class MonitorSpider(scrapy.Spider):

    name = 'monitor'

    def start_requests(self):
        urls = [
            'https://me-cn.secure.mercedes-benz.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        login_url = response.xpath('//a[@id="loginButtonLandingpage"]/@data-layer-url').extract_first()
        self.logger.info('Parse function called on %s', login_url)
        if login_url:
            yield scrapy.Request(url=login_url, method='GET', callback=self.parse2)

    def parse2(self, response):
        return scrapy.FormRequest.from_response(response, formdata={'username': 'leiming.chen@daimler.com',
                                                                             'password': 'Welcome2016'},
                                                    callback=self.after_login)

    def after_login(self,response):
        self.logger.info('Parse function called on %s', response.text)

        return scrapy.FormRequest.from_response(response,
                                         callback=self.after_login2)

    def after_login2(self,response):
        self.logger.info('Parse function called on %s', response.text)
