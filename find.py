from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import auth
import logging
import datetime


def getData(driver, link):
    driver.get(link)
    if(driver.current_url == 'https://sso.phoenixit.ru/login'):
        auth.second_login(driver)
    try:
        element_1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.h1_liga"))
        )
        element_2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "time.p1_liga"))
        )
        name = element_1.text.replace("\n", "")
        birthDay = element_2.get_attribute('datetime')
        return (name, birthDay, link)
    except Exception:
        logging.info("exception.link: " + link)
    return("", 0, 0)


def is_near(str_date):
    mounth = int(str_date.split('.')[1])
    day = int(str_date.split('.')[0])

    tday = datetime.date.today()
    bday = datetime.date(tday.year, mounth, day)

    tdelta = datetime.timedelta(days=4)
    if(tday == bday):
        return 1
    if(tdelta + tday == bday):
        return 2
    return (0)


def getDataEmployee(owner, driver):
    links = []
    dataArray = []

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, owner))
        )
        master = element.find_element(By.XPATH,
                                      "../..").find_elements_by_tag_name('a')
        for _ in master:
            links.append(_.get_attribute('href'))

        for _ in links:
            dat = getData(driver, _)
            if(len(dat[0]) == 0):
                logging.info("employee.drop")
                continue
            dataArray.append(dat)
            logging.info("employee.name: " + dat[0])
        return dataArray
    except Exception:
        logging.info("Exception master")
