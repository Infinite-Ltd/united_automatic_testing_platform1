from output_to_excel import *
from execute_cases import excute_case
import pymysql
from sql import sql
from testcase import TestCase
from SeleniumHelper import SeleniumHelper
from configparser import *
# import lxml
# from lxml import etree
# import codecs


class AutomaticPlatform:

    def __init__(self, run_flag=True):
        self.run_flag = run_flag

    def start_execute_case(self):
        '''
        用户操作启动程序
        :return:无返回值
        '''
        # HTML_file = codecs.open('Sample.html', 'r', 'utf-8')
        # HTML_contents = HTML_file.read()
        # html = etree.HTML(HTML_contents)
        frames = []
        #创建一个读取ini文件的对象
        configparser = ConfigParser()
        configparser.read('frame.ini')
        for frame in configparser['framenames'].values():
            frames.append(frame)
        #新建一个动作执行者对象
        print(frames)
        helper = SeleniumHelper(frames)
        #打开网址登录系统
        try:
            helper.login()
            time.sleep(20)
        except Exception as e:
            pass
        time.sleep(4)
        # 首先创建一个新的保存测试结果的Excel文件，命名规则为：启动系统日期--test_result.xlsl
        logfile = Logfile()
        logfile.read_file()
        logfile.init_excel()
        print(logfile.wb)
        #testcase = TestCase()
        case_number = 2
        # @@@连接数据库，获得数据库连接
        # 打开数据库连接（ip、用户名、密码、数据库名）
        #db = pymysql.connect(host="10.110.15.25", port=3306, user="test", passwd="123456", charset='utf8')
        # 使用cursor()创建游标对象cursor
        #cur = db.cursor()
        print('连上数据库了')
        #不断获取run_flag的状态，已确定是否需要停止用例的执行
        while True:

            #dict = 获取一个用例的信息的方法：返回一个字典
            dict = ()
            #获取到的dict赋值给testcase的dict、name属性

            #testcase.datatuple, testcasename = sql(cur, case_number), sql(cur, case_number)[0][5]
            #datatuple = sql(cur, case_number-1)
            # datatuple = (('1', 'click', '勤务设置', '', '', '修改组别管理', '1'), ('2', 'click', '组别管理', '', '', '', '1'),
            #              ('3', 'click', '新增', '', '', '', '1'), ('4', 'click', '请选择', '', '', '', '1'),
            #              ('5', 'find', '简海波', '', '', '', '1'), ('6', 'clickcheckbox', '', '', '', '1'),
            #              ('7', 'click', '确定' , '', '', '', '1'), ('8', 'click', '保存', '', '', '', '1'))
            # datatuple = (('1', 'click', '勤务设置', '', '', '修改组别管理', '1'), ('2', 'click', '组别管理', '', '', '', '1'),
            #              ('3', 'click', '新增', '', '', '', '1'), ('4', 'sendkeys', '组别名称', '请选择你的心动女生', '', '', '1'),
            #              ('5', 'click', '保存', '', '', '', '1'), ('6', 'result', '请选择你的心动女生', '', '', '1'))
            datatuple = (('1', 'click', '综合查询', '', '', '查看基础信息', '1'), ('2', 'click', '检查站', '', '', '', '1'),
                         ('3', 'click', '云峰边境检查站', '', '', '', '1'), ('4', 'sendkeys', '姓名/警号', '李鱼龙', '', '', '1'),
                         ('5', 'result', '李鱼龙', '', '', '', '1'), ('6', 'click', '重置', '', '', '1'),
                         ('7', 'click', '查询', '', '', '', '1',), ('8', 'result', '钱勇', '', '', '', '1'))
            #如果用例的数据为空则停止遍历
            if not datatuple:
                print('数据库是空的')
                break
            print(datatuple)
            testcasename = datatuple[0][5]

            dict = datatuple
            #创建测试用例对象
            testcase = TestCase(datatuple, testcasename)
            #写入每一行第一列为测试用例的名称
            logfile.write_result(case_number, 1, case_number-1)
            logfile.write_result(case_number, 2, testcasename)
            #判断用例是否执行成功，执行成功，则在该条日志对应地方写入用例执行通过，否则写入用例执行失败
            if excute_case(helper, logfile, case_number, testcase, dict):
                #helper.driver.switch_to_default_content()
                #time.sleep(2)
                #写入Excel文件的第二个单元格
                print(testcasename+'执行通过')
                logfile.write_result(case_number, 3, '执行通过')
            else:
                #helper.driver.switch_to_default_content()
                print(testcasename+'执行失败')
                logfile.write_result(case_number, 3, '执行失败')
            helper.driver.switch_to_default_content()
            case_number += 1
            time.sleep(1)
            #刷新页面
            helper.refresh()
            break
        #db.close()
        logfile.wb.save(r'D:\testresult\test_result--'+time.strftime('%b-%d-%Y-%H-%M-%S')+'.xlsx')

    def stop_execute_case(self):
        '''
        用户停止执行用例方法
        :return: 无返回值
        '''
        self.run_flag = False

automaticplatform = AutomaticPlatform()
automaticplatform.start_execute_case()
