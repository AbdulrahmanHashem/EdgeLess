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
# client_socket.sendall(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}".encode())


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
        # left_button, right_button, middle_button = pyautogui.mouseDown()
        #
        # # Listen for left mouse button press and release
        # if left_button:
        #     handle_mouse_event("mouse", x, y, "left")
        #     while pyautogui.mouseDown()[0]:
        #         pass
        #
        # # Listen for right mouse button press and release
        # if right_button:
        #     handle_mouse_event("mouse", x, y, "right")
        #     while pyautogui.mouseDown()[1]:
        #         pass
        #
        # # Listen for middle mouse button press and release
        # if middle_button:
        #     handle_mouse_event("mouse", x, y, "middle")
        #     while pyautogui.mouseDown()[2]:
        #         pass

        # Listen for mouse movement
        new_x, new_y = pyautogui.position()
        if new_x != x or new_y != y:
            x, y = new_x, new_y
            handle_mouse_event(";mouse", x, y, "move")


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
        try:
            mouse_listener.start()
        except Exception:
            print(Exception)

        keyboard_listener = threading.Thread(target=listen_for_keyboard_events)
        keyboard_listener.daemon = True  # Thread dies when main program exits
        try:
            keyboard_listener.start()
        except Exception:
            print(Exception)
finally:
    print(f"Client {client_address[0]}:{client_address[1]} has disconnected.")
    client_socket.close()
    server_socket.close()
