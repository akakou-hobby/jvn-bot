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
        'Critical': 9.0,
        'High': 8.0,
        'Medium': 5.0,
        'Low': 2.0 
    }

    def __init__(self, text):
        self.vendor = ''
        self.product = ''
        self.cvss = ''

        text = text.replace(' ', '')

        for cmd in text.split(','):
            key, value = cmd.split(':')

            if key == 'vendor':
                self.vendor = value
            if key == 'product':
                self.product = value
            if key == 'cvss' and value.isdecimal():
                self.cvss = float(value)
            if key == 'severity':
                try:
                    self.cvss = self.matrix[value]
                except KeyError as e:
                    pass

        if not self.cvss:
            self.cvss = 0

    def generate_condition(self, channel):
        condition = Condition()
        condition.vendor = self.vendor
        condition.product = self.product
        condition.cvss = self.cvss
        condition.channel = channel

        return condition

@app.route(f'/add', methods=['POST'])
def add():
    '''スラッシュコマンドを受け取る'''
    token = request.form['token']
    text = request.form['text']
    channel = request.form['channel_name']

    if token == settings.SLASH_CMD_TOKEN:
        cmd = Command(text)
        condition = cmd.generate_condition(channel)

        session.add(condition)
        session.commit()

    return 'ok'

@app.route(f'/info', methods=['POST'])
def info():
    '''スラッシュコマンドを受け取る'''
    token = request.form['token']
    channel = request.form['channel_name']

    msg = ''

    if token == settings.SLASH_CMD_TOKEN:
        conditions = session.query(Condition) \
            .filter(Condition.channel == channel) \
            .all()
        

        for condition in conditions:
            msg += str(condition)

    if not msg:
        msg = "フィルタは見つかりませんでした。"

    return msg

@app.route(f'/del', methods=['POST'])
def delete():
    '''スラッシュコマンドを受け取る'''
    token = request.form['token']
    text = request.form['text']
    channel = request.form['channel_name']

    msg = 'failed'
    if token == settings.SLASH_CMD_TOKEN:
        if text.isdecimal():
            _id = int(text)
            condition = session.query(Condition) \
                .filter(Condition._id == _id, Condition.channel == channel)

            if condition:
                condition.delete()
                session.commit()
                msg = 'ok'
            else:
                msg = 'not found'

    return msg


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=False)
    app.run(host='0.0.0.0', port=80, debug=True)

