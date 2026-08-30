import time
import vgamepad as vg
import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import os

gamepad = vg.VX360Gamepad()
windows = gw.getWindowsWithTitle('mGBA')
SCREENSHOT_PATH = "screenshot.png"
SPRITE_PATH = os.path.join("shiny sprites", "charmander.png")
THRESHOLD = 22.5


def main():
    i = 458
    failed = 12

    print("Virtual controller connected. Starting in 3 seconds...")

    time.sleep(3)

    while(True):

        soft_reset()

        # Open the game
        time.sleep(3.5)
        press_A()

        time.sleep(.2)
        press_A()

        time.sleep(.2)
        press_A()

        time.sleep(3)
        press_A()

        time.sleep(1)
        press_B()

        time.sleep(2.4)
        press_A()

        time.sleep(.8)
        press_A()

        time.sleep(1)
        press_A()

        time.sleep(.6)
        press_A()

        time.sleep(.9)
        press_A()

        time.sleep(4.2)
        press_B()

        time.sleep(2)
        press_A()

        time.sleep(3.4)
        summary()

        time.sleep(1.5)

        screenshot()

        result, distance = is_shiny(SCREENSHOT_PATH, SPRITE_PATH)

        if(result):
            break
        else:
            if(distance > 80):
                failed += 1
            else:
                i += 1
            print(f'{result} on try {i} with {failed} failed encounters\n\n')
            if os.path.exists(SCREENSHOT_PATH):
                os.remove(SCREENSHOT_PATH)


import subprocess
import re
import pyautogui

def get_window_rect(window_name="mGBA"):
    try:
        win_id = subprocess.check_output(
            ["xdotool", "search", "--onlyvisible", "--name", window_name]
        ).decode().strip().split('\n')[0]

        subprocess.run(["xdotool", "windowactivate", win_id])

        geometry = subprocess.check_output(["xdotool", "getwindowgeometry", win_id]).decode()
        pos = re.search(r"Position:\s+(\d+),(\d+)", geometry)
        size = re.search(r"Geometry:\s+(\d+)x(\d+)", geometry)

        x, y = int(pos.group(1)), int(pos.group(2))
        w, h = int(size.group(1)), int(size.group(2))

        return x, y, w, h
    except Exception as e:
        print(f"Could not locate window '{window_name}': {e}")
        return None

def screenshot():
    rect = get_window_rect("mGBA")
    if rect:
        x, y, width, height = rect
        img = pyautogui.screenshot(region=(x, y, width, height))
        img.save('screenshot.png')

def soft_reset():
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

    gamepad.update()
    time.sleep(.1)

    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

    gamepad.update()

def summary():

    press_START()

    time.sleep(.2)
    press_A()

    time.sleep(.9)
    press_A()

    time.sleep(.3)
    press_A()

def press_A():
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(.1)

    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()

def press_B():
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.update()
    time.sleep(.1)

    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.update()

def press_START():
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    gamepad.update()
    time.sleep(.1)

    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    gamepad.update()

def press_BACK():
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    gamepad.update()
    time.sleep(.1)

    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    gamepad.update()

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
    main()