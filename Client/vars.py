import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

# constants
IP = "127.0.0.1"
PORT = 8200
COLORS = {  # https://www.schemecolor.com/whatsapp-2.php
    "background-green": "#DCF8C6",
    "buttons": "#25D366",
    "list": "#ECE5DD"
}
WIDTH = 800
HEIGHT = 600


# create pyqt5 app
App = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()