#!/usr/bin/env python
# -*- coding:utf-8 -*-
import paramiko
import time


# ssh连接linux服务器
def ssh(sys_ip, username, password, cmds):
    try:
        # 创建ssh客户端
        client = paramiko.SSHClient()
        # 第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 密码方式远程连接
        client.connect(sys_ip, 22, username=username, password=password, timeout=20)
        # 执行命令
        stdin, stdout, stderr = client.exec_command(cmds)
        # 获取命令执行结果,返回的数据是一个list
        result = stdout.readlines()
        return result
    except Exception as e:
        print(e)
    finally:
        client.close()


# Appium服务进行Docker命令重启
def dockerRestart(port):
    sys_ip = "10.100.1.1"
    username = "root"
    password = "123"
    cms = "docker run --name appium-{0} -d -v /home/admin/mapping.json:/root/mapping.json -v /home/admin/appium/test.keystore:/root/test.keystore -v /home/admin/ChromeDriver:/root/webview --net host --privileged appium/appium:1.12.0-p0 appium -a 10.100.1.1 -p {1}".format(
        port, port)
    # print(cms)
    ssh(sys_ip, username, password, cms)


def dockerCmd(commands):
    sys_ip = "10.100.1.1"
    username = "root"
    password = "123"
    # cmds = "docker stop appium-4723"
    cmds = commands
    result = ssh(sys_ip, username, password, cmds)
    # print(result)
    return result
