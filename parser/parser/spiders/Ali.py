from collections import OrderedDict
from uuid import uuid4

import scrapy
import json

from scrapy.spiders import Rule
from scrapy_selenium import SeleniumRequest
import pandas as pd
from ..items import ProductItem

def data_to_json(data):
    data.replace('<script id="__AER_DATA__" type="application/json">', '')
    data = json.loads(data)
    return data


def take_images(data):
    image_blocks = data['gallery']
    images = []
    for image in image_blocks:
        item = {}

        if image['imageUrl']:
            item['image'] = image['imageUrl']
        if image['videoUrl']:
            item['video'] = image['videoUrl']
        images.append(item)
    return images


def take_parameters(data):
    data = data['skuInfo']['propertyList']
    parameters = []
    for info in data:
        parameter = {'title': info['name']}
        values = []
        for value in info['values']:
            values.append({'name': value['displayName'], 'id': value['id']})
        parameter['info'] = values
        parameters.append(parameter)
    return parameters


def take_additional_parameters(data):
    try:
        data = data['widgets'][2]['children'][0]['children'][0]['children'][0]['children'][7]['children'][0]['children'][3][
            'props']['html']
    except Exception as e:
        data = data['widgets'][2]['children'][0]['children'][0]['children'][0]['children'][6]['children'][0]['children'][3][
            'props']['html']
    return data


def take_prices(data):
    data = data['skuInfo']['priceList']
    prices = [price['activityAmount']['value'] for price in data]
    prices = list(OrderedDict.fromkeys(prices))
    return prices


class AliSpider(scrapy.Spider):
    name = "Ali"

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.unique_id = kwargs.get("_job")
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        AliSpider.rules = [
            Rule(SeleniumRequest(url=self.url, callback=self.parse, wait_time=5))
        ]

        super(AliSpider, self).__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        page_api = str(response.css('#__AER_DATA__::text').get())
        page_api = data_to_json(page_api)
        additional_parameters = take_additional_parameters(page_api)

        product_api = page_api['widgets'][2]['children'][0]['children'][0]['children'][0]['props']

        images = take_images(product_api)
        parameters = take_parameters(product_api)
        prices = take_prices(product_api)
        unique_id = str(uuid4())

        item = {
            '????????????????': product_api['name'],
            '????????????????': images,
            '??????????????????': parameters,
            '???????????????????????????? ??????????????????': additional_parameters,
            '????????': prices
        }

        product = ProductItem()
        product['unique_id'] = self.unique_id
        product['name'] = item['????????????????']
        product['images'] = item['????????????????']
        product['parameters'] = item['??????????????????']
        product['prices'] = item['????????']
        product['additional_parameters'] = item['???????????????????????????? ??????????????????']
        product['from_whom'] = "AliExpress"

        yield product
