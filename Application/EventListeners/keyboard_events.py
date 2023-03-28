import keyboard

from keyboard._winkeyboard import official_virtual_keys


class KeyboardHandler:
    def __init__(self, context):
        self.context = context
        self.blocked_keys = {}
        self.last_pressed = ""
        self.session_start = True

    def start_keyboard(self):
        for key in official_virtual_keys:
            self.blocked_keys[official_virtual_keys[key][0]] = \
                keyboard.hook_key(official_virtual_keys[key][0], self.key_handler, suppress=True)
            keyboard.release("shift")
            keyboard.release("ctrl")

    def stop_keyboard(self):
        keyboard.unhook_all()

    def key_handler(self, event: keyboard.KeyboardEvent):
        if self.session_start:
            self.context.server.send_data("new session")
            self.session_start = False

        self.context.server.\
            send_data(f"keyboard,{event.event_type},{event.scan_code},{event.name},{event.time},{event.device},{event.modifiers},{event.is_keypad};")

        if event.name == "*" and self.last_pressed == "ctrl":
            self.context.toggle_session()
            keyboard.add_hotkey("ctrl+*", self.context.toggle_session)

        self.last_pressed = event.name


def key_press_performer(data, context):
    """ Keyboard Key Events executor """
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",")
        if not context.last_time == float(time):
            context.update_last_time(float(time))
            keyboard.send(name, True, False) if event_type == keyboard.KEY_DOWN else keyboard.send(name, False, True)

            if name == "*" and context.ast_pressed == "ctrl":
                keyboard.release("ctrl")
                keyboard.release("*")
            context.last_pressed = name
    except Exception as e:
        print(f"keyboard : {e}")
