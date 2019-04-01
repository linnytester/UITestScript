#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from BaseUtil.B2cUtil import *
import os
import io

if os.path.isfile("./report/result.json") is True:
    with io.open('./report/result.json', 'r', encoding='utf-8') as behave_json:
        cucumber_json = convert(json.load(behave_json))
        file = io.open('./report/result.json', 'w', encoding='utf-8')
        json.dump(cucumber_json, file, ensure_ascii=False)
        file.close()
        print('result.json格式化完成')
else:
    print('result.json文件不存在')

