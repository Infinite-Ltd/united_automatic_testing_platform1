#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SeleniumHelper import SeleniumHelper
from testcase import TestCase


def login(username='admin', password='123456'):
    sh.send_key('//*[@id="userCode"]', username)
    sh.send_key('//*[@id="password"]', password)
    sh.click('//*[@id="loginButton"]')




if __name__ == '__main__':
    url = r'http://172.16.0.229:8080/sdms/home/home'


    sh = SeleniumHelper()
    sh.load(url)
    login(username='admin',password = '123456')

