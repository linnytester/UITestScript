#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os

sys.path.append("..")
from Devices import GetDevices as device
from Devices import DeviceRecord as dr

dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def delete():
    serial = dr.getRecord(dir)
    if serial is not None:
        device.deleteDevice(serial)


# delete()
