# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(580, 364)
        Form.setStyleSheet("#label_header {\n"
"font: 16pt \"Courier\";\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_header = QtWidgets.QLabel(Form)
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)
        self.label_header.setObjectName("label_header")
        self.gridLayout.addWidget(self.label_header, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tab_widget_main = QtWidgets.QTabWidget(Form)
        self.tab_widget_main.setObjectName("tab_widget_main")
        self.tab_importer = QtWidgets.QWidget()
        self.tab_importer.setObjectName("tab_importer")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_importer)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox = QtWidgets.QGroupBox(self.tab_importer)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table_files = QtWidgets.QTableWidget(self.groupBox)
        self.table_files.setObjectName("table_files")
        self.table_files.setColumnCount(0)
        self.table_files.setRowCount(0)
        self.horizontalLayout.addWidget(self.table_files)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.btn_import = QtWidgets.QPushButton(self.groupBox)
        self.btn_import.setObjectName("btn_import")
        self.verticalLayout_2.addWidget(self.btn_import)
        self.btn_clear = QtWidgets.QPushButton(self.groupBox)
        self.btn_clear.setObjectName("btn_clear")
        self.verticalLayout_2.addWidget(self.btn_clear)
        self.btn_batch_shift = QtWidgets.QPushButton(self.groupBox)
        self.btn_batch_shift.setObjectName("btn_batch_shift")
        self.verticalLayout_2.addWidget(self.btn_batch_shift)
        self.btn_batch_normalise = QtWidgets.QPushButton(self.groupBox)
        self.btn_batch_normalise.setObjectName("btn_batch_normalise")
        self.verticalLayout_2.addWidget(self.btn_batch_normalise)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_importer)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.table_nf = QtWidgets.QTableWidget(self.groupBox_2)
        self.table_nf.setObjectName("table_nf")
        self.table_nf.setColumnCount(0)
        self.table_nf.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.table_nf)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.btn_inf = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_inf.setObjectName("btn_inf")
        self.verticalLayout_5.addWidget(self.btn_inf)
        self.btn_inc = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_inc.setObjectName("btn_inc")
        self.verticalLayout_5.addWidget(self.btn_inc)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.gridLayout_6.addLayout(self.verticalLayout_6, 1, 0, 1, 1)
        self.tab_widget_main.addTab(self.tab_importer, "")
        self.tab_normalise = QtWidgets.QWidget()
        self.tab_normalise.setObjectName("tab_normalise")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_normalise)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_raw = QtWidgets.QLabel(self.tab_normalise)
        self.label_raw.setObjectName("label_raw")
        self.horizontalLayout_2.addWidget(self.label_raw)
        self.combo_raw = QtWidgets.QComboBox(self.tab_normalise)
        self.combo_raw.setObjectName("combo_raw")
        self.horizontalLayout_2.addWidget(self.combo_raw)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.table_results = QtWidgets.QTableWidget(self.tab_normalise)
        self.table_results.setObjectName("table_results")
        self.table_results.setColumnCount(0)
        self.table_results.setRowCount(0)
        self.horizontalLayout_5.addWidget(self.table_results)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.edit_p_e = QtWidgets.QLineEdit(self.tab_normalise)
        self.edit_p_e.setObjectName("edit_p_e")
        self.gridLayout_3.addWidget(self.edit_p_e, 3, 1, 1, 1)
        self.edit_p_g = QtWidgets.QLineEdit(self.tab_normalise)
        self.edit_p_g.setObjectName("edit_p_g")
        self.gridLayout_3.addWidget(self.edit_p_g, 4, 1, 1, 1)
        self.label_p_name = QtWidgets.QLabel(self.tab_normalise)
        self.label_p_name.setObjectName("label_p_name")
        self.gridLayout_3.addWidget(self.label_p_name, 0, 0, 1, 1)
        self.edit_p_time = QtWidgets.QLineEdit(self.tab_normalise)
        self.edit_p_time.setObjectName("edit_p_time")
        self.gridLayout_3.addWidget(self.edit_p_time, 1, 1, 1, 1)
        self.btn_p_plot = QtWidgets.QPushButton(self.tab_normalise)
        self.btn_p_plot.setObjectName("btn_p_plot")
        self.gridLayout_3.addWidget(self.btn_p_plot, 8, 0, 1, 2)
        self.label_p_temp = QtWidgets.QLabel(self.tab_normalise)
        self.label_p_temp.setObjectName("label_p_temp")
        self.gridLayout_3.addWidget(self.label_p_temp, 6, 0, 1, 1)
        self.edit_p_p = QtWidgets.QLineEdit(self.tab_normalise)
        self.edit_p_p.setObjectName("edit_p_p")
        self.gridLayout_3.addWidget(self.edit_p_p, 2, 1, 1, 1)
        self.label_p_time = QtWidgets.QLabel(self.tab_normalise)
        self.label_p_time.setObjectName("label_p_time")
        self.gridLayout_3.addWidget(self.label_p_time, 1, 0, 1, 1)
        self.label_p_p = QtWidgets.QLabel(self.tab_normalise)
        self.label_p_p.setObjectName("label_p_p")
        self.gridLayout_3.addWidget(self.label_p_p, 2, 0, 1, 1)
        self.edit_p_name = QtWidgets.QLineEdit(self.tab_normalise)
        self.edit_p_name.setObjectName("edit_p_name")
        self.gridLayout_3.addWidget(self.edit_p_name, 0, 1, 1, 1)
        self.label_p__e = QtWidgets.QLabel(self.tab_normalise)
        self.label_p__e.setObjectName("label_p__e")
        self.gridLayout_3.addWidget(self.label_p__e, 3, 0, 1, 1)
        self.label_p_g = QtWidgets.QLabel(self.tab_normalise)
        self.label_p_g.setObjectName("label_p_g")
        self.gridLayout_3.addWidget(self.label_p_g, 4, 0, 1, 1)
        self.label_p_c = QtWidgets.QLabel(self.tab_normalise)
        self.label_p_c.setObjectName("label_p_c")
        self.gridLayout_3.addWidget(self.label_p_c, 5, 0, 1, 1)
        self.edit_p_c = QtWidgets.QLineEdit(self.tab_normalise)
        self.edit_p_c.setObjectName("edit_p_c")
        self.gridLayout_3.addWidget(self.edit_p_c, 5, 1, 1, 1)
        self.edit_p_temp = QtWidgets.QLineEdit(self.tab_normalise)
        self.edit_p_temp.setObjectName("edit_p_temp")
        self.gridLayout_3.addWidget(self.edit_p_temp, 6, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.setStretch(0, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.gridLayout_7.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.tab_widget_main.addTab(self.tab_normalise, "")
        self.tab_plot = QtWidgets.QWidget()
        self.tab_plot.setObjectName("tab_plot")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_plot)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_result = QtWidgets.QLabel(self.tab_plot)
        self.label_result.setObjectName("label_result")
        self.horizontalLayout_3.addWidget(self.label_result)
        self.combo_result = QtWidgets.QComboBox(self.tab_plot)
        self.combo_result.setObjectName("combo_result")
        self.horizontalLayout_3.addWidget(self.combo_result)
        self.combo_typo = QtWidgets.QComboBox(self.tab_plot)
        self.combo_typo.setObjectName("combo_typo")
        self.horizontalLayout_3.addWidget(self.combo_typo)
        self.btn_plot = QtWidgets.QPushButton(self.tab_plot)
        self.btn_plot.setObjectName("btn_plot")
        self.horizontalLayout_3.addWidget(self.btn_plot)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.graphics_view = CanvasWidget(self.tab_plot)
        self.graphics_view.setObjectName("graphics_view")
        self.verticalLayout_4.addWidget(self.graphics_view)
        self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.tab_widget_main.addTab(self.tab_plot, "")
        self.verticalLayout.addWidget(self.tab_widget_main)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(20, -1, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_labbook = QtWidgets.QPushButton(Form)
        self.btn_labbook.setObjectName("btn_labbook")
        self.horizontalLayout_6.addWidget(self.btn_labbook)
        self.label_labbook = QtWidgets.QLabel(Form)
        self.label_labbook.setObjectName("label_labbook")
        self.horizontalLayout_6.addWidget(self.label_labbook)
        self.horizontalLayout_6.setStretch(1, 1)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)

        self.retranslateUi(Form)
        self.tab_widget_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_header.setText(_translate("Form", "cRaman System"))
        self.groupBox.setTitle(_translate("Form", "Raw"))
        self.btn_import.setText(_translate("Form", "Import Raw"))
        self.btn_clear.setText(_translate("Form", "Clear Raw"))
        self.btn_batch_shift.setText(_translate("Form", "Batch Set Shift"))
        self.btn_batch_normalise.setText(_translate("Form", "Batch Normalise"))
        self.groupBox_2.setTitle(_translate("Form", "Normalised"))
        self.btn_inf.setText(_translate("Form", "Import Normalised"))
        self.btn_inc.setText(_translate("Form", "Clear Normalised"))
        self.tab_widget_main.setTabText(self.tab_widget_main.indexOf(self.tab_importer), _translate("Form", "Import Data"))
        self.label_raw.setText(_translate("Form", "Choose Data"))
        self.label_p_name.setText(_translate("Form", "Name"))
        self.btn_p_plot.setText(_translate("Form", "Plot"))
        self.label_p_temp.setText(_translate("Form", "Temp"))
        self.label_p_time.setText(_translate("Form", "Time"))
        self.label_p_p.setText(_translate("Form", "P:"))
        self.label_p__e.setText(_translate("Form", "E:"))
        self.label_p_g.setText(_translate("Form", "G:"))
        self.label_p_c.setText(_translate("Form", "C:"))
        self.tab_widget_main.setTabText(self.tab_widget_main.indexOf(self.tab_normalise), _translate("Form", "Normalised Data"))
        self.label_result.setText(_translate("Form", "Choose Data"))
        self.btn_plot.setText(_translate("Form", "Plot"))
        self.tab_widget_main.setTabText(self.tab_widget_main.indexOf(self.tab_plot), _translate("Form", "Plot Data"))
        self.btn_labbook.setText(_translate("Form", "Import Labbook"))
        self.label_labbook.setText(_translate("Form", "Labbook: ---"))
from plot_tool import CanvasWidget
