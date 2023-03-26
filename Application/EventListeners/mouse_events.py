import mouse
from pynput.mouse import Listener


class MouseHandler:
    def __init__(self, context):
        self.context = context
        self.is_hooked = False
        self.listener: Listener | None = None
        self.listener = Listener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move, suppress=True)
        self.listener.daemon = True

    def start_mouse(self):
        print("started")
        self.listener.run()

    def stop_mouse(self):
        print("stopped")
        self.listener.stop()

    def on_click(self, x, y, button, down):
        self.context.server.send_data(f"ButtonEvent,{button},{down};")
        return True

    def on_scroll(self, x, y, is_h, delta):
        self.context.server.send_data(f"WheelEvent,{is_h},{delta};")
        return True

    def on_move(self, x, y):
        mouse.move(x, y)
        self.context.server.send_data(f"MoveEvent,{x},{y};")
        return True


def mouse_event_performer(data, screen_ratio):
    """ Mouse event executor """
    try:
        if data.__contains__("Move"):
            button, x, y = data.split(",")
            mouse.play([mouse.MoveEvent(
                x=int(x) * screen_ratio,
                y=int(y) * screen_ratio,
                time=0)], 0)

        elif data.__contains__("Button"):
            button, x, y = data.split(",")
            try:
                mouse.play([mouse.ButtonEvent(
                    event_type=x.strip(),
                    button=y.strip(),
                    time=0)], 0)
            except Exception as e:
                print(e)

        else:
            button, is_h, delta = data.split(",")
            try:
                mouse.play([mouse.WheelEvent(
                    delta=float(delta.strip()),
                    time=0)])
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
