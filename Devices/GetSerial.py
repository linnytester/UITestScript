#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import sys

sys.path.append("..")
from Devices.GetDevices import *


def getSerial():
    while True:
        list = getDevices()
        if list is not None:
            # print('已获取可用测试设备')
            # print('Device：' + list[0])
            serial = list[0]
            break
        else:
            # print('正在获取可用测试设备，30S后重试')
            time.sleep(30)
    return serial
