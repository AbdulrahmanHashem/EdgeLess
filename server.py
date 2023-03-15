import socket
import threading
import pyautogui
import keyboard

# Global constants
HOST = ''  # Use all available interfaces
PORT = 9999  # Arbitrary non-privileged port
BUFFER_SIZE = 1024

# Get screen size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Listen for one connection at a time only
print(f"Server started and listening on port {PORT}...")

# Wait for client to connect
client_socket, client_address = server_socket.accept()
print(f"Client {client_address[0]}:{client_address[1]} is connected.")

# Send screen dimensions to client
client_socket.sendall(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}".encode())

# Mouse event handler
def handle_mouse_event(event_type, x, y, button):
    data = f"{x},{y},{button}"
    message = f"{event_type}:{data}"
    client_socket.sendall(message.encode())

# Keyboard event handler
def handle_keyboard_event(event_type, key, action):
    data = f"{key},{action}"
    message = f"{event_type}:{data}"
    client_socket.sendall(message.encode())

# Start mouse event listener thread
def listen_for_mouse_events():
    while True:
        x, y = pyautogui.position()
        left_button, right_button, middle_button = pyautogui.mouseDown()

        # Listen for left mouse button press and release
        if left_button:
            handle_mouse_event("mouse", x, y, "left")
            while pyautogui.mouseDown()[0]:
                pass

        # Listen for right mouse button press and release
        if right_button:
            handle_mouse_event("mouse", x, y, "right")
            while pyautogui.mouseDown()[1]:
                pass

        # Listen for middle mouse button press and release
        if middle_button:
            handle_mouse_event("mouse", x, y, "middle")
            while pyautogui.mouseDown()[2]:
                pass

        # Listen for mouse movement
        new_x, new_y = pyautogui.position()
        if new_x != x or new_y != y:
            x, y = new_x, new_y
            handle_mouse_event("mouse", x, y, "move")


def listen_for_keyboard_events():
    while True:
        event = keyboard.read_event()
        key = event.name
        action = event.event_type

        # Special keys need to be handled differently
        if key in ["ctrl", "alt", "shift", "win"]:
            key = key.upper()

        handle_keyboard_event("keyboard", key, action)



# Keep the main thread running while the mouse and keyboard listener threads are running
try:
    while True:
        # Start listener threads
        mouse_listener = threading.Thread(target=listen_for_mouse_events)
        mouse_listener.daemon = True  # Thread dies when main program exits
        mouse_listener.start()

        keyboard_listener = threading.Thread(target=listen_for_keyboard_events)
        keyboard_listener.daemon = True  # Thread dies when main program exits
        keyboard_listener.start()
finally:
    print(f"Client {client_address[0]}:{client_address[1]} has disconnected.")
    client_socket.close()
    server_socket.close()

# Close the client socket when the main thread is terminated
# client_socket.close()

# # Server.py
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QThread, pyqtSignal
# import socket
# import sys
#
#
# class ServerThread(QThread):
#     signal = pyqtSignal('PyQt_PyObject')
#
#     def __init__(self):
#         QThread.__init__(self)
#         self.running = False
#         self.connection = None # Declare connection variable
#
#     def run(self):
#         self.running = True
#         host = socket.gethostbyname(socket.gethostname())
#         port = 5000
#
#         try:
#             server_socket = socket.socket()
#             server_socket.bind((host, port))
#             server_socket.listen(1)
#             self.connection, address = server_socket.accept()
#             self.signal.emit(f"Connection from: {str(address)}")
#
#             while self.running:
#                 data = self.connection.recv(1024).decode() # Use connection to receive data
#                 if not data:
#                     break
#                 self.signal.emit(f"From connected user: {str(data)}")
#                 data = input(" -> ")
#                 self.connection.send(data.encode()) # Use connection to send data
#
#         except Exception as e:
#             self.signal.emit(f"Error: {str(e)}")
#
#         finally:
#             if self.connection:
#                 self.connection.close() # Close connection if it exists
#
#     def stop(self):
#         self.running = False
#
#
# class ServerWindow(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#
#         layout = QtWidgets.QVBoxLayout()
#
#         host = socket.gethostbyname(socket.gethostname())
#
#         self.label_ip_address = QtWidgets.QLabel(f"Server IP Address: {host}")
#
#         layout.addWidget(self.label_ip_address)
#
#         self.label_status = QtWidgets.QLabel("Not Connected")
#
#         layout.addWidget(self.label_status)
#
#         self.toggle_button = QtWidgets.QPushButton("Start Server")
#
#         self.toggle_button.clicked.connect(self.on_toggle)
#
#         layout.addWidget(self.toggle_button)
#
#         self.setLayout(layout)
#
#     def on_toggle(self):
#         if not hasattr(self, 'server_thread'): # If server_thread doesn't exist, create it and start the thread
#             self.server_thread = ServerThread()
#             self.server_thread.signal.connect(self.update_label)
#             self.server_thread.start()
#             self.toggle_button.setText("Stop Server")
#         else:
#             if not self.server_thread.running:
#                 delattr(self, 'server_thread') # If server_thread is not running, delete it
#                 return
#             else:
#                 self.server_thread.stop() # If server_thread is running, stop it
#                 if self.server_thread.connection: # If there is an open connection, close it
#                     self.server_thread.connection.close()
#                 delattr(self, 'server_thread')
#                 self.toggle_button.setText("Start Server")
#
#     def update_label(self, text):
#         if text.startswith('Connection from'):
#             text += '\nChoose which edge of the screen activates sending inputs:'
#         elif text.startswith('From connected user'):
#             text += '\nReceived input from client'
#         else:
#             pass
#
#         print(text)
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = ServerWindow()
#     window.show()
#     app.exec_()
