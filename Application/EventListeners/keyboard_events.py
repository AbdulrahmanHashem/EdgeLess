import keyboard

from keyboard._winkeyboard import official_virtual_keys
from keyboard._canonical_names import canonical_names

full = []

for key in official_virtual_keys:
    full.append(key)

for key in canonical_names:
    if full.__contains__(canonical_names[key]) is False:
        full.append(canonical_names[key])

class KeyboardHandler:
    def __init__(self, context):
        self.context = context
        self.blocked_keys = {}
        self.last_pressed = ""
        self.session_on = False

    def start_keyboard(self):
        for key in full:
            try:
                keyboard.hook_key(key, self.key_handler, suppress=True)
            except Exception as e:
                print(e)
            keyboard.release("*")
            keyboard.release("ctrl")
        self.session_on = True

    def stop_keyboard(self):
        keyboard.unhook_all()
        self.session_on = False

    def key_handler(self, event: keyboard.KeyboardEvent):
        self.context.server. \
            send_data(
            f"keyboard,,{event.event_type},,{event.scan_code},,{event.name},,{event.time},,{event.device},,{event.modifiers},,{event.is_keypad};;")

        if event.name == "*" and self.last_pressed == "ctrl":
            self.context.stop_listening_to_controls()

        self.last_pressed = event.name


def key_press_performer(data, context):
    """ Keyboard Key Events executor """
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",,")
        if not context.last_time == float(time):
            context.last_time = float(time)
            keyboard.send(name, True, False) if event_type == keyboard.KEY_DOWN else keyboard.send(name, False, True)

            if name == "*" and context.last_pressed == "ctrl":
                keyboard.release("ctrl")
                keyboard.release("*")
            context.last_pressed = name
    except Exception as e:
        print(f"keyboard : {e}")
