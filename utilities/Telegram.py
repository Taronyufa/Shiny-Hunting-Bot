import telegram_send
import asyncio

from Constant import SCREENSHOT_PATH

def send_message(index):
    with open(SCREENSHOT_PATH, "rb") as file:
        asyncio.run(telegram_send.send(images=[file], captions=[f'Shiny Fount at Try {index}']))

