from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QListWidget, QListView, QLabel
from vars import widget, COLORS
from helpers import send_dict, show_list
import os


class Room(QWidget):
    """
    Class which show the gui of a chat room
    user: username, sock: socket connection, room: room name, listener: thread to handle server messages
    """

    def __init__(self, user: str, sock, room: str, listener):
        # creating window
        super().__init__()
        widget.setWindowTitle("Room")
        widget.setStyleSheet(f"background-color: {COLORS['background-green']};")
        font = QFont()
        self.socket = sock
        self.room = room
        self.user = user

        # start the thread
        self.thread = listener
        self.thread.list_room_signal.connect(self.update_list)
        self.thread.msg_signal.connect(self.add_message)
        self.thread.start()

        # labels
        self.welcome = QLabel(self)
        self.welcome.setGeometry(QRect(10, 30, 300, 31))
        font.setPointSize(20)
        self.welcome.setFont(font)
        self.welcome.setText(f"Welcome {user}!")
        self.welcome.setAlignment(QtCore.Qt.AlignCenter)

        self.label_room = QLabel(self)
        self.label_room.setGeometry(QRect(440, 30, 180, 31))
        self.label_room.setFont(font)
        self.label_room.setText(f"{self.room} room")

        font.setPointSize(16)
        self.label_participants = QLabel(self)
        self.label_participants.setGeometry(QRect(60, 160, 120, 41))
        self.label_participants.setFont(font)
        self.label_participants.setText("participants")

        # images
        path = os.path.dirname(os.path.abspath(__file__))
        icon = QtGui.QIcon()
        self.Sport = QtWidgets.QPushButton(self)
        self.Sport.setGeometry(QRect(10, 80, 83, 65))
        self.Sport.clicked.connect(lambda: self.change_room("Sport"))
        self.Sport.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon.addPixmap(QtGui.QPixmap(f"{path}/files/football.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.Sport.setIcon(icon)
        self.Sport.setIconSize(QtCore.QSize(83, 65))
        self.Sport.setFlat(True)

        icon1 = QtGui.QIcon()
        self.gaming = QtWidgets.QPushButton(self)
        self.gaming.setGeometry(QRect(88, 80, 66, 66))
        self.gaming.clicked.connect(lambda: self.change_room("Gaming"))
        self.gaming.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon1.addPixmap(QtGui.QPixmap(f"{path}/files/gaming.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.gaming.setIcon(icon1)
        self.gaming.setIconSize(QtCore.QSize(66, 66))
        self.gaming.setFlat(True)

        icon2 = QtGui.QIcon()
        self.cooking = QtWidgets.QPushButton(self)
        self.cooking.setGeometry(QRect(160, 80, 80, 70))
        self.cooking.clicked.connect(lambda: self.change_room("Cooking"))
        self.cooking.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon2.addPixmap(QtGui.QPixmap(f"{path}/files/cooking.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cooking.setIcon(icon2)
        self.cooking.setIconSize(QtCore.QSize(80, 70))
        self.cooking.setFlat(True)

        icon3 = QtGui.QIcon()
        self.button_back = QtWidgets.QPushButton(self)
        self.button_back.setGeometry(QRect(20, 500, 70, 70))
        self.button_back.clicked.connect(self.lobby)
        self.button_back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon3.addPixmap(QtGui.QPixmap(f'{path}/files/back.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.button_back.setIcon(icon3)
        self.button_back.setIconSize(QtCore.QSize(70, 70))
        self.button_back.setFlat(True)

        icon3 = QtGui.QIcon()
        self.button_send = QtWidgets.QPushButton(self)
        self.button_send.setGeometry(QRect(660, 495, 100, 46))
        self.button_send.clicked.connect(self.send_message)
        self.button_send.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        icon3.addPixmap(QtGui.QPixmap(f'{path}/files/send.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.button_send.setIcon(icon3)
        self.button_send.setIconSize(QtCore.QSize(100, 46))
        self.button_send.setFlat(True)

        # lists
        self.list_participants = QListView(self)
        self.list_participants.setGeometry(QRect(20, 220, 200, 240))
        self.list_participants.setStyleSheet("background-color: #ECE5DD;")

        font.setPointSize(13)
        self.list_chat = QListWidget(self)
        self.list_chat.setGeometry(QRect(300, 100, 450, 360))
        self.list_chat.setStyleSheet("background-color: #F9F3DF;")
        self.list_chat.setFont(font)
        self.list_chat.setWordWrap(True)

        self.enter_line = QtWidgets.QLineEdit(self)
        self.enter_line.setFont(font)
        self.enter_line.setGeometry(QtCore.QRect(300, 500, 350, 35))
        self.enter_line.setStyleSheet("background-color: #F9F3DF;")

    # update a new list of participants to gui
    def update_list(self, new_message):
        show_list(self.list_participants, new_message[self.room])

    # add message to gui
    def add_message(self, new_message):
        self.list_chat.addItem(QListWidgetItem(new_message['message']))

    # move to lobby
    def lobby(self):
        self.leave_room()
        send_dict({"cmd": "lobby"}, self.socket)
        widget.setCurrentIndex(widget.currentIndex() - 1)

    # change to another room - messages to server
    def change_room(self, name):
        self.leave_room()
        data = {
            "cmd": "join room",
            "name": name,
            "user": self.user
        }
        send_dict(data, self.socket)
        self.update_room(name)

    # change to another room - gui
    def update_room(self, name):
        self.room = name
        self.label_room.setText(f"{self.room} room")
        self.list_chat.clear()
        self.list_participants.reset()

    # send message to room and update your gui
    def send_message(self):
        data = f"{self.enter_line.text()}".strip()
        if data != "":
            msg = QListWidgetItem(f"{self.user}: {data}")
            msg.setBackground(QColor('#b3e5fc'))
            self.list_chat.addItem(msg)
            to_send = {
                'cmd': "message",
                'name': self.room,
                'message': f"{self.user}: {data}"
            }
            send_dict(to_send, self.socket)
        self.enter_line.clear()

    def leave_room(self):
        data = {
            "cmd": "leave room",
            "name": self.room,
            "user": self.user
        }
        send_dict(data, self.socket)
