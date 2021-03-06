#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:48
# @Author : way
# @Site :
# @Describe:

from data_db import SourceData
# from data import SourceData
from flask import Flask, render_template
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


app = Flask(__name__)

source = SourceData()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/os')
def os():
    data = source.os
    return render_template('os.html', title='用户系统分布', data=data, legend=[i.get('name') for i in data])


@app.route('/device')
def device():
    data = source.device
    return render_template('device.html', title='用户设备分布', data=data, legend=[i.get('name') for i in data])


@app.route('/browser')
def browser():
    data = source.browser
    return render_template('browser.html', title='用户浏览器分布', data=data, legend=[i.get('name') for i in data])


@app.route('/request')
def request():
    data = source.request
    xAxis = data.pop('legend')
    return render_template('request.html', title='网页接口访问情况', data=data, legend=list(data.keys()), xAxis=xAxis)


@app.route('/line')
def line():
    data = source.line
    xAxis = data.pop('legend')
    return render_template('line.html', title='24小时访问趋势', data=data, legend=list(data.keys()), xAxis=xAxis)


@app.route('/bar')
def bar():
    data = source.bar
    xAxis = data.pop('legend')
    return render_template('bar.html', title='每日访问情况', data=data, legend=list(data.keys()), xAxis=xAxis)


@app.route('/pie')
def pie():
    data = source.pie
    return render_template('pie.html', title='客户端设备占比', data=data, legend=[i.get('name') for i in data])


@app.route('/china')
def china():
    data = source.china
    return render_template('china.html', title='用户分布', data=data)


@app.route('/wordcloud')
def wordcloud():
    data = source.wordcloud
    return render_template('wordcloud.html', title='爬虫词云', data=data)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
