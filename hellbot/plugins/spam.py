import asyncio

from ..sql.gvar_sql import addgvar, delgvar, gvarstat
from . import *


async def spam(event, msg, count, reply_to, delay, bspam, uspam, media):
    chat = (await event.get_chat()).title
    if media:
        what = "MEDIA_SPAM"
        for i in range(count):
            if not gvarstat("SPAM"):
                return
            await event.client.send_file(event.chat_id, media)
    elif uspam:
        what = "UNLIMITED_SPAM"
        while count == 69:
            if not gvarstat("SPAM"):
                count += 1
                continue
            await event.client.send_message(event.chat_id, msg, reply_to=reply_to)
        count = "∞"
    elif bspam:
        what = "BREAK_SPAM"
        x = int(count % 100)
        y = int((count - x) / 100)
        a = 30
        for i in range(y):
            for j in range(100):
                if not gvarstat("SPAM"):
                    return
                await event.client.send_message(event.chat_id, msg, reply_to=reply_to)
            a += 2
            await asyncio.sleep(a)
    elif delay:
        what = "DELAY_SPAM"
        for i in range(count):
            if not gvarstat("SPAM"):
                return
            await event.client.send_message(event.chat_id, msg, reply_to=reply_to)
            await asyncio.sleep(delay)
    else:
        what = "SPAM"
        for i in range(count):
            if not gvarstat("SPAM"):
                return
            await event.client.send_message(event.chat_id, msg, reply_to=reply_to)

    await event.client.send_message(
        Config.LOGGER_ID,
        f"#{what} \n\n**Spammed** `{count}` **messages in** {chat}")


@hell_cmd(pattern="spam(?:\s|$)([\s\S]*)")
async def spammer(event):
    reply_to = await event.get_reply_message()
    hell = event.text[6:]
    count = int(hell.split(" ", 1)[0])
    msg = str(hell.split(" ", 1)[1]) or reply_to
    addgvar("SPAM", "True")
    await spam(event, msg, count, reply_to, None, None, None, None)


@hell_cmd(pattern="dspam(?:\s|$)([\s\S]*)")
async def dspam(event):
    reply_to = await event.get_reply_message()
    hell = event.text[7:]
    delay = int(hell.split(" ", 2)[0])
    count = int(hell.split(" ", 2)[1])
    msg = str(hell.split(" ", 2)[2]) or reply_to
    addgvar("SPAM", "True")
    await spam(event, msg, count, reply_to, delay, None, None, None)


@hell_cmd(pattern="uspam(?:\s|$)([\s\S]*)")
async def uspam(event):
    reply_to = await event.get_reply_message()
    hell = event.text[7:]
    msg = hell or reply_to
    addgvar("SPAM", "True")
    await spam(event, msg, 69, reply_to, None, None, True, None)


# Special Break Spam Module For HellBot Made By Chirag Bhargava.
# Team HellBot
@hell_cmd(pattern="bspam(?:\s|$)([\s\S]*)")
async def bspam(event):
    reply_to = await event.get_reply_message()
    hell = event.text[7:]
    count = int(hell.split(" ", 1)[0])
    msg = str(hell.split(" ", 1)[1]) or reply_to
    addgvar("SPAM", "True")
    await spam(event, msg, count, reply_to, None, True, None, None)


@hell_cmd(pattern="mspam(?:\s|$)([\s\S]*)")
async def mspam(event):
    reply_to = await event.get_reply_message()
    hell = event.text[7:]
    count = int(hell.split(" ", 1)[0])
    if not reply_to and not reply_to.media:
        return await eod(event, "Reply to a pic/gif/video/sticker to spam.")
    media = reply_to.media
    addgvar("SPAM", "True")
    await spam(event, None, count, reply_to, None, None, None, media)


@hell_cmd(pattern="endspam$")
async def spamend(event):
    if gvarstat("SPAM"):
        delgvar("SPAM")
        await eod(event, "Spam Terminated !!")
    else:
        await eod(event, "Nothing is spamming!!")


CmdHelp("spam").add_command(
    "spam", "<number> <text>", "Sends the text 'X' number of times.", "spam 99 Hello"
).add_command(
    "mspam", "<reply to media> <number>", "Sends the replied media (gif/ video/ sticker/ pic) 'X' number of times", "mspam 100 <reply to media>"
).add_command(
    "dspam", "<delay> <spam count> <text>", "Sends the text 'X' number of times in 'Y' seconds of delay", "dspam 5 100 Hello"
).add_command(
    "uspam", "<reply to a msg> or <text>", "Spams the message unlimited times until you get floodwait error or stop it manually.", "uspam Hello"
).add_command(
    "bspam", "<count> <text or reply>", "Spams the message X times without floodwait. Breaks the spam count to avoid floodwait.", "bspam 9999 Hello"
).add_command(
    "endspam", None, "Terminates the ongoing spam."
).add_info(
    "Spammers Commands"
).add_warning(
    "❌ May Get Floodwait Error Or Limit Your Account"
).add()
