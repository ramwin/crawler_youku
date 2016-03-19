#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-03-19 16:47:46

import redis, sqlite3

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

global conn
conn = sqlite3.connect('crawler.db')

def wxprint(text):
    print(text)

class channel:
    def __init__(self,name):
        self.name = name
    def save(self):
        '''
            insert into channel (name) values ("冰与火之歌")
        '''
        global conn
        try:
            command = '''insert into channel (name) values ("%s");'''%(self.name)
            conn.execute(command)
        except Exception as e:
            wxprint(e)
            conn = sqlite3.connect('crawler.db')


def redis_to_sqlite(): # 把channel的名字输入sqlite
    global conn
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    namelist = map(lambda x: x.decode('utf8'), r.smembers('channelname'))
    for i in namelist:
        c = channel(i)
        c.save()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    redis_to_sqlite()
