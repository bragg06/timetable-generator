import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, 
                             QPushButton, QMessageBox, QHeaderView, QLineEdit, QDialog, QFormLayout, 
                             QSpinBox, QComboBox, QDialogButtonBox, QSizePolicy, QHBoxLayout,QMainWindow,QStackedWidget)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt

class TimetableWindow(QWidget):
    def __init__(self, table_name, label_text,role):
        super().__init__()
        self.table_name = table_name
        self.label_text = label_text
        self.role=role
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Timetable - {self.label_text}')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #f5f5f5; border: 2px solid #dddddd; border-radius: 10px;")
        self.resize(1200, 800)  # Increased the height to accommodate the teacher table
        layout = QVBoxLayout()

        title = QLabel(f'{self.label_text} Timetable')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Day", "Hour 1\n8:00-8:50", "Hour 2\n8:50-9:40", "Break 1\n9:40-10:05", "Hour 3\n10:05-10:55", "Hour 4\n10:55-11:45",
              "Lunch\n11:45-12:45", "Hour 5\n12:45-1:35", "Hour 6\n1:35-2:25", "Break\n2:25-2:50", "Hour 7\n2:50-3:40"]
        )
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setStyleSheet("QTableWidget { background-color: white; border: 1px solid #cccccc; border-radius: 5px; }"
                                       "QHeaderView::section { background-color: #3b5998; color: white; border-radius: 5px; }")
        self.tableWidget.verticalHeader().setVisible(False)

        layout.addWidget(self.tableWidget)

        self.teacherInfoTable = QTableWidget()
        self.teacherInfoTable.setColumnCount(4)
        self.teacherInfoTable.setHorizontalHeaderLabels(["Teacher Code", "Teacher Name", "Subject Code","Subject Name"])
        self.teacherInfoTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.teacherInfoTable.setStyleSheet("QTableWidget { background-color: white; border: 1px solid #cccccc; border-radius: 5px; }"
                                            "QHeaderView::section { background-color: #3b5998; color: white; border-radius: 5px; }")
        self.teacherInfoTable.verticalHeader().setVisible(False)
        layout.addWidget(self.teacherInfoTable)

        self.labInfoTable = QTableWidget()
        self.labInfoTable.setColumnCount(6)
        self.labInfoTable.setHorizontalHeaderLabels(["Teacher Code", "Teacher Name", "Lab Code","Subject code","Subject Name","Lab"])
        self.labInfoTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.labInfoTable.setStyleSheet("QTableWidget { background-color: white; border: 1px solid #cccccc; border-radius: 5px; }"
                                            "QHeaderView::section { background-color: #3b5998; color: white; border-radius: 5px; }")
        self.labInfoTable.verticalHeader().setVisible(False)
        layout.addWidget(self.labInfoTable)

        self.loadTimetableData()
        self.setLayout(layout)

    def loadTimetableData(self):
        self.tableWidget.setRowCount(0)
        try:
            connection = sqlite3.connect('yourdatabase.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            timetable_data = cursor.fetchall()
            teacher_codes = set()

            for row_data in timetable_data:
                row_num = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(row_num, col_num, item)
                    if(self.role == 'Student'):
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
                    if ('/' in str(col_data)) :
                        i=col_data.index('/')+1
                        col_data=col_data[i:]
                    if col_num != 0:  # Assuming first column is 'Day'
                        teacher_codes.add(col_data)

            connection.close()

            self.loadTeacherInfo(teacher_codes)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}", QMessageBox.Ok)

    def loadTeacherInfo(self, teacher_codes):
        self.teacherInfoTable.setRowCount(0)
        try:
            connection = sqlite3.connect('mydatabase.db')
            cursor = connection.cursor()
            for code in teacher_codes:
                cursor.execute(f"SELECT staff_code, name, subject, subject_name FROM {self.table_name}  WHERE staff_code = ?", (code,))
                teacher_data = cursor.fetchone()
                if teacher_data:
                    row_num = self.teacherInfoTable.rowCount()
                    self.teacherInfoTable.insertRow(row_num)
                    for col_num, col_data in enumerate(teacher_data):
                        item = QTableWidgetItem(str(col_data))
                        item.setTextAlignment(Qt.AlignCenter)
                        if(self.role == 'Student'):
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
                        self.teacherInfoTable.setItem(row_num, col_num, item)

            connection.close()

            self.loadLabInfo()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}", QMessageBox.Ok)

    def loadLabInfo(self):
        self.labInfoTable.setRowCount(0)
        try:
            connection = sqlite3.connect('theirdatabase.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            timetable_data = cursor.fetchall()

            for row_data in timetable_data:
                row_num = self.labInfoTable.rowCount()
                self.labInfoTable.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setTextAlignment(Qt.AlignCenter)
                    if(self.role == 'Student'):
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
                    self.labInfoTable.setItem(row_num, col_num, item)
            
            connection.close()
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}", QMessageBox.Ok)



class LoginWindow(QDialog):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'{self.role} Login')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #f5f5f5; border: 2px solid #dddddd; border-radius: 10px;")
        self.resize(600, 400)

        layout = QVBoxLayout()

        logo = QLabel()
        logo.setPixmap(QPixmap('download.jpg').scaled(300, 370, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("QLineEdit { padding: 10px; border: 1px solid #cccccc; border-radius: 5px; }")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("QLineEdit { padding: 10px; border: 1px solid #cccccc; border-radius: 5px; }")

        login_button = QPushButton('Login')
        login_button.setStyleSheet("QPushButton { background-color: #3b5998; color: white; border: none; padding: 10px 24px; "
                                   "text-align: center; text-decoration: none; display: inline-block; font-size: 16px; "
                                   "margin: 4px 2px; cursor: pointer; border-radius: 8px; }"
                                   "QPushButton:hover { background-color: #2e477a; }"
                                   "QPushButton:pressed { background-color: #253960; }")
        login_button.clicked.connect(self.handleLogin)

        self.error_label = QLabel('')
        self.error_label.setStyleSheet("color: blue; font-size : 18px")
        self.error_label.setAlignment(Qt.AlignCenter)

        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)
        layout.addLayout(form_layout)
        layout.addWidget(login_button)
        layout.addWidget(self.error_label)
        self.setLayout(layout)

    def handleLogin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.role == 'Admin':
            if username == 'admin' and password == 'ssn':
                self.accept()
            else:
                self.error_label.setText('Incorrect username or password.')

class StaffLoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Staff Login')
        layout = QVBoxLayout()
        self.label = QLabel('Enter Teacher Code:')
        self.line_edit = QLineEdit()
        self.button = QPushButton('Submit')

        connection = sqlite3.connect('newdatabase.db')
        cursor = connection.cursor()
        cursor.execute("SELECT staff_code FROM MON ")

        staff_names=cursor.fetchall()
        self.staff_names=[part[0] for part in staff_names]
        connection.close()
        
        self.button.clicked.connect(self.submitTeacherCode)
        
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
    def submitTeacherCode(self):
        self.teacher_code = self.line_edit.text()
        if self.teacher_code in self.staff_names:
            self.accept()
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid teacher code.')

class StaffTimetableWindow(QWidget):
    def __init__(self, teacher_code):
        super().__init__()
        self.teacher_code = teacher_code
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Timetable for Teacher Code: {self.teacher_code}')
        self.resize(1200, 800) 
        layout = QVBoxLayout()
        

        connection = sqlite3.connect('newdatabase.db')
        cursor = connection.cursor()

        cursor.execute(f"SELECT name FROM MON WHERE staff_code=?", (self.teacher_code,))
        title=QLabel(cursor.fetchone()[0]+"'s Timetable")
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)


        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        self.table = QTableWidget()
        self.table.setRowCount(len(days))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 'Hour 7'])
        self.table.setVerticalHeaderLabels(days)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("QTableWidget { background-color: white; border: 1px solid #cccccc; border-radius: 5px; }"
                                       "QHeaderView::section { background-color: #3b5998; color: white; border-radius: 5px; }")


        for i, day in enumerate(days):
            cursor.execute(f"SELECT * FROM {day} WHERE staff_code=?", (self.teacher_code,))
            row = cursor.fetchone()
            if row:
                for j in range(7):
                    self.table.setItem(i, j, QTableWidgetItem(row[j+3]))  # skipping the first column (teacher_code)

        connection.close()

        layout.addWidget(self.table)
        self.setLayout(layout)

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Time Table Generator')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(1200, 500)
        image = QLabel(self)
        image.setScaledContents(True)
        image.setPixmap(QPixmap("goodimage.jpg"))

        layout = QVBoxLayout(image)
        self.stackedWidget = QStackedWidget()

        layout1widget = QWidget()
        layout1 = QVBoxLayout()

        title = QLabel('Select Your Role')
        title.setFont(QFont('Arial', 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout1.addWidget(title)

        role_buttons = ['Student', 'Staff', 'Admin']
        button_layout = QHBoxLayout()
        for role in role_buttons:
            button = QPushButton(role)
            button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; padding: 15px 30px; "
                                 "text-align: center; text-decoration: none; display: inline-block; font-size: 18px; "
                                 "margin: 10px; cursor: pointer; border-radius: 10px; }"
                                 "QPushButton:hover { background-color: #2e477a; }"
                                 "QPushButton:pressed { background-color: #253960; }")
            button.clicked.connect(lambda _, r=role: self.handleRoleSelection(r))
            button_layout.addWidget(button)

        layout1.addLayout(button_layout)
        layout1widget.setLayout(layout1)

        layout2widget = QWidget()
        layout2 = QVBoxLayout()
        title = QLabel('Class Timetables')
        title.setFont(QFont('Arial', 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout2.addWidget(title)

        connection = sqlite3.connect('yourdatabase.db')
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        connection.close()

        timetable_names = [table[0] for table in tables]
        self.windows = {}

        labels = ['Class' + str(i + 1) for i in range(len(timetable_names))]
        button_layout2 = QHBoxLayout()
        for name, label in zip(timetable_names, labels):
            button = QPushButton(name)
            button.setStyleSheet("QPushButton { background-color: #3b5998; color: white; border: none; padding: 15px 30px; "
                                 "text-align: center; text-decoration: none; display: inline-block; font-size: 18px; "
                                 "margin: 10px; cursor: pointer; border-radius: 10px; }"
                                 "QPushButton:hover { background-color: #2e477a; }"
                                 "QPushButton:pressed { background-color: #253960; }")
            button.clicked.connect(lambda _, n=name, l=label: self.openTimetableWindow(n, l))
            button_layout2.addWidget(button)

        layout2.addLayout(button_layout2)
        layout2widget.setLayout(layout2)

        self.stackedWidget.addWidget(layout1widget)
        self.stackedWidget.addWidget(layout2widget)

        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
        self.setCentralWidget(image)

    def switchLayout(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def openTimetableWindow(self, table_name, label_text):
        if table_name not in self.windows:
            window = TimetableWindow(table_name, label_text, self.role)
            self.windows[table_name] = window
        self.windows[table_name].show()
        self.switchLayout(0)

    def handleRoleSelection(self, role):
        self.role = role
        if role == 'Admin':
            loginWindow = LoginWindow(role)
            if loginWindow.exec_() == QDialog.Accepted:
                self.switchLayout(1)
        elif role == 'Staff':
            staffLoginWindow = StaffLoginWindow()
            if staffLoginWindow.exec_() == QDialog.Accepted:
                teacher_code = staffLoginWindow.teacher_code
                self.staffTimetableWindow = StaffTimetableWindow(teacher_code)
                self.staffTimetableWindow.show()
        else:
            self.switchLayout(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())
