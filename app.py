from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from main import make_course_list, generate_schedule
import sys
sys.path.append('./models')
from course import Course
from daytime import Daytime

class Ui_MainWindow(object):
    #MainWindow
    def setupUi(self, MainWindow):
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
        #COURSE OFFERING FRAME /*
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
        
        #COURSE OFFERING FRAME */
        #OVERVIEW FRAM /*
        self.overview = QtWidgets.QFrame(self.tab)
        self.overview.setGeometry(QtCore.QRect(620, 70, 391, 451))
        self.overview.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.overview.setFrameShadow(QtWidgets.QFrame.Raised)
        self.overview.setObjectName("overview")

        self.submit = QtWidgets.QPushButton(self.overview)
        self.submit.setGeometry(QtCore.QRect(300, 410, 81, 31))
        #self.submit.clicked.connect(self.generate_button)
        self.submit.setObjectName("submit")

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
        self.current_list = self.overview_list1 #set default list
        self.overview_list1.itemActivated.connect(self.delete_course_popup)
        self.overview_list2.itemActivated.connect(self.delete_course_popup)
        self.overview_list3.itemActivated.connect(self.delete_course_popup)
        self.overview_list4.itemActivated.connect(self.delete_course_popup)
        self.overview_list5.itemActivated.connect(self.delete_course_popup)
        self.overview_list6.itemActivated.connect(self.delete_course_popup)
        self.overview_list7.itemActivated.connect(self.delete_course_popup)

        self.window_tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.window_tabs.addTab(self.tab_2, "")

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
        self.window_tabs.setTabEnabled(1,False)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #------------
        temp = make_course_list("courses.csv")
        self.course_list = temp[0]
        self.course_dict = temp[1]
        self.course_num_list_setup(ui.unique(self.course_list))
        self.course_num_list_translated(ui.unique(self.course_list))

        self.current_item = "" #sets default current item to nothing

        self.overview_tab_widget.currentChanged.connect(self.change_current_list)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Schedule Maker", "Schedule Maker"))

        __sortingEnabled = self.course_num_list_widget.isSortingEnabled()
        self.course_num_list_widget.setSortingEnabled(False)
        self.course_num_list_widget.setSortingEnabled(__sortingEnabled)

        self.course_search_button.setText(_translate("MainWindow", "Search"))

        self.window_tabs.setTabText(self.window_tabs.indexOf(self.tab), _translate("MainWindow", "Course Selection"))
        self.window_tabs.setTabText(self.window_tabs.indexOf(self.tab_2), _translate("MainWindow", "Generate"))

        self.add.setText(_translate("MainWindow", "Add"))

        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab1), _translate("MainWindow", "1"))
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab2), _translate("MainWindow", "2"))
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab3), _translate("MainWindow", "3"))
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab4), _translate("MainWindow", "4"))
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab5), _translate("MainWindow", "5"))
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab6), _translate("MainWindow", "6"))
        self.overview_tab_widget.setTabText(self.overview_tab_widget.indexOf(self.overview_tab7), _translate("MainWindow", "7"))

        self.submit.setText("Generate")

    def unique(self,course_list):
        unique_course_num = sorted(set([course.number for course in course_list]))
        self.unique_course_num = unique_course_num
        return(unique_course_num)

    def course_num_list_setup(self, course_list):
        for x in course_list:
            item = QtWidgets.QListWidgetItem()
            self.course_num_list_widget.addItem(item)

    def course_num_list_translated(self, course_list):
        count = 0
        _translate = QtCore.QCoreApplication.translate
        for x in course_list:
            item = self.course_num_list_widget.item(count)
            item.setText(_translate("MainWindow", str(x)))
            count += 1

    def reset_list(self):
        unique_all = self.unique_course_num
        self.course_num_list_widget.clear()
        self.course_num_list_setup(unique_all)
        self.course_num_list_translated(unique_all)

    def search(self):
        keyword = self.course_search.toPlainText()
        unique_all = self.unique_course_num
        search_list = []
        if keyword == '':
            self.reset_list()
        else:
            search_list = [course for course in unique_all if keyword.upper() in course]
            self.course_num_list_widget.clear()
            self.course_num_list_setup(search_list)
            self.course_num_list_translated(search_list)

    def course_selected(self,item):
        self.current_selected_course = item.text()
        section = self.find_section(item.text())
        self.section_list_setup(section)
        self.section_list_translated(section)

    def find_section(self,course):
        section_list = []
        for i in self.course_list:
            if i.number == course and i.section not in section_list:
                section_list.append(i.section)
        return section_list

    def section_list_setup(self,section):
        self.section_list_widget.clear()
        for i in section:
            item = QtWidgets.QListWidgetItem()
            self.section_list_widget.addItem(item)
    
    def section_list_translated(self,section):
        count = 0
        _translate = QtCore.QCoreApplication.translate
        for i in section:
            item = self.section_list_widget.item(count)
            item.setText(_translate("MainWindow", str(i)))
            count += 1

    def course_display_text(self,item):
        _translate = QtCore.QCoreApplication.translate
        self.current_item = (self.current_selected_course + " / " + item.text())
        self.course_display.setText(_translate("MainWindow", self.current_item))

    def change_current_list(self):
        current_tab = self.overview_tab_widget.currentIndex()
        list_case = {
            1 : self.overview_list1,
            2 : self.overview_list2,
            3 : self.overview_list3,
            4 : self.overview_list4,
            5 : self.overview_list5,
            6 : self.overview_list6,
            7 : self.overview_list7
            }
        self.current_list = list_case[current_tab+1]

    def add_course(self):
        if self.current_item == "":
            pass
        else:
            item = QtWidgets.QListWidgetItem()
            item.setText(self.current_item)
            self.current_list.addItem(item)
            #clears after adding
            self.course_display.setText("")
            self.current_item = ""
    
    def delete_course_popup(self,item):
        self.change_current_list()
        self.current_index = self.current_list.row(item)
        self.delete_window = QtWidgets.QMessageBox()
        self.delete_popup(self.delete_window)
        
    def delete_course(self):
        self.current_list.takeItem(self.current_index)
        self.delete_window.close()

    def delete_popup(self, msgBox):
        msgBox.setWindowTitle("Delete Confirmation")
        msgBox.setText("Are you sure you want to delete this item?")
        delete = msgBox.addButton('Delete', msgBox.ActionRole)
        delete.clicked.disconnect()
        delete.clicked.connect(self.delete_course)
        cancel = msgBox.addButton('Cancel', QtWidgets.QMessageBox.RejectRole)
        msgBox.show()
        msgBox.exec_()
    
    def get_course(self,lst):
        count = lst.count()
        x = []
        for i in range(0,count):
            x.append(lst.item(i).text())
        return x
        
    def generate_button(self):
        x = [self.overview_list1,self.overview_list2,self.overview_list3,self.overview_list4,self.overview_list5,self.overview_list6,self.overview_list7]
        self.submitted_list = list(map(self.get_course,x))
        #print(self.submitted_list)
        #print(generate_schedule(self.submitted_list,self.course_dict))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
 