import random
import re
import time
from db import *
import emoji

from conf import book_name_list
import requests
from utils import get_ua, get_proxy, delete_proxy, request_url, parse_detail
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
            response = request_url(url)
            response = response.text
            html = etree.HTML(response)
            pic_list = html.xpath('//div[@class="pic"]')

            next_url = html.xpath('//span[@class="next"]/a/@href')
            if pic_list:
                for item in pic_list:
                    time.sleep(random.randint(3, 5))
                    book_url = item.xpath('./a/@href')[0]
                    book_id = re.search(r'/subject/(\d+)', book_url).group(1)
                    img_url = item.xpath('./a/img/@src')[0]
                    img_name = book_id + '.' + img_url.split('.')[-1]
                    detail_url = f'https://book.douban.com/subject/{book_id}/'
                    # detail_response = requests.get(detail_url, headers=headers).text
                    detail_response = parse_detail(detail_url).text
                    detail_html = etree.HTML(detail_response)
                    book_name_main = detail_html.xpath('//div[@id="wrapper"]/h1/span/text()')
                    if book_name_main:
                        book_name_main = book_name_main[0]
                    else:
                        print('放弃保存该条')
                        continue
                    try:
                        star = detail_html.xpath('//div[@class="rating_right "]/div[1]/@class')[0]
                        mark = detail_html.xpath(
                            '//div[@class="rating_self clearfix"]/strong[@class="ll rating_num "]/text()')[0]
                        eval_num = detail_html.xpath(
                            '//div[@class="rating_right "]/div[@class="rating_sum"]/span/a/span/text()')[0]
                    except Exception as e:
                        print(f'{tag}:{book_id} 暂无评分')
                        star = None
                        mark = None
                        eval_num = None
                    try:
                        book_info_node = detail_html.xpath('//div[@id="info"]')[0]
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
                        book_introduction = detail_html.xpath(
                            '//div[@id="link-report"]/span[@class="all hidden"]/div/div[@class="intro"]')
                        if book_introduction:
                            book_introduction = book_introduction[0].xpath('string(.)')
                        else:
                            book_introduction = detail_html.xpath(
                                '//div[@id="link-report"]/div/div[@class="intro"]')
                            if book_introduction:
                                book_introduction = book_introduction[0].xpath('string(.)')
                            else:
                                book_introduction = None

                        author_introduction = detail_html.xpath(
                            '//div[@class="related_info"]/div[@class="indent "]/span[@class="all hidden "]/div[@class="intro"]')
                        if author_introduction:
                            author_introduction = author_introduction[0].xpath('string(.)')
                        else:
                            author_introduction = detail_html.xpath(
                                '//div[@class="related_info"]/div[@class="indent "]/div/div[@class="intro"]')
                            if author_introduction:
                                author_introduction = author_introduction[0].xpath('string(.)')
                            else:
                                author_introduction = None

                        content = detail_html.xpath(
                            f'//div[@class="related_info"]/div[@id="dir_{book_id}_full"]')
                        if content:
                            content = content[0].xpath('string(.)')
                        else:
                            content = detail_html.xpath(
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

                            print(f'{tag}:{book_id} {next_url} 保存完成')
                            time.sleep(random.randint(3, 5))
                        else:
                            print(f'已存在，跳过 {tag}:{book_id}  {book_name} {next_url}')
                            continue
                    except:
                        url = False
                if next_url:
                    next_url = base_url + next_url[0]
                    url = next_url
                    time.sleep(random.randint(10, 15))
                else:
                    url = False
            # else:
            #     url = False
