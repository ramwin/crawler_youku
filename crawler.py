#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-03-18 18:00:46


import logging
import time, requests

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='./log/log.log',
                filemode='w')
    
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')

def crawl_web(url):
    ''' 输入: url 
        输出: html'''

def create_url(word):
    ''' 输入: 节目名称, <string>;
        输出: url, <http://index.youku.com/kw=xxxx>
        '''
def convert_data(html):
    state = authenticate(html)
    if state:
        
    else:
        return None

def authenticate(html):
    ''' 输入: html;
        输出: True or False
            判断数据是否和预想的一致'''
    
def get_data(word):
    ''' 输入: 节目名称, string;
        输出: {
            'search': [ # 搜索指数
                ['2016-03-17', 24551],
                ['2016-03-18', 23333],
                ...
            ],
            'vv': [ # 播放指数
                ['2016-03-17', 8413],
                ['2016-03-18', 8413],
            ]
        }
    '''
    url = create_url(word)
    text = crawl_web(url)
    data = convert_data(text)
    return data

def save_data(name, data):
    ''' 把爬取的数据保存下来 '''
def pop_name():
    ''' 每次输出一个需要的节目名字 
        output: <string>'''
def main():
    ''' 运行的函数 '''
    while True:
        time.sleep(60)
        name = pop_name()
        data = get_data(name)
        save(name, data)

if __name__ == '__main__':
    main()
