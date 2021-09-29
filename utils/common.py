# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: test_interface_monitor_script
# author: "Lei Yong"
# creation time: 2021-02-02 18:58
# Email: leiyong711@163.com

import time
import uuid
import re
import json
import traceback
import urllib.parse as up
from utils.log import logger as lg


def get_time():
    "获取日期时间"
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_case_id():
    "生成用例id"
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    uid = f'{date}_{"".join(str(uuid.uuid4()).split("-")).upper()[:12]}'
    return uid


def request_to_curl(url, method, data, headers):
    """请求转curl"""
    format_ = ''  # '\\\n'
    try:
        curl = f"curl '{url}' {format_}"
        if method == 'GET' and data:
            curl = f"curl '{url}?{up.urlencode(data)}' {format_}"

        for k, v in headers.items():
            curl += f" -H '{k}: {v}' {format_}"

        if method == 'POST':
            try:
                curl += f" --data-raw '{json.dumps(data)}' {format_}"
            except:
                curl += f" --data-raw '{data}' {format_}"

        curl += " --compressed\n"
        return curl
    except:
        lg.error(f"request转curl失败,原因:\n{traceback.format_exc()}")
        return ''


def curl_to_request(curl):
    data = curl.split('\\\n')
    url = ''
    params = {}
    headers = {}
    method = 'GET'
    try:
        for i in data:
            if 'curl ' in i:
                url_ = re.findall(r"curl(.*?)'(.*?)'", i)
                if '?' in url_[0][1]:
                    for value in url_[0][1].split('?')[1].split("&"):
                        temp = value.split('=')
                        params.update({temp[0]: temp[1]})
                    url = url_[0][1].split('?')[0]
                else:
                    url = re.findall(r"curl(.*?)'(.*?)'", i)[0][1]
            if '-H ' in i:
                header_ = re.findall(r"-H '(.*?)'", i)[0]
                temp = header_.split(': ')
                headers.update({temp[0]: temp[1]})
            if '--data-raw ' in i:
                method = "POST"
                params_ = re.findall(r"'(.*?)'", i)[0]
                params = json.loads(params_)
    except:
        lg.error(f"curl转request失败,原因: \n{traceback.format_exc()}")
    finally:
        return url, method, params, headers
