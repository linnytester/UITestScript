#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os


# 保存STF测试设备号到本地txt文件
def saveRecord(serial):
    fp = open("record.txt", "w")
    try:
        fp.write(serial)
        fp.write("\n")
    finally:
        fp.close()


# 删除本地txt文件
def deleteRecord():
    try:
        os.remove("record.txt")
    finally:
        return None


# 读取本地txt文件保存的设备号
def getRecord(dir):
    if os.path.exists(dir+"/record.txt"):
        fp = open(dir+"/record.txt", "r")
        try:
            serial = fp.read().strip()
            return serial
        finally:
            fp.close()
    else:
        return None
