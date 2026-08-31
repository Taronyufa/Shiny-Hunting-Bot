# Python libraries
import vgamepad as vg
import numpy as np
import threading
import time
import cv2
import csv
import os

# Python Classes
from utilities.Controller import Controller
from utilities import Screenshot as Sc

gamepad = vg.VX360Gamepad()
SCREENSHOT_PATH = "screenshot.png"
SPRITE_PATH = os.path.join("shiny sprites", "charmander.png")
THRESHOLD = 22.5


def main():

    routine = get_routine()


    with open(os.path.join("csv", "stats.csv"), "r") as f:
        reader = csv.reader(f)
        row = next(reader)

        i = int(row[0])
        failed = int(row[1])

    gp = Controller(gamepad)

    stop_event = threading.Event()
    listener_thread = threading.Thread(target=listen_for_stop, args=(stop_event,), daemon=True)
    listener_thread.start()

    print("Virtual controller connected. Starting in 3 seconds...")

    time.sleep(3)

    while not stop_event.is_set():

        for elem in routine:
            match elem:
                case "a":
                    gp.press_a()
                case "b":
                    gp.press_b()
                case "reset":
                    gp.soft_reset()
                case "summary":
                    gp.summary()
                case _:
                    time.sleep(float(elem))

        time.sleep(1.5)

        Sc.screenshot_windows()

        result, distance = is_shiny(SCREENSHOT_PATH, SPRITE_PATH)

        if result:
            break
        else:
            if distance > 80:
                failed += 1
            else:
                i += 1
            print(f'{result} on try {i} with {failed} failed encounters\n\n')
            if os.path.exists(SCREENSHOT_PATH):
                os.remove(SCREENSHOT_PATH)

    stats = [i, failed]
    with open(os.path.join("csv", "stats.csv"), "w") as f:
        writer = csv.writer(f)
        writer.writerow(stats)


def listen_for_stop(stop_event):
    input("Press ENTER to stop the loop\n")
    stop_event.set()


def get_routine():
    dictionary = {}

    with open(os.path.join("csv", "routines.csv"), "r") as f:
        routines = csv.reader(f)
        next(routines)
        for row in routines:
            dictionary[row[0]] = row[1]

    routine = -1
    while isinstance(routine, int):
        print("\nChoose which routine to use:")

        i = 1
        for keys in dictionary.keys():
            print(f'\t{i}. {keys}')
            i += 1

        routine = int(input()) - 1
        if routine >= 0 and routine < len(dictionary):
            routine = list(dictionary.values())[routine]
        else:
            print("The number does not correspond to any routine")

    routine = routine.split()
    return routine

def get_average_color_screenshot(img, gray_tol=10, gray_value_thresh=150):

    b, g, r = img[:, :, 0].astype(int), img[:, :, 1].astype(int), img[:, :, 2].astype(int)
    channel_spread = np.maximum(np.maximum(b, g), r) - np.minimum(np.minimum(b, g), r)
    value = np.maximum(np.maximum(b, g), r)

    is_grayscale = channel_spread <= gray_tol
    is_bright = value >= gray_value_thresh
    background_mask = is_grayscale & is_bright

    mask = ~background_mask
    pixels = img[:, :, :3][mask]
    if len(pixels) == 0:
        return None
    return pixels.mean(axis=0)


def get_average_color(img):
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        mask = alpha > 10
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = gray < 245

    pixels = img[:, :, :3][mask]

    if len(pixels) == 0:
        return None
    return pixels.mean(axis=0)


def get_sprite_crop(screenshot):
    h, w = screenshot.shape[:2]
    x1, y1 = int(.15 * w), int(0.35 * h)
    x2, y2 = int(0.35 * w), int(0.50 * h)
    return screenshot[y1:y2, x1:x2]


def is_shiny(screenshot_path, shiny_sprite_path, threshold=THRESHOLD):
    screenshot = cv2.imread(screenshot_path, cv2.IMREAD_UNCHANGED)
    shiny_sprite = cv2.imread(shiny_sprite_path, cv2.IMREAD_UNCHANGED)

    if screenshot is None:
        raise FileNotFoundError(f"Could not read {screenshot_path}")
    if shiny_sprite is None:
        raise FileNotFoundError(f"Could not read {shiny_sprite_path}")

    crop = get_sprite_crop(screenshot)

    current_color = get_average_color_screenshot(crop)
    shiny_color = get_average_color(shiny_sprite)

    if current_color is None or shiny_color is None:
        raise ValueError("Could not extract sprite pixels — check crop coordinates or sprite image")

    distance = np.linalg.norm(current_color[:3] - shiny_color[:3])

    print(f"Color distance: {distance:.2f} (threshold: {threshold})")

    return distance < threshold, distance


if __name__ == "__main__":

    while True:

        print("\nChoose an option:\n\t1. Take the screenshot\n\t2. Crop the screenshot\n\t3. Compute the "
              "distance\n\t4. Close the program\n\t5. Start the loop\n")
        x = input("Insert the number: ")

        match x:
            case "1":
                Sc.screenshot_windows()
            case "2":
                img = cv2.imread("screenshoot.png")
                crop = get_sprite_crop(img)
                cv2.imwrite("debug_crop.png",crop)
            case "3":
                is_shiny(SCREENSHOT_PATH, SPRITE_PATH)
            case "4":
                # noinspection PyProtectedMember
                os._exit(0)
            case "5":
                main()
                # noinspection PyProtectedMember
                os._exit(0)
