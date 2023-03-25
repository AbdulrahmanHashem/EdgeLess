import mouse

from pynput.mouse import Listener


class MouseHandler:
    def __init__(self, context):
        self.context = context
        self.is_hooked = False
        self.listener : Listener | None = None

    def start_mouse(self):
        print("started")
        self.listener = Listener(on_click=self.listen, on_scroll=self.listen, on_move=self.on_move, suppress=True)
        self.listener.daemon = True
        self.listener.run()

    def stop_mouse(self):
        print("stopped")
        mouse.unhook_all()
        self.listener.stop()
        del self.listener
        self.listener = None
        self.is_hooked = False

    def on_move(self, x, y):
        mouse.move(x, y)
        self.listen()
        return True

    def listen(self, *args):
        def on_event(event):
            if isinstance(event, mouse.ButtonEvent):
                self.context.server.send_data(f"ButtonEvent, {event.event_type}, {event.button}, {event.time};")
                print(event.event_type)
            elif isinstance(event, mouse.WheelEvent):
                self.context.server.send_data(f"WheelEvent, {event.delta}, {event.time};")
            elif isinstance(event, mouse.MoveEvent):
                if event.x != self.context.mouse_loc[0] or event.y != self.context.mouse_loc[1]:
                    self.context.server.send_data(f"MoveEvent, {event.x}, {event.y}, {event.time};")
                    self.context.update_mouse_loc([event.x, event.y])

        if self.is_hooked is False:
            mouse.hook(on_event)
            self.is_hooked = True
            print("mouse hooked")

        return True
# def listen_to_all_clicks_and_wheel(send, cxy, update_mouse_loc):
#     """ Mouse event listener """
#     def on_event(event):
#         # print(event)
#         if isinstance(event, mouse.ButtonEvent):
#             send(f"ButtonEvent, {event.event_type}, {event.button}, {event.time};")
#         elif isinstance(event, mouse.WheelEvent):
#             send(f"WheelEvent, {event.delta}, {event.time};")
#         elif isinstance(event, mouse.MoveEvent):
#             if event.x != cxy[0] or event.y != cxy[1]:
#                 send(f"MoveEvent, {event.x}, {event.y}, {event.time};")
#                 update_mouse_loc([event.x, event.y])
#
#     mouse.hook(on_event)


def mouse_event_performer(data, screen_ratio):
    """ Mouse event executor """
    try:
        if data.__contains__("Move"):
            button, x, y, t = data.split(",")
            mouse.play([mouse.MoveEvent(
                x=int(x) * screen_ratio,
                y=int(y) * screen_ratio,
                time=t)], 0)

        elif data.__contains__("Button"):
            button, x, y, t = data.split(",")
            try:
                mouse.play([mouse.ButtonEvent(event_type=x.strip(), button=y.strip(), time=t)], 0)
            except Exception as e:
                print(e)
        else:
            button, delta, t = data.split(",")
            try:
                mouse.play([mouse.WheelEvent(delta=float(delta.strip()), time=float(t.strip()))])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
