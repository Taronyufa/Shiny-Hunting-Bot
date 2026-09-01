from PIL import Image
import numpy as np
import cv2
import os


THRESHOLD = 40
SHINY_PATH = os.path.join("shiny sprites", "charmander.png")
SCREENSHOT_PATH = "screenshot.png"
CROP_PATH = "crop.png"


def find_pokemon_summary():

    image = cv2.imread(SCREENSHOT_PATH)
    h, w, _ = image.shape

    mid_x = w // 2
    col_pixels = np.sum(image[:, mid_x, :], axis=1)
    valid_y = np.where(col_pixels > 30)[0]

    y_segments = np.split(valid_y, np.where(np.diff(valid_y) > 1)[0] + 1)
    gba_y = max(y_segments, key=len)
    gy1, gy2 = gba_y[0], gba_y[-1]

    mid_y = gy1 + (gy2 - gy1) // 2
    row_pixels = np.sum(image[mid_y, :, :], axis=1)
    valid_x = np.where(row_pixels > 30)[0]

    x_segments = np.split(valid_x, np.where(np.diff(valid_x) > 1)[0] + 1)
    gba_x = max(x_segments, key=len)
    gx1, gx2 = gba_x[0], gba_x[-1]

    gw, gh = gx2 - gx1, gy2 - gy1
    px1, px2 = gx1 + int(gw * 0.02), gx1 + int(gw * 0.48)
    py1, py2 = gy1 + int(gh * 0.20), gy1 + int(gh * 0.62)

    roi = image[py1:py2, px1:px2]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(roi_gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    roi_h, roi_w = roi.shape[:2]
    best_box = None
    max_area = 0

    for c in contours:
        area = cv2.contourArea(c)
        x, y, bw, bh = cv2.boundingRect(c)
        if 500 < area < (roi_h * roi_w * 0.7) and bw < (roi_w * 0.8) and bh < (roi_h * 0.9):
            if area > max_area:
                max_area = area
                best_box = (px1 + x, py1 + y, bw, bh)

    if best_box:
        bx, by, bw, bh = best_box

        bx -= 5
        by -= 5
        bw += 10
        bh += 10

        return bx, by, bw, bh, image

def crop_pokemon():

    bx, by, bw, bh, image = find_pokemon_summary()

    pokemon_crop = image[by:by + bh, bx:bx + bw]
    crop_gray = cv2.cvtColor(pokemon_crop, cv2.COLOR_BGR2GRAY)

    _, crop_thresh = cv2.threshold(crop_gray, 210, 255, cv2.THRESH_BINARY_INV)
    crop_contours, _ = cv2.findContours(crop_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    alpha_mask = np.zeros(crop_gray.shape, dtype=np.uint8)
    for c in crop_contours:
        if cv2.contourArea(c) > 0.06:
            cv2.drawContours(alpha_mask, [c], -1, 255, thickness=cv2.FILLED)

    b, g, r = cv2.split(pokemon_crop)
    pokemon_bgra = cv2.merge([b, g, r, alpha_mask])

    cv2.imwrite('crop.png', pokemon_bgra)


def median(photo_path):
    with Image.open(photo_path) as img:
        img_rgba = img.convert("RGBA")
        pixels = np.array(img_rgba)

    alpha = pixels[:, :, 3]
    mask = alpha > 10

    sprite_pixels = pixels[mask]
    if len(sprite_pixels) == 0:
        return None

    r_med = int(np.median(sprite_pixels[:, 0]))
    g_med = int(np.median(sprite_pixels[:, 1]))
    b_med = int(np.median(sprite_pixels[:, 2]))

    return (r_med, g_med, b_med)

def color_distance(c1, c2):
    return np.linalg.norm(np.array(c1) - np.array(c2))

def is_shiny():
    crop_pokemon()
    distance = color_distance(median(CROP_PATH), median(SHINY_PATH))
    if distance > THRESHOLD:
        if os.path.exists(CROP_PATH) and os.path.exists(SCREENSHOT_PATH):
            os.remove(CROP_PATH)
            os.remove(SCREENSHOT_PATH)
        print(f'Distance = {distance}')
        return False
    else:
        return True

