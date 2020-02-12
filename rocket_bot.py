from time import sleep
import password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RocketBot():
    def __init__(self):
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1
                                                 })
        self.driver = webdriver.Chrome(
            chrome_options=option,
            executable_path='chromedriver.exe'
        )

    def __del__(self):
        self.driver.close()

    def login(self):

        self.driver.get('https://rc.phoenixit.ru/group/vtb_hb_tube_test')

        login_lable = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "emailOrUsername")))
        login_lable.send_keys(password.RB_LOGIN)

        pass_lable = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "pass")))
        pass_lable.send_keys(password.RB_PASSWORD)

        btn = self.driver.find_element_by_xpath(
            '/html/body/section/div/form/div[2]/button[1]')
        btn.click()

        # TODO: put link in var
        print("[SUCCESS]\tlogging at " + "https://rc.phoenixit.ru/home")

    def select_chat(self):
        self.driver.get('https://rc.phoenixit.ru/group/vtb_hb_tube_test')

    def send_mess(self, message):
        mess_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "msg")))
        mess_box.send_keys(message)

        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.rc-message-box__send")))
        btn.click()
