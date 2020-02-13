#!/usr/bin/python
# -*- coding: utf-8 - *-
from time import sleep
import password
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import mail


class RocketBot():
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')

        option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1
                                                 })
        self.driver = webdriver.Chrome(
            chrome_options=option,
            executable_path='/root/serenchin/birthdayBot/chromedriver'
        )

    def __del__(self):
        self.driver.close()

    def login(self):

        try:
            self.driver.get(password.RB_URL)

            login_lable = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "emailOrUsername")))
            login_lable.send_keys(password.RB_LOGIN)

            pass_lable = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "pass")))
            pass_lable.send_keys(password.RB_PASSWORD)

            btn = self.driver.find_element_by_xpath(
                '/html/body/section/div/form/div[2]/button[1]')
            btn.click()

            logging.info("success logging at " + password.RB_URL)
        except Exception:
            mail.sendMail("sendmail exception rb.login", mail.initMail())

    def send_mess(self, message):
        mess_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "msg")))
        mess_box.send_keys(message)

        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.rc-message-box__send")))
        try:
            btn.click()
        except Exception:
            logging.info("error btn.click()")
