#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

sys.path.append("..")
from Devices.GetDevices import *


# list[0]
def getPlatformVersion(serial):
    s = getDeviceInfo(serial)
    platformVersion = s["device"]["version"]
    return platformVersion


getPlatformVersion(sys.argv[1])
