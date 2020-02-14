#!/usr/bin/python
# -*- coding: utf-8 - *-
import logging
import timeit
from email.header import Header
from email.mime.text import MIMEText

from selenium import webdriver

import auth
import locale_en as locale
import mail
import password
from find import getDataEmployee, is_near
from rocket_bot import RocketBot as rb

PYTHONIOENCODING = "UTF-8"


def main():
    start = timeit.default_timer()

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

        prefs = {
            'profile.default_content_setting_values': {
                'cookies': 2,
                'images': 2,
                'javascript': 2,
                'plugins': 2,
                'popups': 2,
                'geolocation': 2,
                'notifications': 1,
                'auto_select_certificate': 2,
                'fullscreen': 2,
                'mouselock': 2,
                'mixed_script': 2,
                'media_stream': 2,
                'media_stream_mic': 2,
                'media_stream_camera': 2,
                'protocol_handlers': 2,
                'ppapi_broker': 2,
                'automatic_downloads': 2,
                'midi_sysex': 2,
                'push_messaging': 2,
                'ssl_cert_decisions': 2,
                'metro_switch_to_desktop': 2,
                'protected_media_identifier': 2,
                'app_banner': 2,
                'site_engagement': 2,
                'durable_storage': 2
            }
        }

        Options.add_experimental_option('prefs', prefs)

        Options.add_argument('--headless')
        Options.add_argument('--no-sandbox')
        Options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(
            'chromedriver', chrome_options=Options)
        logging.info("load webriver")
    except Exception:
        logging.error("error load webriver")

    # parsing OWNER workers
    auth.first_auth(driver)
    persons = getDataEmployee(OWNER, driver)

    # collecting persons, who will have birthdays today, in 3 or in 7 days
    for pers in persons:
        if(is_near(pers[1]) == 1):
            bday_today += pers[0] + " " + pers[1] + " " + pers[2] + '\n'

        elif(is_near(pers[1]) == 2):
            bday_3_days += pers[0] + " " + pers[1] + " " + pers[2] + '\n'

        elif(is_near(pers[1]) == 3):
            bday_7_days += pers[0] + " " + pers[1] + " " + pers[2] + '\n'

    day0 = len(bday_today)
    day3 = len(bday_3_days)
    day7 = len(bday_7_days)
    msg = ""

    # creating message
    if((day0 + day3 + day7) > 0):
        if(day0 > 0):
            if(day0 > 1):
                msg = msg + locale.TODAY_1
            else:
                msg = msg + locale.TODAY_MANY

            msg = msg + bday_today + '\n'

        if(day3 > 0):
            if(day3 is 1):
                msg = msg + locale.IN_3_DAYS_1
            else:
                msg = msg + locale.IN_3_DAYS_MANY

            msg = msg + bday_3_days + '\n'

        if(day7 > 0):
            if(day7 > 1):
                msg = msg + locale.IN_7_DAYS_1
            else:
                msg = msg + locale.IN_7_DAYS_MANY

            msg = msg + bday_7_days + '\n'

        msg = msg + locale.FINAL

        bot = rb()
        bot.login()
        bot.send_mess(msg)
        logging.info("succes send msg to rocket chat")

    elif((day0 + day3 + day7) is 0):
        logging.info("there are no b-days today, in 3 or in 7 days")

    driver.close()

    stop = timeit.default_timer()
    print('Time: ', stop - start)


main()
