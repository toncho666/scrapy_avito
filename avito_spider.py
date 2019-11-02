# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avito.items import AvitoItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class AvitoSpiderSpider(scrapy.Spider):
    name = 'avito_spider'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        # photos = response.xpath('//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class,"gallery-img-frame")]/@data-url').extract()
        # temp = AvitoItem(photos=photos)
        # yield temp
        loader = ItemLoader(item=AvitoItem(), response=response)
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        # понимаю что некорректно указывать индексами, но пришлось вытащить параметры объявления в отдельные столбцы
        loader.add_xpath('year', '//ul[@class="item-params-list"]/li[5]/text()[last()]')
        loader.add_xpath('brand', '//ul[@class="item-params-list"]/li[1]/text()[last()]')
        loader.add_xpath('model', '//ul[@class="item-params-list"]/li[2]/text()[last()]')
        loader.add_xpath('modification', '//ul[@class="item-params-list"]/li[4]/text()[last()]')
        loader.add_xpath('miliage', '//ul[@class="item-params-list"]/li[6]/text()[last()]')
        # так как на странице два поля (почти одинаковых) с ценой, указываю div только второго поля.
        loader.add_xpath('price',
                         '//div[@class="item-view-content"]//span[@class="price-value-string js-price-value-string"]/span[@class="js-item-price"]/@content')

        yield loader.load_item()
