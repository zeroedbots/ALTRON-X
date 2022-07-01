import asyncio
import os
import re
from random import choice
from pyrogram import filters
from pyrogram.types import Message
import ffmpeg
import requests
from os import path
from modules.clientbot import clientbot, queues
from modules.clientbot.clientbot import client as USER
from modules import converter
from config import que, SUDO_USERS
from modules.helpers.gets import get_file_name
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream


aud_list = [
    ./modules/AUDIO1.mp3,
    ./modules/AUDIO2.mp3,
]



@USER.on_message(filters.user(SUDO_USERS) & filters.command(["vcraid"], ["/", "!", "."]))
async def vcraid(_, e: Message):
    gid = e.chat.id
    uid = e.from_user.id
    inp = e.text.split(None, 2)[1]
    chat = await USER.get_chat(inp)
    chat_id = chat.id
    aud = choice(aud_list) 

    if inp:
         lel = await e.reply_text("**processing**")
         audio = (
         (e.reply_to_message.audio or e.reply_to_message.voice)
         if e.reply_to_message
         else None
         )

         if audio:
             file_name = get_file_name(audio)
             file_path = await converter.convert(
                  (await e.reply_to_message.download(file_name))
                  if not path.isfile(path.join("downloads", file_name))
                  else file_name
             ) 

         ACTV_CALLS = []
         for x in clientbot.pytgcalls.active_calls:
             ACTV_CALLS.append(int(x.chat_id))
         if int(chat_id) in ACTV_CALLS:
             position = await queues.put(chat_id, file=file_path)
             await lel.edit("**💥 Ʌɗɗɘɗ 💿 Søɳʛ❗️\n🔊 Ʌʈ 💞 Ƥøsɩʈɩøɳ » `{}` 🌷 ...**".format(position),
         )
         else:
             await clientbot.pytgcalls.join_group_call(
                     chat_id, 
                     InputStream(
                         InputAudioStream(
                             file_path,
                         ),
                     ),
                     stream_type=StreamType().local_stream,
                 )

             await lel.edit("**💥 Mʋsɩƈ 🎸 Nøω 💞\n🔊 Ƥɭɑyɩɳʛ 😍 ØƤ 🥀 ...**".format(),
             )

    
    
