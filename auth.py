import logging
import password
from selenium.webdriver.common.by import By

URL = password.DEV_URL
LOGIN = password.INTRANET_LOGIN
PASSWORD = password.INTRANET_PASSWORD

# example changing


def first_auth(driver):
    try:
        driver.get(URL)
        driver.find_element(By.NAME, "USER_LOGIN").send_keys(LOGIN)
        driver.find_element(By.NAME, "USER_PASSWORD").send_keys(PASSWORD)
        driver.find_element(By.CLASS_NAME, "login__btn").click()
        logging.info("success first_auth")
    except Exception:
        logging.info("exception first_auth")


def second_login(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(LOGIN)
        driver.find_element(
            By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
        driver.find_element(By.CLASS_NAME, "login__btn").click()
        logging.info("success second_auth")
    except Exception:
        logging.info("exception second_auth")
