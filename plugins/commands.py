from telethon import events
from telethon.tl.types import User
from telethon.tl.custom import Button
from utils import temp_utils
from script import scripts
from vars import ADMINS
from database.data_base import db
import logging
from bot import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.on(events.NewMessage(pattern='/start'))
async def start_message(event):
    user = await db.is_user_exist(event.sender_id)
    if not user:
        sender = await event.get_sender()
        if isinstance(sender, User):
            await db.new_user(event.sender_id, sender.first_name, sender.username)
    btn = [
        [Button.inline("About", data="about"), Button.inline("Souce Code", data="source")],
        [Button.inline("Close", data="close"), Button.inline("Help", data="help")]
    ]
    await event.reply(
        message=scripts.START_TXT.format(event.sender.first_name, temp_utils.USER_NAME, temp_utils.BOT_NAME),
        buttons=btn
    )

@app.on(events.NewMessage(pattern='/logs', from_users=ADMINS))
async def log_file(event):
    """Send log file"""
    try:
        await event.reply(file='Logs.txt')
    except Exception as e:
        await event.reply(str(e))

@app.on(events.NewMessage(pattern='/setskip', from_users=ADMINS))
async def skip_msgs(event):
    if ' ' in event.text:
        _, skip = event.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await event.reply("Skip number should be an integer.")
        await db.update_any(event.sender_id, 'skip', int(skip))
        await event.reply(f"Successfully set SKIP number as {skip}")
        temp_utils.CURRENT = int(skip)
    else:
        await event.reply("Give me a skip number")

@app.on(events.NewMessage(pattern='/set_target'))
async def set_target(event):
    content = event.text
    try:
        target_id = content.split(" ", 1)[1]
    except:
        return await event.reply(
            message="<b>Hey give a channel ID where I'm admin along with the command !</b>"
        )
    try:
        target_id = int(target_id)
    except:
        return await event.reply(
            message="Give me a valid chat ID"
        )
    if target_id and target_id is not None:
        await db.update_any(event.sender_id, 'target_chat', int(target_id))
        return await event.reply(
            message=f"Successfully set target chat ID to {target_id}"
        )
    else:
        return await event.reply(
            message="Give me a valid chat ID"
        )
