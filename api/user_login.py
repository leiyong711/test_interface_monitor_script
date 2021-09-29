# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: test_interface_monitor_script
# author: "Lei Yong"
# creation time: 2021-04-02 11:41
# Email: leiyong711@163.com

import requests


def verifyPassword(email, passwd):
    url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCmxqktAXuErhx7I_tu68JKoqBNdENl6kQ'
    data = {
        "email": email,
        "password": passwd,
        "returnSecureToken": True
    }
    resp = requests.post(url=url, json=data).json()
    if resp['idToken']:
        return resp['idToken'], resp['refreshToken']


def getAccountinfo(idToken):
    url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key=AIzaSyCmxqktAXuErhx7I_tu68JKoqBNdENl6kQ'
    data = {"idToken": idToken}
    resp = requests.post(url=url, json=data).json()
    # print(resp)


def get_token(refresh_token):
    url = 'https://securetoken.googleapis.com/v1/token?key=AIzaSyCmxqktAXuErhx7I_tu68JKoqBNdENl6kQ'
    payload = f'grant_type=refresh_token&refresh_token={refresh_token}'
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    resp = requests.post(url=url, data=payload, headers=headers).json()
    if resp['id_token']:
        return resp['id_token']


def login(id_token, version):
    """登录"""
    url = f'https://web.cloudmall.co/api/v/{version}/user-api/login'
    data = {"firebase_token": id_token}
    resp = requests.post(url=url, json=data).json()
    if resp['user']:
        user_id = resp['user']['id']
        token = resp['token']
        return user_id, token
    return None, None


def get_addresses(user_id, token, version):
    url = f'https://web.cloudmall.co/api/v/{version}/address-api/addresses/list?language=zh-Hans&region=US'
    headers = {
        "userid": user_id,
        "cm-user-token": token
    }
    resp = requests.get(url=url, headers=headers).json()
    addresses = {i['region_code']: i['id'] for i in resp['addresses']}
    return addresses


def user_info(email, passwd, version):
    try:
        temp_token, refresh_token = verifyPassword(email, passwd)
        getAccountinfo(temp_token)
        id_token = get_token(refresh_token)
        user_id, token = login(id_token, version)
        addresses = get_addresses(user_id, token, version)
        return user_id, token, addresses
    except Exception:
        return None, None, None


if __name__ == '__main__':
    user_info('leiyongtest1@163.com', 'LEIyong711', '5.7.0')
