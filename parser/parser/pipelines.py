import json

import asgiref
import scrapy
from asgiref.sync import sync_to_async
from .items import ProductItem


class AliPipeline(object):
    @sync_to_async()
    def process_item(self, item, spider):
        item.save()
        return item
