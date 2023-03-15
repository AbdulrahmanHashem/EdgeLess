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