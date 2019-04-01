#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
from BaseUtil.LogUtil import *


# 获取用户id
def getUserId(telno):
    url = 'http://10.100.1.1:9007/u/Param'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "telNo": telno,
    }
    newdata = json.dumps(data)
    results = requests.post(url, data=newdata, headers=headers)
    try:
        s = json.loads(results.text)
        userId = s['userId']
        return userId
    except:
        return None


# 清空缓存
def clearCache(key):
    url = 'http://10.100.1.1:4055/project/'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {"Ip": "127.0.0.1", "SystemName": "Android", "Token": "", "UserId": "", "MethodName": "home",
            "Data": "{\"Type\":\"0\",\"IsAutoTranLow\":\"0\",\"field\":\"\",\"Key\":\"" + key + "\",\"NewPath\":\"\",\"ApplicationName\":\"\",\"Value\":\"\"}"}
    newdata = json.dumps(data)
    results = requests.post(url, data=newdata, headers=headers)
    s = json.loads(results.text)
    ReturnMessage = s["Message"]
    loggerInfo(ReturnMessage)
