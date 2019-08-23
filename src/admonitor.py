#!/usr/bin/env python3
'''admonitor

MyJVNからアラートをとってきて、Slackに送信する。
'''

__author__  = 'Kosei Akama'
__version__ = '0.1'
__date__    = '2018/08/21'


import requests
import json

import settings


def send_webhook(data):
    '''WEB HOOKを送信する'''
    requests.post(settings.WEB_HOOK_URL, data=json.dumps(data))


if __name__=='__main__':
    send_webhook({
        'text': u'Hello, World!',
        'link_names': 1
    })

