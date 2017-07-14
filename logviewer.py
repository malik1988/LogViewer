#coding: utf-8
from PyQt5.QtWidgets import QFileDialog, QAbstractItemView, QTextBrowser
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtCore

import os
from PyQt5 import uic
uipath, uiname = os.path.split(os.path.realpath(__file__))
uiname = uiname.replace('.py', '.ui')
uifile = os.path.join(uipath, uiname)
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


class LogViewer(ui_mainwindow, qtbaseclass):
    model = None
    header = ('时间', '位置', '类型', '信息')

    def __init__(self):
        ui_mainwindow.__init__(self)
        qtbaseclass.__init__(self)
        self.setupUi(self)

        self.actOpen.triggered.connect(self.file_load)
        self.init_table()

    def file_load(self):
        '''打开文件'''
        file, state = QFileDialog.getOpenFileName(self, '打开日志文件', './',
                                                  '日志文件(*.log)')
        count = 0
        if state:
            with open(file, 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if ' - ' in line:
                        # 找到一行有效的日志记录
                        record = line.split(' - ')
                        for i, value in enumerate(record):
                            self.model.setItem(count, i, QStandardItem(value))
                        count += 1

    def init_table(self):
        self.model = QStandardItemModel(self.tableView)

        # model.setColumnCount(len(self.header))
        # for i, value in enumerate(self.header):
        #     model.setHeaderData(i, QtCore.Qt.Horizontal, value)

        # 通过list/tuple设置表头
        self.model.setHorizontalHeaderLabels(self.header)

        self.tableView.setModel(self.model)
        # 设置表格只读
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置表格按行选择
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

    def slot_table_pressed(self, index):
        '''表格点击事件'''
        row = index.row()
        text = ''
        for i in range(0, self.model.columnCount()):
            text += '%s: %s\n' % (self.header[i],
                                  self.model.index(row, i).data())

        self.textBrowser.setText(text)
