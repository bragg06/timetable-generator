from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
import warnings 

warnings.filterwarnings("ignore", message="Unknown property")
warnings.filterwarnings("ignore", message="Unknown DisplayS")

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Admin Login')
        self.setStyleSheet("background-color: #ECEFF1; border: 2px solid #B0BEC5;")
        self.setFixedSize(900, 200)

        # Main vertical layout
        mlayout = QVBoxLayout()
        
        # Title label
        title = QLabel('Admin Login')
        title.setFont(QFont('Arial', 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("border: none;")  # Ensure no border for the title
        mlayout.addWidget(title)

        # Form layout for username and password fields
        layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login button with styles
        login_button = QPushButton('Login')
        login_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; padding: 10px 24px; "
                                   "text-align: center; text-decoration: none; display: inline-block; font-size: 16px; "
                                   "margin: 4px 2px; cursor: pointer; border-radius: 8px; }"
                                   "QPushButton:hover { background-color: #45a049; }"
                                   "QPushButton:pressed { background-color: #388E3C; }")
        login_button.clicked.connect(self.handleLogin)

        # Add username and password fields and login button to the form layout
        layout.addRow('Username:', self.username_input)
        layout.addRow('Password:', self.password_input)
        layout.addWidget(login_button)

        # Add the form layout to the main layout
        mlayout.addLayout(layout)

        # Set the main layout for the dialog
        self.setLayout(mlayout)

    def handleLogin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == 'admin' and password == 'ssn':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Incorrect username or password.')
class SubjectsWindow(QDialog):
    def __init__(self,room,staffs):
        super().__init__()
        self.room=room 
        self.staffs=staffs
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.room)
        self.setStyleSheet("background-color: #ECEFF1; border: 2px solid #B0BEC5;")
        self.resize(500, 250)

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.sections=[]
        for i in self.staffs:
            combo_box = QComboBox(self)
            k=self.staffs.index(i)
            if k in (0,1,2):
                combo_box.addItems([key for key in subjects if key.startswith("ICS")])
            elif k==3:
                combo_box.addItems([key for key in subjects if key.startswith("IMA")])
            elif k==4:
                combo_box.addItems([key for key in subjects if key.startswith("IPH")])
            else:
                combo_box.addItems([key for key in subjects if key.startswith("LCS")])
            self.sections.append(combo_box)
            form_layout.addRow(f'Subject for {i}:', combo_box)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def getInput(self):
        sections_text = [combo.currentText() for combo in self.sections]
        sub_text=[subjects[bocom] for bocom in sections_text]
        return sections_text,sub_text
 
class RoomsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rooms')
        self.setStyleSheet("background-color: #ECEFF1; border: 2px solid #B0BEC5;")
        self.resize(300, 150)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.room_count = QSpinBox()
        self.room_count.setMinimum(1)
        self.room_count.setMaximum(6)
        form_layout.addRow('Number of Rooms:', self.room_count)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def accept(self):
        room_count = self.room_count.value()
        # Here you would typically save the room count to the database or use it as needed
        print(f'Number of rooms: {room_count}')
        super().accept()

    def getInput(self):
        # Store the selected value from the spin box
        selected_value = self.room_count.value()
        sections=[]
        for i in range (selected_value):
            sections.append('r4'+str(i))
        return sections

subjects={'ICS1023':"Problem solving and programming in Python",'ICS1011':"Problem solving an dprogramming in C",
          'ICS1111':"Digital System Design",'ICS1108':"Computer Organization and Architecture",'ICS1100':"Data Science",
          'ICS1007':"Unix and shell Programming",'ICS1079':"Java programming",'ICS1099':"Web Developement",
          'IMA1001':"Matrices and Application Of Calculus",'IMA1009':"Complex numbers and Laplace Corretion",
          'IMA1005':"Discrete4 Mathematics",'IMA1003':"Probability and Statistical Technique",
          'IPH1549':"Basics of Eletronics",'IPH1577':"Physics for Information Science",'IPH1501':"Classical Mechanics",
          'LCS9009':"Programming in python Lab",'LCS9034':"Java programming lab",'LCS9056':"Web Developement Lab",
          'LCS9066':"Unix and Shell Programming Lab",'LCS9001':"Programming in C Lab"}

def getsubjects(room,staff):
    app = QApplication(sys.argv)
    window=SubjectsWindow(room,staff)
    window.show()
    app.exec_()
    return window.getInput()  # Return the input after the dialog is closed

def getrooms():
    app = QApplication(sys.argv)
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        window=RoomsWindow()
        window.show()
        app.exec_()
        return window.getInput()




