# coding=utf-8
"""
基于后处理Force文件夹，汇集部件气动力（.plt文件），总气动力数据保存至sumAssem文件夹
"""

import os
from PyQt5 import QtCore, QtGui, QtWidgets


class sumForce(object):
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
        self.pushButton_2.clicked.connect(self.sumAssemForce)

    def choicefolder(self):
        if os.path.isdir(self.lineEdit.text()):
            self.workpath = QtWidgets.QFileDialog.getExistingDirectory(self.lineEdit, "选取Force文件夹", self.lineEdit.text())
        else:
            self.workpath = QtWidgets.QFileDialog.getExistingDirectory(self.lineEdit, "选取Force文件夹", "C:/")
        self.lineEdit.setText(self.workpath)
        self.listmodel.setStringList([""])
        self.textEdit.setText("")

    def init_para(self):
        self.workpath = "d:\\TengDun\\tu_20200616\\tongqi\\beta\\postdeal\\Force\\"
        self.qjname = "sumAssem"

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
        files = os.listdir(dir0)
        for i in range(len(files)):
            if os.path.isfile(os.path.join(dir0, files[i])) \
                    and files[i][-4:] == ".plt":
                self.plts.append(files[i])
        print(self.plts)
        return 0

    def sumAssemForce(self):
        if self.seachfiles() != 0:
            return
        qjdir = os.path.join(self.workpath, self.qjname)
        if not os.path.isdir(qjdir):
            os.mkdir(qjdir)
        for fname in self.plts:
            with open(os.path.join(self.workpath, self.dirs[0]+os.sep+fname), 'r') as fr:
                lns0 = fr.readline()
                lns1 = fr.readline()
                frcs = fr.read()
            sumfrc = list(map(float, frcs.split()))
            # for i in range(int(len(sumfrc) / 14)):
            #     print(sumfrc[14 * i:14 * i + 14])

            for nowdir in self.dirs[1:]:
                with open(os.path.join(self.workpath, nowdir+os.sep+fname), 'r') as fr:
                    fr.readline()
                    fr.readline()
                    numlst = list(map(float, fr.read().split()))
                for i in range(len(numlst)):
                    if i % 14 > 3:
                        sumfrc[i] += numlst[i]

            with open(os.path.join(qjdir, fname), 'w') as fw:
                fw.write(lns0)
                fw.write(lns1)
                for i in range(len(sumfrc)):
                    if i % 14 == 0:
                        fw.write("%d " % int(sumfrc[i]))
                    elif i % 14 < 4:
                        fw.write("%10.5f " % sumfrc[i])
                    elif i % 14 == 13:
                        fw.write("%12.8f\n" % sumfrc[i])
                    else:
                        fw.write("%12.8f " % sumfrc[i])

            with open(os.path.join(qjdir, fname), 'r') as fr:
                self.textEdit.setText(fr.read())
                self.lineEdit2.setText("完成部件力（力矩）收集")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frame = QtWidgets.QFrame()
    demo = sumForce()
    demo.setupUi(frame)
    win = QtWidgets.QMainWindow()
    win.setWindowTitle("MainWindow")
    win.setCentralWidget(frame)
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())

