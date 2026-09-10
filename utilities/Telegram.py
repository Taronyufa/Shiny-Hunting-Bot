import time

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

import telegram_send
import asyncio

from utilities.Constant import SCREENSHOT_PATH, CROP_PATH
from utilities.Controller import Controller
import utilities.Screenshot as Sc


def fight_commands(gamepad):

    gp = Controller(gamepad)

    load_dotenv()
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    stop = False

    async def a(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        gp.press_a()
        Sc.screenshot_windows()
        await update.message.reply_text(text="Command sent")

    async def b(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        gp.press_b()
        Sc.screenshot_windows()
        await update.message.reply_text(text="Command sent")

    async def up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        gp.press_up()
        Sc.screenshot_windows()
        await update.message.reply_text(text="Command sent")

    async def down(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        gp.press_down()
        Sc.screenshot_windows()
        await update.message.reply_text(text="Command sent")

    async def right(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        gp.press_right()
        await update.message.reply_text(text="Command sent")

    async def left(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        gp.press_left()
        await update.message.reply_text(text="Command sent")

    async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        gp.press_a()
        time.sleep(3)
        gp.run()
        time.sleep(1)
        gp.press_a()
        time.sleep(1.5)
        await update.message.reply_text(text="Command sent")

    async def screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        Sc.screenshot_windows()
        await update.message.reply_photo(photo = SCREENSHOT_PATH)

    async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.application.stop_running()

    async def stops(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        nonlocal stop
        stop = True
        context.application.stop_running()

    app = ApplicationBuilder().token(telegram_bot_token).build()

    app.add_handler(CommandHandler("a", a))
    app.add_handler(CommandHandler("b", b))
    app.add_handler(CommandHandler("up", up))
    app.add_handler(CommandHandler("down", down))

    app.add_handler(CommandHandler("right", right))
    app.add_handler(CommandHandler("left", left))

    app.add_handler(CommandHandler("run", run))

    app.add_handler(CommandHandler("screen", screen))

    app.add_handler(CommandHandler("resume", resume))
    app.add_handler(CommandHandler("stop", stops))

    # Blocks main thread till context.application.stop_running() is called
    app.run_polling()

    return stop

def send_message(index):
    with open(SCREENSHOT_PATH, "rb") as file:
        asyncio.run(telegram_send.send(images=[file], captions=[f'Shiny Fount at Try {index}']))

