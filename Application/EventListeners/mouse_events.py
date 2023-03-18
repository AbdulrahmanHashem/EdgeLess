import threading
import mouse

controller = threading.Event()


# def listen_to_all():
#     def event_handler(event):
#         """ this handles the mouse events MoveEvent, ButtonEvent, WheelEvent """
#         print(event)
#
#     while True:
#         """ Set up listeners """
#         mouse.hook(event_handler)
#         controller.wait()
#         # mouse.wait()


def listen_to_movement(send):
    def on_move(event):
        if isinstance(event, mouse.MoveEvent):
            print(event)
            send(event)

    mouse.hook(on_move)


def listen_to_lc(send):
    def on_click(event):
        print(event)
        send(event)

    mouse.on_button(on_click, args=(["DOWN"]), buttons=mouse.LEFT, types=mouse.DOWN)
    mouse.on_button(on_click, args=(["UP"]), buttons=mouse.LEFT, types=mouse.UP)
    mouse.on_button(on_click, args=(["DOUBLE"]), buttons=mouse.LEFT, types=mouse.DOUBLE)
    controller.wait()


def listen_to_rc(send):
    def on_click(event):
        print(event)
        send(event)

    mouse.on_button(on_click, args=(["DOWN"]), buttons=mouse.RIGHT, types=mouse.DOWN)
    mouse.on_button(on_click, args=(["UP"]), buttons=mouse.RIGHT, types=mouse.UP)
    mouse.on_button(on_click, args=(["DOUBLE"]), buttons=mouse.RIGHT, types=mouse.DOUBLE)
    controller.wait()
