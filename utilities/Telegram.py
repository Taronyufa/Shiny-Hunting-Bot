import telegram_send
import asyncio

def send_message():
    asyncio.run(telegram_send.send(messages=["Shiny Trovato"]))