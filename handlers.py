import time
import mss
import wave
import win32gui
import pyaudio
from monitoring_stats import *


def audiohandler(filename, event, episode_path):

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(dev)
        if 'Stereo Mix' in dev['name']:
            dev_index = dev['index']
            break

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    input_device_index=dev_index,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames
    count = 0
    prev_sec = round(time.time())
    l1 = []
    while not event.isSet():
        curr_sec = round(time.time())
        if curr_sec == prev_sec:
            count += 1
            data = stream.read(chunk)
            l1.append(data)
            # frames.append(data)
        else:
            # print(f"Count: {count}")
            count = 0
            data = stream.read(chunk)
            l1.append(data)
            for i in l1:
                frames.append(i)
            l1 = []
            prev_sec = curr_sec
        # curr_sec = round(time.time())
        # if curr_sec != prev_sec:
        #     prev_sec = curr_sec
        #     count += 1
        # if count % 600 == 0:
        #     print('miss one frame')
        #     data = stream.read(chunk)
        #     frames.append(data)
    print(len(frames))
    print(int(len(frames)//44))
    how_much = len(frames) - 44*int(len(frames)//44)
    print(how_much)
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


def videohandler(filename, event, episode_path):
    frame_width = 1280
    frame_height = 720
    frame_rate = 30.0
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
        prev_sec = round(time.time())
        count = 0
        another_count = 0
        third_count = 0
        done = False
        # Load image, which will be trying to find
        template = cv2.imread('win.PNG', 0)
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
            # Calculate reward:
            reward = calc_reward(hero_health_percentage_value, hero_concentration_percentage_value,
                                 enemy_health_percentage_value, enemy_concentration_percentage_value,
                                 how_much_seconds)
            # Check if done:
            done = check_win(frame, template, done)
            # Add variables to screen for easy monitoring
            fps_calc.append(time.time() - last_time)
            cv2.putText(frame, "FPS: %.0f" % (1.0 / (time.time() - last_time)),
                        (0, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"How much seconds: {how_much_seconds}", (0, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Hero health: {hero_health_percentage_value * 100:.0f} %", (0, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Enemy health: {enemy_health_percentage_value * 100:.0f} %", (0, 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Hero concentration: {hero_concentration_percentage_value * 100:.0f} %", (0, 190),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Enemy concentration: {enemy_concentration_percentage_value * 100:.0f} %", (0, 210),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Done: {done}", (0, 230),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            curr_sec = round(last_time)
            if curr_sec == prev_sec:
                count += 1
                if count < frame_rate:
                    out.write(frame)
                else:
                    another_count += 1
                    # time.sleep(0.01)
            else:
                out.write(frame)
                count = 0
                prev_sec = curr_sec
                third_count += 1
                # time.sleep(0.018)
            res_img = cv2.resize(img, (64, 64))
            res_img = np.array(res_img)
            curr_time = time.time()
            spend = curr_time - start_time
            if spend > 1:
                interval = int(30 / (1 / (spend - int(spend)))) + 1
            else:
                interval = int(30 / (1 / spend)) + 1

            # with open(f'{episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_frame.npy', 'wb') as f:
            #     np.save(f, res_img)
            # stats = np.array([hero_health_percentage_value, hero_concentration_percentage_value,
            #                   enemy_health_percentage_value, enemy_concentration_percentage_value, reward, done])
            # with open(f'{episode_path}/{str(how_much_seconds).zfill(6)}_{interval}_states.npy', 'wb') as f:
            #     np.save(f, stats)
            # Show frame to you
            cv2.imshow('frame', frame)
            # Press "q" to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                event.set()
                break
    print('Total frames: ' + str(len(frames)))
    print(f'Total seconds: {time.time() - start_time}')
    print("Avg FPS when recording: " + str(1.0 / (sum(fps_calc) / len(fps_calc))))
    print(another_count)
    print(third_count)
    # Clean up
    out.release()
    cv2.destroyAllWindows()
