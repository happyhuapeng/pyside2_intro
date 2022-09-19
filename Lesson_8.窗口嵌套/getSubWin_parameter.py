# -*- coding:utf-8 -*-
# ---
# 获取子窗口的参数，子窗口为动态UI加载
# author：山海关 2022.9
import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow


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


        # ------------------------------------------
        self.subwin2 = SubWin2() # 实例化子窗口2
        # 连接子窗口的自定义信号和槽函数
        self.subwin2.signal_.connect(self.handle_signal)

        # 设置通过ObjectName来连接槽函数
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.Slot()
    def on_OpenButtonSubwin2_clicked(self): # 显示子窗口2
        self.subwin2.ui.show()

    def handle_signal(self, str):  # 处理返回信号函数
        print(str)
        self.label.setText('收到信号：'+str)


class SubWin2(QMainWindow):
    signal_ = QtCore.Signal(str)  # 自定义信号

    def __init__(self, parent=None):
        super(SubWin2, self).__init__(parent=parent)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        # 从文件中加载ui文件，这是套路，加载文件要写这3句，变量名qfile随便起名字
        qfile = QFile(r'.\subWin.ui')  # 选择UI文件
        qfile.open(QFile.ReadOnly)
        qfile.close()

        # 从ui文件定义中动态创建一个相应的窗口对象
        self.ui = QUiLoader().load(qfile)

        self.ui.pushButton_confirm.clicked.connect(self.send_to_main)
        self.ui.pushButton_confirm.clicked.connect(self.ui.close) # close ui


    def send_to_main(self):
        self.name1 = self.ui.lineEdit_2.text()
        self.name2 = self.ui.lineEdit_3.text()
        self.name3 = self.ui.lineEdit.text()
        self.name4 = self.ui.plainTextEdit.toPlainText()

        self.signal_.emit('名称：%s\n描述：%s\n负责人：%s\n处理单位：%s'
                          % (self.name1, self.name2, self.name3, self.name4))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
