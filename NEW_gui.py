# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from ui_design.main import Ui_Form
from functools import partial
import os

app_name = 'cRaman System'


class MainApp(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)  # Initialize Ui

        self.setWindowTitle(app_name)  # window title
        self.label_header.setText(app_name)

        self.data_files = []
        # Create a new variable storage file path and data
        self.data_current_raw_file: str = None
        self.data_param: int = None
        self.data_normalised_file: str = None

        self.init_table_raw_files()
        self.init_table_results()

        # A click event that binds the import
        self.btn_import.clicked.connect(self.handle_select_and_import_files)
        self.btn_clear.clicked.connect(self.handle_clear_raw_files)
        self.tab_widget_main.currentChanged.connect(self.handle_switch_between_tabs)

        # Bind the function to edit the cell of the file list
        self.edit_param.textChanged.connect(self.handle_user_edit_param)
        self.edit_param.setValidator(QtGui.QIntValidator())

        self.combo_raw.currentIndexChanged.connect(self.handle_user_choose_raw_file)
        self.combo_result.currentIndexChanged.connect(self.handle_user_choose_normalised_file)
        self.btn_normalise.clicked.connect(self.handle_normalise_raw_file)
        self.btn_plot.clicked.connect(self.handle_handle_plot)
        self.setMinimumSize(1024, 600)

    def init_table_raw_files(self):
        """Initialize file list table"""
        table_headers = ['FileName', 'FilePath']
        self.table_files.clear()  # clear the list
        self.table_files.setRowCount(0)  # Initial 0 lines
        self.table_files.setColumnCount(len(table_headers))  # Three columns show file status
        #  Set the text displayed in the horizontal header in order
        self.table_files.setHorizontalHeaderLabels(table_headers)

    def init_table_results(self, col: int = None):
        """Initialization result table"""
        self.table_results.clear()  # clear the list
        self.table_results.setRowCount(0)  # Initial 0 lines

        if col == 2:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wave', 'Spectra'])
        elif col == 3:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wave', 'Spectra 1', 'Spectra 2'])
        elif col == 4:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wave', 'Spectra 1', 'Spectra 2', 'Spectra 3'])
        else:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['X', 'N'])

    def handle_select_and_import_files(self):
        """Process user selection and import txt files"""
        # Open file and get file list(ls)
        ls, _ext = QtWidgets.QFileDialog.getOpenFileNames(
            parent=self, caption='Import Raw Data Files', directory='.', filter='Txt Data Files(*.txt)'
            )
        #  Open the txt file in the current path
        #  Determine whether to choose
        if not ls:
            return
        ls.sort()  # Sort file list
        #  Block external signals
        self.table_files.blockSignals(True)
        #  List of files
        for c, fp in enumerate(ls):
            #  Get the current number of rows
            r = self.table_files.rowCount()
            #  Insert the row in the table
            self.table_files.insertRow(r)
            #  Insert list by line number [path, Param, results]
            self.data_files.insert(r,
                                   [os.path.abspath(fp), None, None, None])
            #                 raw file path || shift || normalised content || output file path

            item = QtWidgets.QTableWidgetItem()
            item.setText(os.path.split(fp)[1])  # slice the path to get the file name and set
            item.setStatusTip(fp)  # mouse over to display the file path
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEnabled)  # is enabled
            self.table_files.setItem(r, 0, item)
            #  Set the item in the specified row and first column as a QTableWidgetItem instance object
            item = QtWidgets.QTableWidgetItem()  # center aligned offsets
            item.setText(fp)
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            item.setStatusTip(fp)
            #  can only edit, nothing else
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            #  Set the second column
            self.table_files.setItem(r, 1, item)
        # Turn off signal blocking
        self.table_files.blockSignals(False)

    def fill_table_results(self, data: list):
        if len(data[0]) != self.table_results.columnCount():
            return
        for row in data:
            r = self.table_results.rowCount()
            self.table_results.insertRow(r)
            for c, v in enumerate(row):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(v))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table_results.setItem(r, c, item)

    @classmethod
    def show_warning_message(cls, message: str, title: str = 'Warning', detail: str = None, extra: str = None,
                             parent=None, only_yes: bool = False):
        '''Display warning message'''
        msg_box = QtWidgets.QMessageBox(parent=parent)
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        if isinstance(extra, str) and detail:
            msg_box.setInformativeText(extra)
        if isinstance(detail, str) and detail:
            msg_box.setDetailedText(detail)
        if only_yes is True:
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Yes')
        else:
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Yes')
            btn_no = msg_box.button(QtWidgets.QMessageBox.No)
            btn_no.setText('No')

        msg_box.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msg_box.setEscapeButton(QtWidgets.QMessageBox.No)
        msg_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # QtCore.Qt.NoTextInteraction
        r = msg_box.exec_()
        if r == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    @classmethod
    def show_info_message(cls, message: str, title='Information', detail: str = None, extra: str = None, parent=None,
                          only_yes: bool = False):
        '''Display reminder information'''
        msg_box = QtWidgets.QMessageBox(parent=parent)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        if isinstance(extra, str) and detail:
            msg_box.setInformativeText(extra)
        if isinstance(detail, str) and detail:
            msg_box.setDetailedText(detail)
        if only_yes is True:
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Yes')
        else:
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Yes')
            btn_no = msg_box.button(QtWidgets.QMessageBox.No)
            btn_no.setText('No')

        msg_box.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msg_box.setEscapeButton(QtWidgets.QMessageBox.No)
        msg_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # QtCore.Qt.NoTextInteraction
        r = msg_box.exec_()
        if r == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def handle_clear_raw_files(self):
        """"""
        self.init_table_raw_files()
        self.data_files = []

    def handle_switch_between_tabs(self, index: int):
        """Switch between different TABs"""
        print('foo')
        if index == 1:
            self.handle_switch_to_tab_normalise()

        elif index == 2:
            self.handle_switch_to_tab_plot()

    def handle_switch_to_tab_plot(self):
        """Handle Events when switched to tab Plot"""
        normalised_files = [out for fp, shift, data, out in self.data_files if out]

        self.combo_result.blockSignals(True)
        self.combo_result.clear()
        self.graphics_view.plot_clear()
        if not normalised_files:
            self.data_normalised_file = None
        else:
            self.combo_result.addItems(normalised_files)
            self.data_normalised_file = normalised_files[0]

        self.combo_result.blockSignals(False)

    def handle_switch_to_tab_normalise(self):
        """Handle Events when switched to tab Normalise"""
        files = [fp for fp, shift, data, out in self.data_files]
        self.combo_raw.blockSignals(True)

        if not files:
            self.combo_raw.clear()
            self.data_current_raw_file = None
            self.init_table_results()

        else:
            if self.data_current_raw_file in files:
                index = files.index(self.data_current_raw_file)
                raw_file, shift, data, output_file = self.data_files[index]

                self.combo_raw.clear()
                self.combo_raw.addItems(files)
                self.combo_raw.setCurrentIndex(index)

                if isinstance(data, list) and data:
                    self.init_table_results(col=len(data[0]))
                    self.fill_table_results(data=data)

                else:
                    self.init_table_results()

            else:
                self.data_current_raw_file = files[0]
                self.combo_raw.clear()
                self.combo_raw.addItems(files)
                self.init_table_results()

        self.combo_raw.blockSignals(False)

    def handle_user_choose_raw_file(self, index: int):
        """The drop - down box selects a file"""
        if index < 0:
            return
        self.data_current_raw_file = self.combo_raw.currentText()

        fp, shift, data, out = self.data_files[index]

        if isinstance(shift, int):
            self.edit_param.setText(str(shift))

        print(self.data_current_raw_file, data)
        if data:
            self.init_table_results(col=len(data[0]))
            self.fill_table_results(data=data)
        else:
            self.init_table_results()

    def handle_user_choose_normalised_file(self, index):
        """The drop - down box selects a file"""
        if index < 0:
            return
        self.data_normalised_file = self.combo_result.currentText()

        self.graphics_view.plot_clear()

    def handle_user_edit_param(self, value):
        """User Edit the offset used to shift wavelength"""
        try:
            v = int(float(value))
        except ValueError:
            v = None

        self.data_param = v
        print('the offset used to shift wavelength is', v)

    def handle_normalise_raw_file(self):
        """Handle Normalise a raw file and update ui"""
        ls = []
        if not self.data_current_raw_file:
            ls.append('Please choose a raw data file')
        if not isinstance(self.data_param, int):
            ls.append('Pleas input the offset used to shift wavelength in "Wave Shift"')
        if ls:
            return self.show_warning_message(message=f'Unable to normalise: <br><ul><li>{"</li><li>".join(ls)}</li></ul>')

        the_raw_file = self.data_current_raw_file
        the_raw_file_index = [fp for fp, *_ in self.data_files].index(the_raw_file)
        shift = self.data_param

        from data_process import process, export_data

        # example
        # in file: D:\some-path\001.txt
        # output file or normalised file: D:\some-path\normalised\001.txt

        results = process(fp=the_raw_file, shiftInput=shift)

        fd, fn = os.path.split(the_raw_file)
        out_dir = os.path.join(fd, 'normalised')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.abspath(os.path.join(out_dir, fn))
        export_data(data=results, output_path=out_file)

        self.data_files[the_raw_file_index][1] = self.data_param
        self.data_files[the_raw_file_index][2] = results
        self.data_files[the_raw_file_index][3] = out_file

        if results:
            self.init_table_results(col=len(results[0]))
            self.fill_table_results(data=results)
        else:
            self.init_table_results()

    def handle_handle_plot(self):
        """The processing user clicks plot"""

        normalised_results = [data for fp, shift, data, out in self.data_files if out]
        normalised_files = [out for fp, shift, data, out in self.data_files if out]

        if self.data_normalised_file in normalised_files:
            index = normalised_files.index(self.data_normalised_file)
            data = normalised_results[index]

            self.graphics_view.plot_data(data=data,
                                         title=f'Plot of Normalised {os.path.split(self.data_normalised_file)[1]}')
        else:
            self.graphics_view.plot_clear()
            return self.show_warning_message(message='Please choose a normalised file')





if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    m = MainApp()
    m.show()
    sys.exit(app.exec_())