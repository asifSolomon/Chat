from PyQt5.QtWidgets import QListView, QAbstractItemView, QMessageBox
from rsa import PublicKey, encrypt
import json
import struct
from PyQt5 import QtGui

PUBLIC_KEY = PublicKey(21468076645486133110101681660848174169977541474881806070386243630607550580212210745616607307584702551667153667157302483069777014721221096663089299718499811557525040158962145641647261885038361956799811745241630622072752177876850700896870068138710850226518977702040727250262787167847250335581993423535963729467533243082882348091712066559825205959901346610468582139308514862652246395700578834581357207133645241332554642217799849263694027458313483990467369164577145341374211290264974506899269954350664907069592686245748724376398670858203099738699024653890435890132247061753219194915753562714847138046050501985940129140709, 65537)


def show_list(list_name: QListView, participants: list):
    """
    update QListView to the list of participants
    """
    list_name.reset()
    model = QtGui.QStandardItemModel()
    list_name.setModel(model)
    font = QtGui.QFont()
    font.setPointSize(14)
    list_name.setFont(font)
    for i in participants:
        item = QtGui.QStandardItem(str(i))
        model.appendRow(item)

    list_name.setEditTriggers(QAbstractItemView.NoEditTriggers)


def send_dict(my_dict, sock):
    """
    Send dictionary using socket
    First 8 bytes are the length of the message.
    The message is encrypted using rsa public and private key
    """
    try:
        data = json.dumps(my_dict).encode()
        data = encrypt(data, PUBLIC_KEY)
        msg = struct.pack('>Q', len(data)) + data
        sock.send(msg)
    except ConnectionResetError:
        offline(sock)


def receive_dict(sock):
    """
    Receive dictionary using socket
    First 8 bytes are the length of the message
    """
    try:
        data = recv_msg(sock).decode()
        try:
            dict_data = json.loads(data)
            return dict_data
        except json.JSONDecodeError:
            print("Could not load data with json")

    # if connection is close
    except (ConnectionAbortedError, ConnectionResetError, AttributeError):
        offline(sock)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 8)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>Q', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
