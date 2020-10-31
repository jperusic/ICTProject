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
wave_shift_decimals = 5  # 3.12345 (decimals = 5)
wave_shift_default = 0


class WaiterDialog(QtWidgets.QDialog, WaiterDialogForm):
    """
     a Dialog class
     to tell what's going on while normalising raw file(s).
     The user can not do anything but wait while processing is going on
     """
    def __init__(self, parent):  # a method about how to create an instance of the  "WaiterDialog" class
        super().__init__(parent=parent,
                         flags=QtCore.Qt.FramelessWindowHint)  # inherit of python's OOP(Object Oriented Programming)
        self.setupUi(self)  # apply ui designed by QT Designer --- a ".ui" file converted to a ".py" file

    def clear_shell(self):
        """clear shell messages"""
        self.textBrowser.clear()  # make sure the message box is empty when first shown, avoiding annoying the user.

    def update_shell(self, msg: str):
        """Update running shell"""
        self.textBrowser.append(msg)  # append a new message to the bottom of the message box

    def keyPressEvent(self, event):  # override the QT's key press event
        if not event.key() == QtCore.Qt.Key_Escape:  # Esc key is bypassed
            super(self.__class__, self).keyPressEvent(event)  # other events allowed


class ProcessService(QtCore.QThread):
    """
    a Thread inherited from Qt's QThread --- which allows executing extra jobs, while the ui loop is going on at the
    same time. Raw files can be handled without block the ui loop.
    """
    sig_result = QtCore.pyqtSignal(str, list)  # signal of the transmit results of processed files
    sig_msg = QtCore.pyqtSignal(str)  # signal to tell the ui what's going on in the background.
    sig_finished = QtCore.pyqtSignal()  # a signal to tell all jobs are done.

    def __init__(self, parent):  # a method about how to create an instance of the  "ProcessService" class
        super().__init__(parent)  # inherit parent features
        self.tasks = []  # container to hold tasks

    def reload(self, tasks):  # refresh the tasks
        self.tasks = tasks

    def run(self) -> None:  # actually run to process the tasks
        num = len(self.tasks)  # get num of tasks
        for n, (fp, sh) in enumerate(self.tasks):  # enumerate each task
            try:  # try-except helps to avoid crashing the app when something bad happens
                self.sig_msg.emit(f'<p><span style="color: blue;">[{n+1}/{num}]</span>, Normalising <b>{fp}</b></p>'
                                  )  # emit a message telling what's going on
                r = process(fp=fp, shiftInput=sh)  # call process function the normalise the raw file
                self.sig_result.emit(fp, r)  # emit the results
                self.sig_msg.emit(
                    f'<p><span style="color: blue;">[{n + 1}/{num}]</span>,'
                    f' <span style="color: green;">[SUCCEEDED]</span> to normalise {fp}</p>')  # emit a success message
            except:
                self.sig_msg.emit(f'<p><span style="color: blue;">[{n + 1}/{num}]</span>,'
                                  f' <span style="color: red;">[FAILED]</span> to normalise {fp}</p>')  # emit a failed message
        self.sig_finished.emit()  # emit a message "all tasks processed"


class MainApp(QtWidgets.QWidget, Ui_Form):
    """Main Ui widget"""
    def __init__(self, parent=None):  # a method about how to create an instance of the  "MainApp" class
        super().__init__(parent=parent)  # execute inheriting
        self.setupUi(self)  # Initialize Ui

        self.setWindowTitle(app_name)  # window title
        self.label_header.setText(app_name)  # set app name to the banner

        self.data_files_normalised = []  # store a list of normalised files
        self.data_files_raw = []  # store a list of raw files
        self.data_lab_book = {}  # data label book

        # Create a new variable storage file path and data
        self.data_current_normalised_file: str = None  # path of the current normalised file
        self.data_param: int = None  # data parameters

        self.data_batch_shift: (int, float) = wave_shift_default  # wave shift value for all

        self.init_table_raw_files()  # init raw file table on the "Import Data" tab
        self.init_table_results()  # init normalised file preview table on the "Normalised Data" tab
        self.init_table_nf()  # init normalised table on the "Import Data" tab

        # ################
        # Bind of click event to a function for each button/tab/combobox
        # The function will be executed when a click event(or value changed etc.) is triggered.
        self.btn_import.clicked.connect(self.handle_select_and_import_raw_files)  # import raw files
        self.btn_clear.clicked.connect(self.handle_clear_raw_files)  # clear raw files
        self.tab_widget_main.currentChanged.connect(self.handle_switch_between_tabs)  # bind tab switch event --
        # some code runs before a tab shown to user

        self.combo_raw.currentIndexChanged.connect(self.handle_user_choose_view_normalised_file)  # user change to another normalised file
        self.combo_result.currentIndexChanged.connect(self.handle_user_choose_normalised_file)  # user choose to plot a different normalised file
        self.btn_plot.clicked.connect(self.handle_handle_plot)  # do plot the figure
        self.setMinimumSize(1024, 600)  # set the minimum size of the main app window

        self.combo_typo.clear()  # clear plot style combobox's choices
        self.combo_typo.addItems(['Scatter', 'Line'])  # makes sure plot style choices limited to scatter and line.
        self.btn_inf.clicked.connect(self.handle_user_add_normalised)  # allow user importing normalised file(s)

        # Qt accept QSS to customise the look of the app. QSS supports most features of CSS.
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
        )  # setup the style of "Import Raw" button
        self.btn_clear.setStyleSheet('background-color: #E80505;'
                                     'color: white;'
                                     'min-width: 120px;'
                                     'min-height: 40px;'
                                     'border-radius: 10px;')   # setup the style of "Clear Raw" button

        self.btn_inc.setStyleSheet('background-color: #E80505;'
                                   'color: white;'
                                   'min-width: 100px;'
                                   'min-height: 40px;'
                                   'border-radius: 10px;')  # setup the style of "Clear Normalised" button

        self.btn_labbook.setStyleSheet('''
            QPushButton{
            background-color: blue;
            min-width: 120px;
            min-height: 40px;
            border-radius: 10px;
            color: white;
            }
            ''')  # setup the style of "Import Labbook" button

        self.btn_inf.setStyleSheet('''
                    QPushButton{
                    background-color: #F8D800;
                    min-width: 120px;
                    min-height: 40px;
                    border-radius: 10px;
                    }
                    ''')  # setup the style of "Import Normalised" button

        self.btn_plot.setStyleSheet('''
                    QPushButton{
                    background-color: #BB4E75;
                    min-width: 120px;
                    min-height: 20px;
                    border-radius: 10px;
                    }
                    ''')  # setup the style of "Plot" button in "Plot Data" tab
        self.combo_typo.setStyleSheet('''
                    background-color: #BB4E75;
                    min-width: 100px;
                    min-height: 20px;
                    border-radius: 10px;
        ''')  # setup the style of "plot style" combobox
        self.btn_p_plot.setStyleSheet('''
                    QPushButton{
                    background-color: #BB4E75;
                    min-width: 120px;
                    min-height: 20px;
                    border-radius: 10px;
                    }
                    ''')  # setup the style of "Plot" button in "Normalised Data" tab
        self.btn_batch_shift.setStyleSheet('''
            QPushButton{
            background-color: #B210FF;
            min-width: 120px;
            min-height: 40px;
            border-radius: 10px;
            color: white;
            }
        ''')  # setup the style of "Batch Set Shift" button in "Import Data" tab
        self.btn_batch_normalise.setStyleSheet('''
                    QPushButton{
                    background-color: #28C76F;
                    min-width: 120px;
                    min-height: 40px;
                    border-radius: 10px;
                    color: white;
                    }
                ''')   # setup the style of "Batch Normalise" button in "Import Data" tab

        self.btn_inc.clicked.connect(self.init_table_nf)  # btn "Clear Normalised" --> clear normalised files in "Import Data" tab
        self.btn_labbook.clicked.connect(self.handle_import_lab_book)  # btn "Import Labbook" --> 'Import Labbook'
        self.btn_p_plot.clicked.connect(self.handle_plot_btn_click_in_normalised_tab)  # btn "Plot" in "Normalised Data" tab click event
        self.btn_batch_shift.clicked.connect(self.handle_batch_set_shift)  # btn "Batch Set Shift" in "Import Data"
        # click event
        self.btn_batch_normalise.clicked.connect(partial(self.gather_tasks_and_process, None))  # btn "Batch Normalise" in "Import Data" tan click event

        self.popup = WaiterDialog(self)  # create a popup dialog
        self.batch_service = ProcessService(self)  # define a processing service --- a thread to normalise raw files
        self.batch_service.sig_result.connect(self.handle_receive_result)  # receive results
        self.batch_service.sig_msg.connect(self.popup.update_shell)  # receive messages
        self.batch_service.sig_finished.connect(self.handle_task_finished)  # receive finished message

    def init_table_nf(self):
        """Initialize normalised file list table"""
        table_headers = ['File Name', 'Normalised File Path', 'View Data', 'Plot Data']  # table headers
        self.table_nf.clear()  # clear the list
        self.table_nf.setRowCount(0)  # Initial 0 lines
        self.table_nf.setColumnCount(len(table_headers))  # Three columns show file status
        #  Set the text displayed in the horizontal header in order
        self.table_nf.setHorizontalHeaderLabels(table_headers)  # set table headers
        self.table_nf.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # second column in stretch mode

        self.data_files_to_plot = []  # clear normalised files those imported by user manually

    def init_table_raw_files(self):
        """Initialize raw file list table"""
        table_headers = ['File Name', 'File Path', 'Wave Shift', 'Operation']
        self.table_files.clear()  # clear the list
        self.table_files.setRowCount(0)  # Initial 0 lines
        self.table_files.setColumnCount(len(table_headers))  # Three columns show file status
        #  Set the text displayed in the horizontal header in order
        self.table_files.setHorizontalHeaderLabels(table_headers)  # setup table headers
        self.table_files.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # second column in stretch mode

    def init_table_results(self, col: int = None):
        """Initialization result table in Normalised Data tab """
        self.table_results.clear()  # clear the list
        self.table_results.setRowCount(0)  # Initial 0 lines

        if col == 2:  # display two columns data
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra'])  # setup headers
        elif col == 3:  # display three columns data
            self.table_results.setColumnCount(3)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra 1', 'Spectra 2'])  # setup headers
        elif col == 4:  # display four columns data
            self.table_results.setColumnCount(4)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra 1', 'Spectra 2', 'Spectra 3'])  # setup headers
        else:  # display while there are no data
            self.table_results.setColumnCount(2)
            self.table_results.setHorizontalHeaderLabels(['Wavelength', 'Spectra'])  # setup headers

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
            self.table_files.setItem(r, 1, item)  # place on the ui

            spin = QtWidgets.QDoubleSpinBox()  # create a spin-box to display wave-shift, and allows users to change the value
            spin.setDecimals(wave_shift_decimals)  # setup max decimals supported
            spin.setValue(wave_shift_default)  # set init value as default one
            spin.setMaximum(wave_shift_max)  # set max
            spin.setMinimum(wave_shift_min)  # set min
            self.table_files.setCellWidget(r, 2, spin)  # place on the ui

            btn = QtWidgets.QPushButton()  # the  button to normalise this file
            btn.setText('Normalise')
            self.table_files.setCellWidget(r, 3, btn)
            btn.clicked.connect(partial(self.gather_tasks_and_process, r))  # place on the ui

        # Turn off signal blocking
        self.table_files.blockSignals(False)

    def fill_table_results(self, data: list):
        """Display Normalised data"""
        if len(data[0]) != self.table_results.columnCount():  # do some check num of columns should be exactly same.
            return
        for row in data:  # put data into the table row by row
            r = self.table_results.rowCount()  # get how many rows
            self.table_results.insertRow(r)  # insert a row at the bottom
            for c, v in enumerate(row):  # put each value in the table
                item = QtWidgets.QTableWidgetItem()  # create item
                item.setText(str(v))  # set value
                item.setFlags(QtCore.Qt.ItemIsEnabled)  # make it read-only
                self.table_results.setItem(r, c, item)  # put in the table

    @classmethod
    def show_warning_message(cls, message: str, title: str = 'Warning', detail: str = None, extra: str = None,
                             parent=None, only_yes: bool = True):
        '''Display warning message'''
        msg_box = QtWidgets.QMessageBox(parent=parent)  # create message box
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)  # set waring icon
        msg_box.setText(message)  # set message
        msg_box.setWindowTitle(title)  # set title of the window
        if isinstance(extra, str) and detail:  # check if has extra information
            msg_box.setInformativeText(extra)  # setup extra information
        if isinstance(detail, str) and detail:  # check if has detail
            msg_box.setDetailedText(detail)  # setup detail
        if only_yes is True:  # only yes
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
        msg_box = QtWidgets.QMessageBox(parent=parent)  # create message box
        msg_box.setIcon(QtWidgets.QMessageBox.Information)  # set info icon
        msg_box.setText(message)  # set message
        msg_box.setWindowTitle(title)  # set title of the window
        if isinstance(extra, str) and detail:  # check if has extra information
            msg_box.setInformativeText(extra)  # setup extra information
        if isinstance(detail, str) and detail:  # check if has detail
            msg_box.setDetailedText(detail)  # setup detail
        if only_yes is True:  # only display ok btn
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Ok')
        else:  # display both ok and No btn
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
            btn_yes.setText('Ok')
            btn_no = msg_box.button(QtWidgets.QMessageBox.No)
            btn_no.setText('No')

        msg_box.setDefaultButton(QtWidgets.QMessageBox.Yes)  # default to ok
        msg_box.setEscapeButton(QtWidgets.QMessageBox.No)  # Esc key --> No
        msg_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)  # user can select text in the page
        r = msg_box.exec_()  # popup this window
        if r == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def handle_clear_raw_files(self):
        """Handle Clear Raw Files"""
        self.init_table_raw_files()  # clear table
        self.data_files_raw = []  # clear container

    def handle_switch_between_tabs(self, index: int):
        """Switch between different TABs"""
        print(index)
        if index == 1:
            self.handle_switch_to_tab_normalise()  # switch to "Normalised Data" tab

        elif index == 2:
            self.handle_switch_to_tab_plot()  # switch to "Plot Data" tab

    def get_files_to_plot(self):
        """Gather normalised files for plot"""
        normalised_files = []  # creat an empty container

        if self.data_files_to_plot:
            normalised_files.extend(self.data_files_to_plot)
        # normalised_files = list(set(normalised_files))
        # normalised_files.sort()
        return normalised_files

    def add_one_row_to_table_nf(self, fp):
        """add one file to table normalised file"""
        r = self.table_nf.rowCount()  # get num of rows in the table
        self.table_nf.insertRow(r)  # append an empty row to the bottom

        self.data_files_to_plot.append(fp)  # add a normalised file to the list

        item = QtWidgets.QTableWidgetItem(os.path.split(fp)[1])  # create an item for the filename
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # read-only
        self.table_nf.setItem(r, 0, item)  # put in the table

        item = QtWidgets.QTableWidgetItem(fp)  # create an item for the filepath
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # read-only
        self.table_nf.setItem(r, 1, item)  # put in the table

        btn_view = QtWidgets.QPushButton('View Data')  # create a button to "View Data"
        self.table_nf.setCellWidget(r, 2, btn_view)  # put the newly created btn in the table
        btn_view.clicked.connect(partial(self.switch_and_view_data, r))  # bind click event

        btn_plot = QtWidgets.QPushButton('Plot Data')  # create a button to "PLot Data"
        self.table_nf.setCellWidget(r, 3, btn_plot)  # put the newly created btn in the table
        btn_plot.clicked.connect(partial(self.switch_and_plot_data, r))  # bind click event

    def handle_switch_to_tab_plot(self):
        """Handle Events when switched to tab Plot"""
        normalised_files = self.get_files_to_plot()  # gather files

        self.combo_result.blockSignals(True)  # block signals
        self.combo_result.clear()  # clear the combobox
        self.graphics_view.plot_clear()  # clear figure for next plot
        if not normalised_files:  # no normalised files
            self.data_current_normalised_file = None  # current normalised file as None
        else:
            self.combo_result.addItems(normalised_files)  # put all normalised files in the combobox as choices
        self.combo_result.blockSignals(False)  # enable signals

        if self.data_current_normalised_file in normalised_files:  # current normalised file is valid
            self.combo_result.setCurrentIndex(normalised_files.index(self.data_current_normalised_file))  # switch to it

    def handle_switch_to_tab_normalise(self):
        """Handle Events when switched to tab Normalise"""
        files = self.get_files_to_plot()  # gather normalised files

        self.combo_raw.blockSignals(True)  # block signals

        if not files:  # no normalised files
            self.combo_raw.clear()  # clear the combobox
            self.data_current_normalised_file = None  # set current normalised file as None
            self.init_table_results()  # clear the table that used to preview normalised data

        else:
            if self.data_current_normalised_file in files:  # current normalised file is valid
                index = files.index(self.data_current_normalised_file)  # index of current normalised files

                self.combo_raw.clear()  # clear the choices of normalised file in "Normalised Data"
                self.combo_raw.addItems(files)  # add them to combobox as choices
                self.combo_raw.setCurrentIndex(index)  # set current file as chosen one

            else:
                index = 0  # assume first one as the chosen one
                self.data_current_normalised_file = files[0]  # set first one as current normalised file
                self.combo_raw.clear()  # clear the combobox
                self.combo_raw.addItems(files)  # add to the combobox as choices
                self.init_table_results()  # init table of previewing normalised file

            self.handle_user_choose_view_normalised_file(index)  # handle switch to "Normalised Data" tab with chosen file

        self.combo_raw.blockSignals(False)  # allow signals

    def handle_user_choose_view_normalised_file(self, index: int):
        """The drop - down box selects a file"""
        if index < 0:  # invalid index
            self.data_current_normalised_file = None
            self.init_table_results()
        else:
            self.data_current_normalised_file = self.combo_raw.currentText()  # get chosen file path

            data = read_normalised_data(fp=self.data_current_normalised_file)  # read and parse normalised file

            if data:  # has data
                self.init_table_results(col=len(data[0]))  # init the preview table with exact columns
                self.fill_table_results(data=data)  # put data in the table
            else:
                self.init_table_results()  # init the preview table
        self.handle_update_display_of_lab_book()  # handle display of labbook

    def handle_update_display_of_lab_book(self):
        """Display Lab book in Tab Normalised"""
        data = {}
        if not self.data_current_normalised_file:  # no current normalised file
            pass
        else:
            _, fn = os.path.split(self.data_current_normalised_file)
            name, _ = os.path.splitext(fn)
            if name.endswith('_normalised'):
                name = name[:-11]
                print(name)
            data = self.data_lab_book.get(name, {})  # get labbook items
        if not data:  # no data, make all edit widgets empty
            self.edit_p_name.setText('')
            self.edit_p_time.setText('')
            self.edit_p_p.setText('')
            self.edit_p_e.setText('')
            self.edit_p_g.setText('')
            self.edit_p_c.setText('')
            self.edit_p_temp.setText('')
        else:
            # update edit widget
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
        if index < 0:  # invalid index
            return
        self.data_current_normalised_file = self.combo_result.currentText()  # handle user choose a normalised file

        self.graphics_view.plot_clear()  # clear the figure

    def handle_batch_set_shift(self):
        """Batch set shift wavelength"""
        # get wave shift from user
        intNum, ok = QtWidgets.QInputDialog.getDouble(self, "Setup waveShift for all", "WaveShift:", self.data_batch_shift, wave_shift_min, wave_shift_max, wave_shift_decimals)
        if ok:  # user decide to change the value
            self.data_batch_shift = intNum  # keep the value of default wave shift value
            for r in range(self.table_files.rowCount()):
                spin = self.table_files.cellWidget(r, 2)  # get the spin box
                spin.setValue(intNum)  # update it's value

    def handle_handle_plot(self):
        """The processing user clicks plot"""

        ct = self.combo_typo.currentText()  # current normalised file
        cf = self.combo_result.currentText()  # current style of the figure, either scatter or line.
        print(
            f'Type: {ct}; File: {cf}'
        )
        if cf:  # current normalised file exist
            data = read_normalised_data(cf)  # read amd parse the data
            self.graphics_view.plot_data(data=data,  # plot the data with chosen style
                                         typo=ct.lower(),
                                         title=f'Plot of Normalised {os.path.split(cf)[1]}')
        else:
            self.graphics_view.plot_clear()  # clear the figure
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
        normalised_files = self.get_files_to_plot()  # gather existing normalised files
        for i in ls:  # iterate through the list
            p = os.path.abspath(i)   # abs path
            if p in normalised_files:  # please do not repeat
                old += 1  # log existing num
                continue  # skip existing one

            fn = os.path.split(p)[1]  # get file name
            if '_normalised.txt' not in fn.lower():  # a normalised file should be end with "_normalised.txt"
                invalid += 1  # log invalid file num
                continue  # skip the invalid one

            self.add_one_row_to_table_nf(fp=p)  # add the file the table
            new += 1  # log new valid file
        self.show_info_message(message=f'<h1>Import Report</h1>Success {new}<br>Repeat {old}<br>Invalid {invalid}', parent=self, only_yes=True)

    def handle_import_lab_book(self):
        """Import Lab Book"""
        # file dialog for user choose the labbook
        fp, _ext = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Import Lab Book',
                                                          directory='.', filter='Txt Data Files(*.txt)')

        if not fp:  # no file chosen
            return
        try:
            self.data_lab_book = parse_lab_book(fp=fp)  # parse the labbook
            self.label_labbook.setText(f'Labbook: {os.path.split(fp)[1]}')  # display filename
            return self.show_info_message(message='Lab Book Imported', parent=self, )  # tell user file chosen
        except:
            return self.show_warning_message(message='Parsing Lab Book Failed', parent=self, )  # tell user file invalid

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
        """Handle the btn plot btn in "Normalised Data" tab clicked """
        index = self.combo_raw.currentIndex()  # get current index
        if index < 0:  # invalid index
            return
        self.switch_and_plot_data(index)  # switch to "Plot Data" tab
        self.handle_handle_plot()  # plot the data

    def handle_receive_result(self, fp: str, data: list):
        """"""
        the_raw_file = fp  # the raw file
        results = data  # results
        fd, fn = os.path.split(the_raw_file)  # split dir and the filename
        out_dir = os.path.join(fd, 'normalised')  # normalised dir
        a, b = os.path.splitext(fn)  # split base filename and extension
        fn = f'{a}_normalised{b}'  # generate out filename
        if not os.path.exists(out_dir):  # dir not exist
            os.makedirs(out_dir, exist_ok=True)  # create out
        out_file = os.path.abspath(os.path.join(out_dir, fn))  # out file location
        print(out_file)
        print(data)
        export_data(data=results, output_path=out_file)  # export data to a txt file

        if out_file not in self.data_files_to_plot:  # add to database if not exist
            self.add_one_row_to_table_nf(fp=out_file)  # display the out file in table

    def gather_tasks_and_process(self, index: int = None):
        if self.batch_service.isRunning():   # a jon is going on
            return self.show_warning_message(message='A Job is Running, Please Try Again Later.', parent=self, title='A Job is Running')
        if isinstance(index, int):  # invalid file index
            the_raw_file = self.data_files_raw[index]  # get current raw file
            shift = self.table_files.cellWidget(index, 2).value()  # int(self.table_files.item(index, 2).text())
            tasks = [(the_raw_file, shift), ]  # build tasks
        else:
            tasks = []  # create empty container
            for r in range(self.table_files.rowCount()):  # iterate through the table
                the_raw_file = self.data_files_raw[r]  # the raw file path
                shift = self.table_files.cellWidget(r, 2).value()  # gather it's shift value
                tasks.append((the_raw_file, shift))  # append the task
        if not tasks:  # nor tasks
            return self.show_warning_message(message='There are no jobs. Please import some raw files.', parent=self)
        print(tasks)
        self.batch_service.reload(tasks)  # refresh service
        self.batch_service.start()  # start processing
        # self.show_info_message(message='Please Wait. Processing is running in the background.', parent=self)
        self.popup.clear_shell()  # clear shell window of popup dialog
        self.popup.setFixedSize(self.size())  # setup size
        self.popup.move(self.pos())  # move the dialog
        self.popup.exec_()  # show a non-frame popup to block user from operating

    def handle_task_finished(self):
        """hide popup to allow user to operate"""
        self.popup.accept()  # hide popup window


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    m = MainApp()
    m.show()
    sys.exit(app.exec_())
