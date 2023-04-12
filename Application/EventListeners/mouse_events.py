from typing import Optional

import mouse
from pynput.mouse import Listener

from Application.UserInterface.LoggingUI.Logging import log_to_logging_file


class MouseHandler:
    def __init__(self, context):
        self.context = context
        self.is_hooked = False
        self.listener: Optional[Listener] = None
        self.session_on = False
        self.last_sent_loc = ""

    def start_mouse(self):
        self.listener = Listener(on_click=self.on_click, on_scroll=self.on_scroll, on_move=self.on_move, suppress=True)

        x, y = mouse.get_position()
        self.context.server.send_data(f"new session,|{x},|{y},|"
                                      f"{self.context.master_window.settings.get_setting('Session Start')}")

        self.session_on = True
        self.listener.run()

    def stop_mouse(self):
        if self.listener is not None:
            self.listener.stop()
            self.session_on = False

    def on_click(self, x, y, button, down):
        down = 'down' if down else 'up'
        button = str(button)[7:]
        if button == "x1":
            button = "x"

        self.context.server.send_data(f"ButtonEvent,|{button},|{down};|")
        return True

    def on_scroll(self, x, y, is_h, delta):
        self.context.server.send_data(f"WheelEvent,|{is_h},|{delta};|")
        return True

    def on_move(self, x, y):
        self.context.server.send_data(f"MoveEvent,|{x},|{y};|")
        self.last_sent_loc = f"{x},{y}"
        return True


def mouse_event_performer(data, zero, context):
    """ Mouse event executor """
    if "Move" in data:
        try:
            event, x, y = data.split(",|")
            x = int(zero[0]) - int(x)
            y = int(zero[1]) - int(y)
            cx, xy = mouse.get_position()
            mouse.play([mouse.MoveEvent(x=cx - x, y=xy - y, time=0)])

        except Exception as e:
            log_to_logging_file(f"Move Event Catch : {e}") if context.master_window.settings.get_setting("Logging") else None

    elif "Button" in data:
        try:
            event, button, down = data.split(",|")
            mouse.play([mouse.ButtonEvent(event_type=down, button=button, time=0)])

        except Exception as e:
            log_to_logging_file(f"Button Event Catch : {e}") if context.master_window.settings.get_setting(
                "Logging") else None

    else:
        try:
            event, is_h, delta = data.split(",|")
            mouse.play([mouse.WheelEvent(delta=float(delta.strip()), time=0)])

        except Exception as e:
            log_to_logging_file(f"Wheel Event Catch : {e}") if context.master_window.settings.get_setting(
                "Logging") else None
