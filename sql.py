#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#数据库连接/建表/操作
import pymysql
#import xlwt
import traceback
# db = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", charset='utf8')
# cur = db.cursor()

def sql(cur, casenumber):
    # #打开数据库连接（ip、用户名、密码、数据库名）
    # db = pymysql.connect(host ="localhost", port = 3306, user = "root",passwd = "root",charset = 'utf8')
    # #使用cursor()创建游标对象cursor
    # cur = db.cursor()
    #sql语句
    sql = "SELECT * FROM testcase.testcase_step where testcaseid = "+ str(casenumber) +"  order by abs(idtestcase_step);"
    try:
        # 执行sql语句
        cur.execute(sql)
        data = cur.fetchall()
        #print(data[0][0])  # 返回结果是字典
        return data
    except:
        traceback.print_exc()
        # 如果发生错误
        #print('执行sql出错')
        return print('执行sql出错')
    # 关闭数据库连接
    # db.close()

# sql()