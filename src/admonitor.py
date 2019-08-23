#!/usr/bin/env python3
'''admonitor

MyJVNからアラートをとってきて、Slackに送信する
'''

__author__  = 'Kosei Akama'
__version__ = '0.1'
__date__    = '2018/08/21'


import json
import textwrap

import requests
import feedparser

import settings


URL = 'https://jvndb.jvn.jp/ja/rss/jvndb_new.rdf'


class VulnInfo:
    '''脆弱性情報'''
    def __init__(self, rss_entry):
        '''RSSのEntryから、オブジェクトを生成'''
        self.title = rss_entry['title']
        self.summary = rss_entry['summary']

        self.vendor = rss_entry['sec_cpe']['vendor']
        self.product = rss_entry['sec_cpe']['product']
        
        self.severity = rss_entry['sec_cvss']['severity']
        self.score = rss_entry['sec_cvss']['score']

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
            CVSS：{self.score}

            {self.link}
            '''

        return textwrap.dedent(msg)


def send_webhook(data):
    '''WEB HOOKを送信する'''
    requests.post(settings.WEB_HOOK_URL, data=json.dumps(data))

def get_rss():
    return feedparser.parse(URL)


if __name__=='__main__':
    rss = get_rss()
    index = 0

    vuln = VulnInfo(rss['entries'][index])

    send_webhook({
        'text': str(vuln),
        'link_names': 1
    })