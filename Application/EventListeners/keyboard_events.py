import threading

import keyboard

def listen_for_all_keys(send):
    def on_key(event: keyboard.KeyboardEvent):
        # print({event.event_type},
        #       {event.scan_code},
        #       {event.name},
        #       {event.time},
        #       {event.device},
        #       {event.modifiers},
        #       {event.is_keypad})
        send(f"keyboard,{event.event_type},{event.scan_code},{event.name},{event.time},{event.device},{event.modifiers},{event.is_keypad};")

    keyboard.hook(on_key)


def key_press_performer(data, last_time, update_last_time):
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",")
        if not last_time == float(time):
            update_last_time(float(time))
            keyboard.send(name, True, False) if event_type == keyboard.KEY_DOWN else keyboard.send(name, False, True)
        # keyboard.play([keyboard.KeyboardEvent(event_type=event_type,
        #                                       scan_code=int(scan_code),
        #                                       name=name,
        #                                       time=float(time),
        #                                       device=None,
        #                                       modifiers=None,
        #                                       is_keypad=True if is_keypad.__contains__("True") else False)])
    except Exception as e:
        print(f"keyboard : {e}")

