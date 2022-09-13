import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import (QApplication, QMainWindow,
                               QTreeWidgetItem, QLabel, QFileDialog, QDockWidget)
from enum import Enum  ##枚举类型
from PySide2.QtCore import Slot, Qt, QDir, QFileInfo, QFile
from PySide2.QtGui import QIcon, QPixmap
# from ui_MainWindow import Ui_MainWindow
from PySide2.QtUiTools import QUiLoader


class TreeItemType(Enum):  ##节点类型枚举类型
    itTopItem = 1001  # 顶层节点
    itGroupItem = 1002  # 组节点
    itFileItem = 1003  # 文件节点

class main_ui(object):
    def __init__(self):
        super(main_ui, self).__init__()
        # self.ui=Ui_MainWindow()     #创建UI对象
        # self.ui.setupUi(self)       #构造UI界面
        qfile = QFile(r'D:\code\pyside2-master\TreeDock_whp\MainWindow.ui')  # 选择UI文件
        qfile.open(QFile.ReadOnly)
        qfile.close()
        self.ui = QUiLoader().load(qfile)
        self.ui.resize(2000, 1800)

        self.itemFlags = (Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
                          | Qt.ItemIsEnabled | Qt.ItemIsAutoTristate)  # 节点标志
        self.ui.setCentralWidget(self.ui.scrollArea)
        self.__iniTree() # 初始化树

        # 以下的属性设置在UI Designer里已经设置，这里是代码设置方法
        self.ui.dockWidget.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.ui.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.ui.scrollArea.setWidgetResizable(True)  # 自动调整内部组件大小
        self.ui.scrollArea.setAlignment(Qt.AlignCenter)
        #
        self.ui.AddCase.triggered.connect(self.newCase)  # 工具栏槽函数
        self.ui.AddFiles.triggered.connect(self.open)  # 工具栏槽函数
        self.ui.DeleteItem.triggered.connect(self.__DeleteItem)  # 工具栏槽函数

        self.ui.tree.clicked.connect(self.currentItemChanged)  # 树菜单的响应函数绑定
        self.ui.actClose.triggered.connect(self.ui.close)  # 退出工具栏

        # 设置通过ObjectName来连接槽函数
        # QtCore.QMetaObject.connectSlotsByName(self.ui)



    ##  =================自定义功能函数================================
    def __iniTree(self):  ##初始化目录树
        # self.ui.tree.clear()
        self.ui.tree.setHeaderLabels(['案件目录'])  # 设置头的标题
        self.newCase()

    def newCase(self):  # 建立新案件的根
        icon = QIcon("./icons/15.ico")
        root = QTreeWidgetItem(TreeItemType.itTopItem.value)  # item为树根
        root.setIcon(0, icon)  # 先加图片
        root.setText(0, "新建案件1")  # 再加文字
        root.setFlags(self.itemFlags)
        root.setCheckState(0, Qt.Checked)  # 设置选中状态
        root.setData(0, Qt.UserRole, "")  # 初始化数据为空
        self.ui.tree.addTopLevelItem(root) # 设置根节点
        root.setExpanded(True)  # 展开节点
        # 二级目录
        root_jc = QTreeWidgetItem(TreeItemType.itGroupItem.value)
        root_jc.setIcon(0, icon)  # 先加图片
        root_jc.setText(0, "检 材")  # 再加文字
        root.addChild(root_jc)

        root_yb = QTreeWidgetItem(TreeItemType.itGroupItem.value)
        root_yb.setIcon(0, icon)  # 先加图片
        root_yb.setText(0, "样 本")  # 再加文字
        root.addChild(root_yb)

    ##添加音频文件节点
    def open(self): # 打开文件
        fileList, flt = QFileDialog.getOpenFileNames(self.ui,
                                                     "选择一个或多个文件", "", "Images(*.jpg)")
        # 多选文件,返回两个结果，fileList是一个列表类型，存储了所有文件名； flt是设置的文件filter，即"Images(*.jpg)"
        fold_name = fileList[0].split('/')[-2]  # 选中的文件夹名
        # num = self.ui.tree.topLevelItemCount()
        if (len(fileList) < 1):  # fileList是list[str]
            return

        item = self.ui.tree.currentItem()  # 当前节点

        if item == None:
            return
        else:
            if item.type() == TreeItemType.itFileItem.value:  # 若当前节点是文件节点，取其父节点作为父节点
                parItem = item.parent()  # 否则取当前节点为父节点
                topItem = parItem.parent()
            elif item.type() == TreeItemType.itGroupItem.value:
                parItem = item
                topItem = item.parent()
            else:
                topItem = item
        # root = self.ui.tree.topLevelItem(0)
        topItem.setText(0, "案件名称： " + fold_name)  # 以文件夹名称设置 root 节点名称

        icon = QIcon("./icons/31.ico")
        for i in range(len(fileList)):
            fullFileName = fileList[i]  # 带路径文件名
            fileinfo = QFileInfo(fullFileName)
            nodeText = fileinfo.fileName()  # 不带路径文件名

            item = QTreeWidgetItem(TreeItemType.itFileItem.value)  # 节点类型
            item.setIcon(0, icon)  # 第1列的图标
            item.setText(0, nodeText)  # 第1列的文字
            # item.setText(TreeColNum.colItemType.value,"音频")  #第2列的文字
            item.setFlags(self.itemFlags)
            item.setCheckState(0, Qt.Checked)

            item.setData(0, Qt.UserRole, fullFileName)  # 关联数据为文件全名
            parItem.addChild(item)  # 增加子节点

        parItem.setExpanded(True)  # 展开节点

    def currentItemChanged(self):  ## 树点击文件的回调函数
        self.currentItem = self.ui.tree.currentItem()  # 获取当前菜单
        if (self.currentItem == None):
            return
        nodeType = self.currentItem.type()  # 获取节点类型

        if (nodeType == TreeItemType.itFileItem.value):  # 文件节点
            self.__display()  # 点击内容显示

    def __display(self):  ##显示节点item 内容
        filename = self.currentItem.data(0, Qt.UserRole)
        print(filename)
        # self.ui.statusBar.showMessage(filename)   #状态栏显示文件名

        self.ui.label.setText(filename)

    def __DeleteItem(self):  # 只删除三级目录
        item = self.ui.tree.currentItem()  # 当前节点
        if item == None:
            return
        else:
            if item.type() == TreeItemType.itFileItem.value:  # 若当前节点是文件节点，取其父节点作为父节点
                parItem = item.parent()  # 否则取当前节点为父节点
                parItem.removeChild(item)
            else:
                return




##  ===========窗体测试程序=================================        
if __name__ == '__main__':
    # 下面这4句是套路，要想正常显示窗口必须有这4句
    app = QApplication([])
    # 设置窗口风格
    app.setStyle('Fusion')
    mainWin = main_ui()
    mainWin.ui.show()
    app.exec_()
