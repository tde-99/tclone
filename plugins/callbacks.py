from telethon import events
from telethon.tl.custom import Button
from script import scripts
from utils import temp_utils
import logging
from database.data_base import db
from .functions import start_forward
from bot import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@app.on(events.CallbackQuery)
async def query_handler(event):
    data = event.data.decode()
    if data == "close":
        await event.message.delete()
    elif data == "about":
        btn = [
            [Button.inline("Go Back", data="home"), Button.inline("Close", data="close")]
        ]
        await event.edit(
            text=scripts.ABOUT_TXT.format(temp_utils.BOT_NAME),
            buttons=btn
        )
    elif data == "home":
        btn = [
            [Button.inline("About", data="about"), Button.inline("Souce Code", data="source")],
            [Button.inline("Close", data="close"), Button.inline("Help", data="help")]
        ]
        await event.edit(
            text=scripts.START_TXT.format(event.sender.first_name, temp_utils.USER_NAME, temp_utils.BOT_NAME),
            buttons=btn
        )
    elif data == "source":
        btn = [
            [Button.inline("Go Back", data="home"), Button.inline("Close", data="close")]
        ]
        await event.edit(
            text=scripts.SOURCE_TXT,
            buttons=btn
        )
    elif data == "cancel_forward":
        temp_utils.CANCEL[event.sender_id] = True
        await event.answer("Cancelling Process !\n\nIf the bot is sleeping, It will cancell only after the sleeping is over !", alert=True)
    elif data == "help":
        btn = [
            [Button.inline("Go Back", data="home"), Button.inline("Close", data="close")]
        ]
        await event.edit(
            text=scripts.HELP_TXT.format(temp_utils.BOT_NAME),
            buttons=btn
        )
    elif data.startswith("forward"):
        ident, userid = data.split("#")
        if event.sender_id != int(userid):
            return await event.answer("You can't touch this !", alert=True)
        user = await db.get_user(int(userid))
        await event.message.delete()
        await start_forward(app, userid, user['skip'])
