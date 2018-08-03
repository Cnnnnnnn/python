#-*- coding: utf-8 -*-
import time
from selenium.webdriver.support.select import Select
from selenium import webdriver

driver=webdriver.Firefox()
driver.maximize_window()
driver.get("http://114.215.86.109/projects/kshow/issues")
driver.find_element_by_id("username").send_keys("登录用户名")
driver.find_element_by_id("password").send_keys("登录密码")
driver.find_element_by_name("login").click()
time.sleep(2)

ids = [1234]
for aid in ids:
    currentpage = 1
    while currentpage < 20:
        try:
            driver.find_element_by_xpath("//tr[@id='issue-%d']/td[7]/a" % aid)
            currentpage = 20
        except:
             driver.find_element_by_xpath("//*[@id='content']/p[1]/a[@class = 'next']").click()
             currentpage = currentpage + 1
             time.sleep(2)
    driver.find_element_by_xpath("//tr[@id='issue-%d']/td[7]/a" % aid).click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='content']/div[@class='contextual']/a[1]").click()
    time.sleep(2)
    sel = driver.find_element_by_id("issue_status_id")
    Select(sel).select_by_value('5')
    driver.find_element_by_xpath("//*[@id='issue-form']/input[6]").click()
    driver.get("http://114.215.86.109/projects/kshow/issues")

driver.close()