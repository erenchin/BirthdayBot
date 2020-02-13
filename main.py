#!/usr/bin/python
# -*- coding: utf-8 - *-
from email.header import Header
from email.mime.text import MIMEText

from selenium import webdriver

import auth
from find import is_near, getDataEmployee
import mail
import logging
import password
import locale_en as locale
from rocket_bot import RocketBot as rb

PYTHONIOENCODING = "UTF-8"


def main():
    OWNER = password.OWNER
    bday_today = ""
    bday_3_days = ""
    bday_7_days = ""

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # creating *driver* variable and some settings for browser
    try:
        Options = webdriver.ChromeOptions()
        Options.add_argument('--headless')
        Options.add_argument('--no-sandbox')
        Options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(
            '/root/serenchin/birthdayBot/chromedriver', chrome_options=Options)
        logging.info("load webriver")
    except Exception:
        logging.error("error load webriver")

    # parsing OWNER workers
    auth.first_auth(driver)
    persons = getDataEmployee(OWNER, driver)

    # collecting persons, who will have birthdays today, in 3 or in 7 days
    for pers in persons:
        if(is_near(pers[1]) == 1):
            bday_today += pers[0] + pers[1] + pers[2] + '\n'

        elif(is_near(pers[1]) == 2):
            bday_3_days += pers[0] + pers[1] + pers[2] + '\n'

        elif(is_near(pers[1]) == 3):
            bday_7_days += pers[0] + pers[1] + pers[2] + '\n'

    day0 = len(bday_today)
    day3 = len(bday_3_days)
    day7 = len(bday_7_days)
    msg = ""

    # creating message
    if((day0 + day3 + day7) > 0):
        if(day0 > 0):
            if(day0 is 1):
                msg = locale.TODAY_1
            else:
                msg = locale.TODAY_MANY

            msg = msg + bday_today + '\n'

        if(day3 > 0):
            if(day3 is 1):
                msg = locale.IN_3_DAYS_1
            else:
                msg = locale.IN_3_DAYS_MANY

            msg = msg + bday_3_days + '\n'

        if(day7 > 0):
            if(day7 is 1):
                msg = msg + locale.IN_7_DAYS_1
            else:
                msg = msg + locale.IN_7_DAYS_MANY

            msg = msg + bday_7_days + '\n'

        msg = msg + locale.FINAL

        bot = rb()
        bot.login()
        bot.send_mess(msg)
        logging.info("succes send msg")

    driver.close()


main()
