import sys
import logging
from asyncio import sleep
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors.exceptions import ChannelPrivate
from modules.posts import TextPost, PicturePost, StickerPost, RandomPost

client = Client("data/my_account", config_file="data/config.ini", workers=1)

client.start()
count = client.get_dialogs_count()
print(count)
l = []
for x in client.iter_dialogs(count):
    if x.chat.type == 'channel':
        
        if x.chat.username is None:
            print(x.chat.title)
        else:
            
            print('https://t.me/'+x.chat.username)
    
        print('------')
        l.append(x.chat.id)
print(len(l))

        