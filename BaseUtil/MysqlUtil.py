#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import pymssql
import pymysql


# 查询连接System
def selectSQL101(sql):
    db = pymssql.connect(host="10.100.1.1", user="fb", password="123",
                         database="System", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()



# 获取昨天日期
def getYesterDay():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = str(today - oneday)
    return yesterday


