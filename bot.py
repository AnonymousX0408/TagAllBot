import os
import logging
import asyncio
from telegraph import upload_file
from telethon import Button, TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

moment_worker = []

#start
@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    await event.reply("**👋 Hey Welcome In Tag All Bot**\n\n I Can Tag All Users In Your Groups Just Reply \n/all Or /tagall To Any Message And Then See My Power 🔥\n\n**💸 More Ads Free & Fast Bots @ProCoderZBots**",
                      buttons=(
                          [
                              Button.url('『Uᴘᴅᴀᴛᴇs』', 'https://t.me/ProCoderZBots'),
                              Button.url('『Cʜᴀɴɴᴇʟ』', 'https://t.me/Pro_CoderZ'),
                          ],
                          [
                              Button.url('➕ Aᴅᴅ Mᴇ ➕', 'https://t.me/UserTaggerProBot?startgroup=true'),
                          ]
                      ),
                      link_preview=False
                      )

#help
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
    helptext = "**❤️ Welcome In Help Manu**\n I Can Tag All Members In Your Groups Just Reply /all Or /tagall To Any Message And Then See My Power\n\n**💸 More Ads Free & Fast Bots : @ProCoderZBots**"
    await event.reply(helptext,
                      buttons=(
                          [
                              Button.url('『Uᴘᴅᴀᴛᴇs』', 'https://t.me/ProCoderZBots'),
                              Button.url('『Cʜᴀɴɴᴇʟ』', 'https://t.me/Pro_CoderZ'),
                          ],
                          [
                              Button.url('➕ Aᴅᴅ Mᴇ ➕', 'https://t.me/UserTaggerProBot?startgroup=true'),
                          ]
                      ),
                      link_preview=False
                      )

#cancel
@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel(event):
    global moment_worker
    LOGGER.info("😍 Cancel command received")
    if event.chat_id in moment_worker:
        moment_worker.remove(event.chat_id)
        await event.respond("❌ Process canceled!")
    else:
        await event.respond("__There is no proccess on going...__")

#tag
@client.on(events.NewMessage(pattern="^/tagall|/call|/tall|/all|#all|@all?(.*)"))
async def mentionall(event):
    global moment_worker
    if event.is_private:
        return await event.respond("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴠᴀʟɪᴅ ғᴏʀ ɢʀᴏᴜᴘs!**")

    admins = []
    async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        admins.append(admin.id)
    if not event.sender_id in admins:
        return await event.respond("🐣 Sorry Bro, Only Admin can use it.")

    if event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.reply_to_msg_id:
        mode = "text_on_reply"
        msg = event.reply_to_msg_id
        if msg == None:
            return await event.respond("🤙 Sorry I can't Mention Members for Old Post!")
    elif event.pattern_match.group(1) and event.reply_to_msg_id:
        return await event.respond("Give me can an Argument. Ex: `@all Hey, Where are you`")
    else:
        return await event.respond("💫 Please Reply to Message or Give Some Text To Mention! For Example: `@all Hey, Where are you`")

    if mode == "text_on_cmd":
        moment_worker.append(event.chat_id)
        usrnum = 0
        usrtxt = ""
        async for usr in client.iter_participants(event.chat_id):
            usrnum += 1
            usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
            if event.chat_id not in moment_worker:
                await event.respond("**ᴛᴀɢɢɪɴɢ sᴛᴏᴘᴘᴇᴅ sᴜᴄᴄᴇsғᴜʟʟʏ!**")
                return
            if usrnum == 5:
                await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
                await asyncio.sleep(2)
                usrnum = 0
                usrtxt = ""

    if mode == "text_on_reply":
        moment_worker.append(event.chat_id)

        usrnum = 0
        usrtxt = ""
        async for usr in client.iter_participants(event.chat_id):
            usrnum += 1
            usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
            if event.chat_id not in moment_worker:
                await event.respond("**ᴛᴀɢɢɪɴɢ sᴛᴏᴘᴘᴇᴅ sᴜᴄᴄᴇsғᴜʟʟʏ!**")
                return
            if usrnum == 5:
                await client.send_message(event.chat_id, usrtxt, reply_to=msg)
                await asyncio.sleep(2)
                usrnum = 0
                usrtxt = ""

#telegraph 
@client.on(events.NewMessage(pattern="^/t$"))
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("Reply to a supported media file")
        return
    if not (
            (replied.photo and replied.photo.file_size <= 5242880)
            or (replied.animation and replied.animation.file_size <= 5242880)
            or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
            or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4"),
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply("💞 Sorry I Can't Help In This Because This Not Supported If You Want Then You Can Contact With My Boss : @Mr_RoleXG")
        return
    download_location = await client.download_media(
        message=message.reply_to_message,
        file_name="root/downloads/",
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply(message, text=document)
    else:
        await message.reply(
            f"**Hey You...!\nLoook At This\n\n👉 https://telegra.ph{response[0]}**",
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

print("Started Successfully Give A Thanks To My Boss : @Mr_RoleXG")
print("🤙 Need Help Contact My Boss : @Mr_RoleXG")
client.run_until_disconnected()
        
