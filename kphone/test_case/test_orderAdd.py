# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from selenium.webdriver.common.keys import Keys
from test_case.login import Login
work_order = '//*[@id="nav"]/div/li[4]'


class AddTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://vip.test.thinkerx.com/")
        cls.accept_next_alert = True
        cls.driver.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_orderAdd_empty(self):
        driver = self.driver
        Login().login(driver, 1)
        driver.find_element_by_xpath(work_order).click()
        driver.find_element_by_xpath('//*[@id="afterService"]/div[1]/div[1]/button[1]').click()
        # 客户信息为空
        self.submit(u'填写有效的客户', "客户信息为空fail")
        # 部门信息为空
        driver.find_element_by_css_selector("input.el-input__inner").clear()  # 客户名称
        driver.find_element_by_css_selector("input.el-input__inner").send_keys(u"测试")
        time.sleep(1)
        driver.find_element_by_css_selector("body > div.el-select-dropdown > div > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li").click()
        time.sleep(2)
        driver.find_element_by_class_name("hiddenTable").click()
        self.submit(u'选择有效的部门', "部门信息为空fail")
        # 产品分类为空
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[4]/div/label[1]').click()  # 部门
        self.submit(u'选择产品类型', "产品分类为空fail")
        # 填写内容为空
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[3]/div').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@x-placement="bottom-start"]/div/div[1]/ul/li[1]').click()
        time.sleep(1)
        self.submit(u'请填写内容', "填写内容为空fail")
        # 联系方式为空
        text1 = driver.find_element_by_xpath('//div[@class="iframe_b"]/div/div/div/div/div/div/div[@class="edui-editor-iframeholder edui-default"]')
        text = text1.find_element_by_tag_name("iframe")
        driver.switch_to_frame(text)
        driver.find_element_by_xpath('//body').send_keys(u"测试")
        driver.switch_to_default_content()
        time.sleep(1)
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[5]/div/input').clear()
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[5]/div/input').send_keys("1")
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[5]/div/input').send_keys(Keys.BACKSPACE)
        self.submit(u'请填写联系方式', "联系方式为空fail")
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[5]/div/input').send_keys("13812345678")

        # 提交工单
        self.driver.find_element_by_xpath('//*[@id="add"]/div[1]/div/section[2]/section/div[5]/button').click()
        time.sleep(10)
        customer = driver.find_element_by_xpath('//div[@class="listBox container-fluid"]/div[@id="tabel_list"]/table/tbody/tr[1]/td[3]/span').text
        product = driver.find_element_by_xpath('//div[@class="listBox container-fluid"]/div[@id="tabel_list"]/table/tbody/tr[1]/td[4]').text
        detail = driver.find_element_by_xpath('//div[@class="listBox container-fluid"]/div[@id="tabel_list"]/table/tbody/tr[1]/td[5]/div/a/p').text
        recorder = driver.find_element_by_xpath('//div[@class="listBox container-fluid"]/div[@id="tabel_list"]/table/tbody/tr[1]/td[6]/span').text
        self.assertTrue(customer == u"测试客户" and product == u"k-phone" and detail == u"测试" and recorder == u"测试售后", u'提交工单fail')

    def test_orderAdd_full(self):  # 填写全部条件
        driver = self.driver
        driver.get("http://vip.test.thinkerx.com/kphone_web/dist/web/#/order")
        driver.find_element_by_xpath('//*[@id="afterService"]/div[1]/div[1]/button[1]').click()
        time.sleep(1)
        driver.find_element_by_css_selector("input.el-input__inner").clear()  # 客户名称
        driver.find_element_by_css_selector("input.el-input__inner").send_keys(u"测试")
        time.sleep(1)
        driver.find_element_by_css_selector("body > div.el-select-dropdown > div > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li").click()
        time.sleep(2)
        driver.find_element_by_class_name("hiddenTable").click()
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[3]/div').click()  # 产品分类
        time.sleep(1)
        driver.find_element_by_xpath('//div[@x-placement="bottom-start"]/div/div[1]/ul/li[1]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[4]/div/label[1]').click()  # 部门
        time.sleep(1)
        driver.find_element_by_xpath("(//input[@type='text'])[6]").send_keys(u"测试售后")
        time.sleep(1)
        driver.find_element_by_xpath('//div[@x-placement="bottom-start"]/div/div[@class="el-select-dropdown__wrap el-scrollbar__wrap"]/ul/li[1]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[9]/div').click()  # 预计交货时间
        time.sleep(1)
        self.timeSelect('//div[@x-placement="bottom-start"]')
        time.sleep(1)
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[10]/div').click()  # 客户要求完成时间
        time.sleep(1)
        self.timeSelect('//div[@x-placement="top-start"]')
        driver.find_element_by_css_selector("input.el-select__input.is-undefined").clear()  # 提醒谁看
        driver.find_element_by_css_selector("input.el-select__input.is-undefined").send_keys(u"测试售后管理员")
        time.sleep(1)
        driver.find_element_by_css_selector("body > div.el-select-dropdown.is-multiple > div > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li").click()
        #driver.find_element_by_xpath('//div[@class="el-select-dropdown is-multiple"]/div')
        time.sleep(1)
        driver.find_element_by_xpath('// *[ @ id = "add"] / div[1] / div / section[2] / section / div[2] / input').send_keys(u"工单标题")  # 工单标题
        driver.find_element_by_xpath('//*[@id="add"]/div[1]/div/section[2]/section/div[3]/div/div[1]/label[1]/span[1]/span').click()  # 问题类型
        text1 = driver.find_element_by_xpath('//div[@class="iframe_b"]/div/div/div/div/div/div/div[@class="edui-editor-iframeholder edui-default"]')  # 工单内容
        text = text1.find_element_by_tag_name("iframe")
        driver.switch_to_frame(text)
        driver.find_element_by_xpath('//body').send_keys(u"测试")
        driver.switch_to_default_content()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="add"]/div[1]/div/section[2]/section/div[5]/button').click()  # 确定
        time.sleep(1)
        detail = driver.find_element_by_xpath('//div[@class="listBox container-fluid"]/div[@id="tabel_list"]/table/tbody/tr[1]/td[5]/div/a/p').text
        self.assertEqual(detail, u'【软件BUG】 【工单标题】 测试', u"提交工单fail")

    def submit(self, message, failmessage):
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="add"]/div[1]/div/section[2]/section/div[5]/button').click()
        time.sleep(1)
        a = self.driver.find_element_by_xpath('//div[@class="swal-overlay"]/div/div').text
        self.assertEqual(a, message, failmessage)
        time.sleep(1)

    def timeSelect(self, link):
        # 设置为2017年12月30日
        self.driver.find_element_by_xpath(link+'/div[@class="el-picker-panel__body-wrapper"]/div/div[@class="el-date-picker__header"]/span[1]').click()
        self.driver.find_element_by_xpath(link+'/div[1]/div/div[2]/table[@class="el-year-table"]/tbody/tr[3]/td[1]').click()
        self.driver.find_element_by_xpath(link+'/div[1]/div/div[2]/table[@class="el-month-table"]/tbody/tr[3]/td[4]').click()
        self.driver.find_element_by_xpath(link+'/div[1]/div/div[2]/table[@class="el-date-table"]/tbody/tr[2]/td[7]').click()

    def assertResult(self, result, msg):
        try:
            self.assertTrue(result)
            print(msg + " pass")
        except AssertionError:
            print(msg + " fail")
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kphone\\images\\fail\\" + msg + ".png")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def waitForElementDisplay(self, ele):
        temptime = 30
        try:
            while not temptime == 0:
                if self.driver.find_element(ele):
                    return True
                temptime -= 1
        except NoSuchElementException as e:
            return False

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True


