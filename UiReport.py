#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import demjson
import sys
import codecs
import html5lib
import pathlib
from bs4 import BeautifulSoup

resultDatas = []


# 获取UI测试报告
def getNetData(url, buildUrl):
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        soup = BeautifulSoup(response.text, "html5lib")
        tagResult = soup.find_all("tbody")
        if tagResult is None or len(tagResult) == 0:
            return
        trResult = tagResult[1].find_all("tr")
        for td in trResult:
            getTdData(td, buildUrl)
    else:
        print(" url" + url + "请求错误")
        return


def getUIData(jobName, path):
    if fileExists(path):
        soup = BeautifulSoup(readData(path), "html5lib")
        tagResult = soup.find_all("tbody")
        if tagResult is None or len(tagResult) == 0:
            return
        trResult = tagResult[1].find_all("tr")
        for td in trResult:
            getTdData(td, buildUrl)
    else:
        writeData("./UiReport.html", jobName + " Build Failed!")
        print(" path" + path + "文件不存在")
        return


# 解析UI测试报告
def getTdData(tdData, buildUrl):
    tdData = tdData.find_all("td")
    feature = "[feature:" + tdData[0].text + "](" + buildUrl + "cucumber-html-reports/" + tdData[0].find("a").get(
        "href") + ")" + " \\n > ##### "
    failFeaStr = "<font color=#FF0000 size=18>" + " failed:" + tdData[2].text + "</font>"
    steps = " Step: " + "total:" + tdData[6].text + " passed: " + tdData[1].text + " skipped:" + tdData[3].text
    if tdData[2].text != "0":
        steps = steps + failFeaStr
    scenarios = " Scenarios " + "total:" + tdData[9].text + " passed: " + tdData[7].text
    failSceStr = "<font color=#FF0000 size=18>" + " failed:" + tdData[8].text + "</font>"
    if tdData[8].text != "0":
        scenarios += failSceStr
    data = feature + steps + scenarios
    resultDatas.append(data)


# 读文件
def readData(path):
    with codecs.open(path, encoding="utf-8") as f:
        resultData = f.read()
        f.close()
        return resultData


# 写文件
def writeData(path, data):
    with open(path, "w") as f:
        f.write("""{\"msgtype\": \"markdown\",\"markdown\": {\"title\":\"Jenkins\",\"text\": \"""")
        f.write(data)
        f.write("""\",\"hideAvatar\": \"1\"}}""")
        f.flush()
        f.close()


def fileExists(filepath):
    path = pathlib.Path(filepath)
    return path.exists()


def writeReport(jobName, buildUrl, isPerformance, path):
    # newUrl=buildUrl.replace("//","//admin:tuandai123888@")
    # urlArr = [newUrl, "cucumber-html-reports/overview-features.html"]
    # urlArr = buildUrl
    # requestUrl = ''.join(urlArr)
    print("path " + path)
    getUIData(jobName, path)
    if len(resultDatas) == 0:
        if fileExists(path):
            writeData("./UiReport.html", jobName + " Build Success!")
        else:
            writeData("./UiReport.html", jobName + " Build Failed!")
    else:
        rowData = "\\n > #### ".join(resultDatas)
        perfmanceResult = "[性能测试报告](" + buildUrl + "Prism_Report/)"
        name = jobName + " Build Finish! \\n > #### [UI自动化测试报告](" + buildUrl + "cucumber-html-reports/overview-features.html)" + "\\n > #### "
        if isPerformance == "true" and fileExists("PrismReport/result"):
            name = name + perfmanceResult + "\\n > #### " + rowData
        else:
            name = name + rowData

        writeData("./UiReport.html", name)


if __name__ == "__main__":
    jobName = "Tuandai_Automated_Test_Python"
    isPerformance = "false"
    buildUrl = ""
    path = ""

    if len(sys.argv) > 4:
        jobName = sys.argv[1]
        isPerformance = sys.argv[2]
        buildUrl = sys.argv[3]
        path = sys.argv[4]
    else:
        print("参数错误!")

    if len(isPerformance) and len(jobName) and len(buildUrl):
        writeReport(jobName, buildUrl, isPerformance, path)
