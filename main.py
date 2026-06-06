# ═══════════════════════════════════════
#        Standard Library
# ═══════════════════════════════════════
import os
import re
import sys
import time
import json
import random
import string
import shutil
import zipfile
import urllib
import asyncio
import subprocess
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from subprocess import getstatusoutput

# ═══════════════════════════════════════
#        Third-party Libraries
# ═══════════════════════════════════════
import pytz
import aiohttp
import aiofiles
import requests
import ffmpeg
import m3u8
import cloudscraper
import yt_dlp
import tgcrypto
from bs4 import BeautifulSoup
from pytube import YouTube
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ═══════════════════════════════════════
#        Pyrogram
# ═══════════════════════════════════════
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)
from pyrogram.errors import (
    FloodWait,
    BadRequest,
    Unauthorized,
    SessionExpired,
    AuthKeyDuplicated,
    AuthKeyUnregistered,
    ChatAdminRequired,
    PeerIdInvalid,
    RPCError
)
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

# ═══════════════════════════════════════
#        Bot Modules
# ═══════════════════════════════════════
import auth
import itsgolu as helper
from html_handler import html_handler
from itsgolu import *
from clean import register_clean_handler
from logs import logging
from utils import progress_bar
from vars import *

import pyromod.listen
pyromod.listen.Client.listen = pyromod.listen.listen

from db import db

# ═══════════════════════════════════════
#        Global Variables
# ═══════════════════════════════════════
auto_flags = {}
auto_clicked = False
watermark = "/d"
count = 0
userbot = None
timeout_duration = 300

# ═══════════════════════════════════════
#        Bot Init
# ═══════════════════════════════════════
bot = Client(
    "ugx",
    api_id=33891184,
    api_hash=ba3af95840d1746b1bc0609cddb5800d,
    bot_token=8872760790:AAHsvubcuEXr_LsDYLaeKn_D_iL60XQ5qNc,
    workers=300,
    sleep_threshold=60,
    in_memory=True
)

register_clean_handler(bot)

# ═══════════════════════════════════════
#        Config
# ═══════════════════════════════════════
cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
cwtoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTExOTcwNjQsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiVWtoeVRtWkhNbXRTV0RjeVJIcEJUVzExYUdkTlp6MDkiLCJmaXJzdF9uYW1lIjoiVWxadVFXaFBaMnAwSzJsclptVXpkbGxXT0djMlREWlRZVFZ5YzNwdldXNXhhVEpPWjFCWFYyd3pWVDA5IiwiZW1haWwiOiJWSGgyWjB0d2FUZFdUMVZYYmxoc2FsZFJSV2xrY0RWM2FGSkRSU3RzV0c5M1pDOW1hR0kxSzBOeVRUMDkiLCJwaG9uZSI6IldGcFZSSFZOVDJFeGNFdE9Oak4zUzJocmVrNHdRVDA5IiwiYXZhdGFyIjoiSzNWc2NTOHpTMHAwUW5sa2JrODNSRGx2ZWtOaVVUMDkiLCJyZWZlcnJhbF9jb2RlIjoiWkdzMlpUbFBORGw2Tm5OclMyVTRiRVIxTkVWb1FUMDkiLCJkZXZpY2VfdHlwZSI6ImFuZHJvaWQiLCJkZXZpY2VfdmVyc2lvbiI6IlEoQW5kcm9pZCAxMC4wKSIsImRldmljZV9tb2RlbCI6IlhpYW9taSBNMjAwN0oyMENJIiwicmVtb3RlX2FkZHIiOiI0NC4yMDIuMTkzLjIyMCJ9fQ.ONBsbnNwCQQtKMK2h18LCi73e90s2Cr63ZaIHtYueM-Gt5Z4sF6Ay-SEaKaIf1ir9ThflrtTdi5eFkUGIcI78R1stUUch_GfBXZsyg7aVyH2wxm9lKsFB2wK3qDgpd0NiBoT-ZsTrwzlbwvCFHhMp9rh83D4kZIPPdbp5yoA_06L0Zr4fNq3S328G8a8DtboJFkmxqG2T1yyVE2wLIoR3b8J3ckWTlT_VY2CCx8RjsstoTrkL8e9G5ZGa6sksMb93ugautin7GKz-nIz27pCr0h7g9BCoQWtL69mVC5xvVM3Z324vo5uVUPBi1bCG-ptpD9GWQ4exOBk9fJvGo-vRg"

photologo = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'
photoyt   = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'
photocp   = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'
photozip  = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'

BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url="https://t.me/ITsGOLU_OWNER_BOT")]])
keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="🛠️ Help", url="https://t.me/ITsGOLU_OWNER_BOT")]])

image_urls = [
    "https://i.ibb.co/v6Vr7HCt/1000003297.png",
    "https://i.ibb.co/v6Vr7HCt/1000003297.png",
    "https://i.ibb.co/v6Vr7HCt/1000003297.png",
]

# ═══════════════════════════════════════
#        Auth Handlers
# ═══════════════════════════════════════
bot.add_handler(MessageHandler(auth.add_user_cmd,    filters.command("add")    & filters.private))
bot.add_handler(MessageHandler(auth.remove_user_cmd, filters.command("remove") & filters.private))
bot.add_handler(MessageHandler(auth.list_users_cmd,  filters.command("users")  & filters.private))
bot.add_handler(MessageHandler(auth.my_plan_cmd,     filters.command("plan")   & filters.private))

# ═══════════════════════════════════════
#        Auth Filter
# ═══════════════════════════════════════
def auth_check_filter(_, client, message):
    try:
        if message.chat.type == "channel":
            return db.is_channel_authorized(message.chat.id, client.me.username)
        else:
            return db.is_user_authorized(message.from_user.id, client.me.username)
    except Exception:
        return False

auth_filter = filters.create(auth_check_filter)

# ═══════════════════════════════════════
#        Commands
# ═══════════════════════════════════════
@bot.on_message(filters.command("setlog") & filters.private)
async def set_log_channel_cmd(client: Client, message: Message):
    try:
        if not db.is_admin(message.from_user.id):
            await message.reply_text("⚠️ You are not authorized.")
            return
        args = message.text.split()
        if len(args) != 2:
            await message.reply_text("❌ Use: /setlog channel_id\nExample: /setlog -100123456789")
            return
        try:
            channel_id = int(args[1])
        except ValueError:
            await message.reply_text("❌ Invalid channel ID.")
            return
        if db.set_log_channel(client.me.username, channel_id):
            await message.reply_text(f"✅ Log channel set!\nChannel ID: {channel_id}\nBot: @{client.me.username}")
        else:
            await message.reply_text("❌ Failed. Try again.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


@bot.on_message(filters.command("getlog") & filters.private)
async def get_log_channel_cmd(client: Client, message: Message):
    try:
        if not db.is_admin(message.from_user.id):
            await message.reply_text("⚠️ Not authorized.")
            return
        channel_id = db.get_log_channel(client.me.username)
        if channel_id:
            try:
                channel = await client.get_chat(channel_id)
                channel_info = f"📢 Channel: {channel.title}\n"
            except:
                channel_info = ""
            await message.reply_text(
                f"**📋 Log Channel**\n\n🤖 Bot: @{client.me.username}\n{channel_info}🆔 ID: `{channel_id}`"
            )
        else:
            await message.reply_text(f"**📋 Log Channel**\n\n❌ Not set\nUse /setlog to set one.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text("Please upload the cookies file (.txt format).", quote=True)
    try:
        input_message: Message = await client.listen(m.chat.id)
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file. Please upload a .txt file.")
            return
        downloaded_path = await input_message.download()
        with open(downloaded_path, "r") as f:
            cookies_content = f.read()
        with open(cookies_file_path, "w") as f:
            f.write(cookies_content)
        await input_message.reply_text("✅ Cookies updated!\n📂 Saved in `youtube_cookies.txt`.")
    except Exception as e:
        await m.reply_text(f"⚠️ Error: {str(e)}")


@bot.on_message(filters.command("getcookies") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        await client.send_document(chat_id=m.chat.id, document=cookies_file_path,
                                   caption="Here is `youtube_cookies.txt`.")
    except Exception as e:
        await m.reply_text(f"⚠️ Error: {str(e)}")


@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    editable = await message.reply_text(
        "<blockquote>Welcome! Send the **text** to convert into a `.txt` file.</blockquote>"
    )
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.text:
        await message.reply_text("**Send valid text data**")
        return
    text_data = input_message.text.strip()
    await input_message.delete()
    await editable.edit("**🔄 Send file name or /d for default name**")
    inputn: Message = await bot.listen(message.chat.id)
    raw_textn = inputn.text
    await inputn.delete()
    await editable.delete()
    custom_file_name = 'txt_file' if raw_textn == '/d' else raw_textn
    txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
    with open(txt_file, 'w') as f:
        f.write(text_data)
    await message.reply_document(document=txt_file,
                                 caption=f"`{custom_file_name}.txt`\n\n<blockquote>Download your content! 📥</blockquote>")
    os.remove(txt_file)


@bot.on_message(filters.command(["stop"]))
async def restart_handler(_, m):
    await m.reply_text("🚦 **STOPPED**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command("start") & (filters.private | filters.channel))
async def start(bot: Client, m: Message):
    try:
        if m.chat.type == "channel":
            if not db.is_channel_authorized(m.chat.id, bot.me.username):
                return
            await m.reply_text(
                "**✨ Bot is active in this channel**\n\n"
                "• /drm - Download DRM videos\n• /plan - View subscription"
            )
        else:
            is_authorized = db.is_user_authorized(m.from_user.id, bot.me.username)
            is_admin = db.is_admin(m.from_user.id)
            if not is_authorized:
                await m.reply_photo(
                    photo=photologo,
                    caption="**Mʏ Nᴀᴍᴇ [DRM Wɪᴢᴀʀᴅ 🦋](https://t.me/ITsGOLU_OWNER_BOT)\n\n"
                            "Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ\n"
                            "Cᴏɴᴛᴀᴄᴛ [𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®](https://t.me/ITsGOLU_OWNER_BOT) ғᴏʀ ᴀᴄᴄᴇꜱꜱ**",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")],
                        [InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇꜱ 🪔", callback_data="features"),
                         InlineKeyboardButton("ᴅᴇᴛᴀɪʟꜱ 🦋", callback_data="details")]
                    ])
                )
                return
            commands_list = (
                "**>  /drm - ꜱᴛᴀʀᴛ ᴜᴘʟᴏᴀᴅɪɴɢ ᴄᴘ/ᴄᴡ ᴄᴏᴜʀꜱᴇꜱ**\n"
                "**>  /plan - ᴠɪᴇᴡ ʏᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ**\n"
            )
            if is_admin:
                commands_list += "\n**👑 Admin:**\n• /users - List users\n"
            await m.reply_photo(
                photo=photologo,
                caption=f"**Mʏ ᴄᴏᴍᴍᴀɴᴅꜱ [{m.from_user.first_name}](tg://settings)**\n\n{commands_list}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")],
                    [InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇꜱ 🪔", callback_data="features"),
                     InlineKeyboardButton("ᴅᴇᴛᴀɪʟꜱ 🦋", callback_data="details")]
                ])
            )
    except Exception as e:
        print(f"Start error: {str(e)}")


@bot.on_message(~auth_filter & filters.private & filters.command)
async def unauthorized_handler(client, message: Message):
    await message.reply(
        "<b>Mʏ Nᴀᴍᴇ [DRM Wɪᴢᴀʀᴅ 🦋](https://t.me/ITsGOLU_OWNER_BOT)</b>\n\n"
        "<blockquote>You need an active subscription.\nContact admin for premium access.</blockquote>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("💫 Get Premium Access", url="https://t.me/ITsGOLU_OWNER_BOT")
        ]])
    )


@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    await message.reply_text(f"<blockquote>Chat ID:</blockquote>\n`{message.chat.id}`")


@bot.on_message(filters.command(["t2h"]))
async def call_html_handler(bot: Client, message: Message):
    await html_handler(bot, message)


@bot.on_message(filters.command(["logs"]) & auth_filter)
async def send_logs(client: Client, m: Message):
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending logs...**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error:**\n<blockquote>{e}</blockquote>")


# ═══════════════════════════════════════
#        /drm — Main Upload Handler
# ═══════════════════════════════════════
@bot.on_message(filters.command(["drm"]) & auth_filter)
async def txt_handler(bot: Client, m: Message):
    bot_info = await bot.get_me()
    bot_username = bot_info.username

    if m.chat.type == "channel":
        if not db.is_channel_authorized(m.chat.id, bot_username):
            return
    else:
        if not db.is_user_authorized(m.from_user.id, bot_username):
            await m.reply_text("❌ Not authorized.")
            return

    editable = await m.reply_text(
        "__Hii, I am DRM Downloader Bot__\n"
        "<blockquote><i>Send your .txt file with Name: URL format\n"
        "E.g: Lecture 1: https://example.com/video.mp4\n</i></blockquote>\n"
        "<blockquote><i>All input auto-taken in 20 sec</i></blockquote>"
    )

    input: Message = await bot.listen(editable.chat.id)

    if not input.document:
        await m.reply_text("<b>❌ Please send a text file!</b>")
        return
    if not input.document.file_name.endswith('.txt'):
        await m.reply_text("<b>❌ Please send a .txt file!</b>")
        return

    x = await input.download()
    await bot.send_document(OWNER_ID, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    path = f"./downloads/{m.chat.id}"

    pdf_count = img_count = v2_count = mpd_count = 0
    m3u8_count = yt_count = drm_count = zip_count = other_count = 0

    try:
        with open(x, "r", encoding='utf-8') as f:
            content = f.read()

        content = content.split("\n")
        content = [line.strip() for line in content if line.strip()]

        links = []
        for i in content:
            # ✅ FIX: ": " पर split करो ताकि URL टूटे नहीं
            if ": " in i and "://" in i:
                parts = i.split(": ", 1)
                name = parts[0].strip()
                url = parts[1].strip()
            elif "://" in i:
                name = f"File_{len(links)+1}"
                url = i.strip()
            else:
                continue

            links.append([name, url])

            if ".pdf" in url:
                pdf_count += 1
            elif url.endswith((".png", ".jpeg", ".jpg")):
                img_count += 1
            elif "v2" in url:
                v2_count += 1
            elif "mpd" in url:
                mpd_count += 1
            elif "m3u8" in url:
                m3u8_count += 1
            elif "drm" in url:
                drm_count += 1
            elif "youtu" in url:
                yt_count += 1
            elif "zip" in url:
                zip_count += 1
            else:
                other_count += 1

    except UnicodeDecodeError:
        await m.reply_text("<b>❌ File encoding error! Save file as UTF-8.</b>")
        os.remove(x)
        return
    except Exception as e:
        await m.reply_text(f"<b>🔹 Error reading file: {str(e)}</b>")
        os.remove(x)
        return

    await editable.edit(
        f"**Total 🔗 Links: {len(links)}\n"
        f"ᴘᴅғ: {pdf_count}   ɪᴍɢ: {img_count}   ᴠ𝟸: {v2_count}\n"
        f"ᴢɪᴘ: {zip_count}   ᴅʀᴍ: {drm_count}   ᴍ𝟹ᴜ𝟾: {m3u8_count}\n"
        f"ᴍᴘᴅ: {mpd_count}   ʏᴛ: {yt_count}   Oᴛʜᴇʀ: {other_count}\n\n"
        f"Send Index (1-{len(links)})**"
    )

    chat_id = editable.chat.id
    timeout_duration = 3 if auto_flags.get(chat_id) else 20

    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1'

    if not raw_text.isdigit() or int(raw_text) > len(links):
        await editable.edit(f"**🔹 Enter number between 1-{len(links)}**")
        await m.reply_text("**🔹 Exiting...**")
        return

    await editable.edit("**1. Enter Batch Name\n2. Send /d for TXT file name**")

    try:
        input1: Message = await bot.listen(editable.chat.id, timeout=20)
        raw_text1 = input1.text
        await input1.delete(True)
    except asyncio.TimeoutError:
        raw_text1 = '/d'

    batch_name = file_name if raw_text1 == '/d' else raw_text1

    await editable.edit("**Enter Resolution (144/240/360/480/720/1080)\nor /d for 720p**")

    try:
        input2: Message = await bot.listen(editable.chat.id, timeout=20)
        res_text = input2.text
        await input2.delete(True)
    except asyncio.TimeoutError:
        res_text = '/d'

    CR = '720' if res_text == '/d' else res_text

    await editable.edit("**Send Channel ID to upload\nor /d to upload here**")

    try:
        input3: Message = await bot.listen(editable.chat.id, timeout=20)
        ch_text = input3.text
        await input3.delete(True)
    except asyncio.TimeoutError:
        ch_text = '/d'

    channel_id = m.chat.id if ch_text == '/d' else int(ch_text)

    await editable.edit("**Enter Watermark text\nor /d for default**")

    try:
        input4: Message = await bot.listen(editable.chat.id, timeout=20)
        wm_text = input4.text
        await input4.delete(True)
    except asyncio.TimeoutError:
        wm_text = '/d'

    watermark_text = "𝐈𝐓'𝐬𝐆𝐎𝐋𝐔" if wm_text == '/d' else wm_text

    start_index = int(raw_text) - 1
    os.makedirs(path, exist_ok=True)

    await editable.edit(f"**✅ Starting from index {start_index + 1}...**")

    for i, (name, url) in enumerate(links[start_index:], start=start_index + 1):
        prog = await m.reply_text(f"**Processing {i}/{len(links)}:**\n`{name}`")

        try:
            if url.endswith(".pdf") or ".pdf" in url:
                file_path = f"{path}/{name}.pdf"
                await helper.pdf_download(url, file_path)
                await bot.send_document(channel_id, file_path, caption=f"`{name}`")
                if os.path.exists(file_path):
                    os.remove(file_path)

            elif url.endswith((".png", ".jpeg", ".jpg")):
                await bot.send_photo(channel_id, url, caption=f"`{name}`")

            elif "youtu" in url:
                await prog.edit(f"**📥 Downloading YouTube:\n`{name}`**")
                ydl_opts = {
                    'format': f'bestvideo[height<={CR}]+bestaudio/best',
                    'outtmpl': f'{path}/{name}.%(ext)s',
                    'merge_output_format': 'mp4',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                file_path = f"{path}/{name}.mp4"
                if os.path.exists(file_path):
                    await helper.send_vid(bot, m, f"`{name}`", file_path, "/d",
                                          name, prog, channel_id, watermark_text)

            else:
                await prog.edit(f"**📥 Downloading:\n`{name}`**")
                cmd = f'yt-dlp -f "bv[height<={CR}]+ba/b" -o "{path}/{name}.%(ext)s" "{url}"'
                result = await helper.download_video(url, cmd, f"{path}/{name}.mp4")
                if result and os.path.exists(result):
                    await helper.send_vid(bot, m, f"`{name}`", result, "/d",
                                          name, prog, channel_id, watermark_text)
                else:
                    await m.reply_text(f"❌ Failed: `{name}`")

        except Exception as e:
            await m.reply_text(f"❌ Error on `{name}`:\n`{str(e)}`")
            logging.error(f"Error on {name}: {str(e)}")

        finally:
            try:
                await prog.delete()
            except:
                pass

    await m.reply_text(f"**✅ Done! All {len(links) - start_index} files processed.**")
    if os.path.exists(x):
        os.remove(x)
