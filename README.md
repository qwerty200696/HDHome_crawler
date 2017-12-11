---
title: python爬虫实战--selenium模拟登录并自动点击
date: 2017-12-09 22:57:45
categories: Python
tags:
	- python
	- 爬虫
	- selenium
	- HDHome	
---

# python爬虫实战--selenium模拟登录网站HDH并刷魔力值

## 任务介绍

最近刚刚注册了某个网站：[HDHome](http://hdhome.org/)，该站有新手考核任务，其中有一项是需要达到魔力值5000。在魔力值获取方式中，我们看到这一项：“说谢谢 = 0.5个魔力值”，而网站存活种子数量达到16000+，也就意味着对每个种子说一下谢谢，轻松达到8000+的魔力值，于是，这个项目应运而生。


实现思路：
获取种子的页面，在每个页面中找到说谢谢的按钮，并点击后，关闭。依次进行下去即可。

相似任务：

实现对某论坛的自动回复，实现自动获取所有帖子的信息等等相关操作，无论是否需要模拟登录、模拟鼠标操作还是直接解析网站元素。

## selenium 牛刀小试
首先导入相关的库：

```python
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
```
这是整个程序里面用到的所有内容。
其中，`webdriver`是主浏览器，`selenium`都是基于整个浏览器的对象；`WebDriverWait、EC、By`是等待网页元素加载相关的操作；`Keys`是键值，如`Keys.CONTROL`，`Keys.ENTER`等等，`ActionChains`是用鼠标进行一系列的操作。

`webdriver`可用的浏览器有：
```
webdriver.Firefox
webdriver.FirefoxProfile
webdriver.Chrome
webdriver.ChromeOptions
webdriver.Ie
webdriver.Opera
webdriver.PhantomJS
webdriver.Remote
webdriver.DesiredCapabilities
webdriver.ActionChains
webdriver.TouchActions
webdriver.Proxy
```
一开始我选择的是Chrome浏览器，后来改为了Firefox火狐。Chrome浏览器在执行ActionChains时有坑，所以后来才用的Firefox。此外，PhantomJS是匿名浏览器，没有显式的窗口。

那么，开始写程序吧。
```python
driver = webdriver.Firefox()
login_url = "http://hdhome.org/login.php"
login_failed_url = "http://hdhome.org/takelogin.php"
driver.get(login_url)
while self.driver.current_url == login_url or self.driver.current_url == login_failed_url:
    time.sleep(10)
# do something
```

首先，实体化浏览器driver，执行`driver = webdriver.Firefox()`这句的时候，就会有firefox浏览器弹出来了。当执行到`driver.get(login_url)`时，浏览器转到相应的王志网站，后面的while语句是用来等待我们手动登录的，当我们手动登录成功后，会进入到`"http://hdhome.org/index.php"`，与login_url及login_failed_url都不同。接着便可以做自己想做的事情了。

我们发现单个种子的网址是类似这样的：
```python
single_link = "http://hdhome.org/details.php?id={}&hit=1".format(i)
```
i可以从1到30000多。于是，我们可以这样写程序，依次对每个种子执行“说谢谢”操作：
```python
def saythanks(link):
    driver.get(link)
    try:
        driver.find_element_by_xpath("//input[@id='saythanks']").click()
        print(link, " succeed\n")
    except:
        print(link, " not succeed\n")
    finally:
        time.sleep(1)
        pass
        
START = 1
END = 30000
for i in range(START, END):
    link = "http://hdhome.org/details.php?id={}&hit=1".format(i)
    saythanks(link)
driver.close()
```
其中，我们使用`try`、`except`、`finally`语句来尝试定位到'saythanks'说谢谢的按钮元素。由于有时候加载较慢就会找不到，或者是这个种子已经被删除了，所以也导致找不到该元素。

其中定位网页元素的方法有一下几种：
```python
# locate single element in a page:
find_element_by_id
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector

# To find multiple elements (these methods will return a list):
find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector
```
从上面可以看出，我们也可以用`find_element_by_id("saythanks")`同样可以找到说谢谢的按钮。

附上到目前为止的所有程序：
[GitHub地址1](https://github.com/qwerty200696/HDHome_crawler/blob/master/hdh_try_2.py)
完整程序中加上了logging模块，将输出日志也导入到了文件，方面以后查阅。

## 改进一：使用多线程
在上述模块中，可以看到，我们按照种子的顺序依次进行相应的操作。在种子数量很多的时候，会显得很慢，于是，有了这个改进：使用多线程。

我们使用multiprocessing库。
```python
from multiprocessing import Pool
```
先来看一个使用该多线程库的示例程序：
```python
import time
from multiprocessing import Pool

def run(fn):
    # fn: 函数参数是数据列表的一个元素
    time.sleep(1)
    return fn * fn

if __name__ == "__main__":
    testFL = [1, 2, 3, 4, 5, 6]
    print('shunxu:')  # 顺序执行(也就是串行执行，单进程)
    s = time.time()
    for fn in testFL:
        run(fn)

    e1 = time.time()
    print("顺序执行时间：", int(e1 - s))

    print('concurrent:')  # 创建多个进程，并行执行
    pool = Pool(5)  # 创建拥有5个进程数量的进程池
    # testFL:要处理的数据列表，run：处理testFL列表中数据的函数
    rl = pool.map(run, testFL)
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出
    e2 = time.time()
    print("并行执行时间：", int(e2 - e1))
    print(rl)
```
于是，模仿上述程序，我们也使用多线程来执行说谢谢。说谢谢的过程其实有两步：一是打开网页，二是对每个网页定位到每个元素并点击。

如果对一、二两个步骤都执行多线程会出错，可能是由于多窗口的原因。因此我目前只对打开网页的步骤执行了多线程的操作。

上述也提到了，要同时打开多个窗口，则需要使用浏览器的多标签功能。打开一个新的标签的程序需要执行js脚本，如下：
```python
def open_url(url):
    newwindow = 'window.open("{}")'.format(url)
    driver.execute_script(newwindow)
```
于是多线程部分的改进如下：
```python
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
        # 通过移动句柄来说谢谢
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
```
为了不让浏览器检测到，我只是用了三个线程，可以适当的增加。saythanks()下面的部分程序是为了增加更多的延迟并且显示相应的信息。其中`if t % 5 == 0:`中，我们移动到主页上，进行刷新操作，然后定位到用户信息那一栏：
```
bonus = re.search("\s[0-9,.]*\s", mystr).group()
usrName = re.search("\s[a-zA-Z0-9]*\s", mystr).group()
```
这个部分使用了re正则项来找出当前的魔力值以及用户名，并显示出来。

其中，说谢谢的程序也需要对多标签进行相应的改进，程序如下：
```python
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
```
通过在不同窗口的句柄之间移动，来依次进行说谢谢的步骤。
在每个网页加载的时候，我们执行了等待的操作：
```python
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "outer")))
```
一直等到最外层的元素出现。我选择的"outer"这个元素，是在无论这个种子是否存在的时候都会出现的。

```python
driver.switch_to.window(driver.window_handles[-1])
```
将窗口转移到最后打开的那个窗口。
```python
driver.close()
driver.switch_to.window(driver.window_handles[-1])
```
关闭当前的个窗口，并转到当前的最后一个窗口。需要注意的是：窗口虽然关闭了，但是，driver依旧会停在那个已经失效的窗口，并不会自动的转到新的窗口（虽然在浏览器中看上去到了新的窗口），所以，需要我们自己手动的移动窗口的句柄。

这边还存在一个问题，就是多标签的时候，自动切换标签的时候，浏览器会自动弹出来，作为主窗口。这样子便有点烦人，毕竟我们只是想让他在后来自己跑， 所以，我加上了一个虚拟窗口，使用的是`pyvirtualdisplay`库。

以下是`pyvirtualdisplay`库在ubuntu中的安装步骤：
```
pip install pyvirtualdisplay
sudo apt install xvfb
sudo apt install xserver-xephyr
```
下面是`pyvirtualdisplay`具体的使用方式：
```
from pyvirtualdisplay import Display

if __name__ == "__main__":
    display = Display(visible=1, size=(800, 600))
    display.start()
```
把虚拟窗口放在一开始处的位置即可。
也可以将visible改为0，浏览器就完全不可见了。

最后附上这个阶段的完整程序：
[github地址2](https://github.com/qwerty200696/HDHome_crawler/blob/master/hdh_try_4.py)


## 改进二：面向对象编程
这部分的改进就是对函数使用了类，把多个函数合并到了同一个类中去。

## 改进三：使用pyqt获得验证码图片
思路是：从网页中解析到验证码的图片，然后下载到本地；接着使用pyqt弹出一个窗口，窗口中显示获取到的验证码，手动输入验证码后点击关闭。

简化了每次登录的流程，账号、密码记录在程序中自动输入，只需要手动输入验证码。

其中，基于pyqt5图形界面的窗口部分的程序如下：
```python
# CodeRecognition.py
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class CodeRecognition(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("请手动输入验证码")
        self.resize(250, 150)
        self.center()
        # 界面初始化
        self.code_edit = QLineEdit()
        self.label_code = QtWidgets.QLabel()
        self.init_interface()
        self.img_path = './image_3.png'
        self.show_code_img()
        # 输出的识别码
        self.out_code = 'To_be_recognize'

    def init_interface(self):

        label1 = QtWidgets.QLabel('请输入验证码：', self)
        label2 = QtWidgets.QLabel('输入完成后点击关闭按钮即可。', self)
        self.code_edit.setToolTip('请输入验证码')
        button2 = QtWidgets.QPushButton('关闭', self)

        grid = QGridLayout()
        grid.setSpacing(0)

        grid.addWidget(self.label_code, 0, 0, 1, 2)
        grid.addWidget(label1, 1, 0)
        grid.addWidget(self.code_edit, 2, 0)
        grid.addWidget(label2, 3, 0)
        grid.addWidget(button2, 4, 0, 1, 2)

        # 关闭窗口
        button2.clicked.connect(self.close)
        self.setLayout(grid)

    def center(self):
        # 该语句用来计算出显示器的分辨率（screen.width, screen.height）
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def get_text(self):
        self.out_code = self.code_edit.text()
        # print(self.out_code)
        return self.out_code

    def show_code_img(self):
        img = QtGui.QPixmap(self.img_path)
        self.label_code.setPixmap(img)

    def closeEvent(self, event):
        code = self.get_text()
        if len(code) < 4 or len(code) >= 8:
            QtWidgets.QMessageBox.about(self, "验证码输入错误", "请注意：\n验证码一般为4-6位，请重新输入!")
            event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    center = CodeRecognition()

    # 改变输入的图片。
    path = "image_2.png"
    center.img_path = path
    center.show_code_img()

    center.show()
    app.exec_()
    rec_code = center.get_text()
    print("识别的验证码为：", rec_code)
```

最后附上完整的程序：
[github地址3](https://github.com/qwerty200696/HDHome_crawler/blob/master)

