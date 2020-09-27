import random
import re
import time

import emoji

from conf import book_name
import requests

from db import check_book, save_book, update_info, check_data, save_book_info, save_book_content
from utils import get_ua, request_url_list, set_headers
from lxml import etree
import os

base_url = 'https://book.douban.com'


def get_filename(path):
    return os.listdir(path)

def get_id_list(path):
    f = open(path,'r')
    ls = f.read().splitlines()
    f.close()
    return ls

if __name__ == '__main__':
    book_id_list = get_id_list('./经典.txt')
    count = 0
    for book_id in book_id_list:
        url = f'https://book.douban.com/subject/{book_id}/'
        while url:
            response = request_url_list(url)
            # response = requests.get(url, headers=set_headers(),timeout=10)
            response = response.text
            html = etree.HTML(response)
            try:
                book_name_main = html.xpath('//div[@id="wrapper"]/h1/span/text()')[0]
                try:
                    star = html.xpath('//div[@class="rating_right "]/div[1]/@class')[0]
                    mark = html.xpath(
                        '//div[@class="rating_self clearfix"]/strong[@class="ll rating_num "]/text()')[0]
                    eval_num = html.xpath(
                        '//div[@class="rating_right "]/div[@class="rating_sum"]/span/a/span/text()')[0]
                except Exception as e:
                    print(f'{book_id} 暂无评分')
                    star = None
                    mark = None
                    eval_num = None
                img_url = html.xpath('//*[@id="mainpic"]/a/img/@src')[0]
                img_name = book_id + '.' + img_url.split('.')[-1]
                book_info_node = html.xpath('//div[@id="info"]')[0]
                book_name_sub = book_info_node.xpath(
                    './/span[contains(text(),"副标题")]/following-sibling::text()[1]')
                author = book_info_node.xpath(
                    './/span[contains(text(),"作者")]/following-sibling::a[1]/text()')
                publisher = book_info_node.xpath(
                    './/span[contains(text(),"出版社")]/following-sibling::text()[1]')
                page_number = book_info_node.xpath(
                    './/span[contains(text(),"页数")]/following-sibling::text()[1]')
                pub_time = book_info_node.xpath(
                    './/span[contains(text(),"出版年")]/following-sibling::text()[1]')
                price = book_info_node.xpath(
                    './/span[contains(text(),"定价")]/following-sibling::text()[1]')
                ISBN = book_info_node.xpath(
                    './/span[contains(text(),"ISBN")]/following-sibling::text()[1]'
                )
                book_introduction = html.xpath(
                    '//div[@id="link-report"]/span[@class="all hidden"]/div/div[@class="intro"]')
                if book_introduction:
                    book_introduction = book_introduction[0].xpath('string(.)')
                else:
                    book_introduction = html.xpath(
                        '//div[@id="link-report"]/div/div[@class="intro"]')
                    if book_introduction:
                        book_introduction = book_introduction[0].xpath('string(.)')
                    else:
                        book_introduction = None

                author_introduction = html.xpath(
                    '//div[@class="related_info"]/div[@class="indent "]/span[@class="all hidden "]/div[@class="intro"]')
                if author_introduction:
                    author_introduction = author_introduction[0].xpath('string(.)')
                else:
                    author_introduction = html.xpath(
                        '//div[@class="related_info"]/div[@class="indent "]/div/div[@class="intro"]')
                    if author_introduction:
                        author_introduction = author_introduction[0].xpath('string(.)')
                    else:
                        author_introduction = None

                content = html.xpath(
                    f'//div[@class="related_info"]/div[@id="dir_{book_id}_full"]')
                if content:
                    content = content[0].xpath('string(.)')
                else:
                    content = html.xpath(
                        f'//div[@class="related_info"]/div[@id="dir_{book_id}_short"]')
                    if content:
                        content = content[0].xpath('string(.)')
                    else:
                        content = None

                # 数据清洗
                book_name_sub = ' : ' + book_name_sub[0].strip() if book_name_sub else ''
                book_name = book_name_main.strip() + book_name_sub
                page_number = page_number[0].strip() if page_number else None
                author = author[0].strip() if author else None
                publisher = publisher[0].strip() if publisher else None
                pub_time = pub_time[0].strip() if pub_time else None
                price = price[0].strip() if price else None
                ISBN = ISBN[0].strip() if ISBN else None
                if star and star.strip()[-2:] != 'pl':
                    mark = mark.strip() if mark else None
                    eval_num = re.search(r'(\d+)', eval_num).group(1)
                    if star.strip()[-2:] == '00':
                        star = '0'
                    else:
                        star_list = list(star.strip())
                        star = star_list[-2] + '.' + star_list[-1]
                else:
                    star = None
                    mark = None
                    eval_num = None
                if book_introduction:
                    book_introduction = emoji.demojize(book_introduction.strip())
                if author_introduction:
                    author_introduction = emoji.demojize(author_introduction.strip())
                if content:
                    content = content.strip()

                # 数据存储
                book_info_item = {
                    'book_id': book_id,
                    'book_name': book_name,
                    'ISBN': ISBN,
                    'page_number': page_number,
                    'author': author,
                    'publisher': publisher,
                    'pub_time': pub_time,
                    'star': star,
                    'mark': mark,
                    'eval_num': eval_num,
                    'price': price,
                    'book_introduction': book_introduction,
                    'author_introduction': author_introduction,
                    'img_url': img_url,
                    'img_name': img_name
                }

                if check_data(book_id):

                    save_book_info(book_info_item)

                    if content:
                        save_book_content(content, book_id)
                    count = count + 1
                    print(f'{book_id}  保存完成 {count}')
                    break
                else:
                    count = count + 1
                    print(f'{count}已存在，跳过 :{book_id}  {book_name} ')
                    break
            except Exception as e:
                print('出错, ', e)

                continue
