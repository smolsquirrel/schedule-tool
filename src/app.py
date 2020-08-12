import sys
import os
import ctypes
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from random import randint
import webbrowser
from offeringParser import make_course_list, convList
from generateSchedule import checkValid
from generateGraphic import objToArray, graphic, makeFolder

myappid = "scheduleMaker"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

assetsPath = os.path.dirname(os.getcwd()) + r"\assets"


class Frame(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)


class overviewList(QtWidgets.QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 700, 392))
        self.setDragEnabled(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.itemPressed.connect(self.quickDelete)
        self.setAcceptDrops(True)
        self.selectedSection = ""
        self.shifted = False
        style = """
            background-color: #2F3640;
            border: none;
        """
        self.setStyleSheet(style)

    def quickDelete(self, item):
        if self.shifted:
            row = self.row(item)
            self.takeItem(row)

    def dropEvent(self, event):
        if event.source() != self:
            item = QtWidgets.QListWidgetItem()
            font = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)  # TODO CHANGE FONT
            item.setFont(font)
            color = QtGui.QColor(26, 188, 156)  # TODO CHANGE COLOR
            brush = QtGui.QBrush(color)
            item.setForeground(brush)
            item.setText(str(self.selectedSection))
            self.addItem(item)


class MainWin(QtWidgets.QMainWindow):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Message in statusbar.")
        self.statusbar.setVisible(False)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        globalStyle = """
            QScrollBar:vertical {
                width: 15px;
                background-color: #F5F5F5;
                margin: 0;
            }
            QScrollBar:add-line:vertical,QScrollBar:sub-line:vertical{
                width: 0px;
                height: 0px;
                border: none;
                background: none;
            }
            QScrollBar:add-page:vertical, QScrollBar:sub-page:vertical {
                height: 0px;
                background-color: #2F3640;
            }
            QScrollBar:handle:vertical{
                min-height: 100px;
                max-height: 200px;
                border: 0px;
                border-radius: 6px;
                background-color: #232830;
            }
            QScrollBar:vertical {
                background-color: #ffffff;
            }
        """
        self.setStyleSheet(globalStyle)

    def keyPressEvent(self, event):
        if event.key() == 16777248:  # shift
            self.current_list.shifted = True

    def keyReleaseEvent(self, event):
        if event.key() == 16777248:  # shift
            self.current_list.shifted = False

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        x = event.localPos().x()
        y = event.localPos().y()
        self.valid = True
        if (x > 1119 and y < 20) or y > 70:
            self.valid = False

    def mouseMoveEvent(self, event):
        if self.valid:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def setupUi(self):
        self.directory = ""
        self.setFixedSize(1200, 680)
        self.centralwidget = QtWidgets.QWidget(self)

        # Background
        self.background = Frame(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 1200, 680))
        self.background.style = """
            background-color: #57606F;
        """
        self.background.setStyleSheet(self.background.style)

        # Top Bar
        self.topbar = Frame(self.background)
        self.topbar.setGeometry(QtCore.QRect(0, 0, 1200, 70))
        topbarStyle = """
            background-color: #2F3640;
        """
        self.topbar.setStyleSheet(topbarStyle)
        winBtnStyle = """
            border: solid;
            background-color: #282C31;
            color: #F5F6FA;
        """

        self.closeBtn = QtWidgets.QPushButton(self.topbar)
        self.closeBtn.setGeometry(QtCore.QRect(1160, 0, 40, 20))
        self.closeBtn.setText("X")
        self.closeBtn.clicked.connect(lambda: self.close())
        self.closeBtn.setStyleSheet(winBtnStyle)

        self.miniBtn = QtWidgets.QPushButton(self.topbar)
        self.miniBtn.setGeometry(QtCore.QRect(1119, 0, 40, 20))
        self.miniBtn.setText("-")
        self.miniBtn.clicked.connect(lambda: self.showMinimized())
        self.miniBtn.setStyleSheet(winBtnStyle)

        self.line = QtWidgets.QFrame(self.topbar)
        self.line.setGeometry(QtCore.QRect(0, 64, 1201, 16))
        self.line.setStyleSheet("background-color: #232830;")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)

        self.course_offering = Frame(self.background)
        self.course_offering.setGeometry(QtCore.QRect(140, 80, 371, 451))

        self.course_num_list_widget = QtWidgets.QListWidget(self.background)
        self.course_num_list_widget.setGeometry(QtCore.QRect(0, 70, 280, 610))
        self.course_num_list_widget.itemClicked.connect(self.course_selected)
        self.course_num_list_widget.itemSelectionChanged.connect(self.course_selected_alt)
        courseListStyle = """
            background-color: #353B48;
            border: 0;
        """
        self.course_num_list_widget.setStyleSheet(courseListStyle)

        self.section_list_widget = QtWidgets.QListWidget(self.background)
        self.section_list_widget.setGeometry(QtCore.QRect(280, 70, 115, 610))
        self.section_list_widget.setDragEnabled(True)
        self.section_list_widget.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.section_list_widget.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.section_list_widget.itemPressed.connect(self.setCourse)
        self.section_list_widget.itemSelectionChanged.connect(self.setCourseAlt)
        self.section_list_widget.itemActivated.connect(self.add_course)
        sectionStyle = """
            background-color: #353B48;
            border: 0;
        """
        self.section_list_widget.setStyleSheet(sectionStyle)

        self.course_search = QtWidgets.QTextEdit(self.background)
        self.course_search.setGeometry(QtCore.QRect(12, 12, 580, 47))
        self.course_search.textChanged.connect(self.search)
        self.course_search.setPlaceholderText("Search course number")
        searchBarStyle = """
            background-color: #F5F6FA;
            border-color: #707070;
            border-radius: 22px;
            font-size: 30px;
            padding-left: 20px;
        """
        self.course_search.setStyleSheet(searchBarStyle)
        self.course_search.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, offset=QtCore.QPointF(0, 0))
        )

        self.clearSearch = QtWidgets.QPushButton(self.topbar)
        self.clearSearch.setGeometry(QtCore.QRect(605, 12, 47, 47))
        self.clearSearch.clicked.connect(lambda: self.course_search.setText(""))
        font = QtGui.QFont("Segoe UI", 20)  # TODO CHANGE FONT
        self.clearSearch.setFont(font)
        self.clearSearch.setText("X")
        clearStyle = """
            background-color: #F5F6FA;
            width: 46px;
            height: 46px;
            border-radius:23px;
            padding: 2px;
            padding-bottom: 6px;
            color: #707070;
            padding-left: 3px;
        """
        self.clearSearch.setStyleSheet(clearStyle)
        self.clearSearch.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, offset=QtCore.QPointF(0, 0))
        )

        # Bottom Bar
        self.botbar = Frame(self.background)
        self.botbar.setGeometry(QtCore.QRect(394, 590, 806, 90))
        botbarStyle = """
            background-color: #2F3640;
        """
        self.botbar.setStyleSheet(botbarStyle)

        self.generate = QtWidgets.QPushButton(self.botbar)
        self.generate.setGeometry(QtCore.QRect(686, 26, 103, 39))
        self.generate.clicked.connect(self.generate_button)
        generateBtnStyle = """
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #707070;
            border-radius: 19px;
            font-family: "Segoe UI";
            font-size: 20px;
            color: #707070;
            padding-left: 10px;
            padding-bottom: 5px;
            text-align: left;
        """
        self.generate.setStyleSheet(generateBtnStyle)
        self.generate.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, offset=QtCore.QPointF(0, 0)))

        self.directoryBtn = QtWidgets.QPushButton(self.botbar)
        self.directoryBtn.setGeometry(QtCore.QRect(19, 26, 650, 38))
        self.directoryBtn.clicked.connect(self.directoryBox)
        directoryStyle = """
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #707070;
            border-radius: 19px;
            font-family: "Segoe UI";
            color: #707070;
            font-size: 20px;
            padding-left: 10px;
            padding-bottom: 5px;
            text-align: left;
        """
        self.directoryBtn.setStyleSheet(directoryStyle)

        self.directoryBtn.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, offset=QtCore.QPointF(0, 0))
        )
        self.overview_tab_widget = QtWidgets.QTabWidget(self.background)
        self.overview_tab_widget.setGeometry(QtCore.QRect(448, 106, 700, 439))
        self.overview_tab_widget.setToolTipDuration(0)
        self.overview_tab_widget.setIconSize(QtCore.QSize(16, 16))
        overviewStyle = """
            QTabBar:tab{
                width: 90px;
                height: 40px;
                background-color: #262C34;
                border: 1px solid;
                border:none;
                border-color: #707070;
                font-family: "Segoe UI";
                font-size: 20px;
                color: #FFFFFF;
                padding-bottom: 3px;
                bottom: 0;
                position: fixed;
            }
            QTabBar:tab:selected{
                background-color: #16a085;
            }
            QTabWidget:pane{
                border: none;
            }
        """
        self.overview_tab_widget.setStyleSheet(overviewStyle)
        self.overview_tab_widget.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=50, offset=QtCore.QPointF(0, 0))
        )

        self.overview_tab1 = QtWidgets.QWidget()
        self.overview_list1 = overviewList(self.overview_tab1)
        self.overview_tab_widget.addTab(self.overview_tab1, "")
        self.overview_tab2 = QtWidgets.QWidget()
        self.overview_list2 = overviewList(self.overview_tab2)
        self.overview_tab_widget.addTab(self.overview_tab2, "")
        self.overview_tab3 = QtWidgets.QWidget()
        self.overview_list3 = overviewList(self.overview_tab3)
        self.overview_tab_widget.addTab(self.overview_tab3, "")
        self.overview_tab4 = QtWidgets.QWidget()
        self.overview_list4 = overviewList(self.overview_tab4)
        self.overview_tab_widget.addTab(self.overview_tab4, "")
        self.overview_tab5 = QtWidgets.QWidget()
        self.overview_list5 = overviewList(self.overview_tab5)
        self.overview_tab_widget.addTab(self.overview_tab5, "")
        self.overview_tab6 = QtWidgets.QWidget()
        self.overview_list6 = overviewList(self.overview_tab6)
        self.overview_tab_widget.addTab(self.overview_tab6, "")
        self.overview_tab7 = QtWidgets.QWidget()
        self.overview_list7 = overviewList(self.overview_tab7)
        self.overview_tab_widget.addTab(self.overview_tab7, "")
        self.current_list = self.overview_list1  # set default list
        self.ovLst = [
            self.overview_list1,
            self.overview_list2,
            self.overview_list3,
            self.overview_list4,
            self.overview_list5,
            self.overview_list6,
            self.overview_list7,
        ]
        for x in self.ovLst:
            x.itemActivated.connect(self.delete_popup)

        clearBtnStyle = """
            background-color: #FFFFFF;
            border: 1px solid;
            border-color: #707070;
            border-radius: 12;
            color: #707070;
            font-family: "Segoe UI"
        """
        self.clearBtn = QtWidgets.QPushButton(self.background)
        self.clearBtn.setGeometry(QtCore.QRect(1087, 554, 61, 25))
        self.clearBtn.setText("Clear")
        self.clearBtn.setStyleSheet(clearBtnStyle)
        self.clearBtn.pressed.connect(self.clear_popup)
        self.clearBtn.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, offset=QtCore.QPointF(0, 0)))

        self.clearAllBtn = QtWidgets.QPushButton(self.background)
        self.clearAllBtn.setGeometry(QtCore.QRect(1000, 554, 75, 25))
        self.clearAllBtn.setText("Clear all")
        self.clearAllBtn.setStyleSheet(clearBtnStyle)
        self.clearAllBtn.pressed.connect(self.clearAll_popup)
        self.clearAllBtn.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, offset=QtCore.QPointF(0, 0))
        )

        self.setCentralWidget(self.background)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.course_list, self.course_dict = make_course_list(self.filename)
        self.course_num_list_setup(self.unique(self.course_list))

        self.current_item = ""  # sets default current item to nothing

        self.overview_tab_widget.currentChanged.connect(self.change_current_list)

    def retranslateUi(self):
        self.setWindowTitle("Schedule Maker")

        __sortingEnabled = self.course_num_list_widget.isSortingEnabled()
        self.course_num_list_widget.setSortingEnabled(False)
        self.course_num_list_widget.setSortingEnabled(__sortingEnabled)

        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab1), "1")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab2), "2")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab3), "3")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab4), "4")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab5), "5")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab6), "6")
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab7), "7")

        self.generate.setText("Generate")

        self.directoryBtn.setText("Choose save directory")

    def unique(self, course_list):
        unique_course_num = sorted(set([course.number for course in course_list]))
        self.unique_course_num = unique_course_num
        return unique_course_num

    def course_num_list_setup(self, course_list):
        for x in course_list:
            item = QtWidgets.QListWidgetItem()

            font = QtGui.QFont("Segoe UI", 20, QtGui.QFont.Bold)
            item.setFont(font)
            color = QtGui.QColor(26, 188, 156)
            brush = QtGui.QBrush(color)
            item.setForeground(brush)
            self.course_num_list_widget.addItem(item)
            item.setText(str(x))

    def reset_list(self):
        unique_all = self.unique_course_num
        self.course_num_list_widget.clear()
        self.course_num_list_setup(unique_all)

    def search(self):
        keyword = self.course_search.toPlainText().strip()
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

    def course_selected_alt(self):
        item = self.course_num_list_widget.currentItem()
        self.course_selected(item)

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
            font = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
            item.setFont(font)
            color = QtGui.QColor(26, 188, 156)
            brush = QtGui.QBrush(color)
            item.setForeground(brush)
            item.setText(str(i))
            self.section_list_widget.addItem(item)

    def setCourse(self, item):
        self.current_item = self.current_selected_course + " / " + item.text()
        self.current_list.selectedSection = self.current_item

    def setCourseAlt(self):
        item = self.section_list_widget.currentItem()
        self.setCourse(item)

    def change_current_list(self):
        current_tab = self.overview_tab_widget.currentIndex()
        num = [1, 2, 3, 4, 5, 6, 7, 8]
        list_case = dict(zip(num, self.ovLst))
        self.current_list = list_case[current_tab + 1]

    def add_course(self):
        if self.current_item == "":
            pass
        else:
            item = QtWidgets.QListWidgetItem()
            font = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
            item.setFont(font)
            color = QtGui.QColor(26, 188, 156)
            brush = QtGui.QBrush(color)
            item.setForeground(brush)
            item.setText(str(self.current_item))
            self.current_list.addItem(item)

    def clear_popup(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Clear Confirmation")
        msgBox.setText("Are you sure you want to clear?")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        clear = msgBox.addButton("Clear", msgBox.ActionRole)
        clear.clicked.connect(lambda: self.current_list.clear())
        cancel = msgBox.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
        msgBox.exec_()

    def clearAll_popup(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Clear All Confirmation")
        msgBox.setText("Are you sure you want to clear all?")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        clear = msgBox.addButton("Clear all", msgBox.ActionRole)
        clear.clicked.connect(self.clearAll)
        cancel = msgBox.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
        msgBox.exec_()

    def delete_popup(self, item):
        self.change_current_list()
        self.current_index = self.current_list.row(item)
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Delete Confirmation")
        msgBox.setText("Are you sure you want to delete this item?")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        delete = msgBox.addButton("Delete", msgBox.ActionRole)
        delete.clicked.connect(self.delete_course_pop)
        cancel = msgBox.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
        self.cb = QtWidgets.QCheckBox("Do not show me again")
        dontShow = msgBox.setCheckBox(self.cb)
        msgBox.exec_()

    def delete_course_pop(self):
        if self.cb.checkState():
            for x in self.ovLst:
                x.itemActivated.disconnect()
                x.itemActivated.connect(self.delete_course)
        self.current_list.takeItem(self.current_index)

    def delete_course(self, item):
        self.change_current_list()
        self.current_index = self.current_list.row(item)
        self.current_list.takeItem(self.current_index)

    def clearAll(self):
        temp = [x.clear() for x in self.ovLst]
        del temp

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
        for i in self.ovLst:
            if len(i) < 1:
                self.noValidOutput()
                return
        self.submitted_list = convList(list(map(self.get_course, self.ovLst)), self.course_dict)
        output = checkValid(self.submitted_list)
        if output:
            unique = randint(1000, 9999)
            folderPath = f"{self.directory}/{unique}"
            os.mkdir(folderPath)
            for permutation in output:
                arr, courseOrder = objToArray(permutation)
                graphic(arr, courseOrder, folderPath)
            webbrowser.open(folderPath)
        else:
            self.noValidOutput()

    def directoryBox(self):
        self.directoryBtn.disconnect()  # prevents opening multiple dialogs
        Tk().withdraw()
        self.directory = askdirectory()
        if self.directory:  # if not empty
            self.directoryBtn.setText(self.directory)
        self.directoryBtn.clicked.connect(self.directoryBox)

    def noDirectory(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle("Alert")
        msgBox.setText("Please choose an output directory.")
        msgBox.exec_()

    def noValidOutput(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle("Alert")
        msgBox.setText("No valid schedule combinations.")
        msgBox.exec_()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setFixedSize(300, 320)

        self.uploadBtn = QtWidgets.QPushButton(Form)
        self.uploadBtn.setStyle
        self.uploadBtn.setGeometry(QtCore.QRect(100, 240, 100, 40))
        self.uploadBtn.clicked.connect(self.fileDialog)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 20, 201, 201))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(assetsPath + "\icon.png"))

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
                self.window = MainWin(self.filename)
                self.window.setupUi()
                self.window.show()
                LandingPage.hide()
            except:
                self.alert()

    def alert(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle("Alert")
        msgBox.setText("Invalid course offering file or failed to parse.")
        msgBox.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(assetsPath + "\icon.png"))
    LandingPage = QtWidgets.QMainWindow()
    landingPage = Ui_Form()
    landingPage.setupUi(LandingPage)
    LandingPage.show()

    sys.exit(app.exec_())
