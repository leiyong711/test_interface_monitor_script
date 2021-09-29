# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: test_interface_monitor_script
# author: "Lei Yong"
# creation time: 2021-02-02 16:01
# Email: leiyong711@163.com


import json
import jsonschema
from utils.log import logger


def check_field(data, case_file_path):
    """
    json响应内容检测
    :param data:
    :param case_file_path:
    :return:验证结果, 失败原因
    """
    try:
        with open(case_file_path, 'r', encoding='utf8')as fp:
            schema = json.load(fp)
    except FileNotFoundError:
        logger.error(f"请填写正确的验证模型路径\n当前路径参数: {case_file_path}\n")
        raise FileNotFoundError("请填写正确的验证模型路径")
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, e
    except Exception as e:
        logger.error(f"json响应断言失败\n参数: {str(data)}\n断言模型: {case_file_path}\n原因: {e}\n")
        return True, None


if __name__ == '__main__':
    check_field({}, "../caseData/item.json")
