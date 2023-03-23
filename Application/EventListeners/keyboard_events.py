import threading

import keyboard

def listen_for_all_keys(send):
    def on_key(event: keyboard.KeyboardEvent):
        print({event.event_type},
              {event.scan_code},
              {event.name},
              {event.time},
              {event.device},
              {event.modifiers},
              {event.is_keypad})
        send(f"keyboard,{event.event_type},{event.scan_code},{event.name},{event.time},{event.device},{event.modifiers},{event.is_keypad};")

    keyboard.hook(on_key)


def key_press_performer(data: str):
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",")
        keyboard.play([keyboard.KeyboardEvent(event_type=event_type,
                                              scan_code=scan_code,
                                              name=name,
                                              time=time,
                                              device=device,
                                              modifiers=modifiers,
                                              is_keypad=is_keypad)])
    except Exception as e:
        print(e)
