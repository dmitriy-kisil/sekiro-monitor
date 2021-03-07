import numpy as np
import cv2


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
    x1, y1, x2, y2 = 645, 44, 872, 45
    enemy_concentration = image[y1:y2, x1:x2]
    grid_HSV = cv2.cvtColor(enemy_concentration, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([10, 175, 150])
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
    hero_health_percentage_value = round((mask > 0).mean(), 2)
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
    enemy_health_percentage_value = round((mask > 0).mean(), 2)
    if enemy_health_percentage_value > 0.1:
        cv2.rectangle(image, (x1, y1), (x1 + int((x2 - x1) * enemy_health_percentage_value), y2), (0, 0, 255), 2)
        cv2.line(image, (x1 + int((x2 - x1) * enemy_health_percentage_value), y1 - 10),
                 (x1 + int((x2 - x1) * enemy_health_percentage_value), y2), (0, 0, 255), 2)
    return enemy_health_percentage_value


def check_win(frame, template, done):
    # Convert to gray to better recognizing
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Crop recognition window from frame
    check_win = img_gray[120:410, 510:730]
    # Opencv will try to find pixels, which are similar ot given icon
    res = cv2.matchTemplate(check_win, template, cv2.TM_CCORR_NORMED)
    # You may to play with this value a bit, cause results are sensitive to this value
    threshold = 0.85
    # Remain only those pixels, which contain icon at given threshold
    loc = np.where(res >= threshold)
    if any(loc[0]):
        done = True
    return done


def calc_reward(hero_health, hero_concentration, enemy_health, enemy_concentration, how_much_seconds):
    reward = (hero_health + hero_concentration) - (enemy_health + enemy_concentration)
    reward = reward - (how_much_seconds / 100) if reward > 0 else reward + (how_much_seconds / 100)
    return reward
