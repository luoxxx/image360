# -*- coding: utf-8 -*-
import json
import time
import random
from ..items import Image360Item
from scrapy_redis.spiders import RedisSpider
import scrapy

class ImageSpider(RedisSpider):
    name = 'image'
    # allowed_domains = ['www']
    redis_key = 'img:start_urls'
    start_url = 'https://image.so.com/zjl?ch={ch}&sn={sn}'
    num = 0
    # 分布式爬虫
    def start_requests(self):
        for i in range(0, 10):
            time.sleep(random.random() * 2)
            yield self.make_requests_from_url(url=self.start_url.format(ch='ch', sn=i * 30))
            # yield Request(url=self.start_url.format(ch='ch', sn=i * 30), dont_filter=False, callback=self.parse)
    # def make_request_from_data(self, data):
    #     data = json.loads(data)
    #     url = data.get('url')
    #     print(url)
    def make_requests_from_url(self, url):
        return scrapy.Request(url)
        # for i in range(0, 2):
        #     time.sleep(random.random() * 2)
        #     yield scrapy.Request(self.start_url.format(ch='ch', sn=i * 30))

    def parse(self, response):
        items = Image360Item()
        res = json.loads(response.text)
        nums = res.get('count')
        end = res.get('end')
        lists = res.get('list')
        # print(lists)
        # 图片信息获取
        for i in range(nums):
            items['name'] = lists[i]['title']+'.jpg'
            items['img'] = lists[i]['qhimg_url']
            yield scrapy.Request(items['img'], callback=self.download)
    def download(self, response):
        res = response.body
        path = '../image/'+str(self.num)+'.jpg'
        self.num += 1
        with open(path, 'wb') as f:
            f.write(res)


    # 普通爬虫
    # def start_requests(self):
    #     # for u in range(5):
    #     for i in range(1, 3):
    #         time.sleep(random.random() * 2)
    #         yield scrapy.Request(url=self.start_url.format(ch='ch', sn=i * 30), callback=self.parse)
    #
    # def parse(self, response):
    #     items = Image360Item()
    #     dir = response.url
    #     print(dir)
    #     res = json.loads(response.text)
    #     num = res.get('count')
    #     end = res.get('end')
    #     lists = res.get('list')
    #     # 图片信息获取
    #     # for i in range(num):
    #     #     items['name'] = lists[i]['title']+'.jpg'
    #     #     items['url'] = lists[i]['qhimg_url']
    #     #     yield items
