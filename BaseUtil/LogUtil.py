#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 创建一个日志器logger并设置其日志级别为DEBUG
import logging
import sys

logger = logging.getLogger('TuanDai_UiTest')
logger.setLevel(logging.DEBUG)

# 创建一个流处理器handler并设置其日志级别为DEBUG
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# 创建一个格式器formatter并将其添加到处理器handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)


def loggerInfo(string):
    logger.info(string)


def loggerError(string):
    logger.error(string)
