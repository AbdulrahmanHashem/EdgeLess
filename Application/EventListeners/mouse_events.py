import mouse


""" listeners """

def listen_to_all_clicks_and_wheel(send, cxy, update_mouse_loc):
    def on_event(event):
        # print(event)
        if isinstance(event, mouse.ButtonEvent):
            send(f"ButtonEvent, {event.event_type}, {event.button}, {event.time};")
        elif isinstance(event, mouse.WheelEvent):
            send(f"WheelEvent, {event.delta}, {event.time};")
        elif isinstance(event, mouse.MoveEvent):
            if event.x != cxy[0] or event.y != cxy[1]:
                send(f"MoveEvent, {event.x}, {event.y}, {event.time};")
                update_mouse_loc([event.x, event.y])

    mouse.hook(on_event)


""" mouse event executors """


def mouse_event_performer(data, screen_ratio):
    """ Mouse event handler """
    try:
        if data.__contains__("Move"):
            button, x, y, t = data.split(",")
            mouse.play([mouse.MoveEvent(
                x=int(x) * screen_ratio,
                y=int(y) * screen_ratio,
                time=t)], 0)

        elif data.__contains__("Button"):
            button, x, y, t = data.split(",")
            try:
                mouse.play([mouse.ButtonEvent(event_type=x.strip(), button=y.strip(), time=t)], 0)
            except Exception as e:
                print(e)
        else:
            button, delta, t = data.split(",")
            try:
                mouse.play([mouse.WheelEvent(delta=float(delta.strip()), time=float(t.strip()))])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
