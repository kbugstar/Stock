# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_UseWeChat.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(QtWidgets.QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1132, 599)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(550, 60, 581, 531))
        self.groupBox.setObjectName("groupBox")
        self.cB_ipCheck = QtWidgets.QCheckBox(self.groupBox)
        self.cB_ipCheck.setGeometry(QtCore.QRect(140, 50, 71, 16))
        self.cB_ipCheck.setObjectName("cB_ipCheck")
        self.lb_from_3 = QtWidgets.QLabel(self.groupBox)
        self.lb_from_3.setGeometry(QtCore.QRect(10, 50, 31, 16))
        self.lb_from_3.setObjectName("lb_from_3")
        self.le_minspan = QtWidgets.QLineEdit(self.groupBox)
        self.le_minspan.setGeometry(QtCore.QRect(40, 50, 31, 20))
        self.le_minspan.setObjectName("le_minspan")
        self.lb_from_4 = QtWidgets.QLabel(self.groupBox)
        self.lb_from_4.setGeometry(QtCore.QRect(80, 50, 31, 16))
        self.lb_from_4.setObjectName("lb_from_4")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 571, 16))
        self.label.setObjectName("label")
        self.listView_Ip = QtWidgets.QListView(self.groupBox)
        self.listView_Ip.setGeometry(QtCore.QRect(10, 80, 561, 441))
        self.listView_Ip.setObjectName("listView_Ip")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 1121, 41))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.lb_from = QtWidgets.QLabel(self.groupBox_2)
        self.lb_from.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.lb_from.setObjectName("lb_from")
        self.tE_From = QtWidgets.QTimeEdit(self.groupBox_2)
        self.tE_From.setGeometry(QtCore.QRect(80, 10, 81, 22))
        self.tE_From.setObjectName("tE_From")
        self.lb_from_2 = QtWidgets.QLabel(self.groupBox_2)
        self.lb_from_2.setGeometry(QtCore.QRect(170, 10, 21, 16))
        self.lb_from_2.setObjectName("lb_from_2")
        self.tE_End = QtWidgets.QTimeEdit(self.groupBox_2)
        self.tE_End.setGeometry(QtCore.QRect(190, 10, 81, 22))
        self.tE_End.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.tE_End.setObjectName("tE_End")
        self.pBtn_Start = QtWidgets.QPushButton(self.groupBox_2)
        self.pBtn_Start.setGeometry(QtCore.QRect(280, 10, 81, 23))
        self.pBtn_Start.setObjectName("pBtn_Start")
        self.pBtn_Stop = QtWidgets.QPushButton(self.groupBox_2)
        self.pBtn_Stop.setGeometry(QtCore.QRect(370, 10, 81, 23))
        self.pBtn_Stop.setObjectName("pBtn_Stop")
        self.pBtn_Save = QtWidgets.QPushButton(self.groupBox_2)
        self.pBtn_Save.setGeometry(QtCore.QRect(510, 10, 81, 23))
        self.pBtn_Save.setObjectName("pBtn_Save")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 70, 531, 31))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 371, 16))
        self.label_3.setObjectName("label_3")
        self.cB_DbExport = QtWidgets.QCheckBox(self.groupBox_3)
        self.cB_DbExport.setGeometry(QtCore.QRect(410, 10, 51, 16))
        self.cB_DbExport.setObjectName("cB_DbExport")
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 110, 531, 481))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 351, 16))
        self.label_2.setObjectName("label_2")
        self.listView = QtWidgets.QListView(self.groupBox_4)
        self.listView.setGeometry(QtCore.QRect(10, 30, 511, 441))
        self.listView.setObjectName("listView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "微信 - Tdx 捕图 消息 通知"))
        self.groupBox.setTitle(_translate("Dialog", "检测 捕图软件机状态 设置"))
        self.cB_ipCheck.setText(_translate("Dialog", "运行"))
        self.lb_from_3.setText(_translate("Dialog", "间隔"))
        self.lb_from_4.setText(_translate("Dialog", "分钟"))
        self.label.setText(_translate("Dialog", "检测捕图软件 在交易日(或者b) 从 B时刻 到 C时刻 每隔D分钟,如果没有向数据库添加数据情况,微信通知"))
        self.lb_from.setText(_translate("Dialog", "运行时间从"))
        self.tE_From.setDisplayFormat(_translate("Dialog", "h:mm"))
        self.lb_from_2.setText(_translate("Dialog", "到"))
        self.tE_End.setDisplayFormat(_translate("Dialog", "h:mm"))
        self.pBtn_Start.setText(_translate("Dialog", "开始"))
        self.pBtn_Stop.setText(_translate("Dialog", "停止"))
        self.pBtn_Save.setText(_translate("Dialog", "保存配置"))
        self.label_3.setText(_translate("Dialog", "导出 当日数据库 记录(每隔5 分钟) 导出一次 到 文件 (日期.xls)"))
        self.cB_DbExport.setText(_translate("Dialog", "运行"))
        self.label_2.setText(_translate("Dialog", "编辑\"WeList.xls\",信息发送到\"微信\"和自己的\"文件传输助手\"里"))
