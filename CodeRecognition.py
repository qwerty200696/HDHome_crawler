# -*- coding: utf-8 -*-
"""手动输入验证码"""
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
        # button1 = QtWidgets.QPushButton('确认', self)
        button2 = QtWidgets.QPushButton('关闭', self)

        grid = QGridLayout()
        grid.setSpacing(0)

        grid.addWidget(self.label_code, 0, 0, 1, 2)
        grid.addWidget(label1, 1, 0)
        grid.addWidget(self.code_edit, 2, 0)
        grid.addWidget(label2, 3, 0)

        # grid.addWidget(button1, 4, 0, 1, 2)
        grid.addWidget(button2, 4, 0, 1, 2)
        # grid.alignment()

        # 信号与槽中不能带有括号，只需要函数名。
        # button1.clicked.connect(self.get_text)
        # 只是关闭窗口，但是这不退出程序。很关键，quit就直接推出程序了貌似。
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
        # self.get_text()
        # reply = QtWidgets.QMessageBox.question(self, '确认退出', '你确定要退出么？',
        #                                        QtWidgets.QMessageBox.Yes,
        #                                        QtWidgets.QMessageBox.No)
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
