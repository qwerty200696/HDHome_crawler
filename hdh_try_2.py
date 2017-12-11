#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import selenium.webdriver as webdriver
import time
import logging

'''
单线程稳定版。
'''

log_file = "xxx_log_1.txt"
logging.basicConfig(filename=log_file, level=logging.INFO)

login_url = "http://xxxx.org/login.php"
driver = webdriver.Chrome()

driver.get(login_url)

while (driver.current_url == login_url):
    time.sleep(10)

print("login is succeed now...\nstart loop now...")


def saythanks(link):
    driver.get(link)

    try:
        driver.find_element_by_xpath("//input[@id='saythanks']").click()
        print(i, " succeed\n")
        logging.info(str(i) + " succeed~\n")
    except:
        print(i, " not succeed\n")
        logging.info(str(i) + " not succeed!\n")
    finally:
        time.sleep(1)
        pass


START = 6951
END = 10000
for i in range(START, END):
    link = "http://xxxx.xxx/details.php?id={}&hit=1".format(i)
    saythanks(link)

driver.close()
