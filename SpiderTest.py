from requests import ConnectTimeout

from utils import *

url = 'https://book.douban.com/subject/1046265/'

api_url = 'http://127.0.0.1:5010/get/'

if __name__ == '__main__':
    res = requests.get(url, headers=set_headers())
    print(res.headers)
    print(res.url)
    print(res.request)
    print(res.text)
    # res = request_url(url)
    # print(res.text)
    # print(res.status_code)
