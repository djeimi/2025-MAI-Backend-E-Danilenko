from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from django.test import TransactionTestCase
import time

from selenium.webdriver.common.by import By

class SeleniumTests(TransactionTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument('--disable-features=CalculateNativeWinOcclusion')
        options.add_argument('--disable-dev-shm-usage')

        service = Service('/usr/local/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_admin_login(self):
        # admin_url = str("self.live_server_url") + '/admin/'
        # print('admin_url ' + admin_url)
        self.driver.get("http://127.0.0.1:8000/admin")
        

        username_input = self.driver.find_element(by=By.NAME, value='username')
        username_input.send_keys('danilenko_e')
        

        password_input = self.driver.find_element(by=By.NAME, value='password')
        password_input.send_keys('pass')

        self.driver.find_element(By.XPATH, '//input[@value="Log in"]').click()
        
        # self.assertTrue('case-sensitive' in self.driver.page_source)
        self.assertTrue('Site administration' in self.driver.page_source)
