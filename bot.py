from telethon import TelegramClient, events, __version__
from telethon.tl import types
from datetime import date, datetime
from vars import SESSION, API_HASH, API_ID, BOT_TOKEN, LOG_CHANNEL, PORT, ADMINS
from typing import Union, Optional, AsyncGenerator
from script import scripts
from utils import temp_utils
from database.data_base import db
from aiohttp import web
from plugins.functions import gather_task
from plugins import web_server
import logging
import pytz
import logging.config

#Get logging configuration
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("telethon").setLevel(logging.ERROR)

async def fetch_from_db(bot):
    try:
        users = await db.get_forwarding()
        await gather_task(bot, users)
    except Exception as e:
        logging.exception(e)
        for admin in ADMINS:
            await bot.send_message(
                entity=int(admin),
                message=f"Error: Starting Pending Forwards || {e}"
            )

class Bot(TelegramClient):

    def __init__(self, **kwargs):
        super().__init__(
            SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            **kwargs
        )

    async def start_bot(self):
        await super().start(bot_token=BOT_TOKEN)
        me = await self.get_me()
        temp_utils.ME = me.id
        temp_utils.USER_NAME = me.username
        temp_utils.BOT_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Telethon v{__version__} (Layer {layer}) started on {me.username}.")
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(entity=LOG_CHANNEL, message=scripts.RESTART_TXT.format(today, time))
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        await fetch_from_db(self)


    async def stop_bot(self, *args):
        await super().disconnect()
        logging.info("Bot stopped. Bye.")

app = Bot()

# load plugins
import plugins.callbacks
import plugins.commands

app.run_until_disconnected()
