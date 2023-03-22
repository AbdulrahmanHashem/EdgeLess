import mouse


""" listeners """


def listen_to_lc(send=None):
    def on_click(event):
        # print(event)
        send(event)

    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOWN}, {mouse.LEFT};"]), buttons=mouse.LEFT, types=mouse.DOWN)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.UP}, {mouse.LEFT};"]), buttons=mouse.LEFT, types=mouse.UP)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOUBLE}, {mouse.LEFT};"]), buttons=mouse.LEFT, types=mouse.DOUBLE)


def listen_to_rc(send=None):
    def on_click(event):
        # print(event)
        send(event)

    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOWN}, {mouse.RIGHT};"]), buttons=mouse.RIGHT, types=mouse.DOWN)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.UP}, {mouse.RIGHT};"]), buttons=mouse.RIGHT, types=mouse.UP)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOUBLE}, {mouse.RIGHT};"]), buttons=mouse.RIGHT, types=mouse.DOUBLE)


def listen_to_mc(send=None):
    def on_click(event):
        # print(event)
        send(event)

    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOWN}, {mouse.MIDDLE};"]), buttons=mouse.RIGHT, types=mouse.DOWN)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.UP},  {mouse.MIDDLE};"]), buttons=mouse.RIGHT, types=mouse.UP)
    mouse.on_button(on_click, args=([f"ButtonEvent, {mouse.DOUBLE}, {mouse.MIDDLE};"]), buttons=mouse.RIGHT, types=mouse.DOUBLE)


def listen_to_mm(cxy) -> str | None:
    x, y = mouse.get_position()
    return f"MoveEvent, {x}, {y};" if x != cxy[0] or y != cxy[1] else None


""" mouse event executors """


def perform_lc():
    pass


def perform_rc():
    pass


def perform_mm():
    pass


# mouse.play([mouse.ButtonEvent(event_type=x, button=y, time=0)], 0)