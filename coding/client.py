import socket   
import sys
import select

import settings
import manager
import strings
import terminal

client = socket.socket(settings.IPV4, settings.CONNECT_TCP)
client.settimeout(settings.CLIENT_TIMEOUT)

try:
    print(strings.TRYING_CONNECTION)
    client.connect((settings.LOCAL_HOST, settings.PORT))
except:
    sys.exit(strings.CAN_NOT_CONNECT)

print(strings.CONNECTION_SUCCESS)
manager.welcome(client)
client_stream = [client, sys.stdin]

while True:
    read_list,write_list,exception_list = select.select(client_stream, [], [])

    for input in read_list:

        if input == client:

            try:
                response = input.recv(settings.INPUT_SIZE)
            except:
                sys.exit(strings.DISCONNECTED_FROM_SERVER)

            if response:
                terminal.print_response(response)
            else:
                sys.exit(strings.DISCONNECTED_FROM_SERVER)

        else:
            send_command = sys.stdin.readline()
            terminal.filter_client_command(send_command, client)