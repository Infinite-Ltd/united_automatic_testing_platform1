#coding=utf-8
# File name: main_program.py
# Author:   苗佳艺 姜福良    Version: R1.0      Date: 2018/3/30
# Description:   // 与主控通信获取需执行的用例编号；读取数据库中用例对应元素；执行用例；判断结果并返回给主控。
# Others:        // 3.30新增功能暂未验证
# Function List: // class（动作函数）、class（用例类）、class（创建用例线程）、class（执行用例线程）
# History:       // 3.30 修改通过关键字读取数据库； 增加Action wait动作； 增加try动作，当出现xpath等其他因素引起的动作无法继续执行的异常时，回复主控False；
#                   4.2  修改如果出现false，停止后续动作的执行，让给主控回复false结果
#                   4.10 修改查询N的结果判断
from urllib.request import localhost
from selenium import webdriver
import unittest
import time
from queue import Queue
import threading
import pymysql
import socket
import json
import logging
import logging.handlers
import datetime
import traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

mControlAddr =("10.110.36.220", 8001)                #执行完用例后，给主控回复结果，给主控发送json的IP及端口号
sendToTonyAddr = ("10.110.36.202", 1209)             #每一次向Tony模块通信，给Tony发消息的IP及端口号

class action:
    def __init__(self,element,driver):
        self.element = element
        self.driver = driver

    def execAction(self):
        pass

    def getHtmlAction(self,driver):
        try:
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
            print("跳转页面ok")
        except Exception as m:
            print("获取ing")

        time.sleep(1)
        pageSource = self.driver.page_source
        fh = open('INMindex.html', 'w', encoding='utf-8')
        fh.write(pageSource)
        fh.close()
        print("生成html成功")

class mouseClickAction(action):
    def __init__(self,element,driver):
        super(mouseClickAction,self).__init__(element,driver)

    def execAction(self,elementName):
        print('exec mouse click action:%s' %(elementName))
        self.driver.find_element_by_xpath(elementName).click()
        self.driver.implicitly_wait(1)
        super().getHtmlAction(self)

class InputAction(action):
    def __init__(self,element,driver,value):
        super(InputAction,self).__init__(element,driver)
        self.value = value

    def execAction(self,elementName):
        print("exec input action:%s" %(elementName))
        try:
            self.driver.find_element_by_xpath(elementName).clear()                                 #3.14新增 clear输入窗口
            self.driver.find_element_by_xpath(elementName).send_keys(self.value)
        except :
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
            self.driver.find_element_by_xpath(elementName).clear()                                 # 3.14新增 clear输入窗口
            self.driver.find_element_by_xpath(elementName).send_keys(self.value)
        super().getHtmlAction(self)

class select(action):
    def __init__(self, element, driver, value):
        super(select, self).__init__(element, driver)
        self.value = value

    def execAction(self,elementName):
        print('exec select atcion:%s' %(elementName))
        sel = self.driver.find_element_by_xpath(elementName)
        Select(sel).select_by_visible_text(self.value)
        super().getHtmlAction(self)

class wait(action):                                  #3.30新增 Action wait动作  ，用于等待n秒，n为用例中value对应值
    def __init__(self, element, driver, value):
        super(wait, self).__init__(element, driver)
        self.value = value

    def execAction(self,elementName):
        print('exec wait atcion:%s' %(self.value))
        time.sleep(self.value)
        # super().getHtmlAction(self)              #wait动作暂时不需要获取html及与主程序通信

class QueryAction(action):
    def __init__(self, element, driver, value):
        super(QueryAction, self).__init__(element, driver)
        self.value = value
    def execAction(self):
        print('exec query atcion:%s' %(self.element))
        #3.22新增 通过读取html文件，查询其中是否有element字段
        time.sleep(1)
        pageSource = self.driver.page_source
        fh = open('INMindex.html', 'w', encoding='utf-8')
        fh.write(pageSource)
        fh.close()

        htmlFile = open(r"E:/IotAutoTest/MjyPython/INMindex.html",'r', encoding='UTF-8')
        content = htmlFile.read()
        a = content.find(self.element)

        ###打印日志部分
        f_handler = logging.FileHandler('iot_test.log')
        f_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(f_handler)
        if(a!=-1):
            print("ok该条用例通过了")
            logger.debug('success' )
            return "Succeed"
            ###----------------------------
        if(a==-1):
            print("no该条用例不通过")
            logger.debug('failed')
            return "Fail"

#新增 查询动作  “查询yes”认为 ，有该元素则此条用例通过。 “查询yes”-----------QueryAction
#新增 查询动作  “查询no”认为，无该元素则此条用例通过。   “查询no”----------- QueryNoAction
class QueryNoAction(action):
    def __init__(self, element, driver, value):
        super(QueryNoAction, self).__init__(element, driver)
        self.value = value
    def execAction(self):
        print('exec query atcion:%s' %(self.element))
        super().getHtmlAction(self)
        htmlFile = open(r"E:/IotAutoTest/MjyPython/INMindex.html",'r', encoding='UTF-8')
        content = htmlFile.read()
        a = content.find(self.element)
        ###打印日志部分
        f_handler = logging.FileHandler('iot_test.log')
        f_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(f_handler)
        if(a!=-1):                                        #4.10 修改查询结果的反馈
            print("no该条用例不通过")
            logger.debug('Fail' )
            return "Fail"
            ###----------------------------
        if(a==-1):
            print("ok该条用例通过了")
            logger.debug('Succeed')
            return "Succeed"
###------------------------分隔符--------------------以上为动作函数--------------------


#用例类
class TestCase:
    def __init__(self,driver,data=None,respondDate=None):
        self.actionList = []
        self.driver = driver
        self.actions = data
        self.elementList = None
        self.respondDate=respondDate
        print(self.respondDate)
        for action in self.actions:
            #创建两个Action 第一个执行Action 第二个做检查Action
            execAction = self.creatAction(action[:3])
            checkAction = self.creatAction(action[3:6])
            twoAction = [execAction,checkAction]
            self.actionList.append(twoAction)

    def exec(self):
        print("run action")
        for action in self.actionList:
            elementName = self.updataElementList(action[0].element)
            try:                               #3.30新增 每一个动作的执行使用try，如果因xpath提供错误或其他因素导致无法执行，则给主控回复False
                action[0].execAction(elementName)
                self.checkUdp()
                if action[1]!=None:
                    result = action[1].execAction()
                    print("-----------------------------"+result) #4.10调试用 可删
                    if result == 'Fail':
                        self.respondToMaster("Fail")
                        return
            except:
                print("!!!!!THIS IS FALSE!!!!!")    #3.30新增 如果出现false，将该异常保存在false_log文本文件中
                f = open("false_log.txt", 'a')
                # f.write(caseQueue)                     #4.9新增 打印false日志时打印出用例信息
                traceback.print_exc(file=f)
                f.flush()
                f.close()
                self.respondToMaster("False")
                return                               #4.2新增  如果出现false，停止后续动作的执行，让给主控回复false结果
        self.respondToMaster("Succeed")

    def respondToMaster(self,result):
        self.driver.refresh()                          #3.28新增 查询操作后 刷新界面
        print("refresh success 123456")
        rawDate=self.respondDate.decode()
        rawJson = json.loads(rawDate)
        rawJson["srcName"]="INM"
        rawJson["dstName"]="mControl"
        rawJson["fun_code"] = "endExec"
        rawJson["execResult"]=result
        respondJdson = json.dumps(rawJson)
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.sendto(respondJdson.encode(), mControlAddr)
        print(rawJson)                                 #4.9新增 打印出回复主控的内容
        print("Done, have respond to master ")
        time.sleep(1)
        soc.close()

    def checkUdp(self):
        # 定义socket通信类型 ipv4，udp
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.bind(("10.110.36.202", 1213))
        soc.sendto('again'.encode(), sendToTonyAddr)
        data, addr = soc.recvfrom(1024)
        if data.decode() == 'ACK':
            print("通信成功")
        time.sleep(1)
        soc.close()

    def creatAction(self,action):
        print(action)
        newAction = None
        if action[0] == 'click':
            newAction = mouseClickAction(action[1],self.driver)
        elif action[0] == 'input':
            newAction = InputAction(action[1],self.driver,action[2])
        elif action[0] == 'select':
            newAction = select(action[1],self.driver,action[2])
        elif action[0] == 'wait':
            newAction = wait(action[1], self.driver, action[2])
        elif action[0] == '查询':                                                #查询 默认为有就是通过
            newAction = QueryAction(action[1],self.driver,action[2])
        elif action[0] == '查询N':
            newAction = QueryNoAction(action[1],self.driver,action[2])
        return newAction

    def updataElementList(self,element):
        conn = pymysql.Connect(host='8.8.8.155', port=3306, user='root', passwd='root', db='iot_auto_test', charset='UTF8')
        cursor = conn.cursor()
        sql = "select * from tony_test"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.elementList = result
        cursor.close()
        conn.close()

        for name in result:
            if name[0] == element:
                return name[1]
#用例类

##-----------------------------以上是类的分隔符----------------------------------



##-----------------------------以下是线程开始-------------------------------------

#创建用例线程
class CreatTestCase(threading.Thread):
    def __init__(self,caseQueue):
        threading.Thread.__init__(self)
        self.pCaseQueue = caseQueue

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("10.110.36.202", 1111))

        #链接数据库
        self.conn = pymysql.Connect(host='8.8.8.155', port=3306, user='root', passwd='root', db='iot_auto_test', charset='UTF8')
        self.cursor = self.conn.cursor()

        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()                     # 全屏
        self.driver.get('http://8.8.8.1:18086/INM/hytera/index.html')
        self.driver.find_element_by_id("usename").clear()
        self.driver.find_element_by_id("usename").send_keys("Eadmin")
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys("admin123")
        self.driver.find_element_by_id("button_login_Id").click()

        ##在执行用例之初，首先获取一次页面的html文件。以获得第一个用例第一步元素的xpath。
        pageSource = self.driver.page_source
        fh = open('INMindex.html', 'w', encoding='utf-8')
        fh.write(pageSource)
        fh.close()
        print("生成html成功")

        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc.bind(("10.110.36.202", 1245))
            soc.sendto('Module1_0001'.encode(), sendToTonyAddr)
            data, addr = soc.recvfrom(1024)
            if data.decode() == 'ACK':
                print("首次与tony通信成功")
            time.sleep(1)
            soc.close()
        except:
            print("第一次与tony通信 error")
            quit()

    def run(self):
        print('CreatTestCase Running')
        while True:
            data, addr = self.s.recvfrom(1024)
            if data.decode() != 'ACK':
                respondData = data
                caseName =  self.processReceiveData(data, addr)
                caseNamet = caseName
                self.s.sendto(caseNamet.encode(),sendToTonyAddr)
            else:
                caseparm = self.readCaseFromSql(caseName)
                print("11111111")
                print(caseparm)
                case = TestCase(self.driver,caseparm,respondData)
                self.pCaseQueue.put(case)

    def processReceiveData(self,data,addr):
        rawData = data.decode()
        print(rawData)       #打印json包
        rawJson = json.loads(rawData)
        print(rawJson)       #将json格式数据转换为字典
        caseName = rawJson["caseNumber"]
        rawJson["srcName"]="INM"
        rawJson["dstName"]="mControl"
        rawJson["fun_code"]= "ACK"
        respondJdson = json.dumps(rawJson)
        self.s.sendto(respondJdson.encode(),addr)
        return caseName

    def readCaseFromSql(self,caseName):
        resultList = []
        sql = "select * from INM_Manage WHERE case_id LIKE '%%%s%%'" %(caseName)      #3.30新增 通过用例编号，找到有该编号关键字的对应6行数据表
        self.cursor.execute(sql)              #执行数据库操作
        result=self.cursor.fetchall()         #接受全部的返回结果行
        caseAction = result[0]
        case = result[1]
        caseValue = result[2]
        checkAction = result[3]
        checkCase = result[4]
        checkValue = result[5]
        for i in range(len(caseAction)):              #len()计算caseAction的个数，range()在for中根据给定的次数，重复动作
            if i == 0:
                continue
            if caseAction[i] == None:
                continue
            else:
                list = [caseAction[i],case[i],caseValue[i],checkAction[i],checkCase[i],checkValue[i]]
                resultList.append(list)               # append() 方法用于在列表末尾添加新的对象

        sql = "select * from tony_test"
        self.cursor.execute(sql)
        result2 = self.cursor.fetchall()
        '''
        print(result2)
        for i in result2:
            for j in resultList:
                if i[0] == j[1]:
                    j[1] = i[1]

                if i[0] == j[4]:
                    j[4] == i[1]
        '''
        resultList.reverse()                           # reverse() 对列表的元素进行反向排序。
        return resultList
#创建用例线程

##---------------------------------------------------线程的分隔符--------------------------------------

#执行用例线程
class RunTest(threading.Thread):

    def __init__(self,caseQueue):
        threading.Thread.__init__(self)
        self.cCaseQueue = caseQueue

    def run(self):
        print('RunTest Running')
        while True:
            if not self.cCaseQueue.empty():
                case = self.cCaseQueue.get()
                case.exec()
#执行用例线程



if __name__ == '__main__':
   caseQueue = Queue()
   creatThread = CreatTestCase(caseQueue)
   RunThread = RunTest(caseQueue)
   creatThread.start()
   RunThread.start()

