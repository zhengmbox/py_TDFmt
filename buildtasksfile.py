from PyQt5 import QtCore, QtGui, QtWidgets
from basefile import Ui_Form
from modifySaveAs import ModifySaveAs


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt);
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)


class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            w = 0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)


if __name__ == '__main__':

    def getbasefilesignal(connect):
        modifyfile.lineedit_basefile.setText(connect)

    import sys

    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(ProxyStyle())
    w = TabWidget()
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("zoom.png"), "编辑基准文件")
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("1.png"), "修改另存文件")
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("2.png"), "批量修改另存")
    basefile = Ui_Form()
    basefile.setupUi(w.widget(0))
    basefile.mySignal.connect(getbasefilesignal)
    modifyfile = ModifySaveAs()
    modifyfile.setupUi(w.widget(1))
    modifyfile.lineedit_basefile.setText(basefile.lineEdit.text())

    win = QtWidgets.QMainWindow()
    win.setWindowTitle("MainWindow")
    win.setCentralWidget(w)
    win.resize(800, 600)
    win.show()

    sys.exit(app.exec_())
