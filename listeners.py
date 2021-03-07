import os
import time
import numpy as np
from pynput import keyboard, mouse

start_time = time.time()


def on_press_keyboard(key):
    episodes_available = [int(item) for item in os.listdir('episodes') if os.path.isdir(os.path.join('episodes', item))]
    if episodes_available:
        next_episode = max(episodes_available)
    else:
        next_episode = 0
    episode_path = 'episodes/' + str(next_episode)
    curr_time = time.time()
    global start_time
    spend = curr_time - start_time
    how_much_seconds = int(curr_time - start_time)
    if spend > 1:
        interval = int(30 / (1 / (spend - int(spend)))) + 1
    else:
        interval = int(30 / (1 / spend)) + 1
    actions = [0, 0, 0, 0, 0, 0]
    alphanumeric_actions = ['w', 'a', 's', 'd']
    try:
        special_actions = {key.shift: 'shift', key.space: 'space'}
        if key in special_actions.keys():
            print('special key {0} pressed'.format(
                key))
            actions[list(special_actions.keys()).index(key) + len(alphanumeric_actions)] = 1
        if key.char in alphanumeric_actions:
            print('alphanumeric key {0} pressed'.format(key.char))
            actions[alphanumeric_actions.index(key)] = 1
        # print(f'Save {"".join([str(i) for i in actions])} as {episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_keyboard.npy')
        with open(f'{episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_keyboard.npy', 'wb') as f:
            np.save(f, np.array(actions))
        if key.char == 'q':
            # Stop listener
            return False
    except AttributeError:
        # print(f'Save {"".join([str(i) for i in actions])} as {episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_keyboard.npy')
        with open(f'{episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_keyboard.npy', 'wb') as f:
            np.save(f, np.array(actions))


def create_keyboard_listener():
    keyboard_listener = keyboard.Listener(on_press=on_press_keyboard)
    return keyboard_listener


def create_mouse_listener():
    mouse_listener = mouse.Listener(on_click=on_click_mouse)
    return mouse_listener


def on_click_mouse(x, y, button, pressed):
    episodes_available = [int(item) for item in os.listdir('episodes') if os.path.isdir(os.path.join('episodes', item))]
    if episodes_available:
        next_episode = max(episodes_available)
    else:
        next_episode = 0
    episode_path = 'episodes/' + str(next_episode)
    curr_time = time.time()
    global start_time
    spend = curr_time - start_time
    how_much_seconds = int(curr_time - start_time)
    if spend > 1:
        interval = int(30 / (1 / (spend - int(spend)))) + 1
    else:
        interval = int(30 / (1 / spend)) + 1
    actions = [0, 0]
    mouse_actions = {mouse.Button.left: 'leftclick', mouse.Button.right: 'rightclick'}
    if pressed and button in mouse_actions.keys():
        actions[list(mouse_actions.keys()).index(button)] = 1
        # print(f'Save {"".join([str(i) for i in actions])} as {episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_mouse.npy')
        with open(f'{episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_mouse.npy', 'wb') as f:
            np.save(f, np.array(actions))
