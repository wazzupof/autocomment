import random
import logging
from asyncio import sleep
import pyrogram
from pyrogram.errors import SlowmodeWait
import os
import openai
openai.api_key = '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'


def reply(func):
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except SlowmodeWait as sw:
            if sw.x > 30:
                logging.info(f'Script wont sleep {sw.x}s - >30s ({sw})')
                return
            logging.warning(f'Sleeping {sw.x}s due to {sw}')
            await sleep(sw.x)
            await func(*args, **kwargs)
        await sleep(0.25)

    return wrapper


class TextPost:
    def __init__(self, text, delay=0):
        self.text = text
        self.delay = delay

    @reply
    async def reply_to(self, message: pyrogram.types.Message, app: pyrogram.Client):
        if message.caption or message.text:
            post_text = message.text if message.text else message.caption
        else:
            return
        content = "Напиши комментарий к посту в телеграме со следующим текстом '" + post_text + \
            "'Не более 100 символов, отвечай в роли мужчины"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content}
            ]
        )

        print()
        answer = await app.send_message(message.chat.id, completion.choices[0].message.content, reply_to_message_id=message.id)
        print(answer)


class PicturePost:
    def __init__(self, picture, text=None, delay=0):
        self.picture = picture
        self.text = text
        self.delay = delay

    @reply
    async def reply_to(self, message: pyrogram.types.Message, app: pyrogram.Client):
        await app.send_photo(message.chat.id, self.picture, caption=self.text, reply_to_message_id=message.message_id, schedule_date=message.date + self.delay)


class RandomPost:

    def __init__(self, *args):
        self.posts = args

    async def reply_to(self, message: pyrogram.types.Message, app: pyrogram.Client):
        await random.choice(self.posts).reply_to(message, app)


class StickerPost:
    def __init__(self, sticker_id, delay=0):
        self.sticker_id = sticker_id
        self.delay = delay

    @reply
    async def reply_to(self, message: pyrogram.types.Message, app: pyrogram.Client):
        await app.send_sticker(message.chat.id, sticker=self.sticker_id, reply_to_message_id=message.message_id, schedule_date=message.date + self.delay)
