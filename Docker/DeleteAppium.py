#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os

sys.path.append("..")
from Docker import AppiumRecord as docker
from BaseUtil import SSHUtil as ssl
from BaseUtil import LogUtil as log

dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def delete():
    try:
        port = docker.getRecord(dir)
        if port is not None:
            ssl.dockerCmd('docker rm -f appium-' + port)
        docker.deleteRecord()
    except:
        log.loggerError('手动删除Appium_Docker失败')
