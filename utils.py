import random
import time
from urllib.request import urlretrieve
from conf import CUSTOM_USER_AGENT
import requests
from lxml import etree


def get_ua():
    return random.choice(CUSTOM_USER_AGENT)


headers = {
    "User-Agent": get_ua()
}


def set_headers():
    return {"User-Agent": random.choice(CUSTOM_USER_AGENT)}


def get_proxy(api_url):
    r = requests.get(api_url)

    return r.json().get("proxy")


def delete_proxy(proxy):
    requests.get(f'http://127.0.0.1:5010/delete/?proxy={proxy}')


def download_img(url, book_id, tag):
    suffix = url.split('.')[-1]
    r = requests.get(url).content

    if not r:
        print('下载错误', tag, book_id, url)
        time.sleep(5)
        r = requests.get(url, headers=headers).content
        with open(f'{tag}/{book_id}.{suffix}', 'wb') as f:
            f.write(r)
    else:
        with open(f'{tag}/{book_id}.{suffix}', 'wb') as f:
            f.write(r)


api_url = 'http://127.0.0.1:5010/get/'
IP_POOL = []


def set_proxy():
    if len(IP_POOL) == 0:
        # url = 'http://dps.kdlapi.com/api/getdps/?orderid=949966318479162&num=10&pt=1&dedup=1&sep=2'
        appcode = '3c1f510aad8b41fc9af31e0c4ad47420'
        url = 'http://zip.market.alicloudapi.com/devtoolservice/ipagency?foreigntype=0&protocol=1'
        header = {
            'Authorization': 'APPCODE ' + appcode
        }

        r = requests.get(url=url, headers=header, timeout=10).json()
        ip_list = r.get('result')
        for ip in ip_list:
            ip = ip.split('/')[-1]
            IP_POOL.append(ip.strip())
    print(IP_POOL)
    return random.choice(IP_POOL)


def request_url(url):
    while True:
        ip = get_proxy(api_url)
        proxy = {
            'https': 'https://' + ip,
            # 'http': 'http://' + ip
        }
        try:
            res = requests.get(url, headers=set_headers(), proxies=proxy, timeout=30)
            # html = etree.HTML(res.text)
            # if url.find('subject') != -1:
            #     book_name_main = html.xpath('//div[@id="wrapper"]/h1/span/text()')[0]
            if res.status_code == 200:
                return res
            # IP_POOL.remove(ip)
            continue
        except Exception as e:
            print(f'IP:{ip} 请求出错')
            # IP_POOL.remove(ip)
            continue


def parse_detail(url):
    while True:
        ip = set_proxy()
        proxy = {
            'https': 'https://' + ip,
            # 'http': 'http://' + ip
        }
        try:
            res = requests.get(url, headers=set_headers(), proxies=proxy, timeout=20)
            if res.status_code == 200:
                return res
            IP_POOL.remove(ip)
            continue
        except Exception as e:
            print(f'解析详情页 IP:{ip} 请求出错')
            IP_POOL.remove(ip)
            continue


def request_url_list(url):

    ip = set_proxy()
    proxy = {
        'https': 'https://' + ip,
        # 'http': 'http://' + ip
    }
    try:
        res = requests.get(url, headers=set_headers(), proxies=proxy, timeout=30)
        # res = requests.get(url, headers=set_headers(), timeout=30)
    except Exception as e:
        print(f'IP:{ip} 请求出错 换个ip再次请求')
        IP_POOL.remove(ip)
        res = request_url_list(url)
    return res



if __name__ == '__main__':
    download_img('https://img1.doubanio.com/view/subject/s/public/s24514468.jpg', '100033')
