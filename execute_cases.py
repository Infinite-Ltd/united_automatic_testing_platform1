from xpathgeter import *
from SeleniumHelper import *
from action_result import *
from output_to_excel import *



def excute_case(helper, logfile, case_number,  case_object, case_dict):
    '''
    执行每条用例,按照每个step拆分，每个action使用try-except包围，方便打详细的日志
    :param case_object: 传入一个测试用例的对象
    :param case_dict: 传入从数据库中读取的测试用例的步骤的字典（{step1:(action,action_name,param,...etc.)）
    :return: 如果执行成功，返回True,否则返回False
    '''
    #使用count记录下当前执行的时第几个step，为第几列
    #case_number = case_number
    column = 4
    for step in case_dict:
        #保存当前页面的源码HTML->Sample.html代码
        helper.get_html_action()
        step_first = str.strip(step[1])
        #time.sleep(10)
        #print('-----'+get_xpath_str(step[2])+'------------')
        # if not get_xpath_str(step[2]):
        #     print('哇哦 没找到xpath呢')
        #判断动作是否为find
        if step_first == 'find':
            case_object.parent_xpath = get_real_parentpath_str(step[2])
            case_object.real_flag = False
            if case_object.parent_xpath == '':
                case_object.parent_xpath = helper.get_frame_html_action(step[2], case_object)
            #column += 1
            time.sleep(1)
            #continue
        #判断动作是否为click
        elif step_first == 'click':
            try:

                helper.get_html_action()
                #time.sleep(2)
                xpath = get_xpath_str(step[2], case_object.parent_xpath, case_object.real_flag)
                print("xpath :"+xpath)
                #如果xpath没找到，到frame里面去寻找
                if xpath == '':
                    xpath = helper.get_frame_html_action(step[2], case_object)
                print('点击动作，点击' + step[2])
                helper.click(xpath)
            except Exception as e:
                traceback.print_exc()
                logfile.write_result(case_number, column, "点击"+step[2]+'的时候出错')
                return False
            if not is_success(step[4]):
                logfile.write_result(case_number, column, '点击'+step[2]+'失败了')
                return False
        #判断动作是否为send_key
        elif step_first == 'sendkeys':
            try:
                xpath = ''
                #if case_object.real_flag:
                helper.get_html_action()
                # time.sleep(2)
                xpath = get_xpath_str(step[2], case_object.parent_xpath, case_object.real_flag)
                # 如果xpath没找到到iframe中去寻找
                if not xpath:
                    xpath = helper.get_frame_html_action(step[2], case_object)
                print('输入动作，在' + step[2])
                #else:
                #xpath = case_object.parent_xpath
                helper.send_key(xpath, step[3], case_object)
            except Exception as e:
                #traceback.print_exc()
                logfile.write_result(case_number, column, '在'+step[2]+'里输入文字'+step[3]+'时出错')
                return False
        #判断动作是否为select
        elif step_first == 'select':
            try:
                helper.get_html_action()
                xpath = get_xpath_str(step[2], case_object.parent_xpath, case_object.real_flag)
                # 如果xpath没找到到iframe中去寻找
                if not xpath:
                    xpath = helper.get_frame_html_action(step[2], case_object)
                print('选择动作，在' + step[2])
                helper.select(xpath, step[3])
            except Exception as e:
                traceback.print_exc()
                logfile.write_result(case_number, column, '在'+step[2]+'下拉列表中选择'+step[3]+'的时候出错')
                return False
        elif step_first == 'clickcheckbox':
            try:
                helper.get_html_action()
                xpath = get_xpath_str(step[2], case_object.parent_xpath, case_object.real_flag)
                if not xpath:
                    xpath = helper.get_frame_html_action(step[2], case_object)
                print('点击checkbox'+step[2])
                helper.clickcheckbox(xpath)
            except Exception as e:
                traceback.print_exc()
                logfile.write_result(case_number, column, '在点击'+step[2]+'的CheckBox时出错')
                return False
        elif step_first == 'result':
            try:
                helper.get_html_action()
                xpath = get_xpath_str(step[2], case_object.parent_xpath, case_object.real_flag)
                if not xpath:
                    xpath = helper.get_frame_html_action(step[2], case_object)
                print('检查标志：'+step[2]+'是否存在')
                if xpath == '':
                    logfile.write_result(case_number, column, step[2]+'未找到')
                    return False
            except Exception as e:
                logfile.write_result(case_number, column, "在寻找"+step[2]+'的时候出错')
        time.sleep(1)
        helper.driver.switch_to.default_content()
        #@@@省略一万行代码。。。。。
        column += 1
    #如果执行的过程没有任何异常，即全部成功，就返回True
    return True

# def is_signal_exist(signal_name):
#     xpath = get_xpath_str(signal_name, )