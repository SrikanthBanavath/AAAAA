from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import STREAM_MODE, URL, LOG_CHANNEL
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
import humanize
import random

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
    if STREAM_MODE == False:
        return 
    msg = await client.ask(message.chat.id, "**Now send me your file/video to get stream and download link**")
    if not msg.media:
        return await message.reply("**Please send me supported media.**")
    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        user_id = message.from_user.id
        username =  message.from_user.mention 

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        fileName = {quote_plus(get_name(log_msg))}
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
 
        await log_msg.reply_text(
            text=f"•• Link Generated For #{user_id} \n•• UserName : {username} \n\n•• FileName : {fileName}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲", url=stream),  # we download Link
                                                InlineKeyboardButton('𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱⚡️', url=download)]])  # web stream Link
        )
        rm=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🖥𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲", url=stream),
                    InlineKeyboardButton('𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱⚡️', url=download)
                ]
            ] 
        )
        msg_text = """<b>Link Generated⚡️</b>"""

        await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
