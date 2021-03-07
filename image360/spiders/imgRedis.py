import json
import time
import random
from ..items import Image360Item
from scrapy_redis.spiders import RedisSpider
from scrapy import Request, Spider

class ImageSpider(RedisSpider):
    name = 'img'
    # allowed_domains = ['www']
    redis_key = 'img:start_urls'
    # start_urls = ['https://image.so.com/zjl?ch=beauty&sn=0']
# 'img:start_urls' 'https://image.so.com/zjl?ch=beauty&sn=0'
    def parse(self, response):
        items = Image360Item()
        res = json.loads(response.text)
        num = res.get('count')
        end = res.get('end')
        lists = res.get('list')
        # for i in range(10):
        #     print(lists[i]['qhimg_url'])
        # 图片信息获取
        for i in range(10):
            items['name'] = lists[i]['title']+'.jpg'
            items['img'] = lists[i]['qhimg_url']
        #     # name = lists[i]['title']+'.jpg'
        #     # img_url = lists[i]['qhimg_url']
            time.sleep(0.5)
            yield items
            # yield Request(url=img_url, meta={'info': name}, callback=self.download, dont_filter=False)

    def download(self, response):
        items = Image360Item()
        items['name'] = response.meta['info']
        # items['img'] = response.body
        # with open(items['name'],'wb') as f:
        #     f.write(items['img'])
        # print()
        yield items