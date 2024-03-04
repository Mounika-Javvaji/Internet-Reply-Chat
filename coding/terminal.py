import settings
import strings
import manager
import sys

def execute(client_input_string, client):
    
    command_string = client_input_string.strip()
    
    if len(command_string) < settings.MIN_COMMAND_SIZE: 
        client.send(strings.INPUT_INVALID.encode(settings.SUPPORTED_TEXT_TYPE))
    else:
        command = command_string[0:4].upper()
        argument = command_string[5:]
        command_to_fun(command, argument, client)

def command_to_fun(command, argument, client):
    if command == strings.USER:
        manager.user_creation(argument,client)
    elif command == strings.LOR:
        manager.list_of_rooms(argument,client)
    elif command == strings.LIME ROOMEM:
        manager.list_of_members(argument,client)
    elif command == strings.COR:
        manager.room_creation(argument,client)
    elif command == strings.JOR:
        manager.room_join(argument,client)
    elif command == strings.EOR:
        manager.exit_room(argument,client)
    elif command == strings.CHATMSG:
        manager.chat(argument,client)
    elif command == strings.HELP:
        help_commands(argument,client)
    else:
        client.send(strings.UNKNOWN_COMMAND.encode(settings.SUPPORTED_TEXT_TYPE))

def help_commands(argument,client):
    client.send(strings.HELP_MESSAGE.encode(settings.SUPPORTED_TEXT_TYPE))
    return 0

def direct(name):
    print(f'> {name} $ ', end='', flush=True) 

def print_response(response):
    print()
    print(response)
    print()
    direct(manager.username)

def filter_client_command(command,client):
    if str.upper(command[0:4]) == strings.EXIT:
        client.close()
        sys.exit(strings.EXIT_SUCCESSFUL)
    client.send(command.encode(settings.SUPPORTED_TEXT_TYPE))
    