# -*- coding: utf-8 -*-
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re
from test_case.login import Login


class ListTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.maximize_window()
        self.driver.get("http://vip.test.thinkerx.com/")

    def test_orderList(self):
        driver = self.driver
        Login.login(driver, 1)
        driver.find_element_by_xpath('//*[@id="nav"]/span/li[1]').click()

        # 指派处理人
        p = 1
        while not self.findElement('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[9]/div/div/p[1]/a' % p):
            p = p + 1

        driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[9]/div/div/p[1]/a' % p).click()
        driver.find_element_by_xpath('//*[@id="tabel_list"]/div[2]/div[1]/label/div/div/div[1]/input').send_keys(u"测试售后")
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div/div/div[1]/ul/li[1]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="tabel_list"]/div[2]/div[2]/a[1]').click()
        time.sleep(1)
        handler = driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[9]/div/div/p[1]' % p).text
        self.assertEqual(handler, u"已指派(测试售后)  指派", u"指派处理人 fail")

        # 编辑工单
        driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[11]/button[2]' % p).click()
        time.sleep(1)
        driver.find_element_by_xpath('//ul[@class="leftInputArea container"]/li[4]/div[1]/label[2]').click()
        driver.find_element_by_xpath("(//input[@type='text'])[6]").send_keys(u"测试售后")
        time.sleep(1)
        driver.find_element_by_xpath('//div[@x-placement="bottom-start"]/div/div[@class="el-select-dropdown__wrap el-scrollbar__wrap"]/ul/li[1]').click()
        driver.find_element_by_xpath('// *[ @ id = "add"] / div[1] / div / section[2] / section / div[2] / input').clear()
        driver.find_element_by_xpath('// *[ @ id = "add"] / div[1] / div / section[2] / section / div[2] / input').send_keys(u"编辑工单标题")
        driver.find_element_by_xpath('//*[@id="add"]/div[1]/div/section[2]/section/div[3]/div/div[1]/label[2]/span[1]/span').click()  # 问题类型
        text1 = driver.find_element_by_xpath('//div[@class="iframe_b"]/div/div/div/div/div/div/div[@class="edui-editor-iframeholder edui-default"]')  # 工单内容
        text = text1.find_element_by_tag_name("iframe")
        driver.switch_to_frame(text)
        driver.find_element_by_xpath('//body').clear()
        driver.find_element_by_xpath('//body').send_keys(u"编辑测试")
        driver.switch_to_default_content()
        time.sleep(1)
        self.driver.find_element_by_xpath('//div[@id="add"]/div[1]/div/section[2]/section/div[5]/button').click()  # 确定
        time.sleep(1)
        a = self.findElement('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[5]/div/a/p' % p)
        self.assertTrue(a, u'没有编辑成功')
        text = driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[5]/div/a/p' % p).text
        depa = driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[10]/div/div/p[1]' % p).text
        self.assertEquals(text, u'【报表制作】 【编辑工单标题】 编辑测试', u'编辑工单fail')
        self.assertEquals(depa, u'已指派(测试售后)   指派', u'编辑工单fail')


        # 完成工单
        order_id = driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[2]' % p).text
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[11]/button[1]' % p).click()
        time.sleep(1)
        self.assertEquals(order_id, driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[2]' % p).text)

        # 删除工单
        driver.find_element_by_xpath('//*[@id="tabel_list"]/table/tbody/tr[%s]/td[5]/div/a/p' % p).click()
        time.sleep(1)
        windows = driver.window_handles
        driver.switch_to_window(windows[1])
        ele = driver.find_element_by_xpath('//*[@id="after_sale_detail"]/div[1]/div[1]/div[2]/div/span/i')
        ActionChains(driver).move_to_element(ele).perform()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/ul/li[5]').click()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div/div/div[4]/div[2]/button').click()
        driver.switch_to_window(windows[0])

        # 指派给我的
        #


    def findElement(self, element):
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, element)))
            return True
        except selenium.common.exceptions.TimeoutException:
            return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

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

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
