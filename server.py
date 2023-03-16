import threading

import mouse

def on_click(event):
    # print(event.x, event.y)
    print(event)

# Set up listeners
mouse.hook(on_click)
controller = threading.Event()


if __name__ == '__main__':
    while not controller.is_set():
        mouse.wait()
        controller.wait(.1)


# import threading
# from pynput.mouse import Listener as mouse_listener
# from pynput.keyboard import Listener as keyboard_listener
#
#
# def on_move(x, y, button=None, pressed=None):
#     # if pressed:
#     print(x, y, button, pressed)
#
#
# def on_click(x, y, button=None, pressed=None):
#     # if pressed:
#     print(x, y, button, pressed)
#
#
# listener = mouse_listener(on_move=on_move, on_click=on_click)
# controller = threading.Event()
#
# if __name__ == '__main__':
#     listener.start()
#     try:
#         while not controller.is_set():
#             listener.wait()
#             controller.wait(.1)
#         # listener
#     finally:
#         listener.stop()