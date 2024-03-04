import socket
import select
import sys

import settings
import manager
import strings
import terminal

server_switch = settings.switch.ON
server = socket.socket(settings.IPV4, settings.CONNECT_TCP)
server.bind((settings.DEFAULT_HOST,settings.PORT))
server.listen(settings.MAX_CONNECT_REQUEST)
print(strings.SERVER_STARTED)

server_stream  = [server,sys.stdin]

while server_switch == settings.switch.ON:
    read_list,write_list,exception_list = select.select(server_stream,[],[])
    
    for input in read_list:
        if input == server:
            print("here")
            client, ip_address = server.accept()
            data = client.fileno()
            manager.total_clients += 1
            print(strings.NEW_CLIENT, ip_address)
            server_stream.append(client)
        
        elif input == sys.stdin:
            command = sys.stdin.readline()
            if str.upper(command[0:4]) == strings.EXIT:
                server_switch = settings.switch.OFF
            
        else:
            client = input
            try:
                client_input = client.recv(settings.INPUT_SIZE)
            except:
                manager.disconnect(server_stream, client)
                
            if client_input:
                client_input_string = client_input.decode(settings.SUPPORTED_TEXT_TYPE).rstrip()
                terminal.execute(client_input_string, client)
                print(strings.CLIENT_INPUT)
            else:
                # there is no data, client disconnects
                manager.disconnect(server_stream, client)

server.close()
print(strings.SERVER_STOPPED)