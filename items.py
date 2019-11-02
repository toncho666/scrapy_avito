# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst  # первый препроцеессор, второй постпроцессор


# метод для добалвения к адресу фотки 'http:'
def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def price_correct(value):
    return int(value)


class AvitoItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))  # обработка "перед"
    title = scrapy.Field(output_processor=TakeFirst())  # извлекает из получаемого списка значение "после"
    year = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    model = scrapy.Field(output_processor=TakeFirst())
    modification = scrapy.Field(output_processor=TakeFirst())
    miliage = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_correct), output_processor=TakeFirst()) # без TakeFirst возвращается массив из одного значения.
