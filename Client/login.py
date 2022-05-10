from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget

from screens import change_window
from vars import COLORS
from listener import Listener
from helpers import send_dict, receive_dict
from popup import pop_up_message
from vars import widget


class LOG_IN(QWidget):
    """
    Class which show the gui of login page
    sock: socket connection
    """
    def __init__(self, sock, windows: dict):
        super().__init__()

        # set the title and color
        widget.setWindowTitle("Log In")
        widget.setStyleSheet(f"background-color: {COLORS['background-green']};")
        self.socket = sock
        self.data = {}
        self.windows = windows

        # login label
        self.login_label = QtWidgets.QLabel(self)
        self.login_label.setGeometry(QtCore.QRect(350, 70, 110, 40))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.login_label.setFont(font)
        self.login_label.setText("Log In")

        # edit lines
        self.user_edit = QtWidgets.QLineEdit(self)
        font.setPointSize(12)
        self.user_edit.setFont(font)
        self.user_edit.setGeometry(QtCore.QRect(290, 160, 230, 35))
        self.user_edit.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.user_edit.setPlaceholderText("User Name")
        self.user_edit.setAlignment(QtCore.Qt.AlignCenter)

        self.pass_edit = QtWidgets.QLineEdit(self)
        self.pass_edit.setFont(font)
        self.pass_edit.setGeometry(QtCore.QRect(290, 240, 230, 35))
        self.pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_edit.setStyleSheet("border: 2px solid; border-radius:10px; background-color: palette(base); ")
        self.pass_edit.setPlaceholderText("Password")
        self.pass_edit.setAlignment(QtCore.Qt.AlignCenter)

        # log-in button
        self.Button_login = QtWidgets.QPushButton(self)
        self.Button_login.setGeometry(QtCore.QRect(250, 340, 141, 41))
        self.Button_login.setFont(font)
        self.Button_login.setStyleSheet(fr"background-color: {COLORS['buttons']};")
        self.Button_login.clicked.connect(self.login)
        self.Button_login.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Button_login.setText("Log In")

        # sign-up button
        self.Button_sign = QtWidgets.QPushButton(self)
        self.Button_sign.setGeometry(QtCore.QRect(430, 340, 141, 41))
        self.Button_sign.setFont(font)
        self.Button_sign.setStyleSheet(f"background-color: {COLORS['buttons']};")
        self.Button_sign.clicked.connect(self.signup_page)
        self.Button_sign.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.Button_sign.setText("Sign Up")

        # forgot pass
        self.button_forgot = QtWidgets.QPushButton(self)
        self.button_forgot.setGeometry(QtCore.QRect(310, 420, 190, 41))
        font.setPointSize(16)
        self.button_forgot.setFont(font)
        self.button_forgot.setStyleSheet(f"border-radius: 10px;color: #34B7F1;")  # change to label
        self.button_forgot.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button_forgot.clicked.connect(self.forgot_pass)
        self.button_forgot.setText("Forgot Password?")

        # show all the widgets
        self.login_label.setFocus()

    # move pages
    def forgot_pass(self):
        change_window("forgot", self.windows, self.socket, self.windows)

    def signup_page(self):
        change_window("signup", self.windows, self.socket, self.windows)

    # try to log in and act according to the response
    def login(self):
        self.data = {
            "cmd": "login",
            "userID": self.user_edit.text(),
            "pass": self.pass_edit.text()
        }
        send_dict(self.data, self.socket)

        my_dict = receive_dict(self.socket)
        if my_dict['cmd'] == 'error':
            pop_up_message(self.socket, my_dict['message'], 'error')
        else:
            handle_server = Listener(self.socket)
            handle_server.start()
            change_window("lobby", self.windows, self.data["userID"], self.socket, handle_server, self.windows)
            send_dict({"cmd": "lobby"}, self.socket)
