#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import configparser


# 读取ini配置文件字段值
def readConfig(param):
    filePath = os.path.join(os.path.dirname(__file__), '../behave.ini')
    file = os.path.abspath(filePath)
    conf = configparser.ConfigParser()
    conf.read(file)
    name = conf.get("config", param)
    print(name)
    return name

