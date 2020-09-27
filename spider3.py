import random
import re
import time
from db import *
import emoji

from conf import book_name_list
import requests
from utils import get_ua, get_proxy, delete_proxy, request_url, request_url_list
from lxml import etree

base_url = 'https://book.douban.com'
url = 'https://book.douban.com/tag/%E4%B8%9C%E9%87%8E%E5%9C%AD%E5%90%BE'
headers = {
    "User-Agent": get_ua()
}
api_url = 'http://127.0.0.1:5010/get/'

if __name__ == '__main__':
    for tag in book_name_list:
        url = f'https://book.douban.com/tag/{tag}'
        while url:
            # response = requests.get(url, headers=headers)
            response = request_url_list(url)
            response = response.text
            html = etree.HTML(response)
            pic_list = html.xpath('//li[@class="subject-item"]')

            next_url = html.xpath('//span[@class="next"]/a/@href')
            if pic_list:
                for item in pic_list:
                    time.sleep(3)
                    book_url = item.xpath('./div[@class="pic"]/a/@href')[0]
                    book_id = re.search(r'/subject/(\d+)', book_url).group(1)
                    img_url = item.xpath('./div[@class="pic"]/a/img/@src')[0]
                    img_url = book_id + '.' + img_url.split('.')[-1]
                    img_name = book_id + '.' + img_url.split('.')[-1]
                    book_name_main = item.xpath('.//div[@class="info"]/h2/a/text()')[0].strip() if item.xpath(
                        './/div[@class="info"]/h2/a/text()') else ''
                    book_name_sub = item.xpath('.//div[@class="info"]/h2/a/span/text()')[0] if item.xpath(
                        './/div[@class="info"]/h2/a/span/text()') else ''
                    book_name = book_name_main + book_name_sub
                    try:
                        star = item.xpath('.//div[@class="info"]/div[@class="star clearfix"]/span[1]/@class')[0]
                        mark = item.xpath('.//div[@class="info"]/div[@class="star clearfix"]/span[2]/text()')[0]
                        eval_num = item.xpath(
                            './/div[@class="info"]/div[@class="star clearfix"]/span[3]/text()')[0]
                    except:
                        star = None
                        mark = None
                        eval_num = None
                    book_info = item.xpath('.//div[@class="pub"]/text()')[0].strip() if item.xpath(
                        './/div[@class="pub"]/text()') else ''
                    book_item = {
                        'book_name': book_name,
                        'book_id': book_id,
                        'book_info': book_info,
                        'star': star,
                        'eval_num': eval_num,
                        'img_url': img_url,
                        'mark': mark
                    }
                    if check_book(book_id):

                        save_book(book_item)
                        print(f'保存{tag} {book_name} {book_id} {next_url}')
                    else:
                        print(f'{tag} {book_name} {book_id} 已存在')
                        update_info(book_id, book_info)
                        continue
                if next_url:
                    next_url = base_url + next_url[0]
                    if next_url.find('start=1000') != -1:
                        url = False
                    url = next_url
                    time.sleep(3)
                else:
                    url = False
