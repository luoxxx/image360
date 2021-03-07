# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from .items import Image360Item
import os
import scrapy
import requests
from .settings import DEFAULT_REQUEST_HEADERS
class Image360Pipeline(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36'
    }
    def process_item(self, item, spider):
        try:
            # if not os.path.exists('image'):
            #     os.mkdir('image')
            with open('../image/ '+item['name'], 'wb') as f:
                res = requests.get(item['img'], headers=self.headers).content
                # res1 = scrapy.Request(item['img']).body
                f.write(res)
            print('下载成功')
        except Exception as e:
            print('下载失败:', e)
        return item
