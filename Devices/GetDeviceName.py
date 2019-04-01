#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

sys.path.append("..")
from Devices.GetDevices import *


# list[0]
def getDeviceName(serial):
    deviceName = connectDevice(serial)
    return deviceName


getDeviceName(sys.argv[1])
