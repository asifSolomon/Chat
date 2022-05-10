from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QCursor, QIntValidator
from PyQt5.QtWidgets import QWidget
from helpers import send_dict, receive_dict
from popup import pop_up_message
from screens import change_window
from vars import COLORS, widget



class Forgot(QWidget):
    """
    Class which show the gui of forgot password page
    sock: socket connection
    """
    def __init__(self, sock, windows: dict):
        super().__init__()
        self.socket = sock
        self.windows = windows

        # To allow only int
        self.onlyInt = QIntValidator()

        # set the title and color
        widget.setWindowTitle("Forgot password")
        widget.setStyleSheet(f"background-color: {COLORS['background-green']};")

        # forgot password label
        self.forgot_label = QtWidgets.QLabel(self)
        self.forgot_label.setGeometry(QtCore.QRect(270, 70, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.forgot_label.setFont(font)
        self.forgot_label.setText("Forgot password")

        # edit lines
        self.email_edit = QtWidgets.QLineEdit(self)
        font.setPointSize(12)
        self.email_edit.setFont(font)
        self.email_edit.setGeometry(QtCore.QRect(290, 170, 230, 35))
        self.email_edit.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setAlignment(QtCore.Qt.AlignCenter)

        self.pass_edit = QtWidgets.QLineEdit(self)
        self.pass_edit.setFont(font)
        self.pass_edit.setGeometry(QtCore.QRect(290, 240, 230, 35))
        self.pass_edit.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.pass_edit.setPlaceholderText("New Password")
        self.pass_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_edit.hide()

        self.code_edit = QtWidgets.QLineEdit(self)
        self.code_edit.setFont(font)
        self.code_edit.setGeometry(QtCore.QRect(290, 310, 230, 35))
        self.code_edit.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.code_edit.setPlaceholderText("Enter code from email")
        self.code_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.code_edit.setValidator(self.onlyInt)
        self.code_edit.hide()

        # reset and change password button
        self.reset_pwd = QtWidgets.QPushButton(self)
        self.reset_pwd.setGeometry(QtCore.QRect(330, 380, 141, 41))
        self.reset_pwd.setFont(font)
        self.reset_pwd.setStyleSheet(f"background-color: {COLORS['buttons']};")
        self.reset_pwd.clicked.connect(self.reset)
        self.reset_pwd.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.reset_pwd.setText("Reset Pass")

        self.change_pwd = QtWidgets.QPushButton(self)
        self.change_pwd.setGeometry(QtCore.QRect(330, 380, 141, 41))
        self.change_pwd.setFont(font)
        self.change_pwd.setStyleSheet(f"background-color: {COLORS['buttons']};")
        self.change_pwd.clicked.connect(self.change)
        self.change_pwd.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.change_pwd.setText("Change Pass")
        self.change_pwd.hide()

        # back to log in
        self.have_account = QtWidgets.QPushButton(self)
        self.have_account.setGeometry(QtCore.QRect(260, 470, 280, 41))
        font.setPointSize(16)
        self.have_account.setFont(font)
        self.have_account.setStyleSheet(f"border-radius: 10px;color: #34B7F1;")  # change to label
        self.have_account.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.have_account.clicked.connect(self.login_page)
        self.have_account.setText("Back to log in")

    def login_page(self):
        change_window("login", self.windows, self.socket, self.windows)

    # ask for getting code to email and check the response
    def reset(self):
        data = {
            "cmd": "forgot",
            "email": self.email_edit.text()
        }
        send_dict(data, self.socket)

        my_dict = receive_dict(self.socket)
        if my_dict['cmd'] == 'success':
            self.change_pwd.show()
            self.reset_pwd.hide()
            self.code_edit.show()
            self.pass_edit.show()
        else:
            pop_up_message(self.socket, my_dict['message'], my_dict['cmd'])

    # ask for changing password using the code and check the response
    def change(self):
        try:
            code = int(self.code_edit.text())
        except ValueError:
            code = -1

        data = {
            "cmd": "change",
            "email": self.email_edit.text(),
            "new_pass": self.pass_edit.text(),
            "code": code
        }
        send_dict(data, self.socket)
        my_dict = receive_dict(self.socket)
        pop_up_message(self.socket, my_dict['message'], my_dict['cmd'])
