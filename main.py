#coding: utf-8
import sys
from logviewer import LogViewer
from PyQt5.QtWidgets import QApplication,QMainWindow


def main():
    app=QApplication(sys.argv)
    win=LogViewer()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
