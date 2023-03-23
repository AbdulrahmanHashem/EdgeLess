import keyboard


def listen_for_all_keys(send):
    """ Keyboard Key Events Listener """
    def on_key(event: keyboard.KeyboardEvent):
        send(f"keyboard,{event.event_type},{event.scan_code},{event.name},{event.time},{event.device},{event.modifiers},{event.is_keypad};")

    keyboard.hook(on_key)


def key_press_performer(data, last_time, update_last_time):
    """ Keyboard Key Events executor """
    try:
        event, event_type, scan_code, name, time, device, modifiers, is_keypad = data.split(",")
        if not last_time == float(time):
            update_last_time(float(time))
            keyboard.send(name, True, False) if event_type == keyboard.KEY_DOWN else keyboard.send(name, False, True)
    except Exception as e:
        print(f"keyboard : {e}")

