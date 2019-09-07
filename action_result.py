from xpathgeter import get_xpath_str
import traceback

def is_success(step_3):
    '''
    判断是否step下面有成功的提示，如果有的话，则判断是否单个step是否执行成功了
    :param step_3: 传入成功与否的标志
    :return: 成功：True, 失败：False
    '''
    success_flag = True
    if step_3 != '':
        success_flag = (get_xpath_str(step_3) != '')
    else:
        pass
    return success_flag

