import os
import subprocess
from threading import Thread, Event
from listeners import create_mouse_listener, create_keyboard_listener
from collect_episodes import *
from handlers import audiohandler, videohandler


if __name__ == "__main__":
    filename = "sekiro_output3"
    event = Event()
    # You can disable recording audio (currently can not found a way to sync it properly)
    audio_thread = Thread(target=audiohandler, args=(filename, event))
    video_thread = Thread(target=videohandler, args=(filename, event))
    keyboard_listener = create_keyboard_listener()
    mouse_listener = create_mouse_listener()
    keyboard_listener.start()
    mouse_listener.start()
    audio_thread.start()
    video_thread.start()
    audio_thread.join()
    video_thread.join()
    while True:
        if event.isSet():
            # mouse and keyboard listeners will be stopped at this point
            break
    merge_into_movie = f'ffmpeg -y -i {filename}.avi -i {filename}.wav -c copy {filename}.mkv'
    p = subprocess.Popen(merge_into_movie)
    output, _ = p.communicate()
    print(output)
    os.remove(f'{filename}.avi')
    os.remove(f'{filename}.wav')
