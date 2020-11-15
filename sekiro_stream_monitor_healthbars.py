import os
import time
from multiprocessing import Process
import numpy as np
import cv2
import mss
import wave
import win32gui
import pyaudio
import subprocess
from pynput import keyboard


def hero_concentration_percentage(image):
    x1, y1, x2, y2 = 642, 623, 773, 624
    hero_concentration = image[y1:y2, x1:x2]
    grid_HSV = cv2.cvtColor(hero_concentration, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([10, 127, 127])
    upper_orange = np.array([25, 255, 255])
    mask = cv2.inRange(grid_HSV, lower_orange, upper_orange)
    hero_concentration_percentage_value = round(1.0 - (mask > 0).mean(), 2)
    if hero_concentration_percentage_value < 0.95:
        half_distance = x2 - x1
        cv2.rectangle(image, (x1 - int(half_distance * (1.0 - hero_concentration_percentage_value)), y1),
                      (x1 + int(half_distance * (1.0 - hero_concentration_percentage_value)), y2), (0, 0, 255), 2)
        cv2.line(image, (x1 - int(half_distance * (1.0 - hero_concentration_percentage_value)), y1 - 10),
                 (x1 - int(half_distance * (1.0 - hero_concentration_percentage_value)), y2), (0, 0, 255), 2)
        cv2.line(image, (x1 + int(half_distance * (1.0 - hero_concentration_percentage_value)), y1 - 10),
                 (x1 + int(half_distance * (1.0 - hero_concentration_percentage_value)), y2), (0, 0, 255), 2)
    return hero_concentration_percentage_value


def enemy_concentration_percentage(image):
    x1, y1, x2, y2 = 638, 44, 872, 45
    enemy_concentration = image[y1:y2, x1:x2]
    grid_HSV = cv2.cvtColor(enemy_concentration, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([10, 127, 127])
    upper_orange = np.array([25, 255, 255])
    mask = cv2.inRange(grid_HSV, lower_orange, upper_orange)
    enemy_concentration_percentage_value = round(1.0 - (mask > 0).mean(), 2)
    if enemy_concentration_percentage_value < 0.95:
        half_distance = x2 - x1
        cv2.rectangle(image, (x1 - int(half_distance * (1.0 - enemy_concentration_percentage_value)), y1),
                      (x1 + int(half_distance * (1.0 - enemy_concentration_percentage_value)), y2), (0, 0, 255), 2)
        cv2.line(image, (x1 - int(half_distance * (1.0 - enemy_concentration_percentage_value)), y1 - 10),
                 (x1 - int(half_distance * (1.0 - enemy_concentration_percentage_value)), y2), (0, 0, 255), 2)
        cv2.line(image, (x1 + int(half_distance * (1.0 - enemy_concentration_percentage_value)), y1 - 10),
                 (x1 + int(half_distance * (1.0 - enemy_concentration_percentage_value)), y2), (0, 0, 255), 2)
    return enemy_concentration_percentage_value


def hero_health_percentage(image):
    x1, y1, x2, y2 = 75, 655, 460, 656
    hero_healthbar = image[y1:y2, x1:x2]
    grid_HSV = cv2.cvtColor(hero_healthbar, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 127, 75])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(grid_HSV, lower_red, upper_red)
    hero_health_percentage_value = round((mask > 0).mean(), 2) * 100 / 100
    if hero_health_percentage_value > 0.1:
        cv2.rectangle(image, (x1, y1), (x1 + int((x2 - x1) * hero_health_percentage_value), y2), (0, 0, 255), 2)
        cv2.line(image, (x1 + int((x2 - x1) * hero_health_percentage_value), y1 - 10),
                 (x1 + int((x2 - x1) * hero_health_percentage_value), y2), (0, 0, 255), 2)
    return hero_health_percentage_value


def enemy_health_percentage(image):
    x1, y1, x2, y2 = 76, 65, 348, 66
    enemy_healthbar = image[y1:y2, x1:x2]
    grid_HSV = cv2.cvtColor(enemy_healthbar, cv2.COLOR_BGR2HSV)  # Converting to HSV
    lower_red = np.array([0, 127, 75])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(grid_HSV, lower_red, upper_red)
    enemy_health_percentage_value = round((mask > 0).mean() * 100 / 100, 2)
    if enemy_health_percentage_value > 0.1:
        cv2.rectangle(image, (x1, y1), (x1 + int((x2 - x1) * enemy_health_percentage_value), y2), (0, 0, 255), 2)
        cv2.line(image, (x1 + int((x2 - x1) * enemy_health_percentage_value), y1 - 10),
                 (x1 + int((x2 - x1) * enemy_health_percentage_value), y2), (0, 0, 255), 2)
    return enemy_health_percentage_value


def audiohandler(filename):

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second

    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
            if key.char == 'q':
                # Stop listener
                return False
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if 'Stereo Mix' in dev['name']:
            dev_index = dev['index']
            break
    # 10, 19, 22
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    input_device_index=dev_index,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:
        if not listener.running:
            break
        data = stream.read(chunk)
        frames.append(data)
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    # Save the recorded data as a WAV file
    wf = wave.open(f'{filename}.wav', 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def videohandler(filename):
    frame_width = 1280
    frame_height = 720
    frame_rate = 21.0
    fps_calc = []
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'{filename}.avi', fourcc, frame_rate,
                          (frame_width, frame_height))
    with mss.mss() as sct:
        # Part of the screen to capture
        hwnd = win32gui.FindWindow(None, 'Sekiro')
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0] + 8
        y = rect[1] + 32
        w = rect[2] - x - 16
        h = rect[3] - y - 8
        monitor = {"top": y, "left": x, "width": w, "height": h}
        start_time = time.time()
        frames = []
        while True:
            # Time which frame has been captured, need to show how many seconds screen is recorded
            last_time = time.time()
            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(monitor))
            # Resize to better performance
            img = cv2.resize(img, (1280, 720))
            # Without this converting opencv cannot save each frame in a video!
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # Find healthbars percentages:
            hero_health_percentage_value = hero_health_percentage(frame)
            enemy_health_percentage_value = enemy_health_percentage(frame)
            # Find concentrations percentages:
            hero_concentration_percentage_value = hero_concentration_percentage(frame)
            enemy_concentration_percentage_value = enemy_concentration_percentage(frame)
            # Track seconds for screenplay
            how_much_seconds = int(time.time() - start_time)
            # Add variables to screen for easy monitoring
            fps_calc.append(time.time() - last_time)
            cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)),
                        (0, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"How much seconds: {how_much_seconds}", (0, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Hero health: {hero_health_percentage_value * 100} %", (0, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Enemy health: {enemy_health_percentage_value * 100} %", (0, 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Hero concentration: {hero_concentration_percentage_value * 100} %", (0, 190),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Enemy concentration: {enemy_concentration_percentage_value * 100} %", (0, 210),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            frames.append(frame)
            # Show frame to you
            cv2.imshow('frame', frame)
            # Press "q" to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    print('Total frames: ' + str(len(frames)))
    print(f'Total seconds: {time.time() - start_time}')
    print("Avg FPS when recording: " + str(1.0 / (sum(fps_calc) / len(fps_calc))))
    print('Avg FPS when writing to video file: ' + str(len(frames)/(time.time() - start_time)))
    print("Writing frames to video")
    for i in frames:
        out.write(i)
    print("Writing is done!")
    # Clean up
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    filename = "sekiro_output3"
    # You can disable recording audio (currently can not found a way to sync it properly)
    proc2 = Process(target=videohandler, args=(filename,))
    proc1 = Process(target=audiohandler, args=(filename,))
    proc2.start()
    proc1.start()
    proc2.join()
    proc1.join()
    merge_into_movie = f'ffmpeg -y -i {filename}.avi -i {filename}.wav -c copy {filename}.mkv'
    p = subprocess.Popen(merge_into_movie)
    output, _ = p.communicate()
    print(output)
    os.remove(f'{filename}.avi')
    os.remove(f'{filename}.wav')
