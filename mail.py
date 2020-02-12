#!/usr/bin/python
# -*- coding: utf-8 - *-
import logging
import smtplib
import password
from email.header import Header
from email.mime.text import MIMEText

SERVER = password.EMAIL_SERVER
LOGIN = password.EMAIL_LOGIN
PASSWORD = password.EMAIL_PASSWORD
EMAIL_TO = password.EMAIL_TO
EMAIL_FROM = password.EMAIL_FROM


def initMail():
    try:
        smtpObj = smtplib.SMTP(SERVER, 587)
        smtpObj.starttls()
        smtpObj.login(LOGIN, PASSWORD)
        return smtpObj
    except Exception:
        logging.info("exception initMail")


def sendMail(str, smtpObj):
    msg = MIMEText(
        str, 'plain', 'utf-8')
    msg['Subject'] = Header(
        'Уведомление о дне рождения!', 'utf-8')
    smtpObj.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    smtpObj.quit()
