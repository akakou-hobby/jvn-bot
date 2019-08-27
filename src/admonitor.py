#!/usr/bin/env python3
'''admonitor

MyJVNからアラートをとってきて、Slackに送信する
'''

__author__  = 'Kosei Akama'
__version__ = '0.1'
__date__    = '2018/08/21'


import sys
import time
import json
import textwrap
import traceback
from datetime import datetime

import feedparser
from slack import WebClient as SlackClient

import settings
from model import session, Condition


ALERT_CHANNEL = 'alert'
RSS_URL = 'http://localhost:8000/main.rdf'

SLEEP = 10


sc = SlackClient(settings.CLIENT_TOKEN)

class VulnInfo:
    '''脆弱性情報'''
    def __init__(self, rss_entry):
        '''RSSのEntryから、オブジェクトを生成'''
        self.title = rss_entry['title']
        self.summary = rss_entry['summary']

        self.vendor = rss_entry['sec_cpe']['vendor']
        self.product = rss_entry['sec_cpe']['product']
        
        self.severity = rss_entry['sec_cvss']['severity']
        str_cvss = rss_entry['sec_cvss']['score']
        self.cvss = float(str_cvss)

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
        self.last_time = datetime.fromtimestamp(now)
        # self.last_time = datetime.fromtimestamp(0)
        self.last_id = ''
    
    def read_feed(self):
        '''RSSフィードをとってくるジェネレーター'''
        while True:
            feeds = feedparser.parse(RSS_URL)
            time.sleep(SLEEP)

            for entry in self.split_updated(feeds):
                yield VulnInfo(entry)
            
            print('loop')

    def split_updated(self, feeds):
        entries = feeds['entries']

        for entry in entries[::-1]:
            str_time = entry['published']
            published_time = datetime.strptime(str_time, '%Y-%m-%dT%H:%M+09:00')
            _id = entry['id']

            if self.last_time <= published_time and self.last_id != _id:
                self.last_time = published_time
                self.last_id = _id
                yield entry


def main():
    '''メイン関数'''
    rss = VulnInfoRSS()
    conditions = session.query(Condition).all()

    for vuln in rss.read_feed():
        channels = []

        for condition in conditions:
            if condition.hit(vuln):
                channels.append(condition.channel)

        channels = list(set(channels))

        for channel in channels:
            sc.chat_postMessage(
                channel=channel,
                text=str(vuln)
            )
            time.sleep(SLEEP)


if __name__=='__main__':
    try:
       main()
    except:
        error = traceback.format_exc()

        sc.chat_postMessage(
            channel=ALERT_CHANNEL,
            text=error
        )

        print(error, file=sys.stderr)