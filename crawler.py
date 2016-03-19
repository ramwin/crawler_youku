#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-03-18 18:00:46


import logging
import time, requests, re, json, datetime
import redis
import base64

# Redis 数据库配置
REDIS_HOST = '192.168.1.111'
REDIS_PORT = 6379
REDIS_DB = 0
CHANNELNAME_DB = 'channelname'
CHANNELNAME_GOTTEN_DB = 'channelname:gotten'

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='./log/log.log',
                filemode='w')
    
logging.debug('记录debug')
logging.info('记录info')
logging.warning('记录warning')
logging.warning('爬虫脚本启动')

def wxprint(text):
    print(text)

def crawl_web(url):
    ''' 输入: url 
        输出:   
            成功: html
            失败: None'''
    logging.debug('crawl_web from {0}'.format(url))
    try:
        response = requests.get(url,timeout=10)
    except:
        logging.error('无法从服务器获取数据,url: {0}'.format(url))
        return None
    if response.status_code == 200:
        return response.text
    else:
        logging.error('爬取数据，服务器返回数据不是200, url: {0}'.format(url))
        return None

def create_url(word):
    ''' 输入: 节目名称, <string>;
        输出: url, <http://index.youku.com/kw=xxxx>
        '''
    logging.debug('create_url for {0}'.format(word))
    word = base64.encodebytes(word.encode('utf8'))
    word = word.replace(b'+',b'%252b')
    word = word.replace(b'=',b'%253d')
    word = word.replace(b'/',b'%252f').strip()
    url = 'http://index.youku.com/vr_keyword/id_' + word.decode('utf8') + "?type=alldata"
    return url

def parse_data(html):
    ''' 输入: html;
        输出: json解析后的data or None
            判断数据是否和预想的一致
        data格式: 
            [
                {
                    'name': '还珠格格',
                    'vv':
                    'search': [
                        '2016-03-17',
                        '2010-07-03',
                        [
                            '5167', # 2016-03-17 的搜索
                            '1789',
                            '1279',
                            ...
                            '4994', # 2010-07-03 的搜索
                        ]
                    ]
                }
            ]
        '''
    logging.debug('convert_data')
    pattern = re.compile(r"var allnetData = eval\('\('\+'([\s\S]+?)'\+'\)'\);")
    match = re.search(pattern,html)
    if match:
        logging.debug('match')
        try: 
            raw_data = match.groups()[0]
            data = json.loads(raw_data)
            return data
        except: 
            return None
    else: 
        logging.error('doesn\'t match')
        logging.error(html)
        return None

def convert_data(data):
    ''' 输入 json解析的data,
        输出 方便存储的data '''
    logging.debug('convert_data')
    data = data[0]
    if data['vv']: 
        data['vv'] = expand_data(data['vv'])
    if data['search']: 
        data['search'] = expand_data(data['search'])
    return data

def expand_data(data):
    ''' 输入 ['2015-03-17','2016-03-18',
                ['1556','456','456'...],
                ]
        输出 [
            ('2015-03-17','1556'),
            ('2015-03-18','7955'),
            ...
        ]
    '''
    range_list = date_range(data[0],data[1])
    result = []
    index = 0
    for i in range_list:
        result.append((i,data[2][index]))
        index += 1
    return result

def date_range(start,end):
    ''' 输入: '2015-03-17', '2016-03-17' # 输入datetime.date类型也可以
        # 如果是逆序的话就会导致输出结果也是逆序的
        输出: [
            '2015-03-17',
            '2015-03-18',
        ]
    '''
    result = []
    start_date = str_to_date(start) if isinstance(start, str) else start
    end_date = str_to_date(end) if isinstance(end, str) else end
    interval = (end_date-start_date).days
    step = 1 if interval > 0 else -1
    for i in range(0, interval+step, step):
        tmp_date = start_date + datetime.timedelta(i)
        result.append(tmp_date.strftime('%Y-%m-%d'))
    return result

def str_to_date(string):
    ''' 输入 '2015-03-17'
        输出 datetime.date(2015,03,17)'''
    return datetime.date(*list(map(int, re.search(r'^(\d+?)-(\d+?)-(\d+?)$',
                        string).groups())))

def get_data(word):
    ''' 输入: 节目名称, string;
        输出: {
            'search': [ # 搜索指数
                ['2016-03-17', '24551'],
                ['2016-03-18', '23333'],
                ...
            ],
            'vv': [ # 播放指数
                ['2016-03-17', '8413'],
                ['2016-03-18', '8413'],
            ],
            'name': '还珠格格',
        }
        失败则返回 None
    '''
    url = create_url(word)
    html = crawl_web(url)
    raw_data = parse_data(text)
    if raw_data:
        data = convert_data(data)
        return data
    else:
        logging.error('parse_data 失败')
        return None

def save_data(name, data):
    ''' 把爬取的数据保存下来 '''

def pop_name():
    ''' 每次输出一个需要的节目名字 
        output: <string>'''
    return True
    
def main():
    ''' 运行的函数 '''
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        name_map = map(lambda x: x.decode('utf8'), r.smembers('channelname'))
        name_gotten = map(lambda x: x.decode('utf8'), r.smembers('channelname:gotten'))
        name_failed = map(lambda x: x.decode('utf8'), r.smembers('channelname:failed'))
    except:
        logging.error('无法从数据库获取数据')
        return 0
    for i in name_map:
        if (not i in name_gotten) and (not i in name_failed):
            data = get_data(name)
            save(name, data)
            time.sleep(60)

def test():
    # url = create_url('还珠格格')
    # html = crawl_web(url)
    file = open('./html','r')
    html = file.read()
    raw_data = parse_data(html)
    data = convert_data(raw_data)
    print(data)

    
if __name__ == '__main__':
    test()
