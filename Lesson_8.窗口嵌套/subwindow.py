# -*- coding:utf-8 -*-


import sys
import random
from PySide2 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир", "Hello world"]
        self.resize(1024, 768)
        self.setWindowTitle('主窗口')

        # --- 布局和控件 ---#

        # 中心控件
        self.center_widget = QtWidgets.QWidget()
        # 中心控件布局
        self.center_widget_layout = QtWidgets.QVBoxLayout()
        # 标签
        self.label = QtWidgets.QLabel('Hello world') # label
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        self.Button = QtWidgets.QPushButton('点击打开 sub-window1')
        self.Button.setObjectName('OpenButtonSubwin1') # SetObjectName相当于给这个实例命了个名字。——唯一标识符
        # 此处必须得给两个button重命名，否则下面的回调函数不好写。
        self.Button2 = QtWidgets.QPushButton('点击打开 sub-window2')
        self.Button2.setObjectName('OpenButtonSubwin2')
        # 将标签添加到布局里
        self.center_widget_layout.addWidget(self.label)
        self.center_widget_layout.addWidget(self.Button)
        self.center_widget_layout.addWidget(self.Button2)
        # 将布放置到中心控件上
        self.center_widget.setLayout(self.center_widget_layout)
        # 将中心控件设定到主窗口
        self.setCentralWidget(self.center_widget)

        # 可以看出窗口》画布layout》控件button等。

        # 初始化子窗口1
        self.subwindow1 = SubWindow1(parent=self)
        # ------------------------------------------
        self.subwindow2 = SubWindow2() # 初始化子窗口2
        # 连接子窗口的自定义信号和槽函数
        self.subwindow2.signal_.connect(self.on_sub2_signal)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)


    @QtCore.Slot()
    def on_OpenButtonSubwin1_clicked(self): # 显示子窗口1，对应上面重命名部分
        self.subwindow1.show()

    @QtCore.Slot()
    def on_OpenButtonSubwin2_clicked(self): # 显示子窗口2
        self.subwindow2.show()

    def on_sub2_signal(self, num):  # 子窗口的槽函数
        print('收到信号：', num)
        self.label.setText('收到信号：'+random.choice(self.hello))



class SubWindow1(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """
        第一种传参的方法：
            1. 为了避免一些问题的出现，避免所有变量重复定义
            2. 子窗口调用主窗口变量，要用 self.parent().window().[控件]
            3. 主窗口中初始化子窗口要指定parent为自己
            4. 主窗口直接可以调用子窗口变量
        :param parent:
        """
        super(SubWindow1, self).__init__(parent=parent)

        self.setWindowTitle('Sub window1')
        self.setFixedSize(800, 250)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # --- 布局和控件 ---#

        # 中心控件
        self.center_widget_sub = QtWidgets.QWidget()
        # 中心控件布局
        self.center_widget_layout_sub = QtWidgets.QVBoxLayout()
        # 按钮
        self.ButtonInSubWin1 = QtWidgets.QPushButton('点击更改主窗口文字')
        self.ButtonInSubWin1.setObjectName('ButtonSubWindow1') # 把button控件另外命名，不然回调不好用
        # 将标签添加到布局里
        self.center_widget_layout_sub.addWidget(self.ButtonInSubWin1)
        # 将布放置到中心控件上
        self.center_widget_sub.setLayout(self.center_widget_layout_sub)
        # 将中心控件设定到主窗口
        self.setCentralWidget(self.center_widget_sub)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.Slot()
    def on_ButtonSubWindow1_clicked(self): # 更改主窗口显示内容
        self.parent().window().label.setText(random.choice(self.parent().window().hello))


class SubWindow2(QtWidgets.QMainWindow):
    signal_ = QtCore.Signal(int) # 自定义信号

    def __init__(self, parent=None):
        """
        第二种传参的方法，自定义信号：
            1. 此方法不用指定parent，主窗口和子窗口是独立的
            2. 子窗口中，要在def init 函数之前定义信号，函数中通过[自定义信号].emit()来发出信号
            3. 主窗口中，初始化子窗口后要连接信号
            4. 信号的槽函数参数和发出新信号的类型要一致
        :param parent:
        """
        super(SubWindow2, self).__init__(parent=parent)

        self.setWindowTitle('Sub window2')
        self.setFixedSize(600, 250)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # --- 布局和控件 ---#

        # 中心控件
        self.center_widget_sub = QtWidgets.QWidget()
        # 中心控件布局
        self.center_widget_layout_sub = QtWidgets.QVBoxLayout()
        # 按钮
        self.ButtonInSubWin2 = QtWidgets.QPushButton('Click to change word in MainWindow')
        self.ButtonInSubWin2.setObjectName('ButtonSubWindow2')
        # 将标签添加到布局里
        self.center_widget_layout_sub.addWidget(self.ButtonInSubWin2)
        # 将布放置到中心控件上
        self.center_widget_sub.setLayout(self.center_widget_layout_sub)
        # 将中心控件设定到主窗口
        self.setCentralWidget(self.center_widget_sub)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.Slot()
    def on_ButtonSubWindow2_clicked(self):
        self.signal_.emit(10) # 发射信号


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
