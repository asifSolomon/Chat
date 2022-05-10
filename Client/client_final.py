#  chat - client side
#  Author: Solomon Asif
import sys
import socket
from vars import widget, WIDTH, HEIGHT, App, IP, PORT
from forgot import Forgot
from lobby import Lobby
from signup import SIGN_UP
from login import LOG_IN
from room import Room
from popup import offline

windows = {"login": LOG_IN,
           "forgot": Forgot,
           "lobby": Lobby,
           "signup": SIGN_UP,
           "room": Room}


def gui(sock):
    # create the instance of our Window
    window = LOG_IN(sock, windows)

    # setting  the fixed sizes of window
    widget.setFixedWidth(WIDTH)
    widget.setFixedHeight(HEIGHT)

    widget.addWidget(window)
    widget.show()
    window.login_label.setFocus()

    # start the app
    sys.exit(App.exec())


# run the client
def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        print('Connected to server\n')

        # GUI
        gui(my_socket)
    except ConnectionRefusedError:
        offline(my_socket)


if __name__ == '__main__':
    main()
