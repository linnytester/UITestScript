import sys
import time
from appium import webdriver
from behave import *
sys.path.append("..")
from BaseUtil.AppiumUtil import *
from BaseUtil.CsvUtil import *
from BaseUtil.LogUtil import *
from BaseUtil import Globalvar as gl
gl._init()

if __name__ == '__main__':
    self.driver = webdriver.Remote()


@Given('点击{page}的{element}')
def clickElement(self, page, element):
    ele = getElement(page, element)
    # loggerInfo(ele)
    click(self.driver, ele)


@When('看见{page}的{element}')
def idSeeElement(self, page, element):
    ele = getElement(page, element)
    sure = isExistElement(self.driver, ele)
    assert sure is True, '没有看到元素' + element


@When('看到{page}的{element}标题')
def ifSeeElementTitle(self, page, element):
    new_element = element + '标题'
    ele = getElement(page, new_element)
    title = getText(self.driver, ele)
    loggerInfo(title)
    assert title == element, '没有看到标题' + element


@When('点击{page}的{element}')
def ifClickElement(self, page, element):
    ele = getElement(page, element)
    click(self.driver, ele)


@When('开始点击{page}的{element}')
def ClickElement(self, page, element):
    ele = getElement(page, element)
    click(self.driver, ele)
    # 用于投资智享标时，点击确认承接，金额自动调整后，再次点击确认承接
    if gl.get_value('platformName') == 'Android':
        if findElement(self.driver, ['id', 'com.junte:id/snackbar_text', '金额必须为X元']) is not None:
            time.sleep(2)
            click(self.driver, ele)
    elif gl.get_value('platformName') == 'ios':
        if findElement(self.driver, ['id', 'iosHLinvestButton', '金额必须为X元']) is not None:
            time.sleep(2)
            click(self.driver, ele)


@When('在{page}的{element}填入{keys}')
def sendKeyDang(self, page, element, keys):
    ele = getElement(page, element)
    sendKeys(self.driver, ele, keys)


@When('{page}的{element}为{result}')
def isResultTrue(self, page, element, result):
    ele = getElement(page, element)
    text = getText(self.driver, ele)
    assert text == result, page + '的' + element + '不为' + result


@Then('点击{page}的{element}')
def clickElement(self, page, element):
    ele = getElement(page, element)
    click(self.driver, ele)


@Then('看见{page}的{element}')
def seeElement(self, page, element):
    ele = getElement(page, element)
    sure = isExistElement(self.driver, ele)
    assert sure is True, '没有看见元素' + element


@Then('检查{page}的{element}，或{page2}的{element2}')
def seeOrderElement(self, page, element, page2, element2):
    ele = getElement(page, element)
    sure = findElement(self.driver, ele)
    # assert sure is True, '没有看见元素' + str(ele)
    if sure is None:
        ele2 = getElement(page2, element2)
        sure2 = findElement(self.driver, ele2)
        assert sure2 is not None, '没有看见元素' + element + '或' + element2


@Then('看到{page}的{element}标题')
def seeElementTitle(self, page, element):
    elements = element + '标题'
    ele = getElement(page, elements)
    title = getText(self.driver, ele)
    loggerInfo(title)
    assert title == element, '没有看到标题' + element


@Then('清空{page}的{element}')
def clearElement(self, page, element):
    ele = getElement(page, element)
    clear(self.driver, ele)


@Then('在{page}的{element}填入{keys}')
def sendKey(self, page, element, keys):
    ele = getElement(page, element)
    if keys == '新密码':
        keys = new_number()
    sendKeys(self.driver, ele, keys)


@Then('打开{page}成功')
def openPage(self, page):
    loggerInfo('打开' + page + '成功')


@Then('返回')
def comeBack(self):
    if gl.get_value('platformName') == 'Android':
        goBack(self.driver)
    elif gl.get_value('platformName') == 'ios':
        ios_goBack(self.driver)


@Then('切换为{model}模式')
def swtichTo(self, model):
    time.sleep(3)
    if model == 'webview':
        count = 0
        while 10 > count:
            if getWebView(self.driver) is True:
                switchToWebView(self.driver)
                break
            else:
                count = count + 1
                time.sleep(3)
    elif model == 'native':
        switchToNative(self.driver)


@Then('坐标点击{page}的{element}')
def doClickByXY(self, page, element):
    if gl.get_value('platformName') == 'ios':
        if element == '消息中心':
            se = getSize(self.driver)
            width = se[0]
            height = se[1]
            clickByXY(self.driver, width / 10, height / 20)
        else:
            click(self.driver, getElement(page, element))
    else:
        click(self.driver, getElement(page, element))


@When('存在{page}的{element}，{done}，并{made}')
def ifSomething(self, page, element, done, made):
    ele = getElement(page, element)
    if findElement(self.driver, ele) is not None:
        if done == '点击它':
            click(self.driver, ele)
        if made == '返回':
            time.sleep(3)
            comeBack(self)


@Then('等待{page}的{element}出现，{done}')
def waitForClick(self, page, element, done):
    ele = getElement(page, element)
    i = 0
    while i < 8:
        if findElement(self.driver, ele) is not None:
            if done == '点击它':
                click(self.driver, ele)
            break
        else:
            i = i + 1
            time.sleep(1)


@When('等待{sec}秒')
def wait(self, sec):
    time.sleep(int(sec))


@When('弹出{tanchuan}的{tips}是单笔转让金额最少{money}元，{done}它，重新在{page}的{element}填入')
def reWrite(self, tanchuan, tips, money, done, page, element):
    ele = getElement(tanchuan, tips)
    sure = isExistElement(self.driver, ele)
    if sure is True:
        if done == '点击':
            ele2 = getElement('弹窗', '我知道了')
            click(self.driver, ele2)
            ele3 = getElement(page, element)
            sendKeys(self.driver, ele3, money)
    else:
        pass


@Then('选择{page}的{element}')
def choose(self, page, element):
    ele = getElement(page, element)
    if gl.get_value('platformName') == 'Android':
        click(self.driver, ele)
    elif gl.get_value('platformName') == 'ios':
        if element == '教育培训':
            ele_ios = getElement(page, '完成')
            click(self.driver, ele_ios)


@When('若看见{page1}的{element1}，{done1}，否则看见{page2}的{element2}，{done2}')
def doneThings(self, page1, element1, done1, page2, element2, done2):
    el1 = getElement(page1, element1)
    el2 = getElement(page2, element2)
    if findElement(self.driver, el1) is not None:
        if done1 == '点击它':
            click(self.driver, el1)
        elif done1 == '返回':
            comeBack(self)
    elif findElement(self.driver, el2) is not None:
        if done1 == '点击它':
            click(self.driver, el2)
        elif done1 == '返回':
            comeBack(self)


@When('发现{page1}的{element1}，{done1}，并{done2}下{page2}的{element2}')
def findDone(self, page1, element1, done1, done2, page2, element2):
    el1 = getElement(page1, element1)
    el2 = getElement(page2, element2)
    if findElement(self.driver, el1) is not None:
        if done1 == '点击它':
            click(self.driver, el1)
        elif done1 == '返回':
            comeBack(self)
        if element1 == '风险提示':
            time.sleep(5)
        if findElement(self.driver, el2) is not None:
            if done2 == '点击':
                click(self.driver, el2)
