# -*- coding: utf-8 -*-
"""
Created on 2017-11-10
@author: cnn
Project:编写Web测试用例
"""

import unittest
from test_case import test_fast_order
import HTMLTestRunner_cn
import os


# 构造测试集
def Suite1():
    suite = unittest.TestSuite()
    suite.addTest(test_fast_order.FastOrderTest('test_fast_order_1_open'))
    suite.addTest(test_fast_order.FastOrderTest('test_fast_order_7_set_type'))
    return suite


def Suite2():
    suite = unittest.TestSuite()
    return suite


def Suite_All():
    all_test = unittest.TestSuite((Suite1(), Suite2()))
    return all_test


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    filename = path + '/report/result.html'
    fp = open(filename, 'wb')

    runner = HTMLTestRunner_cn.HTMLTestRunner(
        stream=fp,
        title='测试结果',
        description='测试报告.'
    )
    # 执行测试
    #runner = unittest.TextTestRunner()
    test_dir = './'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')  # 所有测试用例
    runner.run(Suite1())
    fp.close()
