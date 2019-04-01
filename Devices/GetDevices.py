#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 获取STF空闲设备
import requests
import json
import sys
sys.path.append("..")
from BaseUtil.LogUtil import *
from Devices.DeviceRecord import *

url = 'http://10.100.1.1/api/v1/devices'
post_url = 'http://10.100.1.1/api/v1/user/devices'
token = '5fdf9ef731d847d9a9367ca878ebaa9f59ca71c8cbae44809342bfc9e349'
headers = {
    'Authorization': 'Bearer ' + token
}
post_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token

}


# 获取可用空闲的设备
def getDevices():
    result = requests.get(url, headers=headers)
    # print(result.text)
    s = json.loads(result.text)
    resu = s['success']
    listDevices = []
    if resu is not False:
        devices = s["devices"]
        num = 0
        for device in devices:
            # print(device["present"])
            # print(device["owner"])
            if device["present"] is True and device["owner"] is None:
                listDevices.append(device["serial"])
                num = num + 1
        if num == 0:
            listDevices = None
        return listDevices
    else:
        loggerError("连接STF失败！")
        return listDevices
    pass


# 获取单个可用设备的详细信息
def getDeviceInfo(serial):
    uri = url + '/' + serial
    result = requests.get(uri, headers=headers)
    s = json.loads(result.text)
    return s


# 连接设备
def connectDevice(serial):
    data = {"serial": serial}
    data = json.dumps(data)
    result = requests.post(post_url, data=data, headers=post_headers)
    s = json.loads(result.text)
    if s["success"] is True:
        uri = post_url + '/' + serial + '/remoteConnect'
        remote = requests.post(uri, headers=post_headers)
        remoteConnectUrl = json.loads(remote.text)
        saveRecord(serial)
        return remoteConnectUrl["remoteConnectUrl"]
    else:
        loggerError(serial+'设备连接失败')
        return None


# 断开设备
def deleteDevice(serial):
    uri = post_url + '/' + serial
    result = requests.delete(uri, headers=headers)
    result = json.loads(result.text)
    deleteRecord()
    if result["success"] is True:
        loggerInfo(serial+'设备断开连接成功')
    else:
        loggerError(serial+'设备断开连接失败')
