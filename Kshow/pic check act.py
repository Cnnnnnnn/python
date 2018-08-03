# coding=utf-8

import unittest
import os

from extend import Appium_Extend
from appium import webdriver


class Test(unittest.TestCase):
    # 初始化环境
    def setUp(self):
        desired_caps = {}
        desired_caps["platformName"] = "Android"
        desired_caps["platformVersion"] = "4.3"
        desired_caps["deviceName"] = "788a6ab5"
        desired_caps["appPackage"] = "com.android.settings"
        desired_caps["appActivity"] = ".Settings"

        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

        self.extend = Appium_Extend(self.driver)

        # 回到主屏幕
        self.driver.press_keycode(3)

        # 退出测试

    def tearDown(self):
        self.driver.quit()

    def test_get_screen_by_element(self):
        element = self.driver.find_element_by_id("com.android.deskclock:id/imageview")

        self.extend.get_screenshot_by_element(element).write_to_file("f:\\screen", "image")
        self.assertTrue(os.path.isfile("f:\\screen\\image.png"))

    def test_same_as(self):
        element = self.driver.find_element_by_id("com.android.deskclock:id/imageview")

        load = self.extend.load_image("f:\\screen\\image.png")
        # 要求百分百相似
        result = self.extend.get_screenshot_by_element(element).same_as(load, 0)
        self.assertTrue(result)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Test("test_get_screen_by_element"))
    suite.addTest(Test("test_same_as"))
    # 执行测试
    unittest.TextTestRunner().run(suite)