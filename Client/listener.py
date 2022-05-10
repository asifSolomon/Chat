from PyQt5 import QtCore
from helpers import receive_dict
from popup import offline


class Listener(QtCore.QThread):
    """
    Thread is used to listen to the server via socket
    The thread call to function in order to update the gui
    """
    msg_signal = QtCore.pyqtSignal(dict)
    list_lobby_signal = QtCore.pyqtSignal(dict)
    list_room_signal = QtCore.pyqtSignal(dict)

    def __init__(self, sock):
        super(Listener, self).__init__()
        self.socket = sock
        self.done = False

    def run(self):
        while not self.done:
            try:
                data = receive_dict(self.socket)
                if data['cmd'] == "participants_lobby":
                    self.list_lobby_signal.emit(data)
                elif data['cmd'] == 'participants_room':
                    self.list_room_signal.emit(data)
                elif data['cmd'] == 'message':
                    self.msg_signal.emit(data)
                else:
                    print("error")

            except (ConnectionAbortedError, ConnectionResetError):
                offline(self.socket)
                self.done = True
