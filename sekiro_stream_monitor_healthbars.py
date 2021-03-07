import os
import subprocess
import shutil
from threading import Thread, Event
from listeners import create_mouse_listener, create_keyboard_listener
# from collect_episodes import *
from handlers import audiohandler, videohandler


if __name__ == "__main__":
    # if os.path.exists('episodes'):
    #     shutil.rmtree('episodes')
    # else:
    #     os.mkdir('episodes')
    filename = "sekiro_output3"
    event = Event()
    episodes_available = [int(item) for item in os.listdir('episodes') if os.path.isdir(os.path.join('episodes', item))]
    if episodes_available:
        next_episode = max(episodes_available) + 1
    else:
        next_episode = 0
    os.mkdir('episodes/' + str(next_episode))
    episode_path = 'episodes/' + str(next_episode)
    # print('wait')
    # time.sleep(3.0)
    # print('started')
    # You can disable recording audio (currently can not found a way to sync it properly)
    audio_thread = Thread(target=audiohandler, args=(filename, event, episode_path))
    video_thread = Thread(target=videohandler, args=(filename, event, episode_path))
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
