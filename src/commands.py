#!/usr/bin/env python3
'''commands

Slackのスラッシュコマンドを受け取って、フィルタリング情報を追加する。
'''

__author__  = 'Kosei Akama'
__version__ = '0.1'
__date__    = '2018/08/26'


from flask import Flask, render_template, request, redirect, url_for, Response
import json

from model import Condition, session
import settings


app = Flask(__name__)

class Command:
    # TODO: データ構造をもう一度考え直す
    # TODO: 調べて正しいものを設定
    matrix = {
        '緊急': 9.0,
        '高': 8.0,
        '中': 5.0,
        '低': 2.0 
    }

    def __init__(self, text):
        text = text.replace(' ', '')

        for cmd in text.split(','):
            key, value = cmd.split(":")

            if key == "vendor":
                self.vendor = value
            if key == "product":
                self.product = value
            if key == "cvss" and value.isdecimal():
                self.cvss = float(value)
            if key == "severity":
                try:
                    self.cvss = self.matrix[value]
                except KeyError as e:
                    pass

    def generate_condition(self, channel):
        condition = Condition()
        condition.vendor = self.vendor
        condition.product = self.product
        condition.cvss = self.cvss
        condition.channel = self.channel

        return condition

@app.route(f'/slash', methods=['POST'])
def index():
    '''スラッシュコマンドを受け取る'''
    token = request.form['token']
    text = request.form['text']

    if token == settings.SLASH_CMD_TOKEN:
        print(text)

    return 'ok'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=False)
    # app.run(host='0.0.0.0', port=80, debug=True)

    cmd = Command("vendor:MS, product:Office, severity:高")
    print((cmd.product, cmd.vendor, cmd.cvss))
    condition = cmd.generate_condition()

    session.add(condition)
    session.commit()
