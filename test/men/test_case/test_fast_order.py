# -*- coding: utf-8 -*-

import unittest, time
from selenium import webdriver
from test_case import test_login
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

TEST_URL = "http://mentest01.thinkerx.com/jishubuceshi_mini_alum/mini2015_5.0.4/index.php?r=login"


class FastOrderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get(TEST_URL)
        cls.accept_next_alert = True
        cls.driver.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def test_fast_order_1_open(self):
        driver = self.driver
        test_login.Login.login(driver)
        driver.find_element_by_xpath('//*[@id="order_fast"]/div/div[2]').click()
        windows = driver.window_handles
        driver.switch_to_window(windows[1])
        self.assertTrue(self.is_element_present('xpath', '//*[@id="clientfast"]/div[@class="page_main clb"]/div[1]/h3/p'), u'打开快速下单fail')
        #driver.switch_to_window(windows[0])

    def test_fast_order_2_clentinfo(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="customer_name"]').send_keys(u'自动化测试客户')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="other_customer_name_popup"]/ul/li').click()
        time.sleep(2)
        phone = driver.execute_script("return $('#phone').val();")
        deliver = driver.execute_script('return $("#c_delivery").val();')
        brand = driver.find_element_by_xpath('//*[@id="brand_id"]/option').text
        service = driver.execute_script("return $('#service_user').val();")
        manage = driver.execute_script("return $('#area_manager').val();")
        note = driver.execute_script('return $("#customer_note").val();')
        self.assertEqual(phone, '18855555555', u'电话不匹配')
        self.assertEqual(deliver, u'大运物流', u'物流不匹配')
        self.assertEqual(brand, u'新格尔', u'品牌不匹配')
        self.assertEqual(service, u'小张', u'客服不匹配')
        self.assertEqual(manage, u'小李', u'区域经理不匹配')
        self.assertEqual(note, u'自动化测试客户别删', u'客户备注不匹配')

    def test_fast_order_3(self):
        driver = self.driver
        Select(driver.find_element_by_id('client_format')).select_by_value("1")
        driver.find_element_by_xpath('//*[@id="add_line"]').click()
        driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[4]').click()
        driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[4]/div/ul/li[4]/a').click()
        driver.find_element_by_xpath('//*[@id="start_count"]').click()
        driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(2)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="total_money"]/span').text, '1,949', u'计算总金额不对')
        self.assertEqual(driver.execute_script('return $("#31").val();'), u'凹弧吊趟门', u'产品名称不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[6]/input').get_attribute("value"), '2060', u'总高不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[7]/input').get_attribute("value"), '1780', u'总宽不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[8]/input').get_attribute("value"), '2', u'扇数不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[11]/input').get_attribute("value"), '280', u'墙厚不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[19]/input').get_attribute("value"), u'花梨木', u'型材颜色不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[20]/input').get_attribute("value"), 'DT-002', u'款式不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[21]/input').get_attribute("value"), u'凹弧吊趟', u'竖框不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[22]/input').get_attribute("value"), u'白玻', u'面玻不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[23]/input').get_attribute("value"), u'白玻', u'底玻不对')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[29]').text, '3.67', u'面积不对')

    def test_fast_order_4_check(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="clientfast"]/div[4]/div[1]/div/a[3]').click()
        time.sleep(1)
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[12]/a').text, u'自动化测试客户', u'客户错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[9]').text, u'凹弧吊趟门', u'公式目录错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[10]').text, u'新格尔', u'品牌错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="color"]').text, u'花梨木', u'颜色错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="product_name"]').text, u'凹弧吊趟门', u'品名错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="dimension"]').text, '1780*2060*2', u'尺寸错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="shouldLoadLater money show_money blue"]').text, '1949.3', u'金额错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="delivery show_delivery"]/a').text, u'大运物流', u'物流错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="address"]').text, u'测试地址', u'地址错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="salesman_uid"]').text, u'小李', u'区域经理错误')
        self.assertEqual(driver.find_element_by_xpath('//*[@id="rows"]/div[2]/ul[1]/li[@class="package"]').text, '2', u'打包数不对')

    def test_fast_order_5_set_photo_show(self):
        driver = self.driver
        driver.get("http://mentest01.thinkerx.com/jishubuceshi_mini_alum/mini2015_5.0.4/index.php?r=clientOrder/fast")
        driver.find_element_by_xpath('//*[@id="canshu_btn"]').click()
        Select(driver.find_element_by_xpath('//*[@id="fast_photo_show"]')).select_by_value("1")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="add_line"]').click()
        driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[4]').click()
        ele = driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[4]/div/ul/li[4]/a')
        ActionChains(driver).move_to_element(ele).perform()
        self.assertEqual(driver.find_element_by_class_name('aui_state_focus').get_attribute('style'), "position: absolute; left: -9999em; top: 320px; width: auto; z-index: 1987;", u'公式图是否弹框显示错误')

        driver.find_element_by_xpath('//*[@id="canshu_btn"]').click()
        Select(driver.find_element_by_xpath('//*[@id="fast_photo_show"]')).select_by_value("0")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="add_line"]').click()
        driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[4]').click()
        ele = driver.find_element_by_xpath('//*[@id="form-table_box"]/ul[2]/li[4]/div/ul/li[4]/a')
        ActionChains(driver).move_to_element(ele).perform()
        self.assertEqual(driver.find_element_by_class_name('aui_state_focus').get_attribute('style'), "position: absolute; left: 760px; top: 180px; width: auto; z-index: 1988;", u'公式图是否弹框显示错误')

    def test_fast_order_6_set_more_time(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="canshu_btn"]').click()
        Select(driver.find_element_by_xpath('//*[@id="fast_more_time"]')).select_by_value('0')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="clientfast"]/div[4]/div[3]/div[1]/div/dl[12]/dd').click()
        text = driver.find_element_by_xpath('//*[@id="_my97DP"]').find_element_by_tag_name("iframe")
        driver.switch_to_frame(text)
        self.assertEqual(driver.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[7]/td[1]').get_attribute('class'), "WinvalidDay", u'下单时间不允许大于当天失败')
        driver.switch_to_default_content()

        driver.find_element_by_xpath('//*[@id="canshu_btn"]').click()
        Select(driver.find_element_by_xpath('//*[@id="fast_more_time"]')).select_by_value('1')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="clientfast"]/div[4]/div[3]/div[1]/div/dl[12]/dd').click()
        text = driver.find_element_by_xpath('//*[@id="_my97DP"]').find_element_by_tag_name("iframe")
        driver.switch_to_frame(text)
        self.assertEqual(driver.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[7]/td[1]').get_attribute('class'), "Wday", u'下单时间允许大于当天失败')
        driver.switch_to_default_content()

    def test_fast_order_7_set_type(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="canshu_btn"]').click()
        Select(driver.find_element_by_xpath('//*[@id="fast_type"]')).select_by_value('1')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="customer_name"]').send_keys(u'自动化测试客户')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="other_customer_name_popup"]/ul/li').click()
        driver.find_element_by_xpath('//*[@id="fastScript_line"]').click()
        driver.find_element_by_xpath('//*[@id="script_ui"]/div[2]/div/div/div[2]/h2').click()
        driver.find_element_by_xpath('//*[@id="script_ui"]/div[3]/div/div/div[2]/div[1]/div/div').click()
        time.sleep(1)
        self.assertTrue(self.is_element_present('xpath', '//*[@id="clientfast"]/div[@class="aui_state_focus aui_state_lock"]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/iframe'), u'看图下单方式fail')
        driver.find_element_by_xpath('//*[@id="clientfast"]/div[@class="aui_state_focus aui_state_lock"]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[1]/td/div/a').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="clientfast"]/div[@class="aui_state_lock"]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[1]/td/div/a').click()
        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="canshu_btn"]').click()
        Select(driver.find_element_by_xpath('//*[@id="fast_type"]')).select_by_value('2')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="customer_name"]').send_keys(u'自动化测试客户')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="other_customer_name_popup"]/ul/li').click()
        driver.find_element_by_xpath('//*[@id="fastScript_line"]').click()
        driver.find_element_by_xpath('//*[@id="script_ui"]/div[2]/div/div/div[2]/h2').click()
        driver.find_element_by_xpath('//*[@id="script_ui"]/div[3]/div/div/div[2]/div[1]/div/div').click()
        self.assertTrue(self.is_element_present('xpath', '//*[@id="form-table_box"]/ul[2]/li[4]/input[@value="凹弧平开门"]'), 'fail')
        driver.find_element_by_xpath('//*[@id="clientfast"]/div[@class="aui_state_lock aui_state_focus"]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[1]/td/div/a').click()

        driver.find_element_by_xpath('//*[@id="canshu_btn"]').click()
        Select(driver.find_element_by_xpath('//*[@id="fast_type"]')).select_by_value('0')

    def test_fast_order_6_operate(self):
        pass




