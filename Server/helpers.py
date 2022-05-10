import json
import struct
from rsa import PrivateKey, decrypt

# not visible to clients
PRIVATE_KEY = PrivateKey(21468076645486133110101681660848174169977541474881806070386243630607550580212210745616607307584702551667153667157302483069777014721221096663089299718499811557525040158962145641647261885038361956799811745241630622072752177876850700896870068138710850226518977702040727250262787167847250335581993423535963729467533243082882348091712066559825205959901346610468582139308514862652246395700578834581357207133645241332554642217799849263694027458313483990467369164577145341374211290264974506899269954350664907069592686245748724376398670858203099738699024653890435890132247061753219194915753562714847138046050501985940129140709, 65537, 11533477434287826123770848674745614909909505436457474555323393685857778787229988069982073129571841740416082723758204725977749651514708845269248075953868194533300259989882023679703960262299398601354419209579513443895197086086730187953032611030347289708493014417979949734569822747344764591992646768137064452500911635291609303217916773802665371345803981625650391056818083873352125089137146240450354082870806568966710786738989336712030177898817800035721002225367909870188738384409532988924539453276496566913605702708936680095999402399201386003454973813771036004992770440432708222542630533413563048518309790940992289549901, 2394706066032944056068962867420423441965489077380817613370931420625221401349028060692361169903661105022596212484961419213262653766854117151220826017855257869953640146453111955471180806425964134545522703401968564559603466778542624435121955161231124676989049419368140656082526708067636796241593649327959939872212508694494354055223, 8964806558096719674908251269425701727649407887965490309367581574016880101151937931404663320634045893145138474886293917354101569348529703249182107030593107019669539301624414712636924927867203538325401117277543680289638990007756716647601680771316194556565625894351723984157264815777290316483)


# print all the connected client sockets
def print_client_sockets(client_sockets):
    for c in client_sockets:
        # print IP and PORT of all clients
        print("\t", c.getpeername())


def send_dict(my_dict, client_sockets, current_socket):
    """
    Send dictionary using socket
    First 8 bytes are the length of the message
    """
    try:
        data = json.dumps(my_dict).encode()
        msg = struct.pack('>Q', len(data)) + data
        current_socket.send(msg)
    except ConnectionResetError:
        client_sockets.remove(current_socket)
        current_socket.close()


def receive_dict(sock):
    """
    Receive dictionary using socket
    First 8 bytes are the length of the message.
    The message is decrypt using rsa public and private key
    """
    try:
        data = recv_msg(sock).decode()
        try:
            dict_data = json.loads(data)
        except json.JSONDecodeError:
            print("Could not load data with json")
            dict_data = {"cmd": "close"}

    # if connection is close
    except (ConnectionAbortedError, ConnectionResetError, AttributeError):
        dict_data = {"cmd": "close"}
    return dict_data


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 8)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>Q', raw_msglen)[0]
    # Read the message data
    return decrypt(recvall(sock, msglen), PRIVATE_KEY)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


# send new lists of participants to clients
def update_lists(rooms_participants, messages_to_send, room_name, new_room):
    for s in rooms_participants['lobby']:
        data = {
            "cmd": "participants_lobby",
            "Gaming": [*rooms_participants["Gaming"]],  # unpack to names
            "Cooking": [*rooms_participants["Cooking"]],
            "Sport": [*rooms_participants["Sport"]]
        }
        messages_to_send.append((s, data))
    if new_room:
        for s in rooms_participants[room_name].values():
            data = {
                "cmd": "participants_room",
                room_name: [*rooms_participants[room_name]],  # unpack to names
            }
            messages_to_send.append((s, data))


# remove socket from list of participants and notify other clients
def remove_socket(sock, rooms_participants, messages_to_send):
    for key, value in rooms_participants["Cooking"].items():
        if value == sock:
            del rooms_participants["Cooking"][key]
            update_lists(rooms_participants, messages_to_send, "Cooking", True)
            return
    for key, value in rooms_participants["Sport"].items():
        if value == sock:
            del rooms_participants["Sport"][key]
            update_lists(rooms_participants, messages_to_send, "Sport", True)
            return
    for key, value in rooms_participants["Gaming"].items():
        if value == sock:
            del rooms_participants["Gaming"][key]
            update_lists(rooms_participants, messages_to_send, "Gaming", True)
            return
    for value in rooms_participants["lobby"]:
        if value == sock:
            rooms_participants["lobby"].remove(sock)
            return
