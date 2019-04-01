#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 全局变量


def _init():
    """
    初始化
    :rtype:
    """
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    """定义全局变量"""
    _global_dict[name] = value


def get_value(name, defValue=None):
    """获取变量值"""
    try:
        return _global_dict[name]
    except KeyError:
        return defValue
