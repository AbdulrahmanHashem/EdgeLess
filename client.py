import socket
import pyautogui

# Global constants
SERVER_HOST = "192.168.1.100"  # Replace with your server's IP address
SERVER_PORT = 9999
BUFFER_SIZE = 1024

# Create client socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Receive screen dimensions from server
screen_dimensions = client_socket.recv(BUFFER_SIZE).decode()
screen_width, screen_height = map(int, screen_dimensions.split(","))
print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}. Screen dimensions: ({screen_width}, {screen_height})")

# Set the screen size of the local computer to match the remote server
pyautogui.size()

# Mouse event handler
def handle_mouse_event(data):
    x, y, button = data.split(",")
    x = int(x)
    y = int(y)
    button = button.strip()

    # Perform mouse action based on button value
    if button == "left":
        pyautogui.click(x=x, y=y, button="left")
    elif button == "right":
        pyautogui.click(x=x, y=y, button="right")
    elif button == "middle":
        pyautogui.click(x=x, y=y, button="middle")
    elif button == "move":
        pyautogui.moveTo(x=x, y=y)

# Keyboard event handler
def handle_keyboard_event(data):
    key, action = data.split(",")
    key = key.strip()
    action = action.strip()

    # Perform keyboard action based on key and action values
    if action == "down":
        pyautogui.keyDown(key)
    elif action == "up":
        pyautogui.keyUp(key)
    else:
        pyautogui.press(key)

# Receive data from client and handle mouse and keyboard events
try:
    while True:
        data = client_socket.recv(BUFFER_SIZE).decode()
        if not data:  # No data received means the client has disconnected
            break
        event_type, payload = data.split(":")
        if event_type == "mouse":
            handle_mouse_event(payload)
        elif event_type == "keyboard":
            handle_keyboard_event(payload)
finally:
    print(f"disconnected.")
    client_socket.close()

# # Client.py
# from PyQt5 import QtWidgets
# import sys
# import socket
#
#
# class ClientWindow(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#
#         layout = QtWidgets.QVBoxLayout()
#
#         self.ip_input = QtWidgets.QLineEdit()
#         self.ip_input.setPlaceholderText("Enter server IP")
#
#         self.connect_button = QtWidgets.QPushButton("Connect")
#         self.connect_button.clicked.connect(self.on_connect)
#
#         layout.addWidget(self.ip_input)
#         layout.addWidget(self.connect_button)
#
#         self.setLayout(layout)
#
#     def on_connect(self):
#         host = self.ip_input.text()
#
#         port = 5000
#
#         try:
#             client_socket = socket.socket()
#             client_socket.settimeout(1)
#             client_socket.connect((host, port))
#             client_socket.settimeout(None)
#
#             message = input(" -> ")
#
#             while message.lower().strip() != 'bye':
#                 client_socket.send(message.encode())
#                 data = client_socket.recv(1024).decode()
#
#                 print('Received from server: ' + data)
#
#                 message = input(" -> ")
#
#             client_socket.close()
#
#         except socket.timeout:
#             print(f"Unable to connect to server at {host}:{port}")
#
#         except Exception as e:
#             print(f"Error: {str(e)}")
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = ClientWindow()
#     window.show()
#     app.exec_()