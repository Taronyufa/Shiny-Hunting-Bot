import cv2
import numpy as np
import os

SCREENSHOT_PATH = "screenshot.png"
SPRITE_PATH = os.path.join("shiny sprites", "charmander.png")
THRESHOLD = 22.5  # tweak based on testing — see calibration notes below


def get_average_color_screenshot(img, gray_tol=10, gray_value_thresh=150):
    """
    Average BGR color of sprite pixels in a screenshot crop.
    Excludes background pixels that are grayscale (R≈G≈B, i.e. white/gray
    stripes) AND reasonably bright — this removes the white background and
    the gray stripe lines, but keeps dark grayscale pixels (like the sprite's
    black outline) since those are part of the sprite.
    """
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
    """Average BGR color of the actual sprite pixels, ignoring background."""
    if img.shape[2] == 4:
        # Has alpha channel -> use only non-transparent pixels
        alpha = img[:, :, 3]
        mask = alpha > 10
    else:
        # No alpha -> exclude near-white background pixels
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

    print(f"Current avg color (BGR): {current_color}")
    print(f"Shiny avg color (BGR): {shiny_color}")
    print(f"Color distance: {distance:.2f} (threshold: {threshold})")

    return distance < threshold


if __name__ == "__main__":
    try:
        result = is_shiny(SCREENSHOT_PATH, SPRITE_PATH)
        print(result)
    finally:
        if os.path.exists(SCREENSHOT_PATH):
            pass  # os.remove(SCREENSHOT_PATH)
