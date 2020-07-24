from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
import sys

sys.path.append("./models")
from offeringParser import make_course_list, convList
from generateSchedule import checkValid
from generateGraphic import objToArray, graphic, makeFolder


class Ui_MainWindow(object):
    # MainWindow
    def setupUi(self, MainWindow, offering):
        self.directory = ""

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1111, 681)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.window_tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.window_tabs.setEnabled(True)
        self.window_tabs.setGeometry(QtCore.QRect(0, 0, 1111, 661))

        self.window_tabs.setObjectName("window_tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        # COURSE OFFERING FRAME /*
        self.course_offering = QtWidgets.QFrame(self.tab)
        self.course_offering.setGeometry(QtCore.QRect(140, 80, 371, 451))
        self.course_offering.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.course_offering.setFrameShadow(QtWidgets.QFrame.Raised)
        self.course_offering.setObjectName("course_offering")

        self.course_num_list_widget = QtWidgets.QListWidget(self.course_offering)
        self.course_num_list_widget.setGeometry(QtCore.QRect(10, 50, 251, 341))
        self.course_num_list_widget.setObjectName("course_num_list_widget")
        self.course_num_list_widget.itemActivated.connect(self.course_selected)

        self.section_list_widget = QtWidgets.QListWidget(self.course_offering)
        self.section_list_widget.setGeometry(QtCore.QRect(280, 50, 81, 341))
        self.section_list_widget.setObjectName("section_list_widget")
        self.section_list_widget.itemActivated.connect(self.course_display_text)

        self.course_search_button = QtWidgets.QPushButton(self.course_offering)
        self.course_search_button.setGeometry(QtCore.QRect(190, 10, 75, 23))
        self.course_search_button.setObjectName("course_search_button")
        self.course_search_button.clicked.connect(self.search)

        self.course_search = QtWidgets.QTextEdit(self.course_offering)
        self.course_search.setGeometry(QtCore.QRect(10, 10, 171, 31))
        self.course_search.setObjectName("course_search")

        self.course_display = QtWidgets.QTextBrowser(self.course_offering)
        self.course_display.setGeometry(QtCore.QRect(70, 400, 191, 31))
        self.course_display.setObjectName("course_display")

        self.add = QtWidgets.QPushButton(self.course_offering)
        self.add.setGeometry(QtCore.QRect(280, 400, 81, 31))
        self.add.setObjectName("add")
        self.add.clicked.connect(self.add_course)
        # COURSE OFFERING FRAME */

        # OVERVIEW FRAME /*
        self.overview = QtWidgets.QFrame(self.tab)
        self.overview.setGeometry(QtCore.QRect(620, 70, 391, 491))
        self.overview.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.overview.setFrameShadow(QtWidgets.QFrame.Raised)
        self.overview.setObjectName("overview")

        self.submit = QtWidgets.QPushButton(self.overview)
        self.submit.setGeometry(QtCore.QRect(300, 410, 81, 31))
        self.submit.clicked.connect(self.generate_button)
        self.submit.setObjectName("submit")

        self.directoryBtn = QtWidgets.QPushButton(self.overview)
        self.directoryBtn.setGeometry(QtCore.QRect(0, 410, 150, 31))
        self.directoryBtn.clicked.connect(self.directoryBox)
        self.directoryBtn.setObjectName("directoryBtn")

        self.path_display = QtWidgets.QTextBrowser(self.overview)
        self.path_display.setGeometry(QtCore.QRect(0, 450, 381, 31))
        self.path_display.setObjectName("path_display")

        self.overview_tab_widget = QtWidgets.QTabWidget(self.overview)
        self.overview_tab_widget.setGeometry(QtCore.QRect(0, 10, 381, 391))
        self.overview_tab_widget.setToolTipDuration(0)
        self.overview_tab_widget.setIconSize(QtCore.QSize(16, 16))
        self.overview_tab_widget.setObjectName("overview_tab_widget")

        self.overview_tab1 = QtWidgets.QWidget()
        self.overview_tab1.setObjectName("overview_tab1")
        self.overview_list1 = QtWidgets.QListWidget(self.overview_tab1)
        self.overview_list1.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.overview_list1.setObjectName("overview_list1")
        self.overview_tab_widget.addTab(self.overview_tab1, "")
        self.overview_tab2 = QtWidgets.QWidget()
        self.overview_tab2.setObjectName("overview_tab2")
        self.overview_list2 = QtWidgets.QListWidget(self.overview_tab2)
        self.overview_list2.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.overview_list2.setObjectName("overview_list2")
        self.overview_tab_widget.addTab(self.overview_tab2, "")
        self.overview_tab3 = QtWidgets.QWidget()
        self.overview_tab3.setObjectName("overview_tab3")
        self.overview_list3 = QtWidgets.QListWidget(self.overview_tab3)
        self.overview_list3.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.overview_list3.setObjectName("overview_list3")
        self.overview_tab_widget.addTab(self.overview_tab3, "")
        self.overview_tab4 = QtWidgets.QWidget()
        self.overview_tab4.setObjectName("overview_tab4")
        self.overview_list4 = QtWidgets.QListWidget(self.overview_tab4)
        self.overview_list4.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.overview_list4.setObjectName("overview_list4")
        self.overview_tab_widget.addTab(self.overview_tab4, "")
        self.overview_tab5 = QtWidgets.QWidget()
        self.overview_tab5.setObjectName("overview_tab5")
        self.overview_list5 = QtWidgets.QListWidget(self.overview_tab5)
        self.overview_list5.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.overview_list5.setObjectName("overview_list5")
        self.overview_tab_widget.addTab(self.overview_tab5, "")
        self.overview_tab6 = QtWidgets.QWidget()
        self.overview_tab6.setObjectName("overview_tab6")
        self.overview_list6 = QtWidgets.QListWidget(self.overview_tab6)
        self.overview_list6.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.overview_list6.setObjectName("overview_list6")
        self.overview_tab_widget.addTab(self.overview_tab6, "")
        self.overview_tab7 = QtWidgets.QWidget()
        self.overview_tab7.setObjectName("overview_tab7")
        self.overview_list7 = QtWidgets.QListWidget(self.overview_tab7)
        self.overview_list7.setGeometry(QtCore.QRect(0, 0, 381, 371))
        self.overview_list7.setObjectName("overview_list7")
        self.overview_tab_widget.addTab(self.overview_tab7, "")
        self.current_list = self.overview_list1  # set default list
        self.overview_list1.itemActivated.connect(self.delete_popup)
        self.overview_list2.itemActivated.connect(self.delete_popup)
        self.overview_list3.itemActivated.connect(self.delete_popup)
        self.overview_list4.itemActivated.connect(self.delete_popup)
        self.overview_list5.itemActivated.connect(self.delete_popup)
        self.overview_list6.itemActivated.connect(self.delete_popup)
        self.overview_list7.itemActivated.connect(self.delete_popup)
        # */

        self.window_tabs.addTab(self.tab, "")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1111, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.window_tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # ------------
        self.course_list, self.course_dict = make_course_list(offering)
        self.course_num_list_setup(self.unique(self.course_list))

        self.current_item = ""  # sets default current item to nothing

        self.overview_tab_widget.currentChanged.connect(self.change_current_list)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Schedule Maker")

        __sortingEnabled = self.course_num_list_widget.isSortingEnabled()
        self.course_num_list_widget.setSortingEnabled(False)
        self.course_num_list_widget.setSortingEnabled(__sortingEnabled)

        self.course_search_button.setText("Search")

        self.window_tabs.setTabText(self.window_tabs.indexOf(self.tab), "Course Selection")

        self.add.setText("Add")

        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab1), "1")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab2), "2")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab3), "3")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab4), "4")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab5), "5")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab6), "6")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab7), "7")

        self.submit.setText("Generate")

        self.directoryBtn.setText("Choose save directory")

    def unique(self, course_list):
        unique_course_num = sorted(set([course.number for course in course_list]))
        self.unique_course_num = unique_course_num
        return unique_course_num

    def course_num_list_setup(self, course_list):
        for x in course_list:
            item = QtWidgets.QListWidgetItem()
            self.course_num_list_widget.addItem(item)
            item.setText(str(x))

    def reset_list(self):
        unique_all = self.unique_course_num
        self.course_num_list_widget.clear()
        self.course_num_list_setup(unique_all)

    def search(self):
        keyword = self.course_search.toPlainText()
        unique_all = self.unique_course_num
        search_list = []
        if keyword == "":
            self.reset_list()
        else:
            search_list = [course for course in unique_all if keyword.upper() in course]
            self.course_num_list_widget.clear()
            self.course_num_list_setup(search_list)

    def course_selected(self, item):
        self.current_selected_course = item.text()
        section = self.find_section(item.text())
        self.section_list_setup(section)

    def find_section(self, course):
        section_list = []
        for i in self.course_list:
            if i.number == course and i.section not in section_list:
                section_list.append(i.section)
        return section_list

    def section_list_setup(self, section):
        self.section_list_widget.clear()
        for i in section:
            item = QtWidgets.QListWidgetItem()
            self.section_list_widget.addItem(item)
            item.setText(str(i))

    def course_display_text(self, item):
        self.current_item = self.current_selected_course + " / " + item.text()
        self.course_display.setText(self.current_item)

    def change_current_list(self):
        current_tab = self.overview_tab_widget.currentIndex()
        list_case = {
            1: self.overview_list1,
            2: self.overview_list2,
            3: self.overview_list3,
            4: self.overview_list4,
            5: self.overview_list5,
            6: self.overview_list6,
            7: self.overview_list7,
        }
        self.current_list = list_case[current_tab + 1]

    def add_course(self):
        if self.current_item == "":
            pass
        else:
            item = QtWidgets.QListWidgetItem()
            item.setText(self.current_item)
            self.current_list.addItem(item)
            # clears after adding
            self.course_display.setText("")
            self.current_item = ""

    def delete_popup(self, item):
        self.change_current_list()
        self.current_index = self.current_list.row(item)
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Delete Confirmation")
        msgBox.setText("Are you sure you want to delete this item?")
        msgBox.setIcon(QMessageBox.Warning)
        delete = msgBox.addButton("Delete", msgBox.ActionRole)
        delete.clicked.connect(self.delete_course)
        cancel = msgBox.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
        msgBox.exec_()

    def delete_course(self):
        self.current_list.takeItem(self.current_index)

    def get_course(self, lst):
        count = lst.count()
        x = []
        for i in range(0, count):
            x.append(lst.item(i).text())
        return x

    def generate_button(self):
        if not self.directory:
            self.noDirectory()
            return
        x = [
            self.overview_list1,
            self.overview_list2,
            self.overview_list3,
            self.overview_list4,
            self.overview_list5,
            self.overview_list6,
            self.overview_list7,
        ]
        for i in x:
            if len(i) < 1:
                self.noValidOutput()
                return
        self.submitted_list = convList(list(map(self.get_course, x)), self.course_dict)
        output = checkValid(self.submitted_list)
        if output:
            for permutation in output:
                arr, courseOrder = objToArray(permutation)
                graphic(arr, courseOrder, self.subDir)
        else:
            self.noValidOutput()

    def directoryBox(self):
        self.directoryBtn.disconnect()  # prevents opening multiple dialogs
        Tk().withdraw()
        self.directory = askdirectory()
        if self.directory:  # if not empty
            self.path_display.setText(self.directory)
            self.subDir = makeFolder(self.directory)
        self.directoryBtn.clicked.connect(self.directoryBox)

    def noDirectory(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Alert")
        msgBox.setText("Please choose an output directory.")
        msgBox.exec_()

    def noValidOutput(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Alert")
        msgBox.setText("No valid schedule combinations.")
        msgBox.exec_()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("landing")
        Form.resize(300, 320)

        self.uploadBtn = QtWidgets.QPushButton(Form)
        self.uploadBtn.setGeometry(QtCore.QRect(100, 240, 100, 40))
        self.uploadBtn.setObjectName("uploadBtn")
        self.uploadBtn.clicked.connect(self.fileDialog)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 20, 201, 201))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("icon.png"))
        self.label.setObjectName("label")

        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setWindowTitle("Course offering")
        self.uploadBtn.setText("Upload")

        self.filename = ""

    def fileDialog(self):
        self.uploadBtn.disconnect()  # prevents opening multiple dialogs
        Tk().withdraw()
        self.filename = askopenfilename()
        self.uploadBtn.clicked.connect(self.fileDialog)
        if self.filename:
            try:
                self.window = QtWidgets.QMainWindow()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self.window, self.filename)
                self.window.show()
                LandingPage.hide()
            except:
                self.alert()

    def alert(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Alert")
        msgBox.setText("Invalid course offering file or failed to parse.")
        msgBox.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.png"))
    LandingPage = QtWidgets.QMainWindow()
    landingPage = Ui_Form()
    landingPage.setupUi(LandingPage)
    LandingPage.show()

    sys.exit(app.exec_())
