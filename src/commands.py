#!/usr/bin/env python3
'''commands

Slackのスラッシュコマンドを受け取って、フィルタリング情報を追加する。
'''

__author__  = 'Kosei Akama'
__version__ = '0.1'
__date__    = '2018/08/26'


from flask import Flask, render_template, request, redirect, url_for, Response
import json

import settings


app = Flask(__name__)

@app.route(f'/slash', methods=['POST'])
def index():
    '''スラッシュコマンドを受け取る'''
    token = request.form['token']
    text = request.form['text']

    if token == settings.SLASH_CMD_TOKEN:
        print(text)

    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
    # app.run(host='0.0.0.0', port=80, debug=True)