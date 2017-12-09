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
from CodeRecognition import CodeRecognition
import sys
from PyQt5 import QtWidgets
from functools import partial
# import urllib
import os
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

"""
特性：
    1.多线程；
    2.新的桌面窗口，不会弹出。
    3.使用类，只输入验证码。以后可以用匿名浏览器。
"""


def open_url(url):
    newwindow = 'window.open("{}")'.format(url)
    time.sleep(0.5)
    driver.execute_script(newwindow)
    time.sleep(0.5)


class HDH:
    def __init__(self, parent=None):
        global driver
        self.driver = webdriver.Firefox()
        self.log_in()
        driver = self.driver
        self.start_loop()
        pass

    def log_in(self):
        login_url = "http://hdhome.org/login.php"
        login_failed_url = "http://hdhome.org/takelogin.php"
        self.driver.get(login_url)
        # noinspection PyBroadException
        try:
            # wait for loading image
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//img[@alt='CAPTCHA']")))
        except:
            print(self.driver.current_url, "connection failed, quit now ---")
            quit()

        # action = ActionChains(self.driver)
        # action.context_click(code)
        # action.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN)
        # action.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN)
        # # action.send_keys('v')
        # action.send_keys(Keys.ENTER)
        # action.send_keys(Keys.ENTER).perform()

        print("Wait for login...")
        logging.info("Wait for login...")

        # code_url = self.driver.find_element_by_xpath("//img[@alt='CAPTCHA']").get_property("src")
        code = self.driver.find_element_by_xpath("//img[@alt='CAPTCHA']")
        img = code.screenshot_as_png
        img_name = "./code/code{}.png".format(time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time())))
        with open(img_name, 'wb') as f:
            f.write(img)
        rec_code = self.code_recog(img_name)

        self.driver.find_element_by_name("username").send_keys("*********")
        self.driver.find_element_by_name("password").send_keys("*********")
        self.driver.find_element_by_name("imagestring").send_keys(rec_code)
        self.driver.find_element_by_xpath('//input[@type="submit"]').click()

        if self.driver.current_url == login_url or self.driver.current_url == login_failed_url:
            print("login failed, please double check your username/password/verify code.")
            return

        print("Login succeed and start looping now...")
        logging.info("Login succeed and start looping now...")

    def saythanks(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

            # noinspection PyBroadException
            try:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "outer")))
            except:
                self.driver.refresh()
                time.sleep(1)
                print(self.driver.current_url, " refresh ---")

            # noinspection PyBroadException
            try:
                self.driver.find_element_by_xpath("//input[@id='saythanks']").click()
                print(self.driver.current_url, " succeed")
                logging.info(self.driver.current_url + " succeed~")
            except:
                print(self.driver.current_url, " not succeed")
                logging.info(self.driver.current_url + " not succeed!")
            finally:
                time.sleep(1)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])

    def code_recog(self, path):
        app = QtWidgets.QApplication(sys.argv)
        center = CodeRecognition()

        # 改变输入的图片。
        center.img_path = path
        center.show_code_img()

        center.show()
        app.exec_()
        rec_code = center.get_text()
        print("识别的验证码为：", rec_code)
        return rec_code

    def start_loop(self, start=30000, end=33000, thread_num=3):
        t = 1
        for i in range(start, end, thread_num):

            pool = Pool(thread_num)
            all_links = ["http://hdhome.org/details.php?id={}&hit=1".format(i) for i in range(i, i + thread_num)]
            # all_links.append(self.driver)
            print(all_links)
            pool.map(open_url, all_links)

            # noinspection PyBroadException
            try:
                pool.close()
                pool.join()
            except:
                print("multi thread start failed, next!!")
                logging.info("multi thread start failed, next!!")
                time.sleep(5)
                continue
            # 通过移动句柄来说谢谢
            self.saythanks()

            # sleep more
            time.sleep(0.5)
            if t % 3 == 0:
                time.sleep(0.5)
            if t % 5 == 0:
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.refresh()
                mystr = self.driver.find_elements_by_xpath('//span[@class="medium"]')[0].text
                bonus = re.search("\s[0-9,.]*\s", mystr).group()
                usrName = re.search("\s[a-zA-Z0-9]*\s", mystr).group()
                print(self.driver.current_url, "normal refresh,{}bonus is{}now...".format(usrName, bonus))
                logging.info(self.driver.current_url + "normal refresh,{}bonus is{}now...".format(usrName, bonus))
                time.sleep(1)
            t = t + 1
        # self.driver.quit()
        logging.info("{}: loop finished.".format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))


if __name__ == "__main__":
    # display = Display(visible=1, size=(800, 600))
    # display.start()

    driver = webdriver.Firefox()
    log_file = "hdh_log_1.txt"
    logging.basicConfig(filename=log_file, level=logging.INFO)
    h = HDH()
