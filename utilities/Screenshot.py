import pygetwindow as gw
import subprocess
import pyautogui
import re


def get_window_rect(window_name):
    try:
        win_id = subprocess.check_output(
            ["xdotool", "search", "--onlyvisible", "--name", window_name]
        ).decode().strip().split('\n')[0]

        subprocess.run(["xdotool", "windowraise", win_id])

        geometry = subprocess.check_output(["xdotool", "getwindowgeometry", win_id]).decode()
        pos = re.search(r"Position:\s+(\d+),(\d+)", geometry)
        size = re.search(r"Geometry:\s+(\d+)x(\d+)", geometry)

        x, y = int(pos.group(1)), int(pos.group(2))
        w, h = int(size.group(1)), int(size.group(2))

        return x, y, w, h
    except Exception as e:
        print(f"Could not locate window '{window_name}': {e}")
        return None


def screenshot_linux():
    rect = get_window_rect("mGBA")
    if rect:
        x, y, width, height = rect
        img = pyautogui.screenshot(region=(x, y, width, height))
        img.save('screenshot.png')


def screenshot_windows():
    windows = gw.getWindowsWithTitle('mGBA')

    if windows:
        win = windows[0]
        win.activate()

        x, y, width, height = win.left, win.top, win.width, win.height

        img = pyautogui.screenshot(region=(x, y, width, height))
        img.save('screenshot.png')
