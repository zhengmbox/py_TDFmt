# -*- coding: utf-8 -*-

"""
在Qtextedit中搜索并定位关键词
"""
import os
from PyQt5 import QtCore, QtGui, QtWidgets


def delete_tail(ln):
    return ln.replace('\n', '').replace('\r', '')


class Ui_Form(QtWidgets.QWidget):
    # 自定义信号
    mySignal = QtCore.pyqtSignal(str)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(654, 505)

        label = QtWidgets.QLabel("基准文件: ")
        label.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton("选择文件")
        self.pushButton_2 = QtWidgets.QPushButton("载入文件")
        self.pushButton_3 = QtWidgets.QPushButton("回写文件")
        self.pushButton_4 = QtWidgets.QPushButton("确认基准文件")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setStyleSheet('background-color:cyan;font-size:20px')
        label2 = QtWidgets.QLabel("命令信息：")
        self.lineEdit2 = QtWidgets.QLineEdit()
        self.lineEdit2.setEnabled(False)

        label3 = QtWidgets.QLabel("索引词")
        self.combox_indexword = QtWidgets.QComboBox()
        label4 = QtWidgets.QLabel("搜索词")
        self.lineEdit_findword = QtWidgets.QLineEdit()
        label5 = QtWidgets.QLabel("新值")
        label5.setEnabled(False)
        self.lineEdit_newvalue = QtWidgets.QLineEdit()
        self.lineEdit_newvalue.setEnabled(False)
        self.pushButton_next = QtWidgets.QPushButton("下一个")
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addStretch(1)
        vlayout.addWidget(label3)
        vlayout.addWidget(self.combox_indexword)
        vlayout.addStretch(1)
        vlayout.addWidget(label4)
        vlayout.addWidget(self.lineEdit_findword)
        vlayout.addWidget(self.pushButton_next)
        vlayout.addStretch(1)
        vlayout.addWidget(label5)
        vlayout.addWidget(self.lineEdit_newvalue)
        vlayout.addStretch(3)

        gridlayout = QtWidgets.QGridLayout(Form)
        gridlayout.addWidget(label, 1, 1, 2, 1)
        gridlayout.addWidget(self.lineEdit, 1, 2, 1, 4)
        gridlayout.addWidget(self.pushButton, 2, 2, 1, 1)
        gridlayout.addWidget(self.pushButton_2, 2, 3, 1, 1)
        gridlayout.addWidget(self.pushButton_3, 2, 4, 1, 1)
        gridlayout.addWidget(self.pushButton_4, 2, 5, 1, 1)
        gridlayout.addWidget(self.textEdit, 3, 2, 1, 4)
        gridlayout.addWidget(label2, 5, 1, 1, 1)
        gridlayout.addWidget(self.lineEdit2, 5, 2, 1, 4)
        gridlayout.addLayout(vlayout, 3, 1, 1, 1)
        gridlayout.setColumnStretch(2, 1)
        gridlayout.setColumnStretch(3, 1)
        gridlayout.setColumnStretch(4, 1)
        gridlayout.setColumnStretch(5, 1)

        self.combox_indexword.addItems(
            ["", "$I-restart", "$I-n_steps", "$R-Altitude", "$R-p_bar",
             "$I-n_wrest", "$I-vis_mode", "$I-mgrid", "$I-flux_fine", "$I-EntropyCorType",
             "$I-UsingMSM", "$I-order", "$I-iprec", "$S-gridname", "$I-GMRES", "$I-SixDofSlover",
             "$I-NacInNum", "$I-jet_num", "$R-real_dt", "$R-length_ref"])
        self.position = 0

        # self.retranslateUi(Form)
        # QtCore.QMetaObject.connectSlotsByName(Form)

        self.pbconnect()

    def retranslateUi(self, Form):
        pass
        # _translate = QtCore.QCoreApplication.translate
        # Form.setWindowTitle(_translate("Form", "Form"))
        # # self.label.setText(_translate("Form", "基本文件"))
        # self.pushButton.setText(_translate("Form", "选择文件"))
        # self.pushButton_2.setText(_translate("Form", "载入文件"))
        # self.pushButton_3.setText(_translate("Form", "回写文件"))
        # self.pushButton_4.setText(_translate("Form", "确认基准文件"))

    def pbconnect(self):
        self.pushButton.clicked.connect(self.choicefile)
        self.pushButton_2.clicked.connect(self.loadfile)
        self.pushButton_3.clicked.connect(self.rewritefile)
        self.pushButton_4.clicked.connect(self.sendbasefile)
        self.combox_indexword.currentIndexChanged.connect(self.indexwordchange)
        self.lineEdit_findword.textChanged.connect(self.findwordchange)
        self.pushButton_next.clicked.connect(self.nextword)

    def sendbasefile(self):
        self.mySignal.emit(self.lineEdit.text())

    def indexwordchange(self):
        self.position = 0
        keyword = "\\" + self.combox_indexword.currentText()
        self.keywordchange(keyword)

    def findwordchange(self):
        self.position = 0
        keyword = self.lineEdit_findword.text()
        self.keywordchange(keyword)

    def nextword(self):
        keyword = self.lineEdit_findword.text()
        self.position += len(keyword)
        self.keywordchange(keyword)

    def keywordchange(self, keyword):
        if not keyword:
            return
        
        self.lineEdit2.setText(keyword)

        col = QtGui.QColor(255, 0, 0)

        # 恢复默认的颜色
        cursor = self.textEdit.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.setCharFormat(QtGui.QTextCharFormat())
        cursor.clearSelection()
        self.textEdit.setTextCursor(cursor)

        # 文字颜色
        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(col)

        # 正则
        expression = QtCore.QRegExp(keyword)
        self.textEdit.moveCursor(QtGui.QTextCursor.Start)
        cursor = self.textEdit.textCursor()

        # 查找设置颜色
        # pos = 0
        index = expression.indexIn(self.textEdit.toPlainText(), self.position)
        if index >= 0:
            cursor.setPosition(index)
            cursor.movePosition(QtGui.QTextCursor.Right,
                                QtGui.QTextCursor.KeepAnchor, len(keyword))
            cursor.mergeCharFormat(fmt)

            # 计算文本行row，为显示居中将 行号+15
            nline = self.textEdit.toPlainText().count("\n", 0, index) + \
                    self.textEdit.toPlainText().count("\r", 0, index) + 11
            nlinemax = self.textEdit.toPlainText().count("\n") + \
                       self.textEdit.toPlainText().count("\r")
            nline = min(nline, nlinemax)
            # cursor 定位至文本行，用position函数得到这一行在文件流中的位置坐标
            position = self.textEdit.document().findBlockByLineNumber(nline).position()
            cursor.setPosition(position, QtGui.QTextCursor.MoveAnchor)
            # 把鼠标设置为有效setTextCursor，跳转到行
            self.textEdit.setTextCursor(cursor)
            self.position = index
        else:
            self.lineEdit2.setText("已至文末，搜索 %s 未果！" % keyword)
            self.position = 0

    def rewritefile(self):
        self.lineEdit2.setText("回写文件： %s" % self.lineEdit.text())
        txt = self.textEdit.toPlainText()
        with open(self.lineEdit.text(), 'w') as fw:
            fw.write(txt)

    def loadfile(self):
        if os.path.isfile(self.lineEdit.text()):
            self.lineEdit2.setText("载入文件： %s" % self.lineEdit.text())
            with open(self.lineEdit.text(), 'r') as fr:
                lns = fr.readlines()
            self.textEdit.clear()
            for line in lns:
                self.textEdit.append(delete_tail(line))

    def choicefile(self):
        folder, fname = os.path.split(self.lineEdit.text())
        if not os.path.isdir(folder):
            folder, fname = os.path.split(".%sname" % os.sep)
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', folder, "parfile(*.par)")
        if not filename[0] == '':
            self.lineEdit.setText(filename[0])
            self.lineEdit2.setText("选择文件: %s" % filename[0])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frame = QtWidgets.QFrame()
    basefile = Ui_Form()
    basefile.setupUi(frame)
    win = QtWidgets.QMainWindow()
    win.setWindowTitle("MainWindow")
    win.setCentralWidget(frame)
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())
