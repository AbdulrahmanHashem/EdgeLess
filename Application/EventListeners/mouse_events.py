import datetime
import threading

import mouse


""" listeners """


# def listen_to_lc(send=None):
#     def on_click(event):
#         # print(event)
#         send(event)
#
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOWN}, {mouse.LEFT};"]), buttons=mouse.LEFT, types=mouse.DOWN)
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.UP}, {mouse.LEFT};"]), buttons=mouse.LEFT, types=mouse.UP)
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOUBLE}, {mouse.LEFT};"]), buttons=mouse.LEFT, types=mouse.DOUBLE)
#
#
# def listen_to_rc(send=None):
#     def on_click(event):
#         # print(event)
#         send(event)
#
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOWN}, {mouse.RIGHT};"]), buttons=mouse.RIGHT, types=mouse.DOWN)
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.UP}, {mouse.RIGHT};"]), buttons=mouse.RIGHT, types=mouse.UP)
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOUBLE}, {mouse.RIGHT};"]), buttons=mouse.RIGHT, types=mouse.DOUBLE)
#
#
# def listen_to_mc(send=None):
#     def on_click(event):
#         # print(event)
#         send(event)
#
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOWN}, {mouse.MIDDLE};"]), buttons=mouse.MIDDLE, types=mouse.DOWN)
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.UP},  {mouse.MIDDLE};"]), buttons=mouse.MIDDLE, types=mouse.UP)
#     mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOUBLE}, {mouse.MIDDLE};"]), buttons=mouse.MIDDLE, types=mouse.DOUBLE)
#
#
# def listen_to_ws(send=None):
#     def on_wheel(event: mouse.WheelEvent):
#         if isinstance(event, mouse.WheelEvent):
#             # print(event)
#             send(f"WheelEvent, {event.delta}, {event.time};")
#
#     mouse.hook(on_wheel)
#
#
# def listen_to_mm(cxy) -> str | None:
#     x, y = mouse.get_position()
#     return f"MoveEvent, {x}, {y};" if x != cxy[0] or y != cxy[1] else None

def listen_to_all_clicks_and_wheel(send, cxy, update_mouse_loc):
    def on_event(event):
        # print(event)
        if isinstance(event, mouse.ButtonEvent):
            send(f"ButtonEvent, {event.event_type}, {event.button}, {event.time};")
        elif isinstance(event, mouse.WheelEvent):
            send(f"WheelEvent, {event.delta}, {event.time};")
        elif isinstance(event, mouse.MoveEvent):
            if event.x != cxy[0] or event.y != cxy[1]:
                send(f"MoveEvent, {event.x}, {event.y}, {event.time};")
                update_mouse_loc([event.x, event.y])

    mouse.hook(on_event)


""" mouse event executors """


def perform_lc():
    pass


def perform_rc():
    pass


def perform_mm():
    pass


""" Testing """


print(datetime.datetime.now())