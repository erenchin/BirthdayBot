#!/usr/bin/python
# -*- coding: utf-8 - *-
from email.header import Header
from email.mime.text import MIMEText

from selenium import webdriver

import auth
import find
import mail
import logging
import password
import locale_en as locale
from rocket_bot import RocketBot as rb

PYTHONIOENCODING = "UTF-8"


def main():
    OWNER = password.OWNER
    bday_today = ""
    bday_7_days = ""

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    try:
        Options = webdriver.ChromeOptions()
        Options.add_argument('--headless')
        Options.add_argument('--no-sandbox')
        Options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(
            '/root/serenchin/birthdayBot/chromedriver', chrome_options=Options)
        logging.info("load webriver")
    except Exception:
        logging.info("error load webriver")

    auth.first_auth(driver)
    data = find.getDataEmployee(OWNER, driver)

    for _ in data:
        if(find.is_near(str(_[1])) == 1):
            bday_today += (_[0] + _[1] + _[2] + "\n")
        elif(find.is_near(str(_[1])) == 2):

            bday_7_days += (_[0] + _[1] + _[2] + "\n")

    day0 = len(bday_today)
    day7 = len(bday_7_days)
    msg = ""

    if((day0 + day7) > 0):
        if(day0 > 0):
            if(day0 is 1):
                msg = locale.TODAY_1
            else:
                msg = locale.TODAY_MANY

            msg = msg + bday_today + '\n'

        if(day7 > 0):
            if(day7 is 1):
                msg = msg + locale.IN_7_DAYS_1
            else:
                msg = msg + locale.IN_7_DAYS_MANY

            msg = msg + bday_7_days + '\n'

        msg = msg + locale.FINAL

        # msg +
        # if((day0 != 0) and (day7 != 0)):
        #     msg = "Them birthday is in today:\n" + bd_today + "\n" + \
        #         "Them birthday is in a few days: \n" + bday_7_days
        # elif(len(bd_today) != 0 and len(bday_7_days) == 0):
        #     msg = "Привет!\n\n Напоминаю, что сегодня у этих замечательных людей день рождения: \n\n" + \
        #         bday_7_days + "\n Если нет подарка, срочно беги! \n\n С уважением BirthdayBot!"
        # elif(len(bd_today) == 0 and len(bday_7_days) != 0):
        #     msg = "Привет!\n\n Напоминаю, что через 7 дней у этих замечательных людей день рождения: \n\n" + \
        #         bday_7_days + "\n Не забудь приготовить подарок! \n\n С уважением BirthdayBot!"
        # mail.sendMail(msg, mail.initMail())
        bot = rb()
        bot.login()
        bot.send_mess(msg)
        logging.info("succes send msg")
    driver.close()


main()
