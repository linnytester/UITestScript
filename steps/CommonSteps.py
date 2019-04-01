#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import string
import sys
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from behave import *

from BaseUtil.GetUtil import getRegisterCode, getUserIdentityCard

sys.path.append("..")
from BaseUtil.AppiumUtil import *
from BaseUtil.CsvUtil import *
from BaseUtil.PostUtil import *
from BaseUtil.MysqlUtil import *
from BaseUtil.LogUtil import *
from BaseUtil import Globalvar as gl
from steps.TDSteps import *

gl._init()

if __name__ == '__main__':
    self.driver = webdriver.Remote()


@Then('绘制手势密码')
def Gesture(self):
    if gl.get_value('platformName') == 'Android':
        if findElement(self.driver, getElement('手势密码', '绘制图')) is not None:
            list_pwd = findElements(self.driver, ['className', 'android.widget.ImageView', '手势密码绘制点'])
            TouchAction(self.driver).press(list_pwd[1]).wait(300).move_to(list_pwd[1]).wait(300).move_to(
                list_pwd[2]).wait(
                100).move_to(list_pwd[3]).release().perform()
            loggerInfo('绘制手势密码')
            if findElement(self.driver, getElement('手势密码', '绘制图')) is not None:
                TouchAction(self.driver).press(list_pwd[1]).wait(300).move_to(list_pwd[1]).wait(300).move_to(
                    list_pwd[2]).wait(
                    100).move_to(list_pwd[3]).release().perform()
                loggerInfo('再次绘制手势密码')

    else:
        # ios点击
        if findElement(self.driver, getElement('手势密码', '绘制图')) is not None:
            # start = findElement(self.driver, getElement('手势密码', '1'))
            # start_height = start.size['height']
            # start_width = start.size['width']
            # start_x = start.location['x']
            # start_y = start.location['y']
            # begin_x = start_x + start_width / 2
            # begin_y = start_y + start_height / 2
            # TouchAction(self.driver).press(x=start_x, y=start_y).wait(800).move_to(x=start_x + start_width * 2,
            #                                                                        y=begin_y).wait(800).move_to(
            #     x=start_x + start_width * 4, y=begin_y).perform().release()
            # loggerInfo('绘制手势密码')
            # if findElement(self.driver, getElement('手势密码', '绘制图')) is not None:
            #     TouchAction(self.driver).press(x=start_x, y=start_y).wait(800).move_to(x=start_x + start_width * 2,
            #                                                                            y=begin_y).wait(800).move_to(
            #         x=start_x + start_width * 4, y=begin_y).perform().release()
            #     loggerInfo('再次绘制手势密码')
            start = findElement(self.driver, getElement('手势密码', '1'))
            start2 = findElement(self.driver, getElement('手势密码', '2'))
            start3 = findElement(self.driver, getElement('手势密码', '3'))
            try:
                loggerInfo('绘制手势密码开始')
                TouchAction(self.driver).press(start).wait(500).move_to(start2).wait(500).move_to(
                    start3).perform().release()
            except RuntimeError as e:
                loggerError(e)
            loggerInfo('绘制手势密码')
            if findElement(self.driver, getElement('手势密码', '绘制图')) is not None:
                TouchAction(self.driver).press(start).wait(500).move_to(start2).wait(500).move_to(
                    start3).perform().release()
                loggerInfo('再次绘制手势密码')


@Then('登录')
def doLogin(self):
    if findElement(self.driver, getElement('登录', '标题')) is None:
        if findElement(self.driver, getElement('注册', '马上登录')) is not None:
            click(self.driver, getElement('注册', '马上登录'))
    username = gl.get_value('username')
    password = gl.get_value('password')
    # 登录操作
    user = getElement('登录', '用户名输入框')
    click(self.driver, user)
    clear(self.driver, user)
    sendKeys(self.driver, user, username)
    pwd = getElement('登录', '密码输入框')
    click(self.driver, pwd)
    clear(self.driver, pwd)
    sendKeys(self.driver, pwd, password)
    login_two(self)


@Given('已登录')
def readyLogin(self):
    if gl.get_value('login') is False:
        click(self.driver, getElement('底部', '我'))
        if findElement(self.driver, getElement('我', '登录注册按钮')) is not None:
            click(self.driver, getElement('我', '登录注册按钮'))
            doLogin(self)
            Gesture(self)
            if findElement(self.driver, getElement('我', '用户名')) is not None:
                gl.set_value('login', True)
            else:
                loggerError('登录失败')
    elif gl.get_value('login') is True:
        loggerInfo('已登录')
        gl.set_value('login', True)


@Given('未登录')
def loginOut(self):
    click(self.driver, getElement('底部', '我'))
    if findElement(self.driver, getElement('我', '登录注册按钮')) is None:
        doSwipe(self, '上')
        click(self.driver, getElement('我', '设置按钮'))
        click(self.driver, getElement('设置', '退出账号'))
        if findElement(self.driver, getElement('设置', '确定退出账号')) is not None:
            click(self.driver, getElement('设置', '确定'))
        if findElement(self.driver, getElement('我', '登录注册按钮')) is not None:
            loggerInfo('退出登录成功')
            gl.set_value('login', False)
        else:
            loggerError('退出登录失败')
    else:
        loggerInfo('未登录')
        gl.set_value('login', False)


@When('向{wp}滑动')
def doSwipe(self, wp):
    se = getSize(self.driver)
    width = se[0]
    height = se[1]
    time.sleep(2)
    if wp == '下':
        swipe(self.driver, width / 2, height / 2, width / 2, height / 4, 500)
    elif wp == '上':
        swipe(self.driver, width / 2, height / 4, width / 2, height * 3 / 4, 500)
    time.sleep(1)


@Given('启动APP')
def firstLaunch(self):
    # 允许所有系统弹窗
    try:
        i = 0
        while 3 > i:
            acceptAll(self.driver)
            i = i + 1
            time.sleep(1)
    except:
        pass
    time.sleep(2)
    if gl.get_value('platformName') == 'Android':
        if findElement(self.driver, getElement('底部', '首页')) is not None:
            loggerInfo('启动APP成功')
            time.sleep(2)
        elif findElement(self.driver, getElement('手势密码', '绘制图')) is not None:
            Gesture(self)
            if findElement(self.driver, getElement('底部', '首页')) is None:
                # 升级弹窗
                if findElement(self.driver, getElement('启动页', '升级弹窗')) is not None:
                    click(self.driver, getElement('启动页', '暂不体验'))
                if findElement(self.driver, getElement('启动页', '活动弹窗关闭按钮')) is not None:
                    click(self.driver, getElement('启动页', '活动弹窗关闭按钮'))
                elif findElement(self.driver, getElement('启动页', '消息弹窗关闭按钮')) is not None:
                    click(self.driver, getElement('启动页', '消息弹窗关闭按钮'))
        # 升级弹窗
        elif findElement(self.driver, getElement('启动页', '升级弹窗')) is not None:
            click(self.driver, getElement('启动页', '暂不体验'))
            if findElement(self.driver, getElement('底部', '首页')) is None:
                if findElement(self.driver, getElement('启动页', '新手体验金弹窗关闭按钮')) is not None:
                    click(self.driver, getElement('启动页', '新手体验金弹窗关闭按钮'))
                elif findElement(self.driver, getElement('启动页', '活动弹窗关闭按钮')) is not None:
                    click(self.driver, getElement('启动页', '活动弹窗关闭按钮'))
                elif findElement(self.driver, getElement('启动页', '消息弹窗关闭按钮')) is not None:
                    click(self.driver, getElement('启动页', '消息弹窗关闭按钮'))
        elif findElement(self.driver, getElement('启动页', '新手体验金弹窗关闭按钮')) is not None:
            click(self.driver, getElement('启动页', '新手体验金弹窗关闭按钮'))
            # 升级弹窗
            if findElement(self.driver, getElement('启动页', '升级弹窗')) is not None:
                click(self.driver, getElement('启动页', '暂不体验'))
        elif findElement(self.driver, getElement('启动页', '活动弹窗关闭按钮')) is not None:
            click(self.driver, getElement('启动页', '活动弹窗关闭按钮'))
        elif findElement(self.driver, getElement('启动页', '消息弹窗关闭按钮')) is not None:
            click(self.driver, getElement('启动页', '消息弹窗关闭按钮'))
        else:
            loggerError('启动APP失败')
            assert True == False, '启动APP失败'
    else:
        if findElement(self.driver, getElement('底部', '首页')) is not None:
            loggerInfo('启动APP成功')
            time.sleep(2)
        elif findElement(self.driver, getElement('手势密码', '绘制图')) is not None:
            Gesture(self)
            if findElement(self.driver, getElement('底部', '首页')) is None:
                if findElement(self.driver, getElement('启动页', '活动弹窗关闭按钮')) is not None:
                    click(self.driver, getElement('启动页', '活动弹窗关闭按钮'))
                elif findElement(self.driver, getElement('启动页', '消息弹窗关闭按钮')) is not None:
                    click(self.driver, getElement('启动页', '消息弹窗关闭按钮'))
        elif findElement(self.driver, getElement('启动页', '新手体验金弹窗关闭按钮')) is not None:
            click(self.driver, getElement('启动页', '新手体验金弹窗关闭按钮'))
        elif findElement(self.driver, getElement('启动页', '活动弹窗关闭按钮')) is not None:
            click(self.driver, getElement('启动页', '活动弹窗关闭按钮'))
        elif findElement(self.driver, getElement('启动页', '消息弹窗关闭按钮')) is not None:
            click(self.driver, getElement('启动页', '消息弹窗关闭按钮'))
        else:
            loggerError('启动APP失败')
            assert True == False, '启动APP失败'


@Then('回到首页')
def backHome(self):
    count = 0
    while 7 > count:
        if findElement(self.driver, getElement('底部', '首页')) is None:
            if gl.get_value('platformName') == 'Android':
                goBack(self.driver)
            elif gl.get_value('platformName') == 'ios':
                if ios_goBack(self.driver) is False:
                    break
            count = count + 1
            loggerInfo('点击返回')
        else:
            loggerInfo('已回到首页')
            break
    assert findElement(self.driver, getElement('底部', '首页')) is not None, '回到首页失败'


@Given('签到{mess}天')
def signData(self, mess):
    tel = gl.get_value('username')
    # 获取userId
    userId = getUserId(tel)
    # 修改UserSign
    signDate = getYesterDay()
    sql1 = "update UserSign set Days='" + mess + "',SignDate='" + signDate + "' where UserId=" + "'" + userId + "'"
    executeSQL(sql1)
    # 获取签到明细ID
    signId = selectOneSQL("select id from UserSign where UserId='" + userId + "'")
    newSignId = signId[0]
    # 删除签到明细表
    sql = "delete from  UserSignDetail  where UserSignId='" + newSignId + "'"
    executeSQL(sql)
    # 插入数据
    procedureSQL(mess, newSignId)
    # 清楚缓存
    # clearCache('usersigncallist') .net缓存key
    # JAVA清除缓存key
    clearCache('J_UserSignCal')
    clearCache('J_UserSignInfo')
    time.sleep(2)


@When('匹配{page}里{element1}为{element2}点击')
def matchElementText(self, page, element1, element2):
    """主要匹配产品进行申购"""
    gl.set_value('matchProduct', False)
    ele = getElement(page, element1)
    loggerInfo(str(ele))
    text = getTexts(self.driver, ele)
    if gl.get_value('platformName') == 'Android':
        loggerInfo('获取到的产品-->' + str(text))
        for i in range(len(text)):
            if element2 in text[i]:
                loggerInfo('点击产品-->' + text[i])
                try:
                    xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[{}]'.format(
                        i + 4)
                    # loggerInfo('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup[{}]'.format(i+4))
                    self.driver.find_element_by_xpath(xpath).click()
                    gl.set_value('matchProduct', True)
                    return
                except Exception as e:
                    loggerError(str(e))

        if gl.get_value('matchProduct') is False:
            swipeUp(self.driver)
            loc = ['id', 'com.junte:id/snackbar_text', '最后一页']
            if findElement(self.driver, loc) is None:
                # 判断是否已经滑动到最后一页
                matchElementText(self, page, element1, element2)
            else:
                loggerError('未找到产品-->' + element2)
                assert True == False
                return
    elif gl.get_value('platformName') == 'ios':
        if text is None:
            swipeUp(self.driver)
            text = getTexts(self.driver, ele)
        del text[0:5]
        loggerInfo('获取到的产品-->' + str(text))
        for i in range(len(text)):
            if element2 in text[i]:
                loggerInfo('点击产品-->' + text[i])
                try:
                    xpath = "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeScrollView[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[{}]".format(
                        i + 1)
                    self.driver.find_element_by_xpath(xpath).click()
                    gl.set_value('matchProduct', True)
                    return
                except Exception as e:
                    loggerError(str(e))

        if gl.get_value('matchProduct') is False:
            productList = []
            for i in range(len(text)):
                if element2 in text[i]:
                    productList.append(text[i])
            if len(productList) > 0:
                swipeUp(self.driver)
                matchElementText(self, page, element1, element2)
            else:
                loggerError('未找到产品-->' + element2)
                assert True == False
                return


@When('出现{page}的{element}，{done}')
def isDoneSometing(self, page, element, done):
    ele = getElement(page, element)
    if findElement(self.driver, ele) is not None:
        if done == '绘制手势密码':
            Gesture(self)
        elif done == '点击它':
            click(self.driver, ele)
        elif done == '进行登录':
            doLogin(self)
            Gesture(self)
            if isExistElement(self.driver, getElement('底部', '首页')) is True:
                gl.set_value('login', True)
            elif findElement(self.driver, getElement('我', '用户名')) is not None:
                gl.set_value('login', True)
    else:
        if done == '进行登录':
            gl.set_value('login', False)


@Then('输入存管交易密码')
def cgtPwd(self):
    pwd = gl.get_value('tradepassword')
    click(self.driver, getElement('存管交易密码', '密码输入框'))
    time.sleep(2)
    sendKeys(self.driver, getElement('存管交易密码', '密码输入框'), pwd)
    if isExistElement(self.driver, getElement('存管交易密码', '我同意')) is True:
        click(self.driver, getElement('存管交易密码', '我同意'))
    click(self.driver, getElement('存管交易密码', '确认按钮'))


@Then('开启交易密码')
def openPassword(self):
    pwd = gl.get_value('tradepassword')
    if gl.get_value('platformName') == 'Android':
        status = getText(self.driver, getElement('密码管理', '开启状态'))
        if status == '交易密码： 开启':
            loggerInfo(status)
        elif status == '交易密码： 关闭':
            click(self.driver, getElement('密码管理', '开关按钮'))
            switchToWebView(self.driver)
            click(self.driver, getElement('存管交易密码', '密码输入框'))
            sendKeys(self.driver, getElement('存管交易密码', '密码输入框'), pwd)
            click(self.driver, getElement('存管交易密码', '确认按钮'))
            switchToNative(self.driver)
            reslut = getText(self.driver, getElement('密码管理', '结果标题'))
            if reslut == '开启成功':
                click(self.driver, getElement('密码管理', '完成'))
    else:
        if isExistElement(self.driver, getElement('密码管理', 'ios开启状态')) is False:
            # 关闭的状态
            click(self.driver, getElement('密码管理', '开关按钮'))
            switchToWebView(self.driver)
            click(self.driver, getElement('存管交易密码', '密码输入框'))
            time.sleep(2)
            sendKeys(self.driver, getElement('存管交易密码', '密码输入框'), pwd)
            click(self.driver, getElement('存管交易密码', '确认按钮'))
            switchToNative(self.driver)
            if isExistElement(self.driver, getElement('密码管理', 'ios开启结果标题')) is True:
                click(self.driver, getElement('密码管理', '完成'))
        else:
            loggerInfo(getElement('密码管理', '开启状态'))


@Then('输入交易密码')
def inputpwd(self):
    # switchToWebView(self.driver)
    time.sleep(3)
    count = 0
    while 10 > count:
        if getWebView(self.driver) is True:
            switchToWebView(self.driver)
            break
        else:
            count = count + 1
            time.sleep(3)
    pwd = gl.get_value('tradepassword')
    click(self.driver, getElement('存管交易密码', '密码输入框'))
    time.sleep(2)
    sendKeys(self.driver, getElement('存管交易密码', '密码输入框'), pwd)
    click(self.driver, getElement('存管交易密码', '确认按钮'))
    switchToNative(self.driver)


@Then('关闭交易密码')
def closePassword(self):
    pwd = gl.get_value('tradepassword')
    if gl.get_value('platformName') == 'Android':
        status = getText(self.driver, getElement('密码管理', '开启状态'))
        if status == '交易密码： 关闭':
            loggerInfo(status)
        elif status == '交易密码： 开启':
            click(self.driver, getElement('密码管理', '开关按钮'))
            switchToWebView(self.driver)
            click(self.driver, getElement('存管交易密码', '密码输入框'))
            sendKeys(self.driver, getElement('存管交易密码', '密码输入框'), pwd)
            click(self.driver, getElement('存管交易密码', '确认按钮'))
            switchToNative(self.driver)
            reslut = getText(self.driver, getElement('密码管理', '结果标题'))
            if reslut == '关闭成功':
                click(self.driver, getElement('密码管理', '完成'))
    else:
        if isExistElement(self.driver, getElement('密码管理', 'ios关闭状态')) is False:
            # 开启的状态
            click(self.driver, getElement('密码管理', '开关按钮'))
            switchToWebView(self.driver)
            click(self.driver, getElement('存管交易密码', '密码输入框'))
            time.sleep(2)
            sendKeys(self.driver, getElement('存管交易密码', '密码输入框'), pwd)
            click(self.driver, getElement('存管交易密码', '确认按钮'))
            switchToNative(self.driver)
            if isExistElement(self.driver, getElement('密码管理', 'ios关闭结果标题')) is True:
                click(self.driver, getElement('密码管理', '完成'))
        else:
            loggerInfo(getElement('密码管理', '开启状态'))


@Then('标记{status}状态')
def loginStatus(self, status):
    if status == '已登录':
        gl.set_value('login', True)
    elif status == '未登录':
        gl.set_value('login', False)


@Given('冷启动APP')
def coldBoot(self):
    adb = 'adb shell am start -W -n Activity'
    os.system(adb)
    # self.driver.start_activity()


# 生成手机号码
def get_phone():
    num_start = ['130', '131', '132', '135', '156', '186', '185', '134', '136', '137', '138', '139', '150', '151',
                 '152', '157', '158', '159', '182', '188', '187', '133', '153', '180', '181', '189']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 8))
    res = start + end
    return res


# 判断手机号码是否已经注册
def phone_is_register(self):
    phone = get_phone()
    result = getUserId(phone)
    if result is None:
        input_phone = getElement('注册', '手机号码输入框')
        clear(self.driver, input_phone)
        sendKeys(self.driver, input_phone, phone)
        pwd = getElement('注册', '密码输入框')
        sendKeys(self.driver, pwd, '123456a')
        click(self.driver, getElement('注册', '获取验证码'))
        time.sleep(2)
        code = getRegisterCode(phone)
        sendKeys(self.driver, getElement('注册', '验证码输入框'), code)
    else:
        phone_is_register(self)


@Then('无邀请人注册')
def uninvitedRegistration(self):
    phone_is_register(self)
    # click(self.driver, getElement('注册', '已阅读'))
    # click(self.driver, getElement('注册', '确定注册'))
    time.sleep(2)


def data_generation():
    str_s = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    for i in range(5):
        str_s += chars[random.randint(0, length)]
    str_x = '123' + str_s
    return str_x


@then('获取{telno}短信验证码填入{page}的{element}')
def writeCode(self, telno, page, element):
    # 获取userId
    userId = getUserId(telno)
    time.sleep(2)
    code = getRegisterCode(telno)
    ele = getElement(page, element)
    sendKeys(self.driver, ele, code)


@then('获取{telno}证件号码填入{page}的{element}')
def writeIdCard(self, telno, page, element):
    # 获取userId
    userId = getUserId(telno)
    idCard = getUserIdentityCard(userId)
    ele = getElement(page, element)
    sendKeys(self.driver, ele, idCard)


@then('智享插入数据{telno}')
def clear_data(self, telno):
    tel = telno
    # 获取userId
    userId = getUserId(tel)
    ow_time = datetime.datetime.now()
    yes_time = ow_time.strftime('%Y-%m-%d 00:00:00.000')
    s_sql = "select CalcDate from ZX where UserId ='{}' and Calcdate='{}'".format(userId,
                                                                                                           yes_time)
    sa_sql = "select TotalAmount from ZXt where UserId ='{}' and Calcdate='{}'".format(userId,
                                                                                                               yes_time)
    result = selectSQL102(s_sql)
    result_amount = selectSQL102(sa_sql)
    result_i = int(result_amount[0])
    if result == '' or result is None:
        e_sql = "INSERT INTO ZX SELECT NEWID(),'{}','{}',0,100000000,GETDATE(),GETDATE()".format(
            userId, yes_time)
        executeSQLZX101(e_sql)
    else:
        loggerInfo("今日的数据已经插入")
        if result_i == 0:
            u_sql = "update ZX set TotalAmount='100000000' where UserId ='{}' and Calcdate='{}'".format(
                userId,
                yes_time)
            executeSQLZX101(u_sql)


@then('关闭APP')
def close_app(self):
    self.driver.close_app()


@then('开启APP')
def lauch_app(self):
    self.driver.launch_app()


@Given('登录固定账号{telno}，{paswd}')
def login_telno(self, telno, paswd):
    click(self.driver, getElement('我', '登录注册按钮'))
    username = telno
    password = paswd
    if findElement(self.driver, getElement('登录', '标题')) is None:
        if findElement(self.driver, getElement('注册', '马上登录')) is not None:
            click(self.driver, getElement('注册', '马上登录'))
    # 登录操作
    user = getElement('登录', '用户名输入框')
    click(self.driver, user)
    clear(self.driver, user)
    sendKeys(self.driver, user, username)
    pwd = getElement('登录', '密码输入框')
    click(self.driver, pwd)
    clear(self.driver, pwd)
    sendKeys(self.driver, pwd, password)
    login_two(self)
    Gesture(self)
    if findElement(self.driver, getElement('我', '用户名')) is not None:
        gl.set_value('login', True)
    else:
        gl.set_value('login', False)
        loggerError('登录失败')


@Given('重新登录{telno}')
def reloadLogin(self, telno):
    password = gl.get_value('password')
    click(self.driver, getElement('底部', '我'))
    if findElement(self.driver, getElement('我', '登录注册按钮')) is None:
        doSwipe(self, '上')
        click(self.driver, getElement('我', '设置按钮'))
        click(self.driver, getElement('设置', '退出账号'))
        if findElement(self.driver, getElement('设置', '确定退出账号')) is not None:
            click(self.driver, getElement('设置', '确定'))
        if findElement(self.driver, getElement('我', '登录注册按钮')) is not None:
            loggerInfo('退出登录成功')
            gl.set_value('login', False)
    login_telno(self, telno, password)


@Then('退出登录')
def loginingOut(self):
    click(self.driver, getElement('底部', '我'))
    if findElement(self.driver, getElement('我', '登录注册按钮')) is None:
        doSwipe(self, '上')
        click(self.driver, getElement('我', '设置按钮'))
        click(self.driver, getElement('设置', '退出账号'))
        if findElement(self.driver, getElement('设置', '确定退出账号')) is not None:
            click(self.driver, getElement('设置', '确定'))
        if findElement(self.driver, getElement('我', '登录注册按钮')) is not None:
            loggerInfo('退出登录成功')
            gl.set_value('login', False)
        else:
            loggerError('退出登录失败')
    else:
        loggerInfo('未登录')
        gl.set_value('login', False)


@Then('判断登录的风险提示，进行登录')
def login_two(self):
    try:
        login = getElement('登录', '登录按钮')
        # 第一种登录提示
        if findElement(self.driver, getElement('登录', '已阅读')) is not None:
            click(self.driver, getElement('登录', '已阅读'))
            time.sleep(2)
            click(self.driver, login)

        # 第二种登录提示
        else:
            click(self.driver, login)
            if findElement(self.driver, getElement('登录', '风险提示')) is not None:
                click(self.driver, getElement('登录', '风险提示'))
                time.sleep(5)
                if findElement(self.driver, getElement('登录', '确认')) is not None:
                    click(self.driver, getElement('登录', '确认'))
    except:
        loggerError('风险提示登录失败')


@Then('判断登录的风险提示，进行登录2')
def login_two2(self):
    try:
        login = getElement('注册', '确定注册')
        # 第一种登录提示
        if findElement(self.driver, getElement('登录', '已阅读')) is not None:
            click(self.driver, getElement('登录', '已阅读'))
            time.sleep(2)
            click(self.driver, login)

        # 第二种登录提示
        else:
            click(self.driver, login)
            if findElement(self.driver, getElement('登录', '风险提示')) is not None:
                click(self.driver, getElement('登录', '风险提示'))
                time.sleep(5)
                if findElement(self.driver, getElement('登录', '确认')) is not None:
                    click(self.driver, getElement('登录', '确认'))
    except:
        loggerError('风险提示登录失败')


@Then('判断出借详情页的风险提示，进行确认出借')
def sub_two(self):
    try:
        submit = getElement('出借详情页', '确认出借')
        # 第一种出借提示
        if findElement(self.driver, submit) is not None:
            click(self.driver, getElement('出借详情页', '已阅读'))
            time.sleep(2)
            click(self.driver, submit)

        # 第二种出借提示
        else:
            if findElement(self.driver, getElement('出借详情页', '风险提示')) is not None:
                click(self.driver, getElement('出借详情页', '风险提示'))
                time.sleep(5)
                if findElement(self.driver, getElement('出借详情页', '确认')) is not None:
                    click(self.driver, getElement('出借详情页', '确认'))
    except:
        loggerError('风险提示出借失败')
