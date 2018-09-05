#coding=utf-8
import os
import unittest
from appium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import tempfile
import HTMLTestRunner
from extend import Appium_Extend

from PIL import Image

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_PATH = BASE_DIR + "/Kshow/images/"


class Test(unittest.TestCase):
    @classmethod
    # 初始化环境
    def setUpClass(cls):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '7.0'
        # 真机名称
        # desired_caps['deviceName'] = 'MI 4LTE'
        # 模拟器名称
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = PATH('C:\\Users\\Administrator\\Desktop\\kshow.apk')
        # 不需要每次都安装apk
        desired_caps['noReset'] = True
        desired_caps['appPackage'] = 'com.thinkerx.kshow2'
        desired_caps['appActivity'] = 'com.thinkerx.kshow.LoginActivity'
        #desired_caps['capability'] = 'uiautomator2'
        desired_caps['automationName'] = 'Uiautomator2'

        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True

        # 启动app
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        cls.driver.implicitly_wait(60)

    @classmethod
    def tearDownClass(cls):
        print(u"启动退出程序")
        cls.driver.quit()
        print("成功退出.......")

    # 开启所有权限(模拟器)
    def open_permissions(self):
        es = self.driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button")
        es.click()
        es.click()
        es.click()
        es.click()
        es.click()
        es.click()
        es1 = self.driver.find_element_by_id("android:id/button1")
        es1.click()
        es1.click()
        es1.click()

    # 开启所有权限(小米4真机)
    def open_permissions1(self):
        es1 = self.driver.find_element_by_id("android:id/button1")
        es1.click()
        es1.click()
        es1.click()
        es1.click()
        es1.click()

    # 登录
    def login_normal(self):
        if self.findElement("com.android.packageinstaller:id/permission_allow_button"):
            self.open_permissions()
            user1 = ["20156666666", "666666"]
            user2 = ["test6", "123456"]
            self.login(user1[0], user1[1])
        else:
            self.driver.find_element_by_id("android:id/button1").click()
            self.driver.find_element_by_id("com.thinkerx.kshow2:id/btn_login").click()

        if self.findElement("com.thinkerx.kshow2:id/iv_menu"):
            print "login pass"
        else:
            print "login fail"

    def test_a_login_debug(self):
        self.driver.find_element_by_id("android:id/button1").click()
        self.driver.find_element_by_id("com.thinkerx.kshow2:id/btn_login").click()

    # 公司模块
    def test_company(self):
        self.driver.find_element_by_class_name("android.support.v7.widget.RecyclerView").find_elements_by_class_name("android.widget.LinearLayout")[0].click()
        time.sleep(5)
        self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\test.png")

        # 公司图片
        if self.findElement("com.thinkerx.kshow2:id/iv_company_image"):
            self.assertResult('公司图片', 'company')

        # 公司介绍
        info = self.driver.find_element_by_id("com.thinkerx.kshow2:id/tv_company_info")
        try:
            assert (info.get_attribute("text") == u"测试公司介绍")
            print "公司介绍 pass"
        except AssertionError:
            print "公司介绍 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\company1.png")

        # 荣誉资质
        self.driver.find_element_by_class_name("android.widget.GridView").find_elements_by_class_name("android.widget.RelativeLayout")[0].click()
        self.assertResult('荣誉资质图片显示', 'zz1')

        self.driver.swipe(self.width()*6/7, self.height()/2, self.width()/7, self.height()/2)
        self.assertResult('荣誉资质图片滑动', 'zz2')

        self.driver.find_element_by_id("com.thinkerx.kshow2:id/back").click()

        # 联系我们
        for i in range(5):
            self.driver.swipe(self.width()/2, self.height()/2, self.width()/2, self.height()/6)
        time.sleep(2)

        com = self.driver.find_element_by_class_name("android.widget.ListView").find_elements_by_class_name("android.widget.TextView")[1]
        try:
            assert (com.text == u"测试")
            print "联系我们 pass"
        except AssertionError:
            print "联系我们 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\company4.png")

        # 新闻模块
        self.driver.find_element_by_class_name("android.widget.HorizontalScrollView").find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')[1].click()
        text1 = self.driver.find_element_by_class_name("android.widget.ListView").find_elements_by_class_name('android.widget.TextView')[0]
        text2 = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[1]
        image = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.ImageView')[0]
        try:
            assert (text1.text == u'豆腐干豆腐干地方出错')
            assert (text2.text == u'111')
            print "新闻列表 pass"
        except AssertionError:
            print "新闻列表 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\news1.png")

        # 进入新闻详情
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.RelativeLayout')[3].click()
        title = self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_title')
        times = self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_time')
        content = self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_content')

        self.driver.get_screenshot_as_file(TEMP_FILE)
        load = self.extend.load_image("f:\\PycharmProjects\\Kshow\\images\\news1.png")
        result1 = self.is_same(load)

        try:
            assert (title.text == u'123')
            assert (times.text == u'2017-07-11 17:21:33')
            assert (content.text == u'123')
            self.assertTrue(result1)
            print "新闻详情页 pass"
        except AssertionError:
            print "新闻详情页 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\news1.png")

        for i in range(3):
            self.driver.swipe(self.width()/2, self.height()/2, self.width()/2, self.height()/6)
        self.assertResult('新闻详情页滑动', 'news2')

        self.driver.find_element_by_id("com.thinkerx.kshow2:id/btn_return").click()

        # 视频播放
        self.driver.find_element_by_class_name("android.widget.HorizontalScrollView").find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')[2].click()

        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.LinearLayout')[1].click()
        if self.findElement('com.thinkerx.kshow2:id/parentPanel'):
            self.driver.find_element_by_id('android:id/button1').click()

        time.sleep(20)
        self.driver.tap([(120, 200)], 100)
        self.driver.tap([(self.width()/2, 1100)], 100)

        result = not self.driver.find_element_by_id('com.thinkerx.kshow2:id/exo_position').text == u'00:00'
        try:
            self.assertTrue(result)
            print "视频播放 pass"
        except AssertionError:
            print "视频播放 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\tv1.png")

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/exo_play').click()
        time.sleep(10)
        self.driver.keyevent(4)
        self.driver.find_element_by_id("com.thinkerx.kshow2:id/id_cstomize_back").click()

    # 产品模块
    def test_product(self):
        self.driver.find_element_by_class_name("android.support.v7.widget.RecyclerView").find_elements_by_class_name("android.widget.LinearLayout")[1].click()
        self.extend = Appium_Extend(self.driver)

        name = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[0]
        price = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[1]
        jb = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[2]

        try:
            self.assertTrue(name.text == u"001+5" and price.text == u'￥25.00/平方' and jb.text == u'最新')
            print "产品列表信息 pass"
        except AssertionError:
            print "产品列表信息 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\product_list.png")

    def test_product1_list(self):
        # 搜索功能
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/edit_text_search').send_keys(u"双成组")
        self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name("android.widget.ImageView")[0].click()
        self.assertResult('产品搜索', 'search')

        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[0].click()
        self.assertResult('双成组素材', 'cz5')
        self.driver.find_element_by_id("com.thinkerx.kshow2:id/btn_return").click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/search_image_delete').click()

        # 分类-样板间
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_category').click()
        self.driver.find_elements_by_class_name('android.widget.TextView')[1].click()
        self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name("android.widget.ImageView")[0].click()
        self.assertResult('场景', 'room')
        self.driver.find_element_by_id("com.thinkerx.kshow2:id/btn_return").click()

        # 分类-素材
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_category').click()
        self.driver.find_elements_by_class_name('android.widget.TextView')[2].click()
        self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name("android.widget.ImageView")[0].click()
        self.assertResult('素材', 'bom')

        # 分类-色卡
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_category').click()
        self.driver.find_elements_by_class_name('android.widget.TextView')[3].click()
        self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name("android.widget.ImageView")[0].click()
        self.assertResult('色卡', 'color')

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_category').click()
        self.driver.find_elements_by_class_name('android.widget.TextView')[0].click()

        # 产品排序
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_sort').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.LinearLayout')[2].click()
        time.sleep(2)
        price = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[1]
        try:
            self.assertTrue(price.text == u'￥3000.00/套')
            print "产品排序 pass"
        except AssertionError:
            print "产品排序 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\sort.png")

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_sort').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.LinearLayout')[0].click()

        # 产品风格
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_style').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.LinearLayout')[0].click()
        name = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[4]
        if name.text == u'5D26066':
            self.assertResult('产品风格', 'style')

        else:
            print 'style fail'
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\style.png")

        # 产品三级目录
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.FrameLayout')[1].click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.FrameLayout')[2].click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.FrameLayout')[3].click()
        try:
            self.assertTrue(not self.driver.find_element_by_id('com.thinkerx.kshow2:id/product_name_text').text == u'绒面深蓝色')
            print "三级目录 pass"
        except AssertionError:
            print "三级目录 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\product_catalog.png")

    def test_product2_detail(self):
        # 成组产品测试
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.FrameLayout')[0].click()
        for i in range(0, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[i]
            if a.text == u'隔断门集锦':
                a.click()
                break
        for i in range(0, 50, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[0]
            if a.text == u'成组test':
                a.click()
                break
            self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)
        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.RelativeLayout')[3].click()
        self.assertResult('成组', 'cz')
        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        self.assertResult('成组换色', 'cz_change_color')

        for i in range(1, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.RadioGroup').find_elements_by_class_name('android.widget.RadioButton')[i]
            if a.text == u'未命名':
                a.click()
                break
            self.driver.swipe(self.width()/2, self.height()*5/6, self.width()/3, self.height()*5/6)
        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[0].click()
        self.assertResult('成组素材2', 'cz2')

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        # 区域属性
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        for i in range(1, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[0]
            if a.text == u'test1':
                a.click()
                break
            self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)

        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.RelativeLayout')[2].click()
        time.sleep(3)
        self.driver.tap([(self.width()/2, self.height()/2)])
        self.assertResult('等高等宽加旋转', 'flip2')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        while not self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.TextView')[4].text == u'水平翻转':
            self.driver.swipe(self.width() / 2, self.height()*4 / 5, self.width() / 2, self.height() / 5)
        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.RelativeLayout')[2].click()
        self.assertResult('水平翻转', 'flip')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        if self.findElement('com.thinkerx.kshow2:id/tv_directory'):
            self.driver.swipe(self.width() / 2, self.height()*9 / 10, self.width() / 2, self.height() / 10)
        for i in range(1, 10, 1):
            b = self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.TextView')[i]
            if b.text == u'自动裁剪按比例':
                b.click()
                break
        self.assertResult('自动裁剪按比例', 'flip3')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        for i in range(1, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.TextView')[i]
            if a.text == u'自适应裁剪':
                a.click()
                break
        self.driver.find_element_by_class_name('android.widget.RadioGroup').find_elements_by_class_name('android.widget.RadioButton')[2].click()
        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        self.assertResult('自适应裁剪', 'flip4')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        # 格条产品
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        for i in range(1, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[i]
            if a.text == u'门图网':
                a.click()
                break
        for i in range(0, 50, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[8]
            if a.text == u'门图网通用框型':
                a.click()
                break
            self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)

        while not self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.TextView')[2].text == u'70圆弧框':
            self.driver.swipe(self.width() / 2, self.height() / 5, self.width() / 2, self.height()*4 / 5)
        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        self.assertResult('格条', 'grid')

        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        self.assertResult('格条色卡变换', 'grid_change_color')

        for i in range(1, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.RadioGroup').find_elements_by_class_name('android.widget.RadioButton')[i]
            if a.text == u'格条样式':
                a.click()
                break
            self.driver.swipe(self.width()/2, self.height()*5/6, self.width()/3, self.height()*5/6)
        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        self.driver.tap([(self.width() / 2, self.height() / 2)])
        self.assertResult('斜格条', 'grid_change_grid')
        time.sleep(2)
        self.driver.tap([(self.width() / 2, self.height() / 2)])

        while not self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.TextView')[1].text == u'LD-15057':
            self.driver.swipe(self.width()*2 / 3, self.height() * 7 / 8, self.width() / 2, self.height() * 7 / 8)
        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        self.driver.tap([(self.width() / 2, self.height() / 2)])
        self.assertResult('图片格条', 'grid_change_grid2')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        for i in range(1, 50, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[7]
            if a.text == u'门图网':
                a.click()
                time.sleep(2)
                self.driver.tap([(self.width() * 7 / 8, self.height() / 2)], 100)
                break
            self.driver.swipe(self.width() / 2, self.height() / 5, self.width() / 2, self.height() / 3)

        # 成组四扇翻转
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.FrameLayout')[0].click()
        for i in range(0, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[0]
            if a.text == u'素材测试':
                a.click()
                break
            self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)
        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.RelativeLayout')[2].click()
        self.assertResult('成组四扇翻转', 'cz3')

        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        while not self.driver.find_element_by_class_name('android.widget.RadioGroup').find_elements_by_class_name('android.widget.RadioButton')[2].text == u'外景':
            self.driver.swipe(self.width() / 2, self.height() * 5 / 6, self.width() / 3, self.height() * 5 / 6)
        self.driver.find_element_by_class_name('android.widget.RadioGroup').find_elements_by_class_name('android.widget.RadioButton')[2].click()
        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[1].click()
        self.driver.tap([(self.width() / 2, self.height() / 2)])
        self.assertResult('成组四扇翻转换素材', 'cz4')
        time.sleep(2)
        self.driver.tap([(self.width() / 2, self.height() / 2)])

        # 产品详情
        for i in range(1, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.RadioGroup').find_elements_by_class_name('android.widget.RadioButton')[i]
            if a.text == u'产品详情':
                a.click()
                break
        self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView').find_elements_by_class_name('android.widget.RelativeLayout')[0].click()
        self.assertResult('产品详情', 'product_detail')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_renturn').click()

        # 拍照搭配
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/iv_take_photo').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.LinearLayout')[1].click()
        if self.driver.find_elements_by_id('com.android.gallery:id/grid'):
            self.driver.tap([(self.width()/4, self.height()/6)])
        if self.findElement('android:id/navigationBarBackground'):
            self.driver.tap([(self.width() / 2, self.height() / 2)])
        # 添加门洞
        self.driver.find_elements_by_class_name('android.widget.LinearLayout')[2].find_elements_by_class_name('android.widget.LinearLayout')[0].click()
        # 删除门洞
        self.driver.find_elements_by_class_name('android.widget.LinearLayout')[2].find_elements_by_class_name('android.widget.LinearLayout')[2].click()
        # 抠除遮挡区
        self.driver.find_elements_by_class_name('android.widget.LinearLayout')[2].find_elements_by_class_name('android.widget.LinearLayout')[1].click()
        time.sleep(2)
        self.driver.tap([(self.width()/5, self.height()/2)])
        self.driver.tap([(self.width()/3, self.height()/2)])
        self.driver.tap([(self.width()/3, self.height()*3/4)])
        self.driver.tap([(self.width()/5, self.height()*3/4)])
        self.driver.tap([(self.width()/5, self.height()/2)])
        self.driver.find_elements_by_class_name('android.widget.LinearLayout')[2].find_elements_by_class_name('android.widget.LinearLayout')[3].click()
        self.assertResult('拍照搭配', 'product_take_photo')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        while not self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[8].text == u'xxx':
            self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[8].click()
        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.RelativeLayout')[2].click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_add_car').click()
        try:
            self.assertTrue(self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_price').text == self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_square_price').text)
            print "产品报价 pass"
        except AssertionError:
            print "产品报价 fail"

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/et_pro_width').send_keys(1500)
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/et_pro_height').send_keys(2000)
        try:
            self.assertTrue(self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_pro_price').text == u'￥669.00')
            print "产品报价输入宽高 pass"
        except AssertionError:
            print "产品报价输入宽高 fail"

        # 扇数设置
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/iv_product_in_room').click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_door_count').click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/Spinner_h_count').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[1].click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/Spinner_v_count').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[2].click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/Spinner_v_display').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[1].click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/h_flip').click()
        self.driver.tap([(self.width()/2, self.height()/10)])
        self.assertResult('扇数设置', 'door_count')
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_return').click()

        # 拍照目录
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_directory').click()
        for i in range(1, 10, 1):
            a = self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[i]
            if a.text == u'拍照产品':
                a.click()
                time.sleep(2)
                self.driver.tap([(self.width() * 7 / 8, self.height() / 2)], 100)
                break
            self.driver.swipe(self.width() / 2, self.height()*7/8, self.width() / 2, self.height() / 4)
        try:
            self.assertTrue(self.findElement('com.thinkerx.kshow2:id/tv_attribution'))
            print "拍照目录 pass"
        except AssertionError:
            print "拍照目录 fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\product_catalog_pic.png")

        # 添加产品
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_add').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.LinearLayout')[0].click()
        self.driver.find_element_by_id('com.android.camera:id/shutter_button').click()
        self.driver.find_element_by_id('com.android.camera:id/btn_done').click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/iv_take_ok').click()
        times = time.strftime('%Y%m%d', time.localtime(time.time()))
        for i in range(1, 50, 1):
            a = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[i]
            try:
                if times in a.text:
                    print "上传产品 pass"
                    break
                self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)
            except AssertionError:
                print "上传产品 fail"
                self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\product_upload.png")

        # 删除产品
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/tv_more').click()
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[0].click()
        for i in range(1, 50, 1):
            a = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[i]
            if times in a.text:
                a.click()
                break
            self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/btn_delete_confirm').click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/confirm_button').click()
        for i in range(1, 50, 1):
            a = self.driver.find_element_by_class_name('android.support.v4.widget.DrawerLayout').find_elements_by_class_name('android.widget.TextView')[i]
            try:
                if times not in a.text:
                    print "删除产品 pass"
                    break
                self.driver.swipe(self.width() / 2, self.height() / 3, self.width() / 2, self.height() / 4)
            except AssertionError:
                print "删除产品 fail"
                self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\product_delete.png")

        self.driver.find_element_by_id('com.thinkerx.kshow2:id/back').click()

    # 打开画册模块
    def album(self):
        self.driver.find_element_by_class_name("android.support.v7.widget.RecyclerView").find_elements_by_class_name("android.widget.LinearLayout")[2].click()
        self.driver.find_element_by_id("com.thinkerx.kshow2:id/btn_back").click()
        while not self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.TextView')[2].text == u'嘻嘻嘻':
            self.driver.swipe(self.width()/2, self.height()*3/4, self.width()/2, self.height()/4)
        self.driver.find_element_by_class_name('android.widget.GridView').find_elements_by_class_name('android.widget.TextView')[2].click()

        # 标签
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[2].click()
        self.assertResult('画册标签', 'album_tags')
        self.driver.find_element_by_class_name('android.widget.ListView').find_elements_by_class_name('android.widget.TextView')[1].click()

        # 分享
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/ll_home').click()
        self.driver.find_element_by_id('com.thinkerx.kshow2:id/iv_weixin').click()

    def findElement(self, element):
        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.ID, element)))
            return True
        except selenium.common.exceptions.TimeoutException:
            return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def edittextclear(self, text):
        '''
        请除EditText文本框里的内容
        @param:text 要清除的内容
        '''
        self.driver.keyevent(123)
        for i in range(0, len(text)):
            self.driver.keyevent(67)

    def width(self):
        return self.driver.get_window_size()['width']

    def height(self):
        return self.driver.get_window_size()['height']

    def login(self, user, password):
            self.driver.find_element_by_id('com.thinkerx.kshow2:id/edit_user').send_keys(user)
            self.driver.find_element_by_id("com.thinkerx.kshow2:id/edit_password").send_keys(password)
            self.driver.find_element_by_id("com.thinkerx.kshow2:id/btn_login").click()

    def assertResult(self, message, pic_name):
        self.extend = Appium_Extend(self.driver)
        time.sleep(8)
        self.driver.get_screenshot_as_file(TEMP_FILE)
        load = self.extend.load_image("f:\\PycharmProjects\\Kshow\\images\\"+pic_name+".png")
        result = self.is_same(load)
        try:
            self.assertTrue(result)
            print message + " pass"
        except AssertionError:
            print message + " fail"
            self.driver.get_screenshot_as_file("f:\\PycharmProjects\\Kshow\\images\\fail\\"+pic_name+".png")

    def is_same(self, load):
        self.driver.get_screenshot_as_file(TEMP_FILE)
        # 对比图片
        image1 = Image.open(TEMP_FILE)
        histogram1 = image1.histogram()
        histogram2 = load.histogram()
        if histogram1 == histogram2:
            return True
        else:
            return False

if __name__ == "__main__":
    unittest.main()
    '''
    suite = unittest.TestSuite()
    suite.addTest(Test("test_login_debug"))
    suite.addTest(Test("test_company"))
    suite.addTest(Test("test_product"))
    suite.addTest(Test("test_product1_list"))
    suite.addTest(Test("test_product2_detail"))

    times = time.strftime('%Y%m%d', time.localtime(time.time()))
    filename = 'F:/PycharmProjects/Kshow/report/testReport_'+times +'.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='result',
        description='report'
    )

    runner.run(suite)
    fp.close()



#打开订单模块
driver.find_element_by_class_name("android.support.v7.widget.RecyclerView").find_elements_by_class_name("android.widget.LinearLayout")[3].click()
driver.find_element_by_id("com.thinkerx.kshow2:id/back").click()

#打开设计工具
driver.find_element_by_class_name("android.support.v7.widget.RecyclerView").find_elements_by_class_name("android.widget.LinearLayout")[4].click()
driver.find_element_by_id("com.thinkerx.kshow2:id/back").click()

#打开图库商城
driver.find_element_by_class_name("android.support.v7.widget.RecyclerView").find_elements_by_class_name("android.widget.LinearLayout")[5].click()
driver.find_element_by_id("com.thinkerx.kshow2:id/btn_back").click()

driver.quit()
'''


