import settings
import strings
import sys
import terminal

clients       = {}
rooms         = {}
total_clients = 0
username      = strings.DEFAULT_USERNAME

def welcome(client):
    complete = 0
    global username
    while not complete:
        print(strings.YOUR_NAME, end='', flush=True)
        username = sys.stdin.readline().rstrip()
        send_data = strings.USER + username
        client.send(send_data.encode(settings.SUPPORTED_TEXT_TYPE))

        try:
            response = client.recv(settings.INPUT_SIZE).decode(settings.SUPPORTED_TEXT_TYPE).rstrip()
        except:
            sys.exit(strings.DISCONNECTED_FROM_SERVER)

        print(response)

        if (response[0:2] == strings.WELCOME_CLIENT[0:2]):
            complete = 1
    terminal.direct(username)

def disconnect(server_stream, client):
    
    global total_clients,clients

    try:
        
        print(strings.CLIENT_DISCONNECT)
        _rooms = clients[client][strings.ROOMS]
        for room in _rooms:
            rooms[room][strings.CLIENTS].remove(clients[client])
        clients.pop(client)

    except:
        print(strings.CLIENT_DISCONNECT_ERR)


    client.close()
    server_stream.remove(client)
    total_clients -= 1

def user_creation(name, client):
    
    if clients.__contains__(client):
        client.send(strings.CLIENT_ALREADY_IN.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    for _client in clients:
        if clients[_client][strings.NAME] == name:
            client.send(strings.CLIENT_EXISTS.encode(settings.SUPPORTED_TEXT_TYPE))
            return 0

    clients[client] = {
        strings.NAME: name,
        strings.ROOMS: [],
        strings.SOCKET: client
    }

    welcome = strings.WELCOME_CLIENT + strings.HELP_MESSAGE
    client.send(welcome.encode(settings.SUPPORTED_TEXT_TYPE))
    return 0

def authenticate(client):
    if (client in clients):
        return True
    else:
        client.send(strings.CLIENT_INVALID.encode(settings.SUPPORTED_TEXT_TYPE))
        return False

def check(name):
    return (len(str.split(name,' ')) > 1 or len(name) == 0)
       
def transmit(rooms,note):
    
    if len(rooms) == 0:
        for client in clients:
            clients[client][strings.SOCKET].send(note.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    while len(rooms) > 0:
        name = rooms.pop(0)
        if rooms.__contains__(name):
            _clients = rooms[name][strings.CLIENTS]
            for client in _clients:
                client[strings.SOCKET].send(note.encode(settings.SUPPORTED_TEXT_TYPE))   
                
def list_of_rooms(argument, client):
    if not (authenticate(client)):
        return 0
    
    send_string = ''
    if len(rooms) > 0:
        send_string += strings.ROOMS_AVAILABLE_TITLE
        for room in rooms:
            send_string += rooms[room][strings.NAME] + strings.NEW_LINE
    else:
        send_string += strings.NO_ROOMS_TITLE  
    client.send(send_string.encode(settings.SUPPORTED_TEXT_TYPE))
    return 0

def list_of_members(argument, client):
    if not (authenticate(client)):
        return 0
        
    if check(argument):
        client.send(strings.INVALID_ROOM_NAME.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    if not rooms.__contains__(argument):
        client.send(strings.ROOM_DOES_NOT_EXIST.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    room_members = rooms[argument][strings.CLIENTS]
    send_string = ""
    send_string += strings.ROOM_MEMBERS
    for member in room_members:
        send_string += member[strings.NAME] + strings.NEW_LINE
    client.send(send_string.encode(settings.SUPPORTED_TEXT_TYPE))
    return 0

def room_creation(name, client):
    if not (authenticate(client)):
        return 0

    if check(name):
        client.send(strings.INVALID_ROOM_NAME.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0
    
    for room in rooms:
        if rooms[room][strings.NAME] == name:
            client.send(strings.ROOM_DOES_NOT_EXIST.encode(settings.SUPPORTED_TEXT_TYPE))
            return 0

    rooms[name] = {
        strings.NAME    : name,
        strings.CLIENTS : []
    }

    send_string = ""
    send_string += strings.ROOM_ADDED
    client.send(send_string.encode(settings.SUPPORTED_TEXT_TYPE))
    return 0

def room_join(name, client):
    if not (authenticate(client)):
        return 0

    if check(name):
        client.send(strings.INVALID_ROOM_NAME.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    if not rooms.__contains__(name):
        client.send(strings.ROOM_DOES_NOT_EXIST.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    room_members = rooms[name][strings.CLIENTS]
    member = clients[client]
    if member in room_members:
        client.send(strings.ALREADY_MEMBER.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    transmit([name], strings.NEW_MEMBER_JOINED)
    room_members.append(member)
    member[strings.ROOMS].append(name)
    client.send(strings.MEMBERSHIP_GRANTED.encode(settings.SUPPORTED_TEXT_TYPE))
    return 0

def exit_room(name, client):
    if not (authenticate(client)):
        return 0

    if check(name):
        client.send(strings.INVALID_ROOM_NAME.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    if not rooms.__contains__(name):
        client.send(strings.ROOM_DOES_NOT_EXIST.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    _clients = rooms[name][strings.CLIENTS]
    _client = clients[client]

    if not (_client in _clients):
        client.send(strings.NOT_MEMBER.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    _clients.remove(_client)
    _client[strings.ROOMS].remove(name)
    transmit([name], strings.MEMBER_LEFT)
    client.send(strings.YOU_LEFT_ROOM.encode(settings.SUPPORTED_TEXT_TYPE))
    
    return 0

def chat(arguments, client):
    if not (authenticate(client)):
        return 0

    arguments_arr = str.split(arguments, " ",1)
    
    if not (len(arguments_arr) == 2 and len(arguments_arr[0]) > 0 and len(arguments_arr[1]) > 0 ):
        client.send(strings.INVALID_MESSAGE_FORMAT.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0

    room = arguments_arr[0]
    message = arguments_arr[1]

    # check if room exists
    if not rooms.__contains__(room):
        client.send(strings.ROOM_DOES_NOT_EXIST.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0    

    _clients = rooms[room][strings.CLIENTS]
    _client = clients[client]
    username = _client[strings.NAME]

    if not (_client in _clients):
        client.send(strings.NOT_MEMBER.encode(settings.SUPPORTED_TEXT_TYPE))
        return 0    

    for receiver in _clients:
        if not (receiver == _client):
            send_string = f"\n{username}@{room}: " + message
            receiver[strings.SOCKET].send(send_string.encode(settings.SUPPORTED_TEXT_TYPE))

    
    send_string = f"You@{room}: " + message
    client.send(send_string.encode(settings.SUPPORTED_TEXT_TYPE))
    return 0