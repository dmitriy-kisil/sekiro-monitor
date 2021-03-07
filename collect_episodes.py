import os
import time
import numpy as np

done = False
reward = -0.1

framerate = 30
# start = time.time()
# time.sleep(0.01)
# spend = time.time() - start
# print(spend)
# spend = 35.47
# if spend > 1:
#     interval = int(30 / (1 / (spend - int(spend)))) + 1
# else:
#     interval = int(30 / (1 / spend)) + 1
# print(interval)
# episodes_available = [int(item) for item in os.listdir('episodes') if os.path.isdir(os.path.join('episodes', item))]
# print(episodes_available)
# if episodes_available:
#     next_episode = max(episodes_available) + 1
# else:
#     next_episode = 0
# print(next_episode)
episodes_available = [int(item) for item in os.listdir('episodes') if os.path.isdir(os.path.join('episodes', item))]
if episodes_available:
    next_episode = max(episodes_available)
else:
    next_episode = 0
episode_path = 'episodes/' + str(next_episode)
episode_files = os.listdir(episode_path)
episode_files.sort()
print(episode_files)
last_second = int(episode_files[-1].split("_")[0])
print(last_second)
for second in range(0, last_second+1):
    for subsecond in range(1, framerate+1):
        try:
            print(f'{episode_path}/{second}_{subsecond}')
            actions = [0, 0, 0, 0, 0, 0, 0, 0]
            second = str(second).zfill(6)
            frame = np.load(f'{episode_path}/{second}_{subsecond}_frame.npy')
            os.remove(f'{episode_path}/{second}_{subsecond}_frame.npy')
            stats = np.load(f'{episode_path}/{second}_{subsecond}_states.npy')
            reward, done = stats[-2], stats[-1]
            stats = stats[:-1]
            os.remove(f'{episode_path}/{second}_{subsecond}_states.npy')
            if os.path.exists(f'{episode_path}/{second}_{subsecond}_mouse.npy'):
                mouse_actions = np.load(f'{episode_path}/{second}_{subsecond}_mouse.npy')
                os.remove(f'{episode_path}/{second}_{subsecond}_mouse.npy')
                actions[6:] = mouse_actions
            if os.path.exists(f'{episode_path}/{second}_{subsecond}_keyboard.npy'):
                keyboard_actions = np.load(f'{episode_path}/{second}_{subsecond}_keyboard.npy')
                os.remove(f'{episode_path}/{second}_{subsecond}_keyboard.npy')
                actions[:6] = keyboard_actions
            actions = np.array(actions)
            reward = np.array(reward)
            done = np.array(done)
            np.savez(f'{episode_path}/{second}_{subsecond}_full', frame=frame,
                     stats=stats, actions=actions, reward=reward, done=done)
        except Exception as e:
            if os.path.exists(f'{episode_path}/{second}_{subsecond}_mouse.npy'):
                os.remove(f'{episode_path}/{second}_{subsecond}_mouse.npy')
            if os.path.exists(f'{episode_path}/{second}_{subsecond}_keyboard.npy'):
                os.remove(f'{episode_path}/{second}_{subsecond}_keyboard.npy')
            print(e)

episode_files = os.listdir(episode_path)
episode_files.sort()
path_to_last_file = os.path.join(episode_path, episode_files[-1])
print(f'Load last file: {path_to_last_file}')
with np.load(path_to_last_file) as data:
    frame = data['frame']
    stats = data['stats']
    actions = data['actions']
    reward = data['reward']
    done = data['done']
print(stats, actions, reward, done)
