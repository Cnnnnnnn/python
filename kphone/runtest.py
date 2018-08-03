# coding=utf-8
'''
Created on 2017-11-10
@author: cnn
Project:编写Web测试用例
'''

import unittest
from test_case import test_orderAdd
from test_case import test_orderList
from lib import HTMLTestRunner_cn
import os


# 构造测试集
def Suite1():
    suite = unittest.TestSuite()
    suite.addTest(test_orderAdd.AddTest('test_orderAdd_empty'))
    suite.addTest(test_orderAdd.AddTest('test_orderAdd_full'))
    return suite


def Suite2():
    suite = unittest.TestSuite()
    suite.addTest(test_orderList.ListTest('test_orderList'))
    return suite


def Suite_All():
    all_test = unittest.TestSuite((Suite1(), Suite2()))
    return all_test


if __name__ == '__main__':
    filename = os.getcwd() + '/report/result.html'
    fp = open(filename, 'wb')
    
    runner = HTMLTestRunner_cn.HTMLTestRunner(
        stream=fp,
        title='测试结果',
        description='测试报告.'
    )

    # 执行测试
    # runner = unittest.TextTestRunner()
    # unittest.TextTestRunner(failfast=True) # 只要遇到fail就停止运行
    runner.run(Suite1())
    fp.close()
