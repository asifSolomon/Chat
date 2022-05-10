from PyQt5.QtWidgets import QMessageBox


# create pop up message
def pop_up_message(sock, message, message_type):
    msg = QMessageBox()
    msg.setText(message)
    if message_type == "error":
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
    elif message_type == "success":
        msg.setWindowTitle("Success")
        msg.setIcon(QMessageBox.Information)

    msg.exec_()


# server is offline
def offline(sock):
    pop_up_message(sock, "Server is offline, try again later", "error")