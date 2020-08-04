# coding=utf-8
"""
由两个后处理的Force文件夹，将对应的数据（.plt文件）合并，保存至新的Force文件夹
"""
import os
from PyQt5 import QtCore, QtGui, QtWidgets


class Force3(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(654, 505)

        label = QtWidgets.QLabel("Force文件夹：")
        label.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit = QtWidgets.QLineEdit()
        self.pushButton = QtWidgets.QPushButton("选择Force文件夹")
        self.pushButton_2 = QtWidgets.QPushButton("计算总力")
        self.listview = QtWidgets.QListView(Form)
        self.listview.setStyleSheet('background-color:blue;font-size:20px')
        self.listmodel = QtCore.QStringListModel()
        self.listview.setModel(self.listmodel)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setStyleSheet('background-color:cyan;font-size:12px')
        label2 = QtWidgets.QLabel("命令信息：")
        label2.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit2 = QtWidgets.QLineEdit()
        self.lineEdit2.setEnabled(False)

        gridlayout = QtWidgets.QGridLayout(Form)
        gridlayout.addWidget(label, 1, 1, 2, 1)
        gridlayout.addWidget(self.lineEdit, 1, 2, 1, 4)
        gridlayout.addWidget(self.pushButton, 2, 2, 1, 1)
        gridlayout.addWidget(self.pushButton_2, 2, 3, 1, 1)
        gridlayout.addWidget(self.listview, 3, 1, 1, 4)
        gridlayout.addWidget(self.textEdit, 3, 2, 1, 4)
        gridlayout.addWidget(label2, 5, 1, 1, 1)
        gridlayout.addWidget(self.lineEdit2, 5, 2, 1, 4)

        self.init_para()
        self.lineEdit.setText(self.workpath)

        self.pbconnect()

    def pbconnect(self):
        self.pushButton.clicked.connect(self.choicefolder)
        self.pushButton_2.clicked.connect(self.AssemForce)

    def choicefolder(self):
        if os.path.isdir(self.lineEdit.text()):
            self.workpath = QtWidgets.QFileDialog.getExistingDirectory(self.lineEdit, "选取Force文件夹", self.lineEdit.text())
        else:
            self.workpath = QtWidgets.QFileDialog.getExistingDirectory(self.lineEdit, "选取Force文件夹", "C:/")
        if self.workpath:
            self.lineEdit.setText(self.workpath)
            self.listmodel.setStringList([""])
            self.textEdit.setText("")

    def init_para(self):
        self.dealpost1 = r"d:\TengDun\tu_20200616\tongqi\beta\postdeal\Force"
        self.dealpost2 = r"d:\TengDun\tu_20200616\tongqi\beta\unpostdeal\Force"
        self.dealpost3 = r"d:\TengDun\tu_20200616\tongqi\beta\un2postdeal\Force"
        self.dealnew = r"d:\TengDun\tu_20200616\tongqi\beta\newpostdeal\Force"
        self.qjname = "sumAssem"
        self.fname = "Beita8.00_Mach0.12.plt"
        self.workpath = self.dealpost1
        if not os.path.isdir(self.dealnew):
            os.makedirs(self.dealnew)

    def seachfiles(self):
        self.dirs = os.listdir(self.workpath)
        if "quanji" in self.dirs:
            self.dirs.remove("quanji")
        if "QJ" in self.dirs:
            self.dirs.remove("QJ")
        if self.qjname in self.dirs:
            self.dirs.remove(self.qjname)
        for i in range(len(self.dirs)):
            if not os.path.isdir(os.path.join(self.workpath, self.dirs[i])):
                del self.dirs[i:]
        print(self.dirs)
        self.listmodel.setStringList(self.dirs)
        if len(self.dirs) < 1:
            self.lineEdit2.setText("部件数太少，请重新选择文件夹")
            return -1
        dir0 = os.path.join(self.workpath, self.dirs[0])
        print(dir0)
        self.plts = []
        self.plts.append(self.fname)
        # files = os.listdir(dir0)
        # for i in range(len(files)):
        #     if os.path.isfile(os.path.join(dir0, files[i])) \
        #             and files[i][-4:] == ".plt":
        #         self.plts.append(files[i])
        print(self.plts)
        return 0

    def AssemForce(self):
        if self.seachfiles() != 0:
            return
        for fname in self.plts:
            for nowdir in self.dirs:
                with open(os.path.join(self.workpath, nowdir+os.sep+fname), 'r') as fr:
                    lns1 = fr.readlines()
                with open(os.path.join(self.dealpost2, nowdir+os.sep+fname), 'r') as fr:
                    lns2 = fr.readlines()
                with open(os.path.join(self.dealpost3, nowdir+os.sep+fname), 'r') as fr:
                    lns3 = fr.readlines()
                if not os.path.isdir(os.path.join(self.dealnew, nowdir)):
                    os.mkdir(os.path.join(self.dealnew, nowdir))
                with open(os.path.join(self.dealnew, nowdir+os.sep+fname), 'w') as fw:
                    lnsnew = lns1
                    lnsnew[7] = lns2[2]
                    lnsnew[9] = lns2[3]
                    lnsnew[8] = lns3[2]
                    lnsnew[10] = lns3[3]
                    fw.writelines(lnsnew)
                if nowdir == self.dirs[-1]:
                    txt = ""
                    for line in lns1:
                        txt += line
                    for line in lns2[2:]:
                        txt += line
                    for line in lns3[2:]:
                        txt += line
                    txt += "\n"
                    for line in lnsnew:
                        txt += line

                    self.textEdit.setText(txt)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frame = QtWidgets.QFrame()
    demo = Force3()
    demo.setupUi(frame)
    win = QtWidgets.QMainWindow()
    win.setWindowTitle("MainWindow")
    win.setCentralWidget(frame)
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())

