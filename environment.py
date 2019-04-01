import sys
import os
from time import sleep
from appium import webdriver

sys.path.append("..")
from BaseUtil.ConfigUtil import *
from BaseUtil import Globalvar as gl
from BaseUtil.SystemCommand import *
from BaseUtil.LogUtil import *
from BaseUtil.SSHUtil import *
from BaseUtil.GetUtil import *
from Devices.GetDevices import *
from steps.CommonSteps import *
from Docker import AppiumRecord as ar

gl._init()


def before_all(self):
    # 设置首次默认未登录
    gl.set_value('login', False)
    getSettingValue(self)
    if gl.get_value('platformName') == 'Android':
        if gl.get_value('stf') == 'false':
            rechange(self, 'deviceName')
            rechange(self, 'platformVersion')
            gl.set_value('android_udid', gl.get_value('deviceName'))
        elif gl.get_value('stf') == 'true':
            # 获取stf设备
            getStfDevice()
            # 重启Appium服务器的Docker
            dockerCmd('docker rm -f appium-' + gl.get_value('appium_port'))
            dockerRestart(gl.get_value('appium_port'))
        connectApp(gl.get_value('deviceName'))
        # 获取测试机屏幕是否已唤醒，执行唤醒操作
        if DeviceStates(gl.get_value('deviceName')) is True:
            unLockDevice(gl.get_value('deviceName'))
        elif DeviceStates(gl.get_value('deviceName')) is False:
            # 按电源键
            os.system(gl.get_value('adb') + ' -s ' + gl.get_value('deviceName') + ' shell input keyevent 26')
            unLockDevice(gl.get_value('deviceName'))
        else:
            assert True == False, 'adb命令执行出错'
        if gl.get_value('noReset') == 'false':
            # 卸载APK
            # connectApp(gl.get_value('deviceName'))
            uninstallApp(gl.get_value('deviceName'))
        if gl.get_value('performance') == 'true':
            # 创建性能监控文件
            connectApp(gl.get_value('deviceName'))
            createPerformanceFile(gl.get_value('deviceName'))

    elif gl.get_value('platformName') == 'ios':
        rechange(self, 'deviceName')
        rechange(self, 'platformVersion')
        getIosDevice()
        # ios卸载重装
        if gl.get_value('noReset') == 'false':
            iosUninstallApp(gl.get_value('udid'))
    pass


# 步骤执行之后
def after_step(self, step):
    if step.status == "failed":
        if gl.get_value('platformName') == 'Android':
            if DeviceStates(gl.get_value('deviceName')) is True:
                unLockDevice(gl.get_value('deviceName'))
            elif DeviceStates(gl.get_value('deviceName')) is False:
                # 按电源键
                os.system(gl.get_value('adb') + ' -s ' + gl.get_value('deviceName') + ' shell input keyevent 26')
                unLockDevice(gl.get_value('deviceName'))
            else:
                loggerError('测试设备已息屏，adb命令执行出错')
        if getWebView(self.driver) is True:
            switchToNative(self.driver)
        # 进行截图操作
        # loggerInfo('截图操作')
        # takeScreen(self.driver)


# 场景执行之后
def after_scenario(self, scenario):
    loggerInfo('已执行完场景')
    # print(scenario.status)
    if scenario.status == 'failed':
        backHome(self)


def before_feature(self, feature):
    if gl.get_value('platformName') == 'Android':
        if gl.get_value('platformVersion') == '4.4.4' or gl.get_value('platformVersion') == '4.4':
            self.driver = webdriver.Remote(
                command_executor='http://' + gl.get_value('url') + '/wd/hub',
                desired_capabilities={
                    'chromeOptions': {'androidProcess': 'com.ju'},
                    'recreateChromeDriverSessions': 'true',
                    'app': gl.get_value('app'),
                    'udid': gl.get_value('android_udid'),
                    'platformName': gl.get_value('platformName'),
                    'platformVersion': gl.get_value('platformVersion'),
                    'deviceName': gl.get_value('android_udid'),
                    'noReset': 'true',
                    'autoGrantPermissions': 'true',
                    'appPackage': 'com.ju',
                    'resetKeyboard': 'true',
                    'unicodeKeyboard': 'true',
                    'useKeystore': 'true',
                })
        else:
            self.driver = webdriver.Remote(
                command_executor='http://' + gl.get_value('url') + '/wd/hub',
                desired_capabilities={
                    'chromeOptions': {'androidProcess': 'com.ju'},
                    'recreateChromeDriverSessions': 'true',
                    'app': gl.get_value('app'),
                    'udid': gl.get_value('android_udid'),
                    'platformName': gl.get_value('platformName'),
                    'platformVersion': gl.get_value('platformVersion'),
                    'deviceName': gl.get_value('android_udid'),
                    'noReset': 'true',
                    'autoGrantPermissions': 'true',
                    'appPackage': 'com.ju',
                    'resetKeyboard': 'true',
                    'unicodeKeyboard': 'true',
                    'useKeystore': 'true',
                    'chromedriverExecutableDir': os.path.dirname(os.path.abspath(__file__)) + '/webview/',  # 本地调试使用
                    'chromedriverChromeMappingFile': os.path.dirname(os.path.abspath(__file__)) + '/mapping.json',  # 本地调试使用
                    'keystorePath': os.path.dirname(os.path.abspath(__file__)) + '/apps/test.keystore',  # 本地调试使用
                    # 'chromedriverExecutableDir': '/root/webview/',
                    # 'chromedriverChromeMappingFile': '/root/mapping.json',
                    # 'keystorePath': '/root/test.keystore',
                    'keystorePassword': '888',
                    'keyAlias': 'td',
                    'keyPassword': '888',
                    'automationName': 'UiAutomator2',
                    'noSign': 'true',
                    'newCommandTimeout': 12000
                })

    elif gl.get_value('platformName') == 'ios':
        self.driver = webdriver.Remote(
            command_executor='http://' + gl.get_value('url') + '/wd/hub',
            desired_capabilities={
                'app': gl.get_value('app'),
                'platformName': gl.get_value('platformName'),
                'platformVersion': gl.get_value('platformVersion'),
                # 'autoAcceptAlerts': 'true',
                # 'autoDismissAlerts': 'true',
                'noReset': 'true',
                'bundleId': 'com.tuandai.client',
                'deviceName': gl.get_value('deviceName'),
                'udid': gl.get_value('udid'),
                'automationName': 'XCUITest',
                'wdaLocalPort': int(gl.get_value('port'))
            })
        if gl.get_value('noReset') == 'false':
            gl.set_value('login', False)


def after_feature(self, feature):
    time.sleep(1)
    self.driver.close_app()


def after_all(self):
    if gl.get_value('platformName') == 'Android':
        if gl.get_value('performance') == 'true':
            pullPerformanceFile(gl.get_value('deviceName'))
        if gl.get_value('stf') == 'true':
            if gl.get_value('list') is not None:
                # ADB断开连接
                loggerInfo('断开ADB测试设备')
                disConnectApp(gl.get_value('deviceName'))
                deleteDevice(gl.get_value('list'))
            # 关闭Appium服务器的Docker
            loggerInfo('docker stop appium-' + gl.get_value('appium_port'))
            dockerCmd('docker stop appium-' + gl.get_value('appium_port'))
            dockerCmd('docker rm -f appium-' + gl.get_value('appium_port'))
    elif gl.get_value('platformName') == 'ios':
        if gl.get_value('performance') == 'true':
            # 留个空位做IOS性能数据上传操作
            loggerInfo('ios性能测试！')
        ios_dev = checkDevice(gl.get_value('udid'))
        result = ios_dev["testing"]
        if result == 'true':
            updateDevice(gl.get_value('udid'), 'false')
        else:
            loggerError('设备已停用，断开失败')


# 获取behave.ini的配置值
def rechange(self, value):
    userdata = self.config.userdata
    if value == 'app':
        if userdata.get(value) is None:
            if gl.get_value('platformName') == 'Android':
                app = 'http://127.0.0.1/app-debug.apk'
                gl.set_value(value, app)
            else:
                app = '/Users/ijknode/workspace/uitest_package/TuanDaiV4/derivedData/Build/Products/Debug-iphonesimulator/TuanDaiV4.app'
                gl.set_value(value, app)
        else:
            gl.set_value(value, userdata.get(value))

    else:
        if userdata.get(value) is None:
            gl.set_value(value, readConfig(value))
        else:
            gl.set_value(value, userdata.get(value))


# 把behave.ini的值配置全局变量
def getSettingValue(self):
    # 性能测试开关
    rechange(self, 'performance')
    # 用户名
    rechange(self, 'username')
    # 登录密码
    rechange(self, 'password')
    # 交易密码
    rechange(self, 'tradepassword')
    # 安卓stf开关
    rechange(self, 'stf')
    # 测试平台ios或安卓
    rechange(self, 'platformName')
    # 卸载重装
    rechange(self, 'noReset')
    # Appium服务地址
    rechange(self, 'url')
    # ios设备的udid
    rechange(self, 'udid')
    # app安装包路径
    rechange(self, 'app')
    # android adb命令路径
    rechange(self, 'adb')
    # serial STF指定测试机
    rechange(self, 'serial')


# Android创建性能测试文件
def createPerformanceFile(ip):
    os.system(gl.get_value('adb') + ' -s ' + ip + ' shell rm -r -f sdcard/Prism')
    os.system(gl.get_value('adb') + ' -s ' + ip + ' shell mkdir sdcard/Prism')
    os.system(gl.get_value('adb') + ' -s ' + ip + ' shell touch sdcard/Prism/com.junte.txt')
    # os.system(gl.get_value('adb') + ' disconnect ' + ip)


# adb连接测试设备
def connectApp(ip):
    count = 0
    max_count = 3600
    while True:
        if count < max_count:
            time.sleep(1)
            # loggerInfo(gl.get_value('adb') + ' devices')
            adbDevice = getOutPut(gl.get_value('adb') + ' devices')
            loggerInfo(adbDevice)
            s_ip = ip + '\tdevice'
            s_error = ip + '\toffline'
            if s_ip in adbDevice:
                break
            else:
                if s_error in adbDevice:
                    os.system(gl.get_value('adb') + ' disconnect ' + ip)
                # loggerInfo(gl.get_value('adb') + ' connect ' + ip)
                result = getOutPut(gl.get_value('adb') + ' connect ' + ip)
                loggerInfo(result)
                if 'already' in result:
                    break
                elif 'failed' in result:
                    loggerError('设备连接异常')
                    break
            time.sleep(30)
            count = count + 30
        else:
            assert count < max_count, 'adb连接测试设备超过1小时，脚本执行失败'


# adb断开连接
def disConnectApp(ip):
    time.sleep(2)
    os.system(gl.get_value('adb') + ' disconnect ' + ip)


# 性能测试文件推送到固定文件夹里
def pullPerformanceFile(ip):
    result = getOutPut(gl.get_value('adb') + ' devices')
    if 'List of devices attached' == result:
        connectApp(gl.get_value('deviceName'))
    os.system(gl.get_value('adb') + ' -s ' + ip + ' pull /sdcard/Prism/com.junte.txt ../PrismReport/data')
    os.system(gl.get_value('adb') + ' -s ' + ip + ' shell rm -r -f sdcard/Prism')


# Android卸载App
def uninstallApp(ip):
    loggerInfo(gl.get_value('adb') + ' -s ' + ip + ' uninstall com.junte')
    os.system(gl.get_value('adb') + ' -s ' + ip + ' uninstall com.junte')


# Android安装App
def installApp(ip, dir):
    loggerInfo(gl.get_value('adb') + ' -s ' + ip + ' install ' + dir)
    os.system(gl.get_value('adb') + ' -s ' + ip + ' install ' + dir)


# ios卸载App
def iosUninstallApp(sid):
    os.system('xcrun simctl uninstall ' + sid + ' com.tuandai.client')


# 获取STF空闲测试设备
def getStfDevice():
    # 循环读取设备
    # 添加最大值限制，2小时7200秒，超时默认失败
    count = 0
    max_count = 7200
    while True:
        if count < max_count:
            list1 = getDevices()
            if list1 is not None:
                if gl.get_value('serial') == 'false':
                    list_devices = ['AQ9SMB85RKKFPRFE', '7854d2c4', 'A5R7N17C22027488', 'BTYNW17324002120']
                    list = [val for val in list1 if val in list_devices]
                    # list = list1
                else:
                    if gl.get_value('serial') in list1:
                        list = [gl.get_value('serial')]
                    else:
                        list = None
                if not list:
                    # 如果可用设备集合为空
                    loggerInfo('正在获取可用测试设备，30S后重试')
                    time.sleep(30)
                else:
                    num = 4723
                    while num < 4823:
                        list_use = dockerCmd('lsof -i:' + str(num))
                        if len(list_use):
                            num = num + 1
                        else:
                            gl.set_value('url', '10.100.97.250:' + str(num))
                            gl.set_value('appium_port', str(num))
                            ar.saveRecord(str(num))
                            break
                    loggerInfo('已获取可用测试设备Device：' + list[0])
                    gl.set_value('android_udid', list[0])
                    gl.set_value('list', list[0])
                    # 获取IP
                    deviceName = connectDevice(list[0])
                    if deviceName is not None:
                        gl.set_value('deviceName', deviceName)
                        s = getDeviceInfo(list[0])
                        gl.set_value('platformVersion', s["device"]["version"])
                        break
                    loggerInfo(list[0] + '测试设备繁忙，30S后重试')
                    time.sleep(30)
            else:
                loggerInfo('正在获取可用测试设备，30S后重试')
                time.sleep(30)
            count = count + 30
        else:
            assert count < max_count, '获取可用测试设备超过2小时，脚本执行失败'


# 获取ios空闲测试设备
def getIosDevice():
    # 检查ios设备占用情况
    count = 0
    max_count = 7200
    while True:
        if count < max_count:
            result = checkDevice(gl.get_value('udid'))
            status = result['testing']
            if status == 'false':
                updateDevice(gl.get_value('udid'), 'true')
                gl.set_value('url', result['server'])
                gl.set_value('port', result['port'])
                gl.set_value('deviceName', result['name'])
                break
            else:
                if gl.get_value('performance') == 'false':
                    device = getUseDevice('ios')
                    if device is not None:
                        loggerInfo('已获取新可用测试设备')
                        new_udid = device['device']
                        gl.set_value('udid', new_udid)
                        updateDevice(gl.get_value('udid'), 'true')
                        gl.set_value('url', device['server'])
                        gl.set_value('port', result['port'])
                        gl.set_value('deviceName', result['name'])
                        break
                loggerInfo('正在获取可用测试设备')
                loggerInfo('30S后重试')
                time.sleep(30)
            count = count + 30
        else:
            assert count < max_count, '获取可用测试设备超过2小时，脚本执行失败'


# 获取安卓测试设备屏幕是否唤醒
def DeviceStates(ip):
    if gl.get_value('stf') == 'true':
        # linux
        if gl.get_value('platformVersion') == '4.4.4':
            result = getOutPut(gl.get_value('adb') + ' -s ' + ip + ' shell dumpsys power | grep "mScreenOn"')
        else:
            result = getOutPut(gl.get_value('adb') + ' -s ' + ip + ' shell dumpsys power | grep "Display Power"')
    else:
        # windows
        # loggerInfo(gl.get_value('adb') + ' -s ' + ip + ' shell dumpsys power | findstr "Display Power:state="')
        result = getOutPut(gl.get_value('adb') + ' -s ' + ip + ' shell dumpsys power | findstr "Display Power:state="')
    if 'Display Power: state=ON' in result or 'mScreenOn=true' in result:
        # 屏幕已唤醒
        loggerInfo('屏幕已唤醒')
        return True
    elif 'Display Power: state=OFF' in result:
        loggerInfo('屏幕未唤醒')
        return False
    else:
        loggerError('命令出错：' + result)
        return None


# 屏幕解锁操作
def unLockDevice(ip):
    if gl.get_value('stf') == 'true':
        # linux
        result = getOutPut(gl.get_value('adb') + ' -s ' + ip + ' shell dumpsys window policy | grep mShowingLockscreen')
    else:
        # windows
        result = getOutPut(
            gl.get_value('adb') + ' -s ' + ip + ' shell dumpsys window policy | findstr mShowingLockscreen')
    if 'mShowingLockscreen=false' in result:
        loggerInfo('屏幕已解锁')
        # # 按home键
        os.system(gl.get_value('adb') + ' -s ' + ip + ' shell input keyevent 3')
    elif 'mShowingLockscreen=true' in result:
        loggerInfo('屏幕未解锁，进行解锁')
        os.system(gl.get_value('adb') + ' -s ' + ip + ' shell input swipe 700 900 700 70')
        time.sleep(2)
        os.system(gl.get_value('adb') + ' -s ' + ip + ' shell input keyevent 3')
