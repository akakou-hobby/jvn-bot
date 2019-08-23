#!/usr/bin/env python3
'''admonitor

MyJVNからアラートをとってきて、Slackに送信する。
'''

__author__  = 'Kosei Akama'
__version__ = '0.1'
__date__    = '2018/08/21'


import json

import requests
import feedparser

import settings


URL = 'https://jvndb.jvn.jp/ja/rss/jvndb_new.rdf'


def send_webhook(data):
    '''WEB HOOKを送信する'''
    requests.post(settings.WEB_HOOK_URL, data=json.dumps(data))

def get_rss():
    return feedparser.parse(URL)


if __name__=='__main__':
    # send_webhook({
    #     'text': u'Hello, World!',
    #     'link_names': 1
    # })

    rss = get_rss()
    index = 0
    print(rss['entries'][index]['title'])

    print(rss['entries'][index]['sec_cpe']['vendor'])
    print(rss['entries'][index]['sec_cpe']['product'])
    print(rss['entries'][index]['sec_cvss']['severity'])
    print(rss['entries'][index]['sec_cvss']['score'])
    print(rss['entries'][index]['link'])
    print(rss['entries'][index]['summary'])
