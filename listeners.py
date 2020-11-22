from pynput import keyboard, mouse


def on_press_keyboard(key):
    alphanumeric_actions = ['w', 'a', 's', 'd']
    try:
        if key.char in alphanumeric_actions:
            print('alphanumeric key {0} pressed'.format(key.char))
        if key.char == 'q':
            # Stop listener
            return False
    except AttributeError:
        special_actions = [key.shift, key.space]
        if key in special_actions:
            print('special key {0} pressed'.format(
                key))


def create_keyboard_listener():
    keyboard_listener = keyboard.Listener(on_press=on_press_keyboard)
    return keyboard_listener


def create_mouse_listener():
    mouse_listener = mouse.Listener(on_click=on_click_mouse)
    return mouse_listener


def on_click_mouse(x, y, button, pressed):
    mouse_actions = [mouse.Button.left, mouse.Button.right]
    if pressed:
        print(button)
