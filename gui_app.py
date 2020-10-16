# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from ui_design.main import Ui_Form
from ui_design.waiter import Ui_Form as WaiterDialogForm
from functools import partial
import os
from data_process import read_normalised_data, parse_lab_book, process, export_data

app_name = 'cRaman System'
wave_shift_min = 0
wave_shift_max = 100000
wave_shift_decimals = 3  # 3.12345 (decimals = 5)
wave_shift_default = 3.0


class WaiterDialog(QtWidgets.QDialog, WaiterDialogForm):
    def __init__(self, parent):
        super().__init__(parent=parent, flags=QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)

    def clear_shell(self):
        """clear shell messages"""
        self.textBrowser.clear()

    def update_shell(self, msg: str):
        """Update running shell"""
        self.textBrowser.append(msg)

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:  # Esc key is bypassed
            super(self.__class__, self).keyPressEvent(event)


class ProcessService(QtCore.QThread):
    sig_result = QtCore.pyqtSignal(str, list)
    sig_msg = QtCore.pyqtSignal(str)
    sig_finished = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.tasks = []

    def reload(self, tasks):
        self.tasks = tasks

    def run(self) -> None:
        num = len(self.tasks)
        for n, (fp, sh) in enumerate(self.tasks):
            try:
                self.sig_msg.emit(f'<p><span style="color: blue;">[{n+1}/{num}]</span>, Normalising <b>{fp}</b></p>')
                r = process(fp=fp, shiftInput=sh)
                self.sig_result.emit(fp, r)
                self.sig_msg.emit(f'<p><span style="color: blue;">[{n + 1}/{num}]</span>, <span style="color: green;">[SUCCEEDED]</span> to normalise {fp}</p>')
            except:
                self.sig_msg.emit(f'<p><span style="color: blue;">[{n + 1}/{num}]</span>, <span style="color: red;">[FAILED]</span> to normalise {fp}</p>')
        self.sig_finished.emit()


class MainApp(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)  # Initialize Ui

        self.setWindowTitle(app_name)  # window title
        self.label_header.setText(app_name)

        self.data_files_normalised = []  # store a list of normalised files
        self.data_files_raw = []  # store a list of raw files
        self.data_lab_book = {}  # data label book

        # Create a new variable storage file path and data
        self.data_current_normalised_file: str = None
        self.data_param: int = None

        self.data_batch_shift: (int, float) = wave_shift_default

        self.init_table_raw_files()
        self.init_table_results()
        self.init_table_nf()

        # A click event that binds the import
        self.btn_import.clicked.connect(self.handle_select_and_import_raw_files)
        self.btn_clear.clicked.connect(self.handle_clear_raw_files)
        self.tab_widget_main.currentChanged.connect(self.handle_switch_between_tabs)

        self.combo_raw.currentIndexChanged.connect(self.handle_user_choose_view_normalised_file)
        self.combo_result.currentIndexChanged.connect(self.handle_user_choose_normalised_file)
        self.btn_plot.clicked.connect(self.handle_handle_plot)
        self.setMinimumSize(1024, 600)

        self.combo_typo.clear()
        self.combo_typo.addItems(['Scatter', 'Line'])
        self.btn_inf.clicked.connect(self.handle_user_add_normalised)

        self.tab_widget_main.setStyleSheet('''
            QTabBar::tab:selected {font: 75 14pt "Courier New";color: black;}
            QTabBar::tab{
             width: 300px;
             height: 30px;
             color: white;
             margin-left: 10px;
             margin-right: 10px;
             font: 12pt "Courier New";
            }
            QTabBar::tab:first {
                background-color: gray; 
            }
            QTabBar::tab:middle {
                background-color: gray; 
            }
            QTabBar::tab:last {
                background-color: gray; 
            }
            
            QTabBar::tab:first:selected {
                background-color: white;
            }
            QTabBar::tab:middle:selected {
                background-color: white;

            }
            QTabBar::tab:last:selected {
                background-color: white;

            }
            
        ''')

        self.btn_import.setStyleSheet(
            '''
            QPushButton{
            background-color: #F8D800;
            min-width: 120px;
            min-height: 40px;
            border-radius: 10px;
            }
            '''
        )
        self.btn_clear.setStyleSheet('background-color: #E80505;'
                                     'color: white;'
                                     'min-width: 120px;'
                                     'min-height: 40px;'
                                     'border-radius: 10px;')

        self.btn_inc.setStyleSheet('background-color: #E80505;'
                                   'color: white;'
                                   'min-width: 100px;'
                                   'min-height: 40px;'
                                   'border-radius: 10px;')

        self.btn_labbook.setStyleSheet('''
            QPushButton{
            background-color: blue;
            min-width: 120px;
            min-height: 40px;
            border-radius: 10px;
            color: white;
            }
            ''')

        self.btn_inf.setStyleSheet('''
                    QPushButton{
                    background-color: #F8D800;
                    min-width: 120px;
                    min-height: 40px;
                    border-radius: 10px;
                    }
                    ''')

        self.btn_plot.setStyleSheet('''
                    QPushButton{
                    background-color: #BB4E75;
                    min-width: 120px;
                    min-height: 20px;
                    border-radius: 10px;
                    }
                    ''')
        self.combo_typo.setStyleSheet('''
                    background-color: #BB4E75;
                    min-width: 100px;
                    min-height: 20px;
                    border-radius: 10px;
        ''')
        self.btn_p_plot.setStyleSheet('''
                    QPushButton{
                    background-color: #BB4E75;
                    min-width: 120px;
                    min-height: 20px;
                    border-radius: 10px;
                    }
                    ''')
        self.btn_batch_shift.setStyleSheet('''
            QPushButton{
            background-color: #B210FF;
            min-width: 120px;
            min-height: 40px;
            border-radius: 10px;
            color: white;
            }
        ''')
        self.btn_batch_normalise.setStyleSheet('''
                    QPushButton{
                    background-color: #28C76F;
                    min-width: 120px;
                    min-height: 40px;
                    border-radius: 10px;
                    color: white;
                    }
                ''')

        self.btn_inc.clicked.connect(self.init_table_nf)
        self.btn_labbook.clicked.connect(self.handle_import_lab_book)
        self.btn_p_plot.clicked.connect(self.handle_plot_btn_click_in_normalised_tab)
        self.btn_batch_shift.clicked.connect(self.handle_batch_set_shift)
        self.btn_batch_normalise.clicked.connect(partial(self.gather_tasks_and_process, None))

        self.popup = WaiterDialog(self)
        self.batch_service = ProcessService(self)
        self.batch_service.sig_result.connect(self.handle_receive_result)
        self.batch_service.sig_msg.connect(self.popup.update_shell)
        self.batch_service.sig_finished.connect(self.handle_task_finished)

    def init_table_nf(self):
        """Initialize normalised file list table"""
        table_headers = ['File Name', 'Normalised File Path', 'View Data', 'Plot Data']
        self.table_nf.clear()  # clear the list
        self.table_nf.setRowCount(0)  # Initial 0 lines
        self.table_nf.setColumnCount(len(table_headers))  # Three columns show file status
        #  Set the text displayed in the horizontal header in order
        self.table_nf.setHorizontalHeaderLabels(table_headers)
        self.table_nf.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.data_files_to_plot = []  # clear normalised files those imported by user manually

    def init_table_raw_files(self):
        """Initialize raw file list table"""
        table_headers = ['File Name', 'File Path', 'Wave Shift', 'Operation']
        self.table_files.clear()  # clear the list
        self.table_files.setRowCount(0)  # Initial 0 lines
        self.table_files.setColumnCount(len(table_headers))  # Three columns show file status
        #  Set the text displayed in the horizontal header in order
        self.table_files.setHorizontalHeaderLabels(table_headers)
        self.table_files.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def init_table_results(self, col: int = None):
        """Initialization result table"""
        self.table_results.clear()  # clear the list
        self.table_results.setRowCount(0)  # Initial 0 lines

        if col == 2:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra'])
        elif col == 3:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra 1', 'Spectra 2'])
        elif col == 4:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra 1', 'Spectra 2', 'Spectra 3'])
        else:
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra'])

    def handle_select_and_import_raw_files(self):
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
            self.data_files_raw.insert(r,
                                   os.path.abspath(fp))
            #                 raw file path

            item = QtWidgets.QTableWidgetItem()
            item.setText(os.path.split(fp)[1])  # slice the path to get the file name and set
            item.setStatusTip(fp)  # mouse over to display the file path
            item.setFlags(QtCore.Qt.ItemIsEnabled)  # is enabled
            self.table_files.setItem(r, 0, item)
            #  Set the item in the specified row and first column as a QTableWidgetItem instance object
            item = QtWidgets.QTableWidgetItem()  # center aligned offsets
            item.setText(fp)
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            item.setStatusTip(fp)
            #  can only edit, nothing else
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            #  Set the second column
            self.table_files.setItem(r, 1, item)

            spin = QtWidgets.QDoubleSpinBox()
            spin.setDecimals(wave_shift_decimals)
            spin.setValue(wave_shift_default)
            spin.setMaximum(wave_shift_max)
            spin.setMinimum(wave_shift_min)
            self.table_files.setCellWidget(r, 2, spin)

            btn = QtWidgets.QPushButton()
            btn.setText('Normalise')
            self.table_files.setCellWidget(r, 3, btn)
            btn.clicked.connect(partial(self.gather_tasks_and_process, r))

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
                             parent=None, only_yes: bool = True):
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
            btn_yes.setText('Ok')
        else:
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Ok')
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
                          only_yes: bool = True):
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
            btn_yes.setText('Ok')
        else:
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Ok')
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
        self.data_files_raw = []

    def handle_switch_between_tabs(self, index: int):
        """Switch between different TABs"""
        print(index)
        if index == 1:
            self.handle_switch_to_tab_normalise()

        elif index == 2:
            self.handle_switch_to_tab_plot()

    def get_files_to_plot(self):
        """Gather normalised files for plot"""
        normalised_files = []

        if self.data_files_to_plot:
            normalised_files.extend(self.data_files_to_plot)
        # normalised_files = list(set(normalised_files))
        # normalised_files.sort()
        return normalised_files

    def add_one_row_to_table_nf(self, fp):
        """add one file to table normalised file"""
        r = self.table_nf.rowCount()
        self.table_nf.insertRow(r)

        self.data_files_to_plot.append(fp)

        item = QtWidgets.QTableWidgetItem(os.path.split(fp)[1])
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table_nf.setItem(r, 0, item)

        item = QtWidgets.QTableWidgetItem(fp)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table_nf.setItem(r, 1, item)

        btn_view = QtWidgets.QPushButton('View Data')
        self.table_nf.setCellWidget(r, 2, btn_view)
        btn_view.clicked.connect(partial(self.switch_and_view_data, r))

        btn_plot = QtWidgets.QPushButton('Plot Data')
        self.table_nf.setCellWidget(r, 3, btn_plot)
        btn_plot.clicked.connect(partial(self.switch_and_plot_data, r))

    def handle_switch_to_tab_plot(self):
        """Handle Events when switched to tab Plot"""
        normalised_files = self.get_files_to_plot()

        self.combo_result.blockSignals(True)
        self.combo_result.clear()
        self.graphics_view.plot_clear()
        if not normalised_files:
            self.data_current_normalised_file = None
        else:
            self.combo_result.addItems(normalised_files)
        self.combo_result.blockSignals(False)

        if self.data_current_normalised_file in normalised_files:
            self.combo_result.setCurrentIndex(normalised_files.index(self.data_current_normalised_file))

    def handle_switch_to_tab_normalise(self):
        """Handle Events when switched to tab Normalise"""
        files = self.get_files_to_plot()

        self.combo_raw.blockSignals(True)

        if not files:
            self.combo_raw.clear()
            self.data_current_normalised_file = None
            self.init_table_results()

        else:
            if self.data_current_normalised_file in files:
                index = files.index(self.data_current_normalised_file)

                self.combo_raw.clear()
                self.combo_raw.addItems(files)
                self.combo_raw.setCurrentIndex(index)

            else:
                index = 0
                self.data_current_normalised_file = files[0]
                self.combo_raw.clear()
                self.combo_raw.addItems(files)
                self.init_table_results()

            self.handle_user_choose_view_normalised_file(index)

        self.combo_raw.blockSignals(False)

    def handle_user_choose_view_normalised_file(self, index: int):
        """The drop - down box selects a file"""
        if index < 0:
            self.data_current_normalised_file = None
            self.init_table_results()
        else:
            self.data_current_normalised_file = self.combo_raw.currentText()

            data = read_normalised_data(fp=self.data_current_normalised_file)

            if data:
                self.init_table_results(col=len(data[0]))
                self.fill_table_results(data=data)
            else:
                self.init_table_results()
        self.handle_update_display_of_lab_book()

    def handle_update_display_of_lab_book(self):
        """Display Lab book in Tab Normalised"""
        data = {}
        if not self.data_current_normalised_file:
            pass
        else:
            _, fn = os.path.split(self.data_current_normalised_file)
            name, _ = os.path.splitext(fn)
            if name.endswith('_normalised'):
                name = name[:-11]
                print(name)
            data = self.data_lab_book.get(name, {})
        if not data:
            self.edit_p_name.setText('')
            self.edit_p_time.setText('')
            self.edit_p_p.setText('')
            self.edit_p_e.setText('')
            self.edit_p_g.setText('')
            self.edit_p_c.setText('')
            self.edit_p_temp.setText('')
        else:
            self.edit_p_name.setText(data['name'])
            self.edit_p_time.setText(data['time'])
            self.edit_p_p.setText(data['p'])
            self.edit_p_e.setText(data['e'])
            self.edit_p_g.setText(data['g'])
            self.edit_p_c.setText(data['c'])
            self.edit_p_temp.setText(data['temp'])

        # print(data)

    def handle_user_choose_normalised_file(self, index):
        """The drop - down box selects a file"""
        if index < 0:
            return
        self.data_current_normalised_file = self.combo_result.currentText()

        self.graphics_view.plot_clear()

    def handle_batch_set_shift(self):
        """Batch set shift wavelength"""
        intNum, ok = QtWidgets.QInputDialog.getDouble(self, "Setup waveShift for all", "WaveShift:", self.data_batch_shift, wave_shift_min, wave_shift_max, wave_shift_decimals)
        if ok:
            self.data_batch_shift = intNum
            for r in range(self.table_files.rowCount()):
                spin = self.table_files.cellWidget(r, 2)
                spin.setValue(intNum)

    # def handle_normalise_raw_file(self, r: int):
    #     """Handle Normalise a raw file and update ui"""
    #     print(self.data_files_raw)
    #     the_raw_file = self.data_files_raw[r]
    #     the_raw_file_index = r
    #     shift = int(self.table_files.item(r, 2).text())
    #
    #     # example
    #     # in file: D:\some-path\001.txt
    #     # output file or normalised file: D:\some-path\normalised\001_normalised.txt
    #
    #     results = process(fp=the_raw_file, shiftInput=shift)
    #
    #     fd, fn = os.path.split(the_raw_file)
    #     out_dir = os.path.join(fd, 'normalised')
    #     a, b = os.path.splitext(fn)
    #     fn = f'{a}_normalised{b}'
    #     if not os.path.exists(out_dir):
    #         os.makedirs(out_dir, exist_ok=True)
    #     out_file = os.path.abspath(os.path.join(out_dir, fn))
    #     export_data(data=results, output_path=out_file)
    #
    #     if out_file not in self.data_files_to_plot:
    #         self.add_one_row_to_table_nf(fp=out_file)

    def handle_handle_plot(self):
        """The processing user clicks plot"""

        ct = self.combo_typo.currentText()
        cf = self.combo_result.currentText()
        print(
            f'Type: {ct}; File: {cf}'
        )
        if cf:
            data = read_normalised_data(cf)
            self.graphics_view.plot_data(data=data,
                                         typo=ct.lower(),
                                         title=f'Plot of Normalised {os.path.split(cf)[1]}')
        else:
            self.graphics_view.plot_clear()
            return self.show_warning_message(message='Please choose a normalised file')

    def handle_user_add_normalised(self):
        """Process the data that the user imported already processed"""
        ls, _ext = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption='Import Normalised Data Files',
                                                          directory='.',
                                                          filter='Txt Data Files(*.txt)')
        if not ls:
            return
        new = 0
        old = 0
        invalid = 0
        normalised_files = self.get_files_to_plot()
        for i in ls:
            p = os.path.abspath(i)
            if p in normalised_files:  # please do not repeat
                old += 1
                continue

            fn = os.path.split(p)[1]
            if '_normalised.txt' not in fn.lower():  # a normalised file should be end with "_normalised.txt"
                invalid += 1
                continue

            self.add_one_row_to_table_nf(fp=p)
            new += 1
        self.show_info_message(message=f'<h1>Import Report</h1>Success {new}<br>Repeat {old}<br>Invalid {invalid}', parent=self, only_yes=True)

    def handle_import_lab_book(self):
        """Import Lab Book"""
        fp, _ext = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Import Lab Book',
                                                          directory='.', filter='Txt Data Files(*.txt)')
        if not fp:
            return
        try:
            self.data_lab_book = parse_lab_book(fp=fp)
            self.label_labbook.setText(f'Labbook: {os.path.split(fp)[1]}')
            return self.show_info_message(message='Lab Book Imported', parent=self, )
        except:
            return self.show_warning_message(message='Parsing Lab Book Failed', parent=self, )

    def switch_and_view_data(self, index):
        """Switch to Tab Normalised Data and apply exact chosen file"""
        self.data_current_normalised_file = self.data_files_to_plot[index]
        self.tab_widget_main.setCurrentIndex(1)

    def switch_and_plot_data(self, index):
        """Switch to Tab Plot Data and view apply chosen file"""
        self.data_current_normalised_file = self.data_files_to_plot[index]
        self.tab_widget_main.setCurrentIndex(2)
        self.handle_handle_plot()

    def handle_plot_btn_click_in_normalised_tab(self):
        """"""
        index = self.combo_raw.currentIndex()
        if index < 0:
            return
        self.switch_and_plot_data(index)
        self.handle_handle_plot()

    def handle_receive_result(self, fp: str, data: list):
        """"""
        the_raw_file = fp
        results = data
        fd, fn = os.path.split(the_raw_file)
        out_dir = os.path.join(fd, 'normalised')
        a, b = os.path.splitext(fn)
        fn = f'{a}_normalised{b}'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.abspath(os.path.join(out_dir, fn))
        export_data(data=results, output_path=out_file)

        if out_file not in self.data_files_to_plot:
            self.add_one_row_to_table_nf(fp=out_file)

    def gather_tasks_and_process(self, index: int = None):
        if self.batch_service.isRunning():
            return self.show_warning_message(message='A Job is Running, Please Try Again Later.', parent=self, title='A Job is Running')
        if isinstance(index, int):
            the_raw_file = self.data_files_raw[index]
            shift = self.table_files.cellWidget(index, 2).value()  # int(self.table_files.item(index, 2).text())
            tasks = [(the_raw_file, shift), ]
        else:
            tasks = []
            for r in range(self.table_files.rowCount()):
                the_raw_file = self.data_files_raw[r]
                shift = self.table_files.cellWidget(r, 2).value()  # int(self.table_files.item(index, 2).text())
                tasks.append((the_raw_file, shift))
        if not tasks:
            return self.show_warning_message(message='There are no jobs. Please import some raw files.', parent=self)
        print(tasks)
        self.batch_service.reload(tasks)
        self.batch_service.start()
        # self.show_info_message(message='Please Wait. Processing is running in the background.', parent=self)
        self.popup.clear_shell()
        self.popup.setFixedSize(self.size())
        self.popup.move(self.pos())
        self.popup.exec_()  # show a non-frame popup to block user from operating

    def handle_task_finished(self):
        """hide popup to allow user to operate"""
        self.popup.accept()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    m = MainApp()
    m.show()
    sys.exit(app.exec_())
