#!/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess


# 封装命令行输出
def getOutPut(commands):
    result = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE)
    txt = result.stdout.read()
    txt = txt.decode()
    row = txt.replace('\r', '').replace('\n', '')
    return row
