from utils import temp_utils
from database.data_base import db
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto, MessageMediaVideo
import logging
import asyncio
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

async def start_forward(bot, userid, skip):
    util = temp_utils.UTILS.get(int(userid))
    if util is not None:
        source_chat_id = util.get('source_chat_id')
        last_msg_id = util.get('last_msg_id')
        TARGET_DB = util.get('target_chat_id')
    else:
        user = await db.get_user(int(userid))
        if user and user['on_process'] and not user['is_complete']:
            source_chat_id = user['source_chat']
            last_msg_id = user['last_msg_id']
            TARGET_DB = user['target_chat']
        else:
            return
    btn = [
        [Button.inline("CANCEL", data="cancel_forward")]
    ]
    active_msg = await bot.send_message(
        entity=int(userid),
        message="<b>Starting Forward Process...</b>",
        buttons=btn
    )
    skipped = int(skip)
    total = 0
    forwarded = 0
    empty = 0
    notmedia = 0
    unsupported = 0
    left = 0
    status = 'Idle'
    async with lock:
        try:
            btn = [
                [Button.inline("CANCEL", data="cancel_forward")]
            ]
            status = 'Forwarding...'
            await active_msg.edit(
                text=f"<b>Forwarding on progress...\n\nTotal: {total}\nSkipped: {skipped}\nForwarded: {forwarded}\nEmpty Message: {empty}\nNot Media: {notmedia}\nUnsupported Media: {unsupported}\nMessages Left: {left}\n\nStatus: {status}</b>",
                buttons=btn
            )
            current = int(skip)
            temp_utils.CANCEL[int(userid)] = False
            await db.update_any(userid, 'on_process', True)
            await db.update_any(userid, 'is_complete', False)
            async for msg in bot.iter_messages(source_chat_id, limit=int(last_msg_id), offset_id=int(skip)):
                if temp_utils.CANCEL.get(int(userid)):
                    status = 'Cancelled !'
                    await active_msg.edit(f"<b>Successfully Cancelled!\n\nTotal: {total}\nSkipped: {skipped}\nForwarded: {forwarded}\nEmpty Message: {empty}\nNot Media: {notmedia}\nUnsupported Media: {unsupported}\nMessages Left: {left}\n\nStatus: {status}</b>")
                    break
                total = current
                left = int(last_msg_id)-int(total)
                current += 1
                if current % 20 == 0:
                    btn = [
                        [Button.inline("CANCEL", data="cancel_forward")]
                    ]
                    await db.update_any(userid, 'fetched', total)
                    status = 'Sleeping for 30 seconds.'
                    await active_msg.edit(
                        text=f"<b>Forwarding on progress...\n\nTotal: {total}\nSkipped: {skipped}\nForwarded: {forwarded}\nEmpty Message: {empty}\nNot Media: {notmedia}\nUnsupported Media: {unsupported}\nMessages Left: {left}\n\nStatus: {status}</b>",
                        buttons=btn
                    )
                    await asyncio.sleep(30)
                    status = 'Forwarding...'
                    await active_msg.edit( 
                        text=f"<b>Forwarding on progress...\n\nTotal: {total}\nSkipped: {skipped}\nForwarded: {forwarded}\nEmpty Message: {empty}\nNot Media: {notmedia}\nUnsupported Media: {unsupported}\nMessages Left: {left}\n\nStatus: {status}</b>", 
                        buttons=btn
                    )
                if msg.text is None and msg.media is None:
                    empty+=1
                    continue
                elif not msg.media:
                    notmedia += 1
                    continue
                elif not isinstance(msg.media, (MessageMediaDocument, MessageMediaPhoto, MessageMediaVideo)):
                    unsupported += 1
                    continue
                try:
                    await msg.copy_to(
                        int(TARGET_DB)
                    )
                    forwarded+=1
                    await asyncio.sleep(1)
                except FloodWaitError as e:
                    btn = [
                        [Button.inline("CANCEL", data="cancel_forward")]
                    ]
                    await active_msg.edit(
                        text=f"<b>Got FloodWait.\n\nWaiting for {e.seconds} seconds.</b>",
                        buttons=btn
                    )
                    await asyncio.sleep(e.seconds)
                    await msg.copy_to(
                        int(TARGET_DB)
                    )
                    forwarded+=1
                    continue
            status = 'Completed !'
        except Exception as e:
            logger.exception(e)
            await active_msg.edit(f'<b>Error:</b> <code>{e}</code>')
        else:
            await db.update_any(userid, 'on_process', False)
            await db.update_any(userid, 'is_complete', True)
            await active_msg.edit(f"<b>Successfully Completed Forward Process !\n\nTotal: {total}\nSkipped: {skipped}\nForwarded: {forwarded}\nEmpty Message: {empty}\nNot Media: {notmedia}\nUnsupported Media: {unsupported}\nMessages Left: {left}\n\nStatus: {status}</b>")

async def gather_task(bot, users):
    tasks = []
    for user in users:
        task = asyncio.create_task(start_forward(bot, user['id'], user['fetched']))
        tasks.append(task)
    await asyncio.gather(*tasks)