#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#相关动作帮助

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from xpathgeter import get_xpath_str
from xpathgeter import get_real_parentpath_str
from xpathgeter import get_all_frame_xpath
from testcase import TestCase
import time
import os
import traceback
#from action import action

class SeleniumHelper:
    def __init__(self, frames=None):
        ie_driver = r"C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe"
        #ie_driver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        if not os.path.exists(ie_driver):
            ie_driver = r"C:\Program Files\Internet Explorer\IEDriverServer.exe"
        self.driver = webdriver.Ie(ie_driver)
        #self.url = r'http://172.16.0.229:8080/sdms/home/home'
        self.frames = frames
        #self.url = r'http://172.16.0.188/'
        self.url = r'https://www.baidu.com/'

    #关闭浏览器
    # def close(self):
    #     time.sleep(3)
    #     self.driver.close()

    #加载浏览器
    def load(self, url, seconds=1):
        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(seconds)

    #登录系统
    def login(self, username='ll', password='123456'):
        self.load(self.url)
        #self.driver.find_element_by_xpath("//input[@id='username']").send_keys(username)
        self.driver.find_element_by_xpath("//*[@src_id='username']").clear()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@src_id='username']").send_keys(username)
        time.sleep(3)
        #self.driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
        self.driver.find_element_by_xpath("//*[@src_id='password']").clear()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@src_id='password']").send_keys(password)
        time.sleep(3)
        #self.send_key('//*[@id="password"]', password)
        #self.click('//*[@id="submitId"]')
        self.click("//*[contains(text(),'登')]")
    #保存页面源代码
    def get_html_action(self, frame_flag=False, framename=''):
        '''
        :param frame_flag: 是否需要跳转到frame
        :param framename: frame的id/name
        :return:
        '''
        try:
            # print(self.driver.current_window_handle)
            # print(len(self.driver.window_handles))
            # if len(self.driver.window_handles) > 1:
            #     print(len(self.driver.window_handles)+self.driver.window_handles[1])
            #     self.driver.switch_to.window(self.driver.window_handles[1])
            if frame_flag:
                self.driver.switch_to.frame(framename)
                print("跳转页面ok")
                pageSourceframe = self.driver.page_source
                #print(pageSourceframe)
        except Exception as m:
            print("获取ing")

        #time.sleep(18)
        pageSource = self.driver.page_source
        #print(pageSource)
        fh = open('Sample.html', 'w', encoding='utf-8')
        fh.write(pageSource)
        time.sleep(2)
        fh.close()
        print("生成html成功")
        #time.sleep(1)

    def get_frame_html_action(self, actionname, testcase):
        print("死鬼，外面没找到才进来找我~~")
        frames = self.frames
        #print(frames)
        xpath = ''
        #frames = get_all_frame_xpath()
        print(frames)
        for frame in frames:
            print(frame)
            self.get_html_action(True, frame)
            time.sleep(1)
            if testcase.real_flag:
                xpath = get_xpath_str(actionname, testcase.parent_xpath, testcase.real_flag)
            else:
                xpath = get_real_parentpath_str(actionname)

            if xpath == '':
                self.driver.switch_to.default_content()
                print("@@@@@@" + xpath)
                raise Exception()
        return xpath
        # self.get_html_action(True, 'ztreeFrame')
        # time.sleep(1)
        # if testcase.real_flag:
        #     xpath = get_xpath_str(actionname, testcase.parent_xpath, testcase.real_flag)
        # else:
        #     xpath = get_real_parentpath_str(actionname)
        # if xpath == '':
        #     self.driver.switch_to.default_content()
        #     #time.sleep(1)
        #     self.get_html_action(True, 'mainFrame')
        #     #time.sleep(1)
        #     if testcase.real_flag:
        #         xpath = get_xpath_str(actionname, testcase.parent_xpath, testcase.real_flag)
        #     else:
        #         xpath = get_real_parentpath_str(actionname)
        #     #self.driver.switch_to.default_content()
        #     return xpath
        # return xpath


    # def get_frame_html_action(self, actionname, testcase):
    #     print("死鬼，外面没找到才进来找我~~")
    #     xpath = ''
    #     self.get_html_action(True, 'ztreeFrame')
    #     time.sleep(1)
    #     xpath = get_xpath_str(actionname, testcase.parent_xpath, testcase.real_flag)
    #     if xpath == '':
    #         self.driver.switch_to.default_content()
    #         #time.sleep(1)
    #         self.get_html_action(True, 'mainFrame')
    #         #time.sleep(1)
    #         xpath = get_xpath_str(actionname, testcase.parent_xpath, testcase.real_flag)
    #         #self.driver.switch_to.default_content()
    #         return xpath
    #     return xpath

    #刷新页面
    def refresh(self):
        self.driver.refresh()

    #清除之前输入的用户名和密码
    def clear(self, name, seconds = 1.0):
        element = self.driver.find_element_by_id(name)
        element.clear()
        time.sleep(seconds)

    #点击
    def click(self, xpath, seconds = 2):
        if xpath == '':
            print('click没有元素')
        else:
            element = self.driver.find_element_by_xpath(xpath)
            #ActionChains(self.driver).click(element).perform()
            element.click()
            time.sleep(seconds)


    #赋值
    def send_key(self, xpath, str, caseobject, seconds = 2):
        #输入输入框的xpath会在文字的左、右侧，此时需要获取准确的输入框位置
        #如果real_flag为true，则没有使用find方法，反之则使用
        # if caseobject.real_flag:
        #     xpath = xpath + "/following::input[1] | preceding-sibling::input[1]"
        # else:
        xpath = xpath + "/..//input[1]"
        print(xpath)
        element = self.driver.find_element_by_xpath(xpath)
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(str)
        time.sleep(seconds)

    #输入完值之后点击enter键
    def send_key_ex(self, xpath, str, seconds = 1.0):
        element = self.driver.find_element_by_xpath(xpath)
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(str)
        element.send_keys(Keys.ENTER)
        time.sleep(seconds)

    #鼠标移动至某一个元素
    def hover(self, xpath, seconds = 1.0):
        element = self.driver.find_element_by_xpath(xpath)
        ActionChains(self.driver).move_to_element(element).build().perform()
        time.sleep(seconds)

    #处理下拉框
    def select(self, xpath, text, seconds = 1):
        xpath = xpath + '/..//select[1]'
        element = self.driver.find_element_by_xpath(xpath)
        #Select(element).select_by_value(index)
        Select(element).select_by_visible_text(text)
        time.sleep(seconds)

    #跳转页面？
    def switch_frame(self, id, seconds = 1.0):
        self.driver.switch_to.frame(id)
        time.sleep(seconds)

    #切换页面?
    def default_frame(self, seconds = 1.0):
        self.driver.switch_to.default_content()
        time.sleep(seconds)

    #上传文件
    def upload_file(self):
        pass

    #点击单选框
    def clickcheckbox(self, xpath):
        '''
        :param xpath:需要返回输入元素父节点的xpath，调用get_parent_xpath方法
        :return:
        '''
        xpath = xpath + "//input[@type='checkbox']"
        self.click(xpath)

    #判断是否新建操作成功，
   # def is_save_success(self):
   #  def to_current(self):
   #      self.driver.switch_to.window(self.driver.window_handles[1])
   #      self.driver.window_handles
# selenium = SeleniumHelper()
# driver = selenium.driver
# selenium.login()
# time.sleep(15)
# driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
# #selenium.
# str1 = "//*[@id='topMenuDiv']/div[7]"
# str2 = "//*[@id='JCXX_ID']/span[3]"
# str3 = "//*[@id='searchtable']/tbody/tr/td[1]/text()[1]"
# # str3 = "//*[@id='searchtable']/tbody/tr/td[2]/input[1]"
# qwtj = driver.find_element_by_xpath(str1)
#
# #xz   = driver.find_element_by_xpath(str3)
# qwtj.click()
# time.sleep(4)
# jltj = driver.find_element_by_xpath(str2)
# jltj.click()
# time.sleep(4)
# selenium.send_key(str3, '123456')