import lxml
from lxml import etree
import codecs
#from SeleniumHelper import SeleniumHelper
import time

HTML_file = codecs.open('Sample.html', 'r', 'utf-8')
HTML_contents = HTML_file.read()
html = etree.HTML(HTML_contents)
#helper = SeleniumHelper()

def get_xpath_str(widget_name, parent_xpath='', real_flag=True):
    '''
    @author:Mr.None
    @date:2018-4-27
    :param widget_name: 输入的参数的文本

    :return: 控件相应的xpath
    '''
    HTML_file = codecs.open('Sample.html', 'r', 'utf-8')
    HTML_contents = HTML_file.read()
    html = etree.HTML(HTML_contents)

    widget_name = str.strip(widget_name)
    #判断iframe的个数
    #iframe_list = get_xpath_from_iframe(html)
    #返回xpath的几种方式
    value_xpath = "//body//div//*[@value='"+widget_name+"']"
    rough_text_xpath = "//body//div//*[contains(text(), '"+widget_name+"')]"
    text_xpath = "//body//div//*[text()='"+widget_name+"']"

    #xpath_list = []
    real_xpath = ''

    # 页面上只有一个widget_name对应的元素
    if html.xpath(value_xpath):
        # xpath_list.append(value_xpath)
        real_xpath = value_xpath
    # 页面是只有一个text对应的元素
    elif html.xpath(text_xpath):
        # xpath_list.append(text_xpath)
        real_xpath = text_xpath
    elif html.xpath(rough_text_xpath):
        real_xpath = rough_text_xpath
    else:
        print('没有找到'+widget_name+"的xpath")
        HTML_file.close()
        #return real_xpath
    # 判断是否找到多个xpath，如果没有，这直接返回一个xpath，如果有，则精确定位
    # if len(xpath_list)>1:
    #     pass
    HTML_file.close()
    #if real_xpath != '':
    if real_flag:
        print("找到"+widget_name+"的xpath: "+real_xpath)
        return real_xpath
    else:
        print("以精确定位，找到"+widget_name+"的xpath: "+parent_xpath + real_xpath.split("body")[1])
        return parent_xpath + real_xpath.split("body")[1]



def get_real_parentpath_str(find_key):
    '''
    获取父节点的路径
    :param find_key:要寻找的控件的名称
    :return: 寻找的控件的父控件的xpath
    '''
    #value_xpath = "//body//*[@value='" + find_key + "']"
    HTML_file = codecs.open('Sample.html', 'r', 'utf-8')
    HTML_contents = HTML_file.read()
    html = etree.HTML(HTML_contents)

    find_key = str.strip(find_key)
    #根据页面规则，写下两条设定好的xpath模板
    #模板一
    value_xpath = "//body//div//*[@value='" + find_key + "']"
    #模板二
    text_xpath = "//body//div//*[contains(text(), '" + find_key + "')]"

    rough_xpath = ''

    #如果可以根据模板一找到元素的xpath，则记录该xpath
    if html.xpath(value_xpath):
        rough_xpath = value_xpath

    #如果可以根据模板二找到元素的xpath，则记录该xpath
    elif html.xpath(text_xpath):
        rough_xpath = text_xpath
    #上述条件都不满足，则返回空的xpath
    else:
        print("没有找到"+find_key+'的父节点的xpath')
        HTML_file.close()
        return rough_xpath
    HTML_file.close()
    print("找到"+find_key+"的父节点的xpath为："+rough_xpath+'/..')
    return rough_xpath+'/..'

def get_all_frame_xpath():

    HTML_file = codecs.open('Sample.html', 'r', 'utf-8')
    HTML_contents = HTML_file.read()
    html = etree.HTML(HTML_contents)
    i = 0
    #frame_xpath = '//body//div//following::iframe['+i+']'
    frames = []
    count = 0
    if i in range(15):
        print('XXXXXXXXXXXXXX')
        if html.xpath('//body//div//following::iframe['+str(i)+']'):
            print('yes')

            frames.append('//body//div//following::iframe['+str(i)+']')
            count += 1
    HTML_file.close()
    return frames


# def get_xpath_from_iframe(tree):
#     iframe_xpaths = []
#     count = 1
#     xpath = "//body//iframe["+str(count)+"]"
#     while tree.xpath("//body//iframe["+str(count)+"]"):
#         iframe_xpaths.append(xpath)
#         count += 1
#     return iframe_xpaths

# def get_frame_html_actioner(helper, actionname, testcase):
#     xpath = ''
#     helper.get_html_action(True, 'ztreeframe')
#     time.sleep(3)
#     xpath = get_xpath_str(actionname, testcase.parent_xpath, testcase.real_flag)
#     if xpath == '':
#         helper.driver.switch_to.default_content()
#         time.sleep(2)
#         helper.get_html_action(True, 'mainframe')
#         time.sleep(3)
#         xpath = get_xpath_str(actionname, testcase.parent_xpath, testcase.real_flag)
#         #self.driver.switch_to.default_content()
#         return xpath
#     return xpath
'''
test code:
'''
#print(get_real_xpath_str('66989401'))
#print(get_xpath_str(, get_, False))
#print(get_xpath_str('姓名/警号'))