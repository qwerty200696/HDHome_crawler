#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import selenium.webdriver as webdriver
import time
import logging

'''
单线程。
以try_new版本为主，弃。
'''

log_file = "hdh_log_1.txt"
logging.basicConfig(filename=log_file, level=logging.INFO)

login_url = "http://hdhome.org/login.php"
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
    link = "http://hdhome.org/details.php?id={}&hit=1".format(i)
    saythanks(link)

driver.close()
# 已经跑的。300
# 500-4192
# 5000 -6950-8307
