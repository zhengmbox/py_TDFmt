import sys, os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append(r"e:\python_project\TDFormat\py_TDFmt")
from ToTDFmt_class import TDDataConverter


# from TDDataConverter import TDDataConverter


def delete_tail(ln):
    return ln.replace('\n', '').replace('\r', '')


class SplitterExample(QWidget):
    def __init__(self):
        super(SplitterExample, self).__init__()
        self.__init_ctrpar()
        self.initUI()

    def initUI(self):
        # 设置全局布局为水平布局，设置标题与初始大小窗口
        hbox = QHBoxLayout()
        self.setWindowTitle("腾盾数据格式转换器")
        self.setGeometry(300, 300, 300, 200)
        self.setGeometry(0, 0, 800, 600)
        # 实例化QFrame控件
        self.topLeft = QFrame()
        self.topRight = QFrame()
        self.bottom = QFrame()
        self.topLeft.setFrameShape(QFrame.StyledPanel)
        self.topRight.setFrameShape(QFrame.StyledPanel)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        # 实例化QSplitter控件并设置初始为水平方向布局
        splitter1 = QSplitter(Qt.Horizontal)
        # 向Splitter内添加控件。并设置游戏的初始大小
        splitter1.addWidget(self.topLeft)
        splitter1.addWidget(self.topRight)
        splitter1.setSizes([250, 50])
        # 实例化Splitter管理器，添加控件到其中，设置垂直方向
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.bottom)
        splitter2.setSizes([200, 200])
        # 设置窗体全局布局以及子布局的添加
        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.initUI_topLeft()
        self.initUI_topRight()
        self.initUI_bottom()
        self.initUI_connect()

        if os.path.isfile('control.last'):
            with open('control.last', 'r') as fr:
                self.lineEditserial.setText(fr.readline())
            self.ctrpar_from_file()

    def initUI_topLeft(self):
        # self.topLeft增加控制参数输入控件
        # 参数：车次
        lableserial = QLabel("车次文件")
        self.lineEditserial = QLineEdit()
        self.pButtonInfile = QPushButton("选infile")
        self.pButtonSerial = QPushButton("读取")
        # 参数：半模
        lable1 = QLabel("半模/全模")
        self.radioButton_2 = QRadioButton("半模")
        self.radioButton_3 = QRadioButton("全模")
        # 参数：飞行高度
        lable2 = QLabel("飞行高度（米）")
        self.lineEdit2 = QLineEdit()
        # 参数：参考长度
        lable3 = QLabel("参考长度（米）")
        self.lineEdit3 = QLineEdit()
        # 参数：舵偏角
        lable4 = QLabel("舵偏角（°）\ndf dfa da de dr")
        self.lineEdit4 = QLineEdit()
        # 参数：原始数据文件夹
        lable5 = QLabel("原始数据文件夹")
        self.lineEdit5 = QLineEdit()
        self.pushbutton5 = QPushButton("选择")
        # 参数：原始数据文件夹
        lable6 = QLabel("格式输出文件夹")
        self.lineEdit6 = QLineEdit()
        self.pushbutton6 = QPushButton("选择")

        label0 = QLabel(self.topLeft)
        label0.setText("输入控制参数")
        label0.setContentsMargins(20, 0, 0, 0)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        label0.setFont(font)
        formLayout = QFormLayout(self.topLeft)
        formLayout.setContentsMargins(0, 30, 0, 0)
        hboxSerial = QHBoxLayout()
        hboxSerial.addWidget(self.lineEditserial)
        hboxSerial.addWidget(self.pButtonInfile)
        hboxSerial.addWidget(self.pButtonSerial)
        formLayout.addRow(lableserial, hboxSerial)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.radioButton_2)
        hbox1.addWidget(self.radioButton_3)
        formLayout.addRow(lable1, hbox1)
        formLayout.addRow(lable2, self.lineEdit2)
        formLayout.addRow(lable3, self.lineEdit3)
        formLayout.addRow(lable4, self.lineEdit4)
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.lineEdit5)
        hbox5.addWidget(self.pushbutton5)
        formLayout.addRow(lable5, hbox5)
        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.lineEdit6)
        hbox6.addWidget(self.pushbutton6)
        formLayout.addRow(lable6, hbox6)

    def initUI_topRight(self):
        # self.topRight窗口增加读取原始部件的控件
        self.pushbuttonOrgAssem = QPushButton("查看\n原始部件")
        self.pButtonAuto = QPushButton("原始部件=>\n输出部件")
        self.orgAssemBrower = QTextBrowser()
        hBox = QHBoxLayout()
        hBox.addWidget(self.pushbuttonOrgAssem)
        hBox.addWidget(self.pButtonAuto)
        vBox = QVBoxLayout(self.topRight)
        vBox.addLayout(hBox)
        vBox.addWidget(self.orgAssemBrower)

    def initUI_bottom(self):
        # self.bottom窗口增加读取原始部件的控件
        self.pButtonRead = QPushButton("读取in文件\n输出部件")
        self.pButtonSave = QPushButton("保存文件")
        self.pButtonSaveAs = QPushButton("另存文件")
        self.outAssemTextEdit = QTextEdit()
        self.outAssemTextEdit.setMaximumWidth(300)
        self.pButtonConvert = QPushButton("转换格式")
        self.txtlog = QTextBrowser()
        vBox = QVBoxLayout()
        vBox.setContentsMargins(0, 0, 0, 0)
        vBox.addWidget(self.pButtonRead)
        vBox.addWidget(self.pButtonSave)
        vBox.addWidget(self.pButtonSaveAs)
        vBox.addWidget(self.pButtonConvert)
        hBox = QHBoxLayout(self.bottom)
        hBox.setContentsMargins(0, 0, 0, 0)
        hBox.addLayout(vBox)
        hBox.addWidget(self.outAssemTextEdit)
        hBox.addWidget(self.txtlog)

    def initUI_connect(self):
        self.pushbutton5.clicked.connect(self.selectfolder5)
        self.pushbutton6.clicked.connect(self.selectfolder6)
        self.pushbuttonOrgAssem.clicked.connect(self.updata_orgAssem)
        self.pButtonRead.clicked.connect(self.readinfile_outAssem)
        self.pButtonAuto.clicked.connect(self.autoupdata_outAssem)
        self.pButtonSave.clicked.connect(self.saveFile)
        self.pButtonSaveAs.clicked.connect(self.saveAsFile)
        self.pButtonInfile.clicked.connect(self.choiceInfile)
        self.pButtonSerial.clicked.connect(self.ctrpar_from_file)
        self.pButtonConvert.clicked.connect(self.convert)

    def convert(self):
        case = TDDataConverter()
        case.run(self.serial)
        logfile = self.serial[:-3] + '.log'
        with open(logfile, 'r') as fr:
            lns = fr.readlines()
        txtlog = logfile + "\n"
        for line in lns:
            txtlog += line
        self.txtlog.append(txtlog)

    def selectfolder5(self):
        if os.path.isdir(self.lineEdit5.text()):
            folder0 = self.lineEdit5.text()
        else:
            folder0 = "./"
        directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", folder0)
        if not directory1 == '':
            self.lineEdit5.setText(directory1)

    def selectfolder6(self):
        if os.path.isdir(self.lineEdit6.text()):
            folder0 = self.lineEdit6.text()
        else:
            folder0 = "./"
        directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", folder0)
        if not directory1 == '':
            self.lineEdit6.setText(directory1)

    def __init_ctrpar(self):
        self.serial = ".%snull0000.in" % os.sep
        self.halfmodel = True
        self.altitude = 0.0
        self.lengthref = 1.0
        self.ruddleangle = "0 0 0 0 0"
        self.orgfolder = ".\\"
        self.outfolder = ".\\"

    def ctrpar_from_file(self):
        self.serial = self.lineEditserial.text()
        if os.path.isfile(self.serial):
            self.txtlog.append("读入文件：%s" % self.serial)
            with open(self.serial, 'r') as fr:
                lns = fr.readlines()
            for line in lns:
                self.txtlog.append(delete_tail(line))
            i = 0
            while i < len(lns):
                lnlst = lns[i].split()
                if (lnlst[0] == '#'):
                    i += 1
                    if (len(lnlst) > 1 and lnlst[1] == 'halfmodel'):
                        self.halfmodel = bool(delete_tail(lns[i]))
                    elif (len(lnlst) > 1 and lnlst[1] == 'altitude'):
                        highlist = delete_tail(lns[i]).split()
                        self.altitude = float(highlist[0])
                        self.lengthref = float(highlist[-1])
                    elif (len(lnlst) > 1 and lnlst[1] == 'df'):
                        self.ruddleangle = delete_tail(lns[i])
                    elif (len(lnlst) > 1 and lnlst[1] == 'outfolder'):
                        self.outfolder = delete_tail(lns[i])
                    elif (len(lnlst) > 1 and lnlst[1] == 'orgfolder'):
                        self.orgfolder = delete_tail(lns[i])
                    elif (len(lnlst) > 1 and lnlst[1] == 'name_outfile'):
                        self.txtOutAssem = ""
                        while len(lns[i]) < 5 or lns[i][:5] != "# FIN":
                            self.txtOutAssem += lns[i]
                            i += 1
                i += 1
        self.showcontrol()
        with open("control.last", 'w') as fw:
            fw.write(self.serial)

    def showcontrol(self):
        self.lineEditserial.setText(self.serial)
        self.radioButton_2.setChecked(self.halfmodel)
        self.lineEdit2.setText(str(self.altitude))
        self.lineEdit3.setText(str(self.lengthref))
        self.lineEdit4.setText(self.ruddleangle)
        self.lineEdit5.setText(self.orgfolder)
        self.lineEdit6.setText(self.outfolder)
        try:
            self.outAssemTextEdit.setText(self.txtOutAssem)
        except:
            pass

    def updata(self):
        self.serial = self.lineEditserial.text()
        self.halfmodel = self.radioButton_2.Checked()
        self.altitude = float(self.lineEdit2.text())
        self.lengthref = float(self.lineEdit3.text())
        self.ruddleangle = self.lineEdit4.text()
        self.outfolder = self.lineEdit5.text()
        self.orgfolder = self.lineEdit6.text()

    def updata_orgAssem(self):
        self.orgfolder = self.lineEdit5.text()
        if not os.path.isdir(self.orgfolder):
            self.txtlog.append("更新原始部件失败，原始数据文件夹%s不存在" % self.orgfolder)
            return
        print(self.lineEdit5.text())
        orgAssemList = ''
        dirs = os.listdir(self.orgfolder)
        ncount = 0
        for name in dirs:
            if os.path.isdir(os.path.join(self.orgfolder, name)):
                print(name)
                ncount += 1
                orgAssemList += name + '\n'
        self.orgAssemBrower.setText("%s \n共%d个部件" % (orgAssemList, ncount))

    def autoupdata_outAssem(self):
        strText = str(self.orgAssemBrower.toPlainText())
        lns = strText.split()[:-1]
        print(lns)
        txtOutAssem = "%20s %20s\n" % ("QJ", "quanji")
        for line in lns:
            if not line == 'quanji':
                txtOutAssem += "%20s %20s\n" % (line, line)
        self.outAssemTextEdit.setText(txtOutAssem)

    def readinfile_outAssem(self):
        try:
            self.outAssemTextEdit.setText(self.txtOutAssem[:-1])
        except:
            pass

    def choiceInfile(self):
        folder, fname = os.path.split(self.lineEditserial.text())
        filename = QFileDialog.getOpenFileName(self, 'Open file', folder, "in file(*.in)")
        if not filename[0] == '':
            self.txtlog.append("Choice and read a in_file: %s" % filename[0])
            self.lineEditserial.setText(filename[0])
            self.ctrpar_from_file()

    def saveAsFile(self):
        print("saveFile")
        folder, fname = os.path.split(self.lineEditserial.text())
        filename = QFileDialog.getSaveFileName(self, 'save file', folder, "in file(*.in)")
        print(filename)
        if filename[0] != '':
            self.serial = filename[0]
            self.lineEditserial.setText(filename[0])
            self.saveFile()

    def saveFile(self):
        print(self.serial)
        if not os.path.isfile(self.serial):
            self.txtlog.append("保存文件失败：指定的文件%s不存在" % self.serial)
            return
        with open(self.serial, 'w') as fw:
            fw.write("# halfmodel\n")
            fw.write("%r\n" % self.radioButton_2.isChecked())
            fw.write("# altitude lref\n")
            fw.write("%s   %s\n" % (self.lineEdit2.text(), self.lineEdit3.text()))
            fw.write("# df dfa da de dr\n")
            fw.write("%s\n" % self.lineEdit4.text())
            fw.write("# orgfolder\n")
            fw.write("%s\n" % self.lineEdit5.text())
            fw.write("# outfolder\n")
            fw.write("%s\n" % self.lineEdit6.text())
            fw.write("# name_outfile and pathnames_in\n")
            self.txtOutAssem = self.outAssemTextEdit.toPlainText()
            if len(self.txtOutAssem) and self.txtOutAssem[-1] != '\n':
                fw.write(self.txtOutAssem + "\n# FIN\n")
            else:
                fw.write(self.txtOutAssem + "# FIN\n")
            self.txtlog.append("保存文件%s，完成" % self.serial)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = SplitterExample()
    ui.show()
    sys.exit(app.exec_())
