#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests


class DouyuSpider:
    def __init__(self):
        """ 初始化DouyuSpider
        创建一个斗鱼直播页面爬虫
        """
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
        # 直播大厅：https://www.douyu.com/directory/all
        # https://www.douyu.com/gapi/rkc/directory/0_0/2
        self.start_url = 'https://www.douyu.com/gapi/rkc/directory/0_0/{:d}'

    def fetch_one_page(self, offset):
        """ 发起请求，获取响应数据
        :param offset: 页面序号
        :return response.content: 二进制响应体数据
        """
        response = requests.get(
            self.start_url.format(offset),
            headers=self.headers
            )
        return response.content

    def parse_json(self, content):
        """解析数据
        :param content: 响应体二进制数据
        :return items, pgcnt: 直播信息列表，当前最大页面数
         """
        results = json.loads(content.decode())['data']
        items = []
        num = 0
        for result in results['rl']:
            item = {}
            item['topic'] = result['c2name']
            item['title'] = result['rn']
            ol = result['ol'] / 10000
            if ol == 0:
                item['hot'] = '0'
            else:
                item['hot'] = f'{ol:.1f}万'
            item['user'] = result['nn']
            item['room_url'] = 'https://www.douyu.com/{}'.format(result['url'])
            items.append(item)
            num += 1
            if num % 20 == 0:
                print(f'完成第{num}条数据')
                print(item)
        return items, int(results['pgcnt'])

    def save_content(self, items):
        """ 保存数据
        :param items: 直播信息列表
        :return None:
        """
        with open('douyu.json', 'a+', encoding='utf-8') as f:
            for data in items:
                json.dump(data, f, ensure_ascii=False)
                f.write('\n')

    def is_next(self, max_pages, offset):
        """ 判断是否有下一页
        :param max_pages: 当前最大页面数
        :param offset:  已爬取页数
        :return next_flag: 是否有下一页
        """
        if offset <  max_pages:
            next_flag = True
        if offset >= max_pages:
            next_flag = False
        return next_flag

    def run(self):
        """ 运行爬虫
        开始爬取数据
        """
        offset = 0
        next_flag = True
        while next_flag:
            offset += 1
            html = self.fetch_one_page(offset)
            items, max_pages = self.parse_json(html)
            self.save_content(items)
            print('*'*10 + f'完成第{offset}页' + '*'*10)
            print(f'最大页数{max_pages}')
            next_flag = self.is_next(max_pages, offset)
            # next_flag = False
        print('已爬取所有页面')


if __name__ == '__main__':
    dou_spider = DouyuSpider()
    dou_spider.run()

