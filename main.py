# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: test_interface_monitor_script
# author: "Lei Yong"
# creation time: 2021-02-02 15:54
# Email: leiyong711@163.com

import sys
import getopt
import traceback
from utils.log import logger as lg
from api.api import start_test


def main(argv):
    node = 'UK'
    count = 2
    proxy = None  # 代理标志位
    try:
        opts, args = getopt.getopt(argv, "h:n:c:p:", ["node=", "count=", "proxy"])
    except getopt.GetoptError:
        print('main.py -p <proxy> -n <node> -c <count>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -p <proxy> -n <node> -c <count>')
        elif opt in ('-n', '--node'):
            node = arg
        elif opt in ('-c', '--count'):
            try:
                count = int(arg)
            except ValueError:
                lg.error(f"读取count参数异常:\n{traceback.format_exc()}")
        elif opt in ('-p', '--proxy'):
            proxy = arg
    lg.info(f'当前国家: {node}\t单接口执行次数: {count}\tproxy: {proxy}')
    start_test(proxy=proxy, count=count, node=node)


if __name__ == '__main__':
    main(sys.argv[1:])
