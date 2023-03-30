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
        keyboard.hook_key("\|".strip("|"), self.key_handler, suppress=True)
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
            f"keyboard,|{event.event_type},|{event.scan_code},|{event.name},|{event.time},|{event.device},|{event.modifiers},|{event.is_keypad};|")

        if event.name == "*" and self.last_pressed == "ctrl":
            self.context.stop_listening_to_controls()

        self.last_pressed = event.name


def key_press_performer(data, context):
    """ Keyboard Key Events executor """
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",|")
        if not context.last_time == float(time):
            context.last_time = float(time)
            keyboard.send(name, True, False) if event_type == keyboard.KEY_DOWN else keyboard.send(name, False, True)

            if name == "*" and context.last_pressed == "ctrl":
                keyboard.release("ctrl")
                keyboard.release("*")
            context.last_pressed = name
    except Exception as e:
        print(f"keyboard : {e}")


full = {
    '[': '[',
    ']': ']',
    ';': ';',
    '"': '"',
    '\]': '\]',
    '=': '=',
    'control-': 'control-break processing',
    'backspace': 'backspace',
    'tab': 'tab',
    'clear': 'clear',
    'enter': 'enter',
    'shift': 'shift',
    'ctrl': 'ctrl',
    'alt': 'alt',
    'pause': 'pause',
    'caps lock ': 'caps lock',
    'ime kana': 'ime kana mode',
    'ime hanguel': 'ime hanguel mode',
    'ime hangul': 'ime hangul mode',
    'ime junja': 'ime junja mode',
    'ime final': 'ime final mode',
    'ime hanja': 'ime hanja mode',
    'ime kanji': 'ime kanji mode',
    'esc': 'esc',
    'ime convert': 'ime convert',
    'ime nonconvert': 'ime nonconvert',
    'ime accept': 'ime accept',
    'ime mode': 'ime mode change request',
    'spacebar': 'spacebar',
    'page up': 'page up',
    'page down': 'page down',
    'end': 'end',
    'home': 'home',
    'left': 'left',
    'up': 'up',
    'right': 'right',
    'down': 'down',
    'select': 'select',
    'print': 'print',
    'execute': 'execute',
    'print screen': 'print screen',
    'insert': 'insert',
    'delete': 'delete',
    'help': 'help',
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'i': 'i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'o': 'o',
    'p': 'p',
    'q': 'q',
    'r': 'r',
    's': 's',
    't': 't',
    'u': 'u',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'y': 'y',
    'z': 'z',
    'left windows': 'left windows',
    'right windows': 'right windows',
    'applications': 'applications',
    'sleep': 'sleep',
    '*': '*',
    '+': '+',
    'separator': 'separator',
    '-': '-',
    'decimal': 'decimal',
    '/': '/',
    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'f10': 'f10',
    'f11': 'f11',
    'f12': 'f12',
    'f13': 'f13',
    'f14': 'f14',
    'f15': 'f15',
    'f16': 'f16',
    'f17': 'f17',
    'f18': 'f18',
    'f19': 'f19',
    'f20': 'f20',
    'f21': 'f21',
    'f22': 'f22',
    'f23': 'f23',
    'f24': 'f24',
    'num lock': 'num lock',
    'scroll lock': 'scroll lock',
    'left shift': 'left shift',
    'right shift': 'right shift',
    'left ctrl': 'left ctrl',
    'right ctrl': 'right ctrl',
    'left menu': 'left menu',
    'right menu': 'right menu',
    'browser back': 'browser back',
    'browser forward': 'browser forward',
    'browser refresh': 'browser refresh',
    'browser stop': 'browser stop',
    'browser search': 'browser search key',
    'browser favorites': 'browser favorites',
    'browser start': 'browser start and home',
    'volume mute': 'volume mute',
    'volume down': 'volume down',
    'volume up': 'volume up',
    'next track': 'next track',
    'previous track': 'previous track',
    'stop media': 'stop media',
    'play/': 'play/pause media',
    'start mail': 'start mail',
    'select media': 'select media',
    'start application': 'start application 1',
    'start appli': 'start application 2',
    ',': ',',
    '.': '.',
    'ime process': 'ime process',
    'attnp': 'attn',
    'crselg': 'crsel',
    'exsel': 'exsel',
    'erase eof': 'erase eof',
    'play': 'play',
    'zoom': 'zoom',
    'reserved': 'reserved ',
    'pa1': 'pa1',
    'clearu': 'clear'
}
