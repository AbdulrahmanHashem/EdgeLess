import mouse

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


# def listen_to_movement(send=None):
#     def on_move(event):
#         if isinstance(event, mouse.MoveEvent):
#             # print(event)
#             send(event)
#
#     mouse.hook(on_move)

def listen_to_lc(send=None):
    def on_click(event):
        # print(event)
        send(event)

    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.LEFT}, {mouse.DOWN};"]), buttons=mouse.LEFT, types=mouse.DOWN)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.LEFT}, {mouse.UP};"]), buttons=mouse.LEFT, types=mouse.UP)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.LEFT}, {mouse.DOUBLE};"]), buttons=mouse.LEFT, types=mouse.DOUBLE)


def listen_to_rc(send=None):
    def on_click(event):
        # print(event)
        send(event)

    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.RIGHT}, {mouse.DOWN};"]), buttons=mouse.RIGHT, types=mouse.DOWN)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.RIGHT}, {mouse.UP};"]), buttons=mouse.RIGHT, types=mouse.UP)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.RIGHT}, {mouse.DOUBLE};"]), buttons=mouse.RIGHT, types=mouse.DOUBLE)


def mouse_movement(cxy) -> str | None:
    x, y = mouse.get_position()
    return f"MoveEvent, {x}, {y};" if x != cxy[0] or y != cxy[1] else None
