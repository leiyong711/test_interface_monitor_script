# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: test_interface_monitor_script
# author: "Lei Yong"
# creation time: 2021-02-02 15:59
# Email: leiyong711@163.com

import json
import curlify
import requests
import traceback
from utils.log import logger as lg
from config.config import MAX_RESPONSE_TIME
from utils.common import request_to_curl


def request(url, method="GET", data={}, headers={}):
    """
    发送网络请求
    :param url:
    :param method:
    :param params:
    :param data:
    :param headers:
    :return:
    """
    curl = ''
    try:
        if method in "GET":
            resp = requests.get(url=url, params=data, headers=headers, timeout=MAX_RESPONSE_TIME)
        elif method in "POST":
            resp = requests.post(url=url, json=data, headers=headers, timeout=MAX_RESPONSE_TIME)
        curl = curlify.to_curl(resp.request)
        timer = int(resp.elapsed.total_seconds() * 1000)
        lg.info(f"url: {url}\t请求耗时: {timer} ms")

        if not curl:
            curl = request_to_curl(url=url, method=method, data=data, headers=headers)

        return resp.json(), {"url": url, "curl": curl, "request_data": json.dumps(data, ensure_ascii=False), "response_data": "", "method": method, "response_time": timer, "result_status": True}

    except json.JSONDecodeError:

        if not curl:
            curl = request_to_curl(url=url, method=method, data=data, headers=headers)

        lg.error(f'\n请求响应解析:\nURL: {url}\nData: {data}\nheaders: {headers}\n{traceback.format_exc()}\n')

        return None, {"url": url, "curl": curl, "request_data": json.dumps(data, ensure_ascii=False), "response_data": resp.text,
                      "method": method, "response_time": -2, "result_status": False}

    except Exception:

        if not curl:
            curl = request_to_curl(url=url, method=method, data=data, headers=headers)

        lg.error(f'\n发送请求失败:\nURL: {url}\nData: {data}\nheaders: {headers}\n{traceback.format_exc()}\n')

        return None, {"url": url, "curl": curl, "request_data": json.dumps(data, ensure_ascii=False), "response_data": str(traceback.format_exc()),
                      "method": method, "response_time": -1, "result_status": False}
