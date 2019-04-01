#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import pandas
sys.path.append("..")
from BaseUtil.LogUtil import *
from BaseUtil import Globalvar as gl
gl._init()


# 获取一级目录
def getPage(ModeName):
    filePath = os.path.join(os.path.dirname(__file__), '../CsvFile/Main.csv')
    file = os.path.abspath(filePath)
    try:
        data = pandas.read_csv(file, encoding='gbk')
        # data['ModeName'] 一列数据
        # data.ix[0, :] 一行数据
        # data.ix[0, :]['Package'] 一行的指定数据
        # print(data.values)[ModeName Package PageName]
        for s in data.values:
            if s[0] == ModeName:
                page = s[1] + '/' + s[2]
                return page
    except Exception as e:
        loggerError(e)


# 分发Android与ios获取元素
def getElement(ModeName, Element):
    page = getPage(ModeName)
    filePath = os.path.join(os.path.dirname(__file__), '../CsvFile/' + page + '.csv')
    file = os.path.abspath(filePath)
    element = []
    try:
        data = pandas.read_csv(file, encoding='gbk')
        # [Name  AndroidLocation AndroidElement IOSLocation IOSElement]
        for s in data.values:
            if s[0] == Element:
                if gl.get_value('platformName') == 'Android':
                    if gl.get_value('platformVersion') == '4.4.4' or gl.get_value('platformVersion') == '4.4':
                        if s[1] == 'android_uiautomator':
                            s[1] = 'xpath'
                            new_s = s[2][6:-2]
                            new_ele = """//android.widget.TextView[@text='{0}']""".format(new_s)
                            s[2] = new_ele
                    element.append(s[1])
                    element.append(s[2])
                    element.append(s[0])
                    return element
                elif gl.get_value('platformName') == 'ios':
                    element.append(s[3])
                    element.append(s[4])
                    element.append(s[0])
                    return element
    except Exception as e:
        loggerError(e)

