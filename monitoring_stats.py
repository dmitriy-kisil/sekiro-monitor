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
    lower_orange = np.array([10, 175, 175])
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
        cv2.line(image, (x1, y1 + 10), (x2, y2 + 10), (0, 0, 255), 2)
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
