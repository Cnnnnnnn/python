

class Login:
    @staticmethod
    def login(driver):
        driver.find_element_by_id("loginname").send_keys('123')
        driver.find_element_by_id("nloginpwd").send_keys('123456')
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/button').click()
