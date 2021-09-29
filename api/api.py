# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: Interface_performance_monitoring_script
# author: "Lei Yong"
# creation time: 2021-02-02 15:55
# Email: leiyong711@163.com


import os
import time
import json
import requests
import datetime
import traceback
from utils import request
from utils.log import logger as lg
from utils.common import get_time, get_case_id
from urllib.parse import urlencode
from config.config import HOST_LIST, SERVER, TOKEN, PROJECT_VERSION
from utils.resultAassertion import check_field
from api.user_login import user_info
from functools import wraps


def check_resp(title, jsonpath):
    def check_resp(func):
        @wraps(func)
        def wappr(*args, **kwargs):
            r, resp_data = func(*args, **kwargs)
            try:
                if r:
                    status, err = check_field(r, jsonpath)
                    try:
                        if err:
                            lg.error(
                                f"\n{'-' * 25} {title} {'-' * 25}\n请求地址: {resp_data['url']}\n请求体: {resp_data['request_data']}\n请求头: {headers}\n错误信息: {r}\n{'-' * 50}\n"
                            )
                            resp_data["status"] = False
                            resp_data["response_time"] = -2
                            resp_data["response_data"] = json.dumps(r, ensure_ascii=False)
                            raise ValueError(f"{title}，校验不通过\n{err}")
                    except ValueError:
                        lg.error(f"{title}，校验不通过\n{traceback.format_exc()}")
            except Exception:
                lg.error(traceback.format_exc())
                e = traceback.format_exc()
                resp_data["status"] = False
                resp_data["response_time"] = -2
                resp_data["response_data"] = str(e)
                lg.error(e)

            return resp_data

        return wappr
    return check_resp


@check_resp("获取board页商品", "caseData/homepage_banner.json")
def get_board(board_id):
    """
    获取board页商品
    :param board:
    :return:
    """
    lg.info("获取board页商品...")
    url = f"{HOST}/api/v/{API_VERSION}/homepage/banner/{board_id}/items"
    region = headers["cm-user-region"]
    data = {"language": "en", "region": region, "mall_or_shop": False, "num_items": 20, "topItemIds": None}
    # params = urlencode(data)
    return request(url=url, data=data, headers=headers)


@check_resp('获取首页版本号', 'caseData/version.json')
def get_version():
    """
    获取首页版本号
    :return:
    """
    lg.info("获取首页版本号...")
    url = f"{HOST}/api/v/{API_VERSION}/homepage/version"
    region = headers["cm-user-region"]
    data = {"language": "en", "region": region}
    # params = urlencode(data)
    return request(url=url, data=data, headers=headers)


@check_resp('获取首页商品推荐', 'caseData/youmaylike.json')
def get_youmaylike():
    """
    获取首页商品推荐
    :return:
    """
    lg.info("获取首页商品推荐...")
    url = f"{HOST}/api/v/{API_VERSION}/listing/youmaylike"
    region = headers["cm-user-region"]
    data = {"language": "en", "region": region, "numItems": 20, "scrollId": None}
    # params = urlencode(data)
    return request(url=url, data=data, headers=headers)


@check_resp('获取DP页商品推荐', 'caseData/item_youmaylike.json')
def get_item_youmaylike(spu_id):
    """
    获取DP页商品推荐
    :param spuid:
    :return:
    """
    lg.info("获取DP页商品推荐...")
    url = f"{HOST}/api/v/{API_VERSION}/listing/item/{spu_id}/youmaylike"
    region = headers["cm-user-region"]
    data = {"language": "en", "region": region, "page": 0, "limit": 20, "scrollId": None}
    # params = urlencode(data)
    return request(url=url, data=data, headers=headers)


@check_resp('获取商品详情', 'caseData/item.json')
def get_item(spu_id):
    """
    获取商品详情
    :param spu_id:
    :return:
    """

    lg.info("获取商品详情...")
    url = f"{HOST}/api/v/{API_VERSION}/content/item/{spu_id}"
    region = headers["cm-user-region"]
    data = {
        "language": "en",
        "region": region,
        "client": f"web_{API_VERSION}",
        # "callback": "jsonp_0"
    }
    # params = urlencode(data)
    return request(url=url, data=data, headers=headers)


def get_price_api(spu_id):
    """
    获取商品 SKU 价格
    :param spu_id:
    :return:
    """
    try:
        lg.info("获取商品 SKU 价格...")
        url = f"{HOST}/api/v/{API_VERSION}/price-api/item/{spu_id}/full"
        region = headers["cm-user-region"]
        data = {"language": "en", "region": region}
        # params = urlencode(data)
        r, resp_data = request(url=url, data=data, headers=headers)
        if r:
            status, err = check_field(r, "caseData/price_api.json")
            try:
                if err:
                    lg.error(
                        f"\n{'-' * 25} 获取商品 SKU 价格 {'-' * 25}\n请求地址: {url}\n请求体: {data}\n请求头: {headers}\n错误信息: {r}\n{'-' * 50}\n"
                    )
                    resp_data["status"] = False
                    resp_data["response_time"] = -2
                    resp_data["response_data"] = json.dumps(r, ensure_ascii=False)
                    raise ValueError(f"获取商品 SKU 价格，校验不通过\n{err}")
            except ValueError:
                lg.error(traceback.format_exc())
        return resp_data, r
    except Exception:
        e = traceback.format_exc()
        resp_data["status"] = False
        resp_data["response_time"] = -2
        resp_data["response_data"] = str(e)
        lg.error(e)
        return resp_data, ""


def get_cart_api_update(sku, count=1):
    """
    添加购物车
    :param sku:
    :param count:
    :return:
    """
    try:
        lg.info("添加购物车...")
        url = f"{HOST}/api/v/{API_VERSION}/cart-api/update"

        data = {"update_info": {sku: count}}
        r, resp_data = request(url=url, method="POST", data=data, headers=headers)
    except Exception:
        e = traceback.format_exc()
        resp_data["status"] = False
        resp_data["response_time"] = -2
        resp_data["response_data"] = str(e)
        lg.error(e)
    return resp_data


@check_resp('统计商品价格', 'caseData/shopping_cal_price.json')
def get_shopping_cal_price(spu, sku, count=1):
    """
    统计商品价格
    :param spu:
    :param sku:
    :param count:
    :return:
    """
    lg.info("统计商品价格...")
    url = f"{HOST}/api/v/{API_VERSION}/shopping/cal_price/v4_4"

    data = {
        "entries": [f"{spu}-{sku}-{count}"],
        "mall_channels": {},
        "coupon_code": "",
        "auto_select_coupon": False,
        "cash": 0,
    }
    return request(url=url, method="POST", data=data, headers=headers)


@check_resp('匿名用户创建订单', 'caseData/order.json')
def place_order_for_guest(spu, sku, count=1):
    """
    匿名用户创建订单
    :param spu:
    :param sku:
    :param count:
    :return:
    """
    lg.info("匿名用户创建订单...")
    url = f"{HOST}/api/v/{API_VERSION}/order-api/place_order_for_guest"
    region = headers["cm-user-region"]
    data = {
        "address": {
            "receiver": "test",
            "mobileNumber": "17620320647",
            "street": "test",
            "street2": "test",
            "city": "td",
            "province": "Colorado",
            "email": "23@163.com",
            "regionCode": region,
            "id": "",
            "updateTime": f"{datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        },
        "email": "23@163.com",
        "entries": [f"{spu}-{sku}-{count}"],
        "mall_channels": {"taobao": f"CN-{region}-PRI-LINE"},
        "no_remove_from_cart": True,
        "onesignal_id": "",
        "couponCode": "",
    }

    if region == "GB":
        data.update({"postcode": "11111-1111"})
    elif region == "US":
        data.update({"postcode": "gd233we"})
    return request(url=url, method="POST", data=data, headers=headers)


def entries(spu, sku, user_anonymous, user_name, password="LEIyong711", count=1):
    """
    登录用户创建订单
    :param spu:
    :param sku:
    :param count:
    :return:
    """
    try:
        lg.info("登录用户创建订单...")
        url = f"{HOST}/api/v/{API_VERSION}/shopping/cart/checkout/entries"

        # 用户登录获取token
        user_id, user_token, addresses = user_info(user_name, password, API_VERSION)

        region = headers["cm-user-region"]
        header = headers.copy()
        header.update(
            {
                "x-cloudmall-access-token": user_token,
                "x-cloudmall-anonymous-user-key": user_anonymous,
                "userid": user_id,
            }
        )

        data = {
            "entries": [f"{spu}-{sku}-{count}"],
            "addr_id": addresses[region],
            "mall_channels": {"taobao": f"CN-{region}-PRI-LINE"},
            "coupon_code": "",
            "no_remove_from_cart": True,
            "cash": 0,
        }

        r, resp_data = request(url=url, method="POST", data=data, headers=header)
        # print(f"\n{'-' * 25} 登录用户下单 {'-' * 25}\n请求地址: {url}\n请求体: {data}\n请求头: {header}\n错误信息: {r}\n{'-' * 50}\n")
        if r:
            status, err = check_field(r, "caseData/user_order.json")
            try:
                if err:
                    lg.error(
                        f"\n{'-' * 25} 登录用户创建订单 {'-' * 25}\n请求地址: {url}\n请求体: {data}\n请求头: {header}\n错误信息: {r}\n{'-' * 50}\n"
                    )
                    resp_data["status"] = False
                    resp_data["response_time"] = -2
                    resp_data["response_data"] = json.dumps(r, ensure_ascii=False)
                    raise ValueError(f"用户创建订单，校验不通过\n{err}")
                return user_id, user_token, resp_data, r["data"]["order"]["short_id"]
            except ValueError:
                lg.error(traceback.format_exc())
        return user_id, user_token, resp_data, None
    except Exception:
        e = traceback.format_exc()
        resp_data["status"] = False
        resp_data["response_time"] = -2
        resp_data["response_data"] = str(e)
        lg.error(e)
        return None, None, resp_data, None


@check_resp('取消订单', 'caseData/cancel_order.json')
def order_api_cancel(user_id, user_token, order_id, user_anonymous):
    """
    取消订单
    :param order_id:
    :return:
    """
    lg.info("取消订单...")
    url = f"{HOST}/api/v/{API_VERSION}/order-api/cancel"

    header = headers.copy()
    header.update(
        {
            "x-cloudmall-access-token": user_token,
            "x-cloudmall-anonymous-user-key": user_anonymous,
            "userid": user_id,
        }
    )

    data = {"orderId": order_id, "cancelReason": "性能监控-测试单"}
    return request(url=url, method="POST", data=data, headers=header)


@check_resp('删除订单', 'caseData/cancel_order.json')
def order_api_delete(user_id, user_token, order_id, user_anonymous):
    """
    删除订单
    :param order_id:
    :return:
    """
    lg.info("删除订单...")
    url = f"{HOST}/api/v/{API_VERSION}/order-api/delete"

    header = headers.copy()
    header.update(
        {
            "x-cloudmall-access-token": user_token,
            "x-cloudmall-anonymous-user-key": user_anonymous,
            "userid": user_id,
        }
    )

    data = {"orderId": order_id}
    return request(url=url, method="POST", data=data, headers=header)


def case(spu_id, board_id, user_anonymous, user_name, password):
    temp = []

    # 获取board页商品
    resp_data = get_board(board_id)
    resp_data["title"] = "获取board页商品"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    # 获取首页版本号
    resp_data = get_version()
    resp_data["title"] = "获取首页版本号"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    # 获取首页商品推荐
    resp_data = get_youmaylike()
    resp_data["title"] = "获取首页商品推荐"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    # 获取DP页商品推荐
    resp_data = get_item_youmaylike(spu_id)
    resp_data["title"] = "获取DP页商品推荐"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    # 获取商品详情页
    resp_data = get_item(spu_id)
    resp_data["title"] = "获取商品详情页"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    # 获取商品SKU价格
    resp_data, price_list = get_price_api(spu_id)
    resp_data["title"] = "获取商品SPU价格"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    try:
        sku_id = [key for key, value in price_list["sku_prices"].items()][0]
    except Exception:
        sku_id = "99017575"

    # 添加购物车
    resp_data = get_cart_api_update(sku_id)
    resp_data["title"] = "添加购物车"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    # 统计商品价格
    resp_data = get_shopping_cal_price(spu_id, sku_id)
    resp_data["title"] = "统计商品价格"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    # 只监控以下版本接口
    if API_VERSION in ['5.7.0', '5.8.0', '5.8.3', '5.10.0']:
        # 匿名用户创建订单
        resp_data = place_order_for_guest(spu_id, sku_id)
        resp_data["title"] = "匿名用户创建订单"
        resp_data["start_time"] = get_time()
        temp.append(resp_data)

    # 登录用户创建订单
    user_id, user_token, resp_data, order_id = entries(spu_id, sku_id, user_anonymous, user_name, password)
    resp_data["title"] = "登录用户创建订单"
    resp_data["start_time"] = get_time()
    temp.append(resp_data)

    if order_id:
        time.sleep(3)
        # 取消订单
        resp_data = order_api_cancel(user_id, user_token, order_id, user_anonymous)
        resp_data["title"] = "取消订单"
        resp_data["start_time"] = get_time()
        temp.append(resp_data)

        # 删除订单
        resp_data = order_api_delete(user_id, user_token, order_id, user_anonymous)
        resp_data["title"] = "删除订单"
        resp_data["start_time"] = get_time()
        temp.append(resp_data)

    return temp


def add_data(proxy, data):
    """
    提交测试结果到数据库
    :param host:
    :param port:
    :param data:
    :return:
    """
    header = {"X-Token": TOKEN}
    # 代理IP
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy,
        }
    if not proxy:
        resp = requests.post(f'{SERVER}/monitor-interface-service/api/add_test_report', json=data, headers=header)
    else:
        resp = requests.post(f'{SERVER}/monitor-interface-service/api/add_test_report', json=data, headers=header, proxies=proxies)
    lg.warning(resp)
    try:
        resp = resp.json()
    except Exception:
        lg.error(f"序列化错误: {resp.text}")
    if resp["code"] == 2000 and resp["status"]:
        return True
    lg.error("回传测试结果数据失败")
    return False


def start_test(proxy, count, node):
    # 代理IP
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy,
        }

    # 用户所在地
    if node in ["US-West", "US-East"]:
        region = "US"
    elif node in "UK":
        region = "GB"
    else:
        region = "US"

    # # 是否统计新老专线差异
    # if node != "US-West":
    #     host_list = ["https://web.cloudmall.co"]
    # else:
    #     host_list = HOST_LIST
    host_list = HOST_LIST

    try:
        if not proxy:
            resp = requests.get(url=f"{SERVER}/monitor-interface-service/api/test").json()
        else:
            resp = requests.get(url=f"{SERVER}/monitor-interface-service/api/test", proxies=proxies).json()

        if resp["code"] == 2000 and resp["status"] and resp["data"]:
            temp = []
            lg.info(f"域名: {host_list}")
            lg.info(f"获取配置信息: {resp}")

            data = resp["data"]

            # 全局headers
            global headers
            headers = {
                "cm-client": "",
                "x-cloudmall-anonymous-user-key": resp["data"]['anonymous'],
                "x-cloudmall-user-region": region,
                "cm-user-region": region,
                "cm-user-language": "en",
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            }

            # 登录用户信息获取
            user_anonymous = data['user_anonymous']  # 登录用户匿名id
            user_name = data['user_name']
            password = data['user_passwd']

            if resp["data"]['api_version']:
                for host in host_list:
                    global HOST
                    HOST = host

                    # 遍历测试所有版本接口
                    for version in data["api_version"]:

                        # 设置全局请求头版本
                        global API_VERSION
                        API_VERSION = version
                        headers["cm-client"] = f"web_{version}"

                        case_list_data = []
                        for i in range(count):
                            case_list_data.append(
                                case(spu_id=data["spu_id"],
                                     board_id=data["board_id"],
                                     user_anonymous=user_anonymous,
                                     user_name=user_name,
                                     password=password
                                     )
                            )
                        temp.append({"version": version, "batch": PROJECT_VERSION, "caseList": case_list_data})
                data = {"node": node, "data": temp}
                for i in range(3):
                    try:
                        send_status = add_data(proxy, data)
                        if send_status:
                            lg.info("回传数据成功")
                            return
                    except Exception:
                        lg.error(f"回传测试结果数据错误，原因: {traceback.format_exc()}")
                lg.error(f"连续3次回传测试结果数据失败")
    except Exception:
        lg.error(f"回传测试网络不通，原因: {traceback.format_exc()}")

