import keyboard

from Application.UserInterface.LoggingUI.Logging import log_to_logging_file


class KeyboardHandler:
    def __init__(self, context):
        self.context = context
        self.blocked_keys = {}
        self.last_pressed = ""
        self.session_on = False

    def start_keyboard(self):
        keyboard.hook(self.key_handler, suppress=True)
        self.session_on = True

        shortcut = self.context.master_window.settings.get_setting("Session Start").split("+")
        for sc in shortcut:
            keyboard.release(sc)

    def stop_keyboard(self):
        keyboard.unhook_all()
        self.session_on = False

    def key_handler(self, event: keyboard.KeyboardEvent):
        msg = f"keyboard" \
              f",|{event.event_type}" \
              f",|{event.scan_code}" \
              f",|{event.name if event.name != 'decimal' else '.'}" \
              f",|{event.time},|{event.device}" \
              f",|{event.modifiers}" \
              f",|{event.is_keypad};|"

        self.context.server.send_data(msg)

        shortcut = self.context.master_window.settings.get_setting("Session Start").split("+")

        if event.name == shortcut[1].lower() and self.last_pressed == shortcut[0].lower():
            self.context.stop_listening_to_controls()
            self.last_pressed = event.name

        self.last_pressed = event.name


def key_press_performer(data, context):
    """ Keyboard Key Events executor """
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",|")
        if not context.last_time == float(time):
            context.last_time = float(time)

            if is_keypad == "False":
                key_event = keyboard.KeyboardEvent(event_type, int(scan_code), name, float(time), None, False)
                keyboard.play([key_event])
            else:
                keyboard.send(name, True, False) if event_type == keyboard.KEY_DOWN else keyboard.send(name, False, True)

            context.last_pressed = name
    except Exception as e:
        log_to_logging_file(f"keyboard : {e}") if context.master_window.settings.get_setting("Logging") else None
