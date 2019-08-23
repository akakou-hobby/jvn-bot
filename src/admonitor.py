#!/usr/bin/env python3
'''admonitor

MyJVNからアラートをとってきて、Slackに送信する
'''

__author__  = 'Kosei Akama'
__version__ = '0.1'
__date__    = '2018/08/21'


import json
import time
import textwrap
from datetime import datetime

import requests
import feedparser

import settings


RSS_URL = 'https://jvndb.jvn.jp/ja/rss/jvndb_new.rdf'
SLEEP = 3


class VulnInfo:
    '''脆弱性情報'''
    def __init__(self, rss_entry):
        '''RSSのEntryから、オブジェクトを生成'''
        self.title = rss_entry['title']
        self.summary = rss_entry['summary']

        self.vendor = rss_entry['sec_cpe']['vendor']
        self.product = rss_entry['sec_cpe']['product']
        
        self.severity = rss_entry['sec_cvss']['severity']
        self.cvss = rss_entry['sec_cvss']['score']

        self.link = rss_entry['link']
    
    def __str__(self):
        '''メッセージを生成する。'''
        msg = f'''
            *{self.title}* 
            {self.summary}

            *製品情報*
            ベンダー名：{self.vendor}
            製品名：{self.product}
            
            *緊急度*
            緊急度：{self.severity}
            CVSS：{self.cvss}

            {self.link}
            '''

        msg = msg.replace('  ', '')
        return msg


class VulnInfoRSS:
    def __init__(self):
        now = time.time()
        # self.last_time = datetime.fromtimestamp(now)
        self.last_time = datetime.fromtimestamp(0)
        self.last_id = ''
    
    def feed(self):
        '''RSSフィードをとってくるジェネレーター'''
        while True:
            feeds = feedparser.parse(RSS_URL)
            entries = feeds['entries']

            time.sleep(SLEEP)

            for entry in entries[::-1]:
                str_time = entry['published']
                published_time = datetime.strptime(str_time, '%Y-%m-%dT%H:%M+09:00')

                if self.last_time <= published_time and self.last_id != entry['id']:
                    # TODO: ここの条件を見直し
                    self.last_time = published_time
                    self.last_id = entry['id']
                    yield VulnInfo(entry)


def send_webhook(data):
    '''WEB HOOKを送信する'''
    requests.post(settings.WEB_HOOK_URL, data=json.dumps(data))

def main():
    '''メイン関数'''
    rss = VulnInfoRSS()

    for vuln in rss.feed():
        time.sleep(5)
        print(vuln)

        send_webhook({
            'text': str(vuln),
            'link_names': 1
        })


if __name__=='__main__':
    main()