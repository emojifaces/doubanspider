import json

import requests

if __name__ == '__main__':
    # appcode = '3c1f510aad8b41fc9af31e0c4ad47420'
    # url = 'http://zip.market.alicloudapi.com/devtoolservice/ipagency?foreigntype=0&protocol=1'
    #
    # header = {
    #     'Authorization': 'APPCODE ' + appcode
    # }
    # r = requests.get(url=url, headers=header, timeout=10)
    # print(r)
    # data = json.loads(r.text)
    # print(data)
    # ip_list = data.get('result')
    # print(ip_list)
    # for ip in ip_list

    ip_list = ['http://103.212.92.241:38005', 'http://85.140.41.157:3128', 'http://81.174.11.227:47324',
               'http://103.15.167.35:41787', 'http://14.99.68.138:80', 'http://105.27.238.167:80',
               'http://195.154.165.153:3838', 'http://212.154.58.118:37470', 'http://162.243.175.14:80',
               'http://162.243.175.14:80', 'http://36.37.139.2:43997', 'http://103.75.34.121:54967',
               'http://54.38.155.94:6582', 'http://134.19.188.195:80', 'http://134.175.143.77:8118',
               'http://123.27.3.246:39915', 'http://162.144.61.12:3838', 'http://36.37.139.2:43997',
               'http://124.12.208.66:80', 'http://181.48.47.26:53281', 'http://114.39.7.40:80',
               'http://181.129.183.19:53281', 'http://168.181.134.119:40683', 'http://36.37.139.2:43997',
               'http://169.239.182.135:80', 'http://154.118.55.42:8768', 'http://191.233.194.1:3128',
               'http://103.6.104.105:38898', 'http://81.163.47.253:41258', 'http://91.193.253.188:23500',
               'http://114.45.27.167:80', 'http://54.38.155.94:6582', 'http://54.38.155.94:6582',
               'http://134.19.188.195:80', 'http://154.118.55.42:8768', 'http://177.139.176.242:65301',
               'http://14.99.68.143:80', 'http://181.48.47.26:53281', 'http://103.6.104.105:38898',
               'http://186.232.15.9:45849', 'http://105.27.238.167:80', 'http://103.75.34.121:54967',
               'http://163.172.226.90:3838', 'http://125.59.157.204:8197', 'http://114.39.106.99:80',
               'http://85.223.157.204:40329', 'http://117.102.119.150:47704', 'http://103.242.106.212:8080',
               'http://85.140.41.157:3128', 'http://105.27.237.26:80']

    for ip in ip_list:
        ip = ip.split('/')[-1]
        print(ip)