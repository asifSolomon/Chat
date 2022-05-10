#   Chat - server side
#   Author: Solomon Asif
import socket
import select
import sqlite3
import os
from datetime import date
from hashlib import sha256
import validation
from mail_service import forgotPass_email, join_email
from helpers import print_client_sockets, receive_dict, remove_socket, update_lists, send_dict

# constants
SERVER_PORT = 8200
SERVER_IP = "0.0.0.0"


# run the server
def main():
    # connect to db
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.abspath(f"{path}/files/chat.db"))

    # set the server
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listening for clients
    server_socket.listen()
    print("Listening for clients...")

    client_sockets = []
    messages_to_send = []
    forgot_pass = {}
    rooms_participants = {
        "Gaming": {},
        "Cooking": {},
        "Sport": {},
        "lobby": []
    }

    while True:
        # finding clients that are ready to read and write
        rlist, wlist, xlist = select.select([server_socket] + client_sockets,client_sockets, [])

        # all the sockets that are ready to read
        for current_socket in rlist:
            # new client joining
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
                print_client_sockets(client_sockets)
            # receiving data
            else:
                # get data
                dict_data = receive_dict(current_socket)

                # remove client
                if dict_data["cmd"] == "close":
                    print("Connection closed")
                    remove_socket(current_socket, rooms_participants, messages_to_send)
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)

                # receive data and add it to messages_to_send (for other clients)
                elif dict_data['cmd'] == "message":
                    for s in rooms_participants[dict_data['name']].values():
                        if s != current_socket:
                            data = {
                                "cmd": "message",
                                "message": dict_data["message"]
                            }
                            messages_to_send.append((s, data))
                # join lobby
                elif dict_data['cmd'] == "lobby":
                    rooms_participants['lobby'].append(current_socket)
                    update_lists(rooms_participants, messages_to_send, "lobby", False)
                # sign up and validation
                elif dict_data['cmd'] == "signup":
                    valid = validation.v_username(dict_data['userID'])
                    if valid != "OK":
                        data = {
                            "cmd": "error",
                            "message": valid
                        }
                    elif dict_data['pass'] != dict_data['confirm']:
                        data = {
                            "cmd": "error",
                            "message": "password and confirm password are not the same"
                        }
                    elif validation.v_pass(dict_data['pass']) != "OK":
                        data = {
                            "cmd": "error",
                            "message": validation.v_pass(dict_data['pass'])
                        }
                    elif validation.v_email(dict_data['email']) != "OK":
                        data = {
                            "cmd": "error",
                            "message": validation.v_email(dict_data['email'])
                        }
                    elif validation.v_Name(dict_data['first name'], dict_data['last name']) != "OK":
                        data = {
                            "cmd": "error",
                            "message": validation.v_Name(dict_data['first name'], dict_data['last name'])
                        }
                    elif validation.v_phone(dict_data['phone']) != "OK":
                        data = {
                            "cmd": "error",
                            "message": validation.v_phone(dict_data['phone'])
                        }
                    else:
                        hashed = sha256(dict_data['pass'].encode()).hexdigest()
                        today = date.today()
                        # dd/mm/YY
                        today = today.strftime("%d/%m/%Y")

                        vars_tup = (dict_data['userID'], hashed, dict_data['first name'], dict_data['last name'],
                                    dict_data['email'], dict_data['phone'], dict_data['Bdate'], today, False)

                        conn.execute("INSERT INTO tblUser (usrUser,usrPswd,usrFname,usrLname,usrEmail,usrPhone,"
                                     "usrBdate,usrJoinDate, usrIsDel)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", vars_tup)
                        conn.commit()

                        data = {
                            "cmd": "success",
                            "message": "successfully signed up"
                        }
                    send_dict(data, client_sockets, current_socket)
                    # join email
                    if data['message'] == "successfully signed up":
                        join_email(dict_data['email'], dict_data['userID'], dict_data['first name'])

                # login
                elif dict_data['cmd'] == "login":
                    query = f"SELECT usrPswd from tblUser WHERE usrUser= ?"
                    try:
                        pwd = conn.execute(query, (dict_data['userID'],)).fetchone()[0]
                        client_pwd = sha256(dict_data['pass'].encode()).hexdigest()
                        if pwd == client_pwd:
                            data = {
                                "cmd": "success",
                            }
                            print("successfully connected")
                        else:
                            data = {
                                "cmd": "error",
                                "message": "wrong password"
                            }
                    except (IndexError, TypeError):
                        data = {
                            "cmd": "error",
                            "message": "Unknown username"
                        }
                    send_dict(data, client_sockets, current_socket)

                # send code to email
                elif dict_data['cmd'] == "forgot":
                    receiver_email = dict_data['email']
                    query = f"SELECT usrEmail from tblUser WHERE usrEmail = ?"
                    try:
                        receiver_email = conn.execute(query, (receiver_email,)).fetchone()[0]
                        data = {
                            "cmd": "success",
                        }
                    except (IndexError, TypeError):
                        data = {
                            "cmd": "error",
                            "message": "Unknown email"
                        }
                    send_dict(data, client_sockets, current_socket)
                    if data['cmd'] == "success":
                        forgot_pass[receiver_email] = forgotPass_email(receiver_email)

                # change password if code is correct
                elif dict_data['cmd'] == "change":
                    receiver_email = dict_data['email']
                    query = f"SELECT usrEmail from tblUser WHERE usrEmail= ?"
                    try:
                        receiver_email = conn.execute(query, (receiver_email,)).fetchone()[0]
                        if forgot_pass[receiver_email] == dict_data['code']:
                            new_pass = dict_data['new_pass']
                            valid = validation.v_pass(new_pass)
                            if valid == "OK":
                                conn.execute("UPDATE tblUser SET usrPswd = ? WHERE usrEmail = ?",
                                             (sha256(new_pass.encode()).hexdigest(), receiver_email))
                                conn.commit()
                                del forgot_pass[receiver_email]
                                data = {
                                    "cmd": "success",
                                    "message": "password was changed"
                                }
                            else:
                                data = {
                                    "cmd": "error",
                                    "message": valid
                                }
                        else:
                            data = {
                                "cmd": "error",
                                "message": "Wrong code"
                            }

                    except (IndexError, TypeError, KeyError):
                        data = {
                            "cmd": "error",
                            "message": "Unknown email or expired code"
                        }
                    send_dict(data, client_sockets, current_socket)

                elif dict_data['cmd'] == "leave lobby":
                    rooms_participants['lobby'].remove(current_socket)

                elif dict_data['cmd'] == "join room":
                    rooms_participants[dict_data['name']][dict_data['user']] = current_socket
                    update_lists(rooms_participants, messages_to_send, dict_data['name'], True)

                elif dict_data['cmd'] == "leave room":
                    del rooms_participants[dict_data['name']][dict_data['user']]
                    update_lists(rooms_participants, messages_to_send, dict_data['name'], True)

        # send the possible messages from messages_to_send
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in wlist:
                try:
                    print(data)
                    send_dict(data, client_sockets, current_socket)
                    messages_to_send.remove(message)
                except ConnectionResetError:
                    print("Connection closed", )
                    remove_socket(current_socket, rooms_participants, messages_to_send)
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                    messages_to_send.remove(message)
    # conn.close() - server should not stop


if __name__ == '__main__':
    main()
