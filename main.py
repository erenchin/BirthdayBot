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
from rocket_bot import RocketBot as rb

PYTHONIOENCODING = "UTF-8"


def main():
    OWNER = password.OWNER
    bdToday = ""
    bdAfter = ""

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    driver = webdriver.Chrome()

    auth.first_auth(driver)
    data = find.getDataEmployee(OWNER, driver)

    for _ in data:
        if(find.is_near(str(_[1])) == 1):
            bdToday += (_[0] + _[1] + _[2] + "\n")
        elif(find.is_near(str(_[1])) == 2):
            bdAfter += (_[0] + _[1] + _[2] + "\n")

    if(len(bdToday) != 0 or len(bdAfter) != 0):
        if(len(bdToday) != 0 and len(bdAfter) != 0):
            msg = "Them birthday is in today:\n" + bdToday + "\n" + \
                "Them birthday is in a few days: \n" + bdAfter
        elif(len(bdToday) != 0 and len(bdAfter) == 0):
            msg = "Привет!\n\n Напоминаю, что сегодня у этих замечательных людей день рождения: \n\n" + \
                bdAfter + "\n Если нет подарка, срочно беги! \n\n С уважением BirthdayBot!"
        elif(len(bdToday) == 0 and len(bdAfter) != 0):
            msg = "Привет!\n\n Напоминаю, что через 7 дней у этих замечательных людей день рождения: \n\n" + \
                bdAfter + "\n Не забудь приготовить подарок! \n\n С уважением BirthdayBot!"
        #mail.sendMail(msg, mail.initMail())
        bot = rb()
        bot.login()
        bot.send_mess(msg)

    driver.close()


main()
