from scipy import ndimage
from PIL import Image
import numpy as np
import os.path
import cv2

from shiny_hunting_bot.utilities.Constant import *


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

        return bx, by, bw, bh, image, True
    else:
        return 0, 0, 0, 0, 0, False

def crop_pokemon_summary():

    bx, by, bw, bh, image, check = find_pokemon_summary()

    if not check:
        return False

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

    return True

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

def is_shiny_summary():

    if not crop_pokemon_summary():
        return False
    distance = color_distance(median(CROP_PATH), median(SHINY_PATH))
    if distance > THRESHOLD:
        if os.path.exists(CROP_PATH) and os.path.exists(SCREENSHOT_PATH):
            os.remove(CROP_PATH)
            os.remove(SCREENSHOT_PATH)
        print(f'Distance = {distance}')
        return False
    else:
        print(f'Distance = {distance}')
        return True

def is_battle() -> bool:
    img = cv2.imread(SCREENSHOT_PATH)
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    row_means = gray.mean(axis=1)
    col_means = gray.mean(axis=0)

    brightness_threshold = 15

    valid_y = np.where(row_means > brightness_threshold)[0]
    valid_x = np.where(col_means > brightness_threshold)[0]

    if len(valid_y) == 0 or len(valid_x) == 0:
        return False

    y_segments = np.split(valid_y, np.where(np.diff(valid_y) > 1)[0] + 1)
    x_segments = np.split(valid_x, np.where(np.diff(valid_x) > 1)[0] + 1)

    gy1, gy2 = max(y_segments, key=len)[[0, -1]]
    gx1, gx2 = max(x_segments, key=len)[[0, -1]]

    gba_screen = img[gy1:gy2, gx1:gx2]
    if gba_screen.shape[0] == 0 or gba_screen.shape[1] == 0:
        return False

    gba = cv2.resize(gba_screen, (240, 160), interpolation=cv2.INTER_NEAREST)

    top_left_roi = gba[10:50, 10:110]
    white_card_pixels = np.sum(np.all(top_left_roi > 200, axis=2))

    hsv_top = cv2.cvtColor(top_left_roi, cv2.COLOR_BGR2HSV)
    green_hp = cv2.inRange(hsv_top, np.array([35, 100, 100]), np.array([85, 255, 255]))
    yellow_hp = cv2.inRange(hsv_top, np.array([15, 100, 100]), np.array([35, 255, 255]))
    red_hp = cv2.inRange(hsv_top, np.array([0, 100, 100]), np.array([10, 255, 255]))
    hp_bar_pixels = (
        cv2.countNonZero(green_hp) + cv2.countNonZero(yellow_hp) + cv2.countNonZero(red_hp)
    )

    bottom_roi = gba[112:155, 10:230]
    blue_bg_mask = cv2.inRange(bottom_roi, np.array([70, 50, 20]), np.array([125, 100, 70]))
    blue_pixels = cv2.countNonZero(blue_bg_mask)
    gold_border_mask = cv2.inRange(bottom_roi, np.array([60, 150, 200]), np.array([140, 230, 255]))
    gold_pixels = cv2.countNonZero(gold_border_mask)

    has_enemy_card = (white_card_pixels > 80) and (hp_bar_pixels > 3)
    has_battle_frame = (blue_pixels > 300) and (gold_pixels > 15)

    return has_enemy_card or (white_card_pixels > 50 and has_battle_frame)

def crop_pokemon_textbox():
    img = Image.open(SCREENSHOT_PATH).convert("RGB")
    w, h = img.size
    arr = np.asarray(img)

    gray = arr.mean(axis=2)
    row_means = gray.mean(axis=1)
    col_means = gray.mean(axis=0)
    brightness_threshold = 15

    valid_y = np.where(row_means > brightness_threshold)[0]
    valid_x = np.where(col_means > brightness_threshold)[0]
    if len(valid_y) == 0 or len(valid_x) == 0:
        return

    y_segments = np.split(valid_y, np.where(np.diff(valid_y) > 1)[0] + 1)
    x_segments = np.split(valid_x, np.where(np.diff(valid_x) > 1)[0] + 1)
    gy1, gy2 = max(y_segments, key=len)[[0, -1]]
    gx1, gx2 = max(x_segments, key=len)[[0, -1]]
    gw, gh = gx2 - gx1, gy2 - gy1
    if gw <= 0 or gh <= 0:
        return

    box = (gx1, gy1 + int(gh * 0.71), gx2, gy2)

    return img.crop(box)

def mask_textbox_white():

    img = crop_pokemon_textbox()
    arr = np.asarray(img)
    h, w, _ = arr.shape

    white_mask = np.all(arr > 200, axis=2)

    labeled, num = ndimage.label(white_mask)
    objects = ndimage.find_objects(labeled)

    keep_labels = []
    for i, sl in enumerate(objects, start=1):
        if sl is None:
            continue
        comp_h = sl[0].stop - sl[0].start
        comp_w = sl[1].stop - sl[1].start
        if comp_w > w * 0.5 or comp_h > h * 0.5:
            continue
        keep_labels.append(i)

    text_only = np.isin(labeled, keep_labels) & white_mask

    out = (text_only.astype(np.uint8) * 255)
    return Image.fromarray(out)

def is_shiny_fight() -> bool:
    img = mask_textbox_white().convert("RGB")
    arr = np.asarray(img)

    white_mask = np.all(arr > 200, axis=2)
    white_count = int(white_mask.sum())

    if(white_count >= 400) and os.path.exists(SCREENSHOT_PATH):
        os.remove(SCREENSHOT_PATH)

    print(f'Number of White Pixel = {white_count}')
    return white_count <= 400
