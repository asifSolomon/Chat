from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QRegExp, QDateTime
from PyQt5.QtGui import QCursor, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QDateEdit

from screens import change_window
from popup import pop_up_message
from vars import widget, COLORS
from helpers import send_dict, receive_dict


class SIGN_UP(QWidget):
    """
    Class which show the gui of a signup page
    user: sock: socket connection
    """

    def __init__(self, sock, windows: dict):
        super().__init__()

        # set the title and color
        widget.setWindowTitle("Sign up")
        widget.setStyleSheet(f"background-color: {COLORS['background-green']};")

        self.windows = windows
        self.socket = sock
        self.data = {}

        # To allow only int
        self.onlyInt = QIntValidator()

        # To allow only letters
        regex_letters = QRegExp(r"['a-zA-Z']+")
        validator_letters = QRegExpValidator(regex_letters, self)

        # sign up label
        self.signup_label = QtWidgets.QLabel(self)
        self.signup_label.setGeometry(QtCore.QRect(345, 70, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.signup_label.setFont(font)
        self.signup_label.setText("Sign up")

        # edit lines
        self.user_name = QtWidgets.QLineEdit(self)
        font.setPointSize(12)
        self.user_name.setFont(font)
        self.user_name.setGeometry(QtCore.QRect(150, 140, 200, 35))
        self.user_name.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.user_name.setPlaceholderText("User Name")
        self.user_name.setAlignment(QtCore.Qt.AlignCenter)

        self.email = QtWidgets.QLineEdit(self)
        self.email.setFont(font)
        self.email.setGeometry(QtCore.QRect(150, 200, 200, 35))
        self.email.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.email.setPlaceholderText("Email")
        self.email.setAlignment(QtCore.Qt.AlignCenter)

        self.pass_line = QtWidgets.QLineEdit(self)
        self.pass_line.setFont(font)
        self.pass_line.setGeometry(QtCore.QRect(150, 260, 200, 35))
        self.pass_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_line.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.pass_line.setPlaceholderText("Password")
        self.pass_line.setAlignment(QtCore.Qt.AlignCenter)

        # confirm pass
        self.pass_con = QtWidgets.QLineEdit(self)
        self.pass_con.setFont(font)
        self.pass_con.setGeometry(QtCore.QRect(450, 260, 200, 35))
        self.pass_con.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_con.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.pass_con.setPlaceholderText("Confirm Password")
        self.pass_con.setAlignment(QtCore.Qt.AlignCenter)

        self.first_name = QtWidgets.QLineEdit(self)
        self.first_name.setFont(font)
        self.first_name.setGeometry(QtCore.QRect(450, 140, 200, 35))
        self.first_name.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.first_name.setPlaceholderText("First Name")
        self.first_name.setAlignment(QtCore.Qt.AlignCenter)
        self.first_name.setValidator(validator_letters)

        self.last_name = QtWidgets.QLineEdit(self)
        self.last_name.setFont(font)
        self.last_name.setGeometry(QtCore.QRect(450, 200, 200, 35))
        self.last_name.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.last_name.setPlaceholderText("Last Name")
        self.last_name.setAlignment(QtCore.Qt.AlignCenter)
        self.last_name.setValidator(validator_letters)

        # phone label
        self.phone_label = QtWidgets.QLabel(self)
        self.phone_label.setGeometry(QtCore.QRect(190, 310, 130, 20))
        self.phone_label.setFont(font)
        self.phone_label.setText("Phone Number")

        self.phone_num = QtWidgets.QLineEdit(self)
        self.phone_num.setFont(font)
        self.phone_num.setGeometry(QtCore.QRect(150, 340, 200, 35))
        self.phone_num.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.phone_num.setPlaceholderText("Phone")
        self.phone_num.setAlignment(QtCore.Qt.AlignCenter)
        self.phone_num.setValidator(self.onlyInt)

        # birth label
        self.birth_label = QtWidgets.QLabel(self)
        self.birth_label.setGeometry(QtCore.QRect(510, 310, 90, 20))
        self.birth_label.setFont(font)
        self.birth_label.setText("Birth Date")

        self.date_edit = QDateEdit(self)
        self.date_edit.setGeometry(QtCore.QRect(450, 340, 200, 35))
        self.date_edit.setFont(font)
        self.date_edit.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.date_edit.setAlignment(QtCore.Qt.AlignCenter)
        d = QDateTime().currentDateTime()
        self.date_edit.setMaximumDateTime(d)

        # sign-up button
        self.Button_sign = QtWidgets.QPushButton(self)
        self.Button_sign.setGeometry(QtCore.QRect(330, 400, 141, 41))
        self.Button_sign.setFont(font)
        self.Button_sign.setStyleSheet(f"background-color: {COLORS['buttons']};")
        self.Button_sign.clicked.connect(self.signup)
        self.Button_sign.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Button_sign.setText("Sign Up")

        # have account?
        self.have_account = QtWidgets.QPushButton(self)
        self.have_account.setGeometry(QtCore.QRect(260, 470, 280, 41))
        font.setPointSize(16)
        self.have_account.setFont(font)
        self.have_account.setStyleSheet(f"border-radius: 10px;color: #34B7F1;")  # change to label
        self.have_account.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.have_account.clicked.connect(self.login_page)
        self.have_account.setText("Already have an account?")

        # show all the widget's placeholders
        self.signup_label.setFocus()

    def login_page(self):
        change_window("login", self.windows, self.socket, self.windows)

    # request to sign up and receive answer from server
    def signup(self):
        self.data = {
            "cmd": "signup",
            "userID": self.user_name.text(),
            "pass": self.pass_line.text(),
            "confirm": self.pass_con.text(),
            "email": self.email.text(),
            "first name": self.first_name.text(),
            "last name": self.last_name.text(),
            "phone": self.phone_num.text(),
            "Bdate": self.date_edit.text()
        }

        send_dict(self.data, self.socket)
        my_dict = receive_dict(self.socket)
        pop_up_message(self.socket, my_dict['message'], my_dict['cmd'])
