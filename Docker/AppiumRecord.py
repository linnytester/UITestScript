#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os


# 保存STF测试设备号到本地txt文件
def saveRecord(port):
    fp = open("appium.txt", "w")
    try:
        fp.write(port)
        fp.write("\n")
    finally:
        fp.close()


# 删除本地txt文件
def deleteRecord():
    try:
        os.remove("appium.txt")
    finally:
        return None


# 读取本地txt文件保存的设备号
def getRecord(dir):
    if os.path.exists(dir+"/appium.txt"):
        fp = open(dir+"/appium.txt", "r")
        try:
            port = fp.read().strip()
            return port
        finally:
            fp.close()
    else:
        return None
