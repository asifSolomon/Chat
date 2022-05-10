import os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QListView

from screens import change_window
from vars import widget, COLORS
from helpers import send_dict, show_list


class Lobby(QWidget):
    """
    Class which show the gui of login page
    has_room(bool): already created room, user: username
    sock: socket connection, listener: thread to handle server messages
    """
    has_room = False

    def __init__(self, user, sock, listener, windows: dict):
        # creating window
        super().__init__()
        widget.setWindowTitle("Lobby")
        widget.setStyleSheet(f"background-color: {COLORS['background-green']};")
        font = QFont()
        self.socket = sock
        self.user = user
        self.windows = windows

        self.thread = listener
        self.thread.list_lobby_signal.connect(self.update_list)
        # maybe next line unnecessary
        self.thread.start()

        # labels
        self.welcome = QLabel(self)
        self.welcome.setGeometry(QRect(250, 50, 300, 31))
        font.setPointSize(24)
        self.welcome.setFont(font)
        self.welcome.setText(f"Welcome {user}!")
        self.welcome.setAlignment(QtCore.Qt.AlignCenter)

        self.label_gaming = QLabel(self)
        self.label_gaming.setGeometry(QRect(355, 130, 91, 41))
        font.setPointSize(18)
        self.label_gaming.setFont(font)
        self.label_gaming.setText("Gaming")

        self.label_cooking = QLabel(self)
        self.label_cooking.setGeometry(QRect(565, 130, 91, 41))
        self.label_cooking.setFont(font)
        self.label_cooking.setText("Cooking")

        self.label_sport = QLabel(self)
        self.label_sport.setGeometry(QRect(160, 130, 91, 41))
        self.label_sport.setFont(font)
        self.label_sport.setText("Sport")

        # images
        path = os.path.dirname(os.path.abspath(__file__))
        icon = QtGui.QIcon()
        self.Sport = QtWidgets.QPushButton(self)
        self.Sport.setGeometry(QRect(95, 180, 180, 142))
        self.Sport.clicked.connect(lambda: self.choose_room("Sport"))
        self.Sport.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon.addPixmap(QtGui.QPixmap(f"{path}/files/football.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.Sport.setIcon(icon)
        self.Sport.setIconSize(QtCore.QSize(180, 142))
        self.Sport.setFlat(True)

        icon1 = QtGui.QIcon()
        self.gaming = QtWidgets.QPushButton(self)
        self.gaming.setGeometry(QRect(320, 180, 145, 145))
        self.gaming.clicked.connect(lambda: self.choose_room("Gaming"))
        self.gaming.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon1.addPixmap(QtGui.QPixmap(f"{path}/files/gaming.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.gaming.setIcon(icon1)
        self.gaming.setIconSize(QtCore.QSize(145, 145))
        self.gaming.setFlat(True)

        icon2 = QtGui.QIcon()
        self.cooking = QtWidgets.QPushButton(self)
        self.cooking.setGeometry(QRect(525, 180, 170, 151))
        self.cooking.clicked.connect(lambda: self.choose_room("Cooking"))
        self.cooking.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon2.addPixmap(QtGui.QPixmap(f"{path}/files/cooking.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cooking.setIcon(icon2)
        self.cooking.setIconSize(QtCore.QSize(170, 151))
        self.cooking.setFlat(True)

        # lists
        self.list_sport = QListView(self)
        self.list_sport.setGeometry(QRect(110, 340, 151, 241))
        self.list_sport.setStyleSheet(f"background-color: {COLORS['list']};")

        self.list_gaming = QListView(self)
        self.list_gaming.setGeometry(QRect(320, 340, 151, 241))
        self.list_gaming.setStyleSheet(f"background-color: {COLORS['list']};")

        self.list_cooking = QListView(self)
        self.list_cooking.setGeometry(QRect(530, 340, 151, 241))
        self.list_cooking.setStyleSheet(f"background-color: {COLORS['list']};")

    # update gui to the participants lists
    def update_list(self, new_message):
        show_list(self.list_cooking, new_message["Cooking"])
        show_list(self.list_sport, new_message["Sport"])
        show_list(self.list_gaming, new_message["Gaming"])

    # choose room from the gui, if it is the firs one - need to create a room
    def choose_room(self, name):
        data = {"cmd": "leave lobby"}
        send_dict(data, self.socket)
        data = {
            "cmd": "join room",
            "name": name,
            "user": self.user
        }
        send_dict(data, self.socket)

        if not Lobby.has_room:
            Lobby.has_room = True
            change_window("room", self.windows, self.user, self.socket, name, self.thread)
        else:
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.currentWidget().update_room(name)
