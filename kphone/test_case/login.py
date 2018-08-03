# -*- coding: utf-8 -*-


class Login:

    def __init__(self):
        pass

    @staticmethod
    def login(driver, role):
        global phone, password
        driver.find_element_by_xpath('//*[@id="header"]/div/ul[2]/span/li[1]').click()
        if role == 1:  # 售后
            phone = 13412345678
            password = 123456
        elif role == 2:  # 市场
            phone = 18866666666
            password = 123456
        elif role == 3:  # 财务
            phone = 13411110001
            password = 123456
        driver.find_element_by_name("phone").clear()
        driver.find_element_by_name("phone").send_keys(str(phone))
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(str(password))
        driver.find_element_by_xpath('//div[@class="title"]/form/button').click()
