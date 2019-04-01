#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import time
import datetime
import random
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait

sys.path.append("..")
from BaseUtil.LogUtil import *
from BaseUtil.CsvUtil import *
from BaseUtil import Globalvar as gl
from appium import webdriver

gl._init()


# driver = webdriver.Remote()


# 查找元素
def findElement(driver, loc):
    if gl.get_value('platformName') == 'Android':
        element = waitElement(driver, loc[0], loc[1])
    elif gl.get_value('platformName') == 'ios':
        element = waitElement_ios(driver, loc[0], loc[1])
    if element is not None:
        loggerInfo('已找到元素-->[' + loc[2] + ']')
    else:
        loggerInfo('未找到元素-->[' + loc[2] + ']')
    return element


# 查找元素集
def findElements(driver, loc):
    # element = waitElements(driver, loc[0], loc[1])
    if gl.get_value('platformName') == 'Android':
        element = waitElements(driver, loc[0], loc[1])
    elif gl.get_value('platformName') == 'ios':
        element = waitElements_ios(driver, loc[0], loc[1])
    if element is not None:
        loggerInfo('已找到元素集-->[' + loc[2] + ']')
    else:
        loggerInfo('未找到元素集-->[' + loc[2] + ']')
    return element


# 判断元素是否存在
def isExistElement(driver, element):
    if findElement(driver, element) is None:
        if findElement(driver, getElement('弹窗', '弹窗提示')) is not None:
            if findElement(driver, getElement('弹窗', '确定')) is not None:
                findElement(driver, getElement('弹窗', '确定')).click()
            else:
                findElement(driver, getElement('弹窗', '取消')).click()
            if findElement(driver, element) is None:
                return False
            else:
                return True
        else:
            return False
    else:
        return True


# 点击操作
def click(self, loc):
    try:
        findElement(self, loc).click()
        loggerInfo('点击元素-->[' + loc[2] + ']')
    except:
        # 判断是否有弹出提示窗，若有则先点击关闭弹窗再进行一次点击操作
        if findElement(self, getElement('弹窗', '弹窗提示')) is not None:
            if findElement(self, getElement('弹窗', '确定')) is not None:
                findElement(self, getElement('弹窗', '确定')).click()
            else:
                findElement(self, getElement('弹窗', '取消')).click()
            findElement(self, loc).click()
            loggerInfo('点击元素-->[' + loc[2] + ']')
        elif findElement(self, getElement('启动页', '活动弹窗关闭按钮')) is not None:
            findElement(self, getElement('启动页', '活动弹窗关闭按钮')).click()
            findElement(self, loc).click()
            loggerInfo('点击元素-->[' + loc[2] + ']')
        else:
            loggerError(loc[2] + '->元素不存在，不可点击')
            assert findElement(self, loc) is not None, loc[2] + '->元素不存在，不可点击'


# 输入操作
def sendKeys(self, loc, str):
    loggerInfo('[' + loc[2] + ']-->输入内容：' + str)
    findElement(self, loc).send_keys(str)


# Android返回
def goBack(driver):
    driver.press_keycode(4)


# ios返回
def ios_goBack(driver):
    if findElement(driver, ['ios_predicate', 'label="back arrow"', '返回']) is not None:
        driver.find_element_by_ios_predicate('label="back arrow"').click()
        return True
    elif findElement(driver, ['ios_predicate', 'label="完成"', '完成按钮']) is not None:
        driver.find_element_by_ios_predicate('label="完成"').click()
        return True
    elif findElement(driver, ['ios_predicate', 'label="sign arrow white"', '签到返回']) is not None:
        driver.find_element_by_ios_predicate('label="sign arrow white"').click()
        return True
    elif findElement(driver, ['ios_predicate', 'label="wei close"', '关闭']) is not None:
        driver.find_element_by_ios_predicate('label="wei close"').click()
        return True
    elif findElement(driver, ['ios_predicate', 'name="iosHLcloseBtn"', '关闭按钮']) is not None:
        driver.find_element_by_ios_predicate('name="iosHLcloseBtn"').click()
        return True
    elif findElement(driver, ['id', 'iosHLcloseButton', '消息关闭']) is not None:
        driver.find_element_by_id('iosHLcloseButton').click()
        return True
    else:
        loggerError('ios返回按钮元素不存在')
        return False


# 清空
def clear(self, loc):
    findElement(self, loc).clear()


# 截图操作
def screen(self, fileName):
    self.save_screenshot(fileName)


# 获取元素的大小坐标
def getSize(driver):
    se = []
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    se.append(width)
    se.append(height)
    return se


# 滑动操作
def swipe(driver, fromx, fromy, tox, toy, times):
    try:
        driver.swipe(fromx, fromy, tox, toy, times)
    except Exception as e:
        loggerError('滑动失败')
        loggerError(e)


# 向上滑动屏幕
def swipeUp(driver, n=1):
    """向上滑动屏幕"""
    l = driver.get_window_size()
    x1 = l['width'] * 0.5  # x坐标
    y1 = l['height'] * 0.75  # 起始y坐标
    y2 = l['height'] * 0.25  # 终点y坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, 1000)


# 向下滑动屏幕
def swipeDown(driver, n=1):
    """向下滑动屏幕"""
    l = driver.get_window_size()
    x1 = l['width'] * 0.5  # x坐标
    y1 = l['height'] * 0.25  # 起始y坐标
    y2 = l['height'] * 0.75  # 终点y坐标
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, 1000)


# 向左滑动屏幕
def swipLeft(driver, n=1):
    """向左滑动屏幕"""
    l = driver.get_window_size()
    x1 = l['width'] * 0.75
    y1 = l['height'] * 0.5
    x2 = l['width'] * 0.25
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, 1000)


# 向右滑动屏幕
def swipRight(driver, n=1):
    """向右滑动屏幕"""
    l = driver.get_window_size()
    x1 = l['width'] * 0.25
    y1 = l['height'] * 0.5
    x2 = l['width'] * 0.75
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, 1000)


# 坐标点击
def clickByXY(driver, x, y):
    driver.tap([(x, y)], 500)


# 切换到WebView
def switchToWebView(driver):
    time.sleep(2)
    try:
        contexts = driver.contexts
        if 'WEBVIEW_stetho_com.junte' in contexts:
            contexts.remove('WEBVIEW_stetho_com.junte')
        driver._switch_to.context(contexts[1])
        loggerInfo(driver.current_context)
    except Exception as e:
        loggerError('切换WebView失败' + str(e))


# 获取WebView
def getWebView(driver):
    contexts = driver.contexts
    if 'WEBVIEW_stetho_com.junte' in contexts:
        contexts.remove('WEBVIEW_stetho_com.junte')
    if contexts[1] is not None:
        return True
    else:
        return False


# 切换到Native
def switchToNative(driver):
    time.sleep(2)
    try:
        contexts = driver.contexts
        driver._switch_to.context(contexts[0])
        loggerInfo(driver.current_context)
    except:
        loggerError('切换Native失败')


# 获取元素的文本
def getText(self, loc):
    loggerInfo('获取元素文本-->[' + loc[2] + ']')
    return findElement(self, loc).text


# 获取元素的文本集合
def getTexts(self, loc):
    element = []
    loggerInfo('获取元素文本-->[' + loc[2] + ']')
    ele = findElements(self, loc)
    if ele is not None:
        for i in ele:
            element.append(i.text)
        return element
    else:
        return None


# 截图操作
def takeScreen(self):
    nowTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filePath = './screens/ %s.png' % nowTime
    self.save_screenshot(filePath)


# 元素滑动操作
def ActionTouch(self, ele1, ele2, ele3):
    e1 = findElement(self, ele1)
    e2 = findElement(self, ele2)
    e3 = findElement(self, ele3)
    TouchAction(self).press(e1).wait(100).move_to(e1).wait(100).move_to(e2).wait(
        100).move_to(e3).release().perform()


# 获取元素坐标
def getEleXY(self, loc):
    element = findElement(self.driver, loc)
    width = element.size["width"]
    height = element.size["height"]

    x = element.location["x"] + width / 2
    y = element.location["y"] + height / 2

    list = {x, y}
    return list


# 元素拖拽操作
def drapAnddrop(driver, el1, el2):
    e1 = findElement(driver, el1)
    e2 = findElement(driver, el2)
    driver.drag_and_drop(e1, e2)


# 处理允许所有系统弹窗
def acceptAll(self):
    self.switch_to.alert.accept()


# 生成随机6位数密碼
def new_number():
    num = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        num += ch
    return num + 'a'


# 单个元素查找等待
def waitElement(self, types, element):
    i = 0
    element1 = None
    while 10 > i:
        try:
            if types == 'id':
                element1 = self.find_element_by_id(element)

            elif types == 'name':
                element1 = self.find_element_by_name(element)

            elif types == 'className':
                element1 = self.find_element_by_class_name(element)

            elif types == 'linkText':
                element1 = self.find_element_by_link_text(element)

            elif types == 'xpath':
                element1 = self.find_element_by_xpath(element)

            elif types == 'ios_predicate':
                element1 = self.find_element_by_ios_predicate(element)

            elif types == 'android_uiautomator':
                element1 = self.find_element_by_android_uiautomator('new UiSelector().' + element)
            break
        except:
            i = i + 1
            # loggerInfo('未找到元素，等待1秒')
            time.sleep(1)
    return element1


# 元素集查找等待
def waitElements(self, types, element):
    i = 0
    element1 = None
    while 10 > i:
        try:
            if types == 'id':
                element1 = self.find_elements_by_id(element)

            elif types == 'name':
                element1 = self.find_elements_by_name(element)

            elif types == 'className':
                element1 = self.find_elements_by_class_name(element)

            elif types == 'linkText':
                element1 = self.find_elements_by_link_text(element)

            elif types == 'xpath':
                element1 = self.find_elements_by_xpath(element)

            elif types == 'ios_predicate':
                element1 = self.find_elements_by_ios_predicate(element)

            elif types == 'android_uiautomator':
                element1 = self.find_elements_by_android_uiautomator('new UiSelector().' + element)
            break
        except:
            i = i + 1
            time.sleep(1)
    return element1


# IOS单个元素查找等待
def waitElement_ios(driver, types, element):
    try:
        if types == 'id':
            WebDriverWait(driver, 10).until(lambda driver_t: driver.find_element_by_id(element).is_displayed())
            element1 = driver.find_element_by_id(element)

        elif types == 'name':
            WebDriverWait(driver, 10).until(lambda driver_t: driver.find_element_by_name(element).is_displayed())
            element1 = driver.find_element_by_name(element)

        elif types == 'className':
            WebDriverWait(driver, 10).until(
                lambda driver_t: driver.find_element_by_class_name(element).is_displayed())
            element1 = driver.find_element_by_class_name(element)

        elif types == 'linkText':
            WebDriverWait(driver, 10).until(
                lambda driver_t: driver.find_element_by_link_text(element).is_displayed())
            element1 = driver.find_element_by_link_text(element)

        elif types == 'xpath':
            WebDriverWait(driver, 10).until(lambda driver_t: driver.find_element_by_xpath(element).is_displayed())
            element1 = driver.find_element_by_xpath(element)

        elif types == 'ios_predicate':
            WebDriverWait(driver, 10).until(
                lambda driver_t: driver.find_element_by_ios_predicate(element).is_displayed())
            element1 = driver.find_element_by_ios_predicate(element)

        return element1
    except:
        return None


# IOS元素集查找等待
def waitElements_ios(driver, types, element):
    try:
        if types == 'id':
            element1 = driver.find_elements_by_id(element)

        elif types == 'name':
            element1 = driver.find_elements_by_name(element)

        elif types == 'className':
            element1 = driver.find_elements_by_class_name(element)

        elif types == 'linkText':
            element1 = driver.find_elements_by_link_text(element)

        elif types == 'xpath':
            element1 = driver.find_elements_by_xpath(element)

        elif types == 'ios_predicate':
            element1 = driver.find_elements_by_ios_predicate(element)

        return element1
    except:
        return None
