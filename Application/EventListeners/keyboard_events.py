import keyboard
from keyboard._winkeyboard import official_virtual_keys


class KeyboardHandler:
    def __init__(self, context):
        self.context = context
        self.blocked_keys = {}
        self.last_pressed = ""
        self.session_start = True

    def on_switch(self):
        def event_handler(event: keyboard.KeyboardEvent):
            if self.session_start:
                self.context.server.send_data("new session")
                self.session_start = False
            self.context.server.send_data(f"keyboard,{event.event_type},{event.scan_code},{event.name},{event.time},{event.device},{event.modifiers},{event.is_keypad};")

            # if event.name == "left alt":
            # print(f"keyboard,{event.event_type},{event.scan_code},{event.name},{event.time},{event.device},{event.modifiers},{event.is_keypad};")

            if event.name == "shift" and self.last_pressed == "ctrl":
                self.on_switch()
            self.last_pressed = event.name

        if self.context.server.connected:
            if not self.blocked_keys:
                for key in official_virtual_keys:
                    self.blocked_keys[official_virtual_keys[key][0]] = keyboard.hook_key(official_virtual_keys[key][0], event_handler, suppress=True)
                    keyboard.release(key)
            else:
                keyboard.unhook_all()
                keyboard.add_hotkey("ctrl+shift", self.on_switch)
                self.blocked_keys = {}


def key_press_performer(data, last_time, update_last_time):
    """ Keyboard Key Events executor """
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",")
        if not last_time == float(time):
            update_last_time(float(time))
            keyboard.send(name, True, False) if event_type == keyboard.KEY_DOWN else keyboard.send(name, False, True)
    except Exception as e:
        print(f"keyboard : {e}")
