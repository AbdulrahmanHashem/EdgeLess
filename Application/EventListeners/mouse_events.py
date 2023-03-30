import mouse
from pynput.mouse import Listener


class MouseHandler:
    def __init__(self, context):
        self.context = context
        self.is_hooked = False
        self.listener: Listener | None = None
        self.session_on = False
        self.session_start = True
        self.last_sent_loc = ""

    def start_mouse(self):
        self.listener = Listener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move, suppress=True)
        self.listener.run()
        self.session_on = True
        self.session_start = True

        for i in range(3):
            if self.session_start:
                x, y = mouse.get_position()
                self.context.server.send_data(f"new session,{x},{y}")
                self.session_start = False

    def stop_mouse(self):
        if self.listener is not None:
            self.listener.stop()
            self.session_on = False

    def on_click(self, x, y, button, down):
        down = 'down' if down else 'up'
        button = str(button)[7:]
        self.context.server.send_data(f"ButtonEvent,{button},{down};")
        return True

    def on_scroll(self, x, y, is_h, delta):
        self.context.server.send_data(f"WheelEvent,{is_h},{delta};")
        return True

    def on_move(self, x, y):
        # print(x, y)
        # mouse.move(x, y)
        self.context.server.send_data(f"MoveEvent,{x},{y};")
        self.last_sent_loc = f"{x},{y}"
        return True


def mouse_event_performer(data, screen_ratio, zero):
    """ Mouse event executor """
    try:
        if data.__contains__("Move"):
            event, x, y = data.split(",")
            ox, oy = zero.split(",")
            x = int(ox) - int(x)
            y = int(oy) - int(y)
            cx, xy = mouse.get_position()
            mouse.play([mouse.MoveEvent(x=cx - x, y=xy - y, time=0)], 0)

        elif data.__contains__("Button"):
            event, button, down = data.split(",")
            try:
                mouse.play([mouse.ButtonEvent(
                    event_type=down.strip(),
                    button=button.strip(),
                    time=0)], 0)
            except Exception as e:
                print(e)

        else:
            event, is_h, delta = data.split(",")
            try:
                mouse.play([mouse.WheelEvent(
                    delta=float(delta.strip()),
                    time=0)])
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
