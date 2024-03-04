***Project Title: Internet Relay Chat (IRC) Implementation***

**Overview:**
This project aims to implement a basic Internet Relay Chat system that enables communication between a server and multiple clients. It facilitates functionalities such as creating and joining chat rooms, listing members and rooms, chatting within rooms, and handling errors. The structure of the project includes client-server architecture where clients connect to a central server to exchange messages.

**System Requirements:**
Python 3.x
Terminal or Command Prompt
Network connectivity

**Setup Instructions:**
Clone or download the project repository from https://github.com/Mounika-Javvaji/Internet-Reply-Chat/tree/main/coding .
Navigate to the project directory in your terminal or command prompt.
Ensure Python 3.x is installed on your system.
Start the server by running python server.py in the terminal.
Open another terminal instance and run python client.py to start a client.

**Usage Instructions:**
Upon running the client program, you will be prompted to enter a username.
Use the following commands to interact with the server:
lor: List all available rooms.
lime room_name: List all members in a specific room.
cor room_name: Create a new room.
jor room_name: Join a room.
eor room_name: Leave a room.
chatmsg room_name message: Send a message in a room.
help: Display available commands and their usage.
exit: Exit the client application.
Follow the on-screen instructions and response messages for further interactions.

**Project Structure:**
server.py: Implementation of the server-side functionality.
client.py: Implementation of the client-side functionality.
manager.py: Module containing functions to handle various command executions.
constants.py: File containing constant values and error messages.
README.md: Documentation file containing project information and usage instructions.

**Conclusion & Future Work:**
The current implementation provides a basic IRC system with essential functionalities. Future enhancements may include the implementation of private messaging, chat room moderation, file transmission, and deployment on cloud servers for scalability
