#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import sys
import json
sys.path.append("..")
from BaseUtil.LogUtil import *


# 查询测试设备占用情况
def checkDevice(device):
    url = """http://10.100.1.1:8899/select?device={0}""".format(device)
    respone = requests.get(url)
    loggerInfo(respone.text)
    result = json.loads(respone.text)
    return result


# 更新测试设备占用字段
def updateDevice(device, testing):
    url = """http://10.100.1.1:8899/update?device={0}&testing={1}""".format(device, testing)
    respone = requests.get(url)
    loggerInfo(respone.text)
    return respone.text


# 获取IOS可用测试设备
def getUseDevice(platform):
    url = """http://10.100.1.1:8899/getUse?platform={0}""".format(platform)
    respone = requests.get(url)
    loggerInfo(respone.text)
    result = json.loads(respone.text)
    return result


# 获取IOS可用测试设备
def getDevicesIsUse(platform):
    url = """http://10.100.1.1:8899/isUse?platform={0}""".format(platform)
    respone = requests.get(url)
    loggerInfo(respone.text)
    return respone.text


# 获取测试库手机号的最新验证码
def getRegisterCode(telno):
    get_url = """http://10.100.1.1:8999/Code.do?telno={0}""".format(telno)
    respone = requests.get(get_url)
    return respone.text


# 获取测试用户的身份证信息
def getUserIdentityCard(userId):
    get_url = """http://10.100.1.1:9002/user/{0}/realTime/info""".format(userId)
    results = requests.get(get_url)
    s = json.loads(results.text)
    identityCard = s['data']['identityCard']
    return identityCard

