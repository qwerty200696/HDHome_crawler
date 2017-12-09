#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import selenium.webdriver as webdriver
import time
import logging
from multiprocessing import Pool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import re

"""
特性：
    1.多线程；
    2.新的桌面窗口，不会弹出。
"""


def open_url(url):
    newwindow = 'window.open("{}")'.format(url)
    time.sleep(0.5)
    driver.execute_script(newwindow)
    time.sleep(0.5)


def saythanks():
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

        # noinspection PyBroadException
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "outer")))
        except:
            driver.refresh()
            time.sleep(1)
            print(driver.current_url, " refresh ---")

        # noinspection PyBroadException
        try:
            driver.find_element_by_xpath("//input[@id='saythanks']").click()
            print(driver.current_url, " succeed")
            logging.info(driver.current_url + " succeed~")
        except:
            print(driver.current_url, " not succeed")
            logging.info(driver.current_url + " not succeed!")
        finally:
            time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])


if __name__ == "__main__":

    display = Display(visible=1, size=(800, 600))
    display.start()

    log_file = "hdh_log_1.txt"
    logging.basicConfig(filename=log_file, level=logging.INFO)

    login_url = "http://hdhome.org/login.php"
    login_failed_url = "http://hdhome.org/takelogin.php"
    driver = webdriver.Chrome()
    # webdriver.PhantomJS

    driver.get(login_url)

    print("Wait for login...")
    logging.info("Wait for login...")

    while driver.current_url == login_url or driver.current_url == login_failed_url:
        time.sleep(10)

    print("Login succeed and start looping now...")
    logging.info("Login succeed and start looping now...")

    START = 25980
    END = 30000
    Thread_Num = 3
    t = 1
    for i in range(START, END, Thread_Num):

        pool = Pool(Thread_Num)
        all_links = ["http://hdhome.org/details.php?id={}&hit=1".format(i) for i in range(i, i + Thread_Num)]
        print(all_links)

        # noinspection PyBroadException
        try:
            rl = pool.map(open_url, all_links)
            pool.close()
            pool.join()
        except:
            print("multi thread start failed, next!!")
            logging.info("multi thread start failed, next!!")
            time.sleep(5)
            continue
        
        saythanks()

        # sleep more
        time.sleep(0.5)
        if t % 3 == 0:
            time.sleep(0.5)
        if t % 5 == 0:
            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            mystr = driver.find_elements_by_xpath('//span[@class="medium"]')[0].text
            bonus = re.search("\s[0-9,.]*\s", mystr).group()
            usrName = re.search("\s[a-zA-Z0-9]*\s", mystr).group()
            print(driver.current_url, "normal refresh,{}bonus is{}now...".format(usrName, bonus))
            logging.info(driver.current_url + "normal refresh,{}bonus is{}now...".format(usrName, bonus))
            time.sleep(1)
        t = t + 1
    driver.quit()
    logging.info("{}: driver quit, program stop.".format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
