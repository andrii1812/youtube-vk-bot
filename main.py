import asyncio
import json
import logging
import os

import telepot
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open

import api
import replies

logging.basicConfig(level=logging.INFO)

config = json.load(open('config.json', 'r'))
logging.debug('config loaded')

vk_api = api.vk_auth(config)
logging.info('authenticated to vk.com')


class YouTubeBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(YouTubeBot, self).__init__(*args, **kwargs)

    async def message_handler(self, text, message_id):
        if not api.validate(text):
            logging.debug('invalid url received: {0}'.format(text))
            await self.reply(replies.INVALID_URL, message_id)
            return

        await self.reply(replies.UPLOAD_STARTED, message_id)
        video_data = api.download(text, config['tmp_path'])
        video_vk_url = api.upload_video(vk_api, video_data.path, video_data.name)
        os.remove(video_data.path)

        logging.info("uploaded: {0} -> {1}".format(text, video_vk_url))
        await self.reply(replies.UPLOADED_VIDEO.format(video_vk_url), message_id)

    async def on_chat_message(self, msg):
        text = msg['text']
        msg_id = msg['message_id']
        try:
            await self.message_handler(text, msg_id)
        except Exception as e:
            await self.reply("Ohh... I've got an error here! {0}".format(e.args), msg_id)

    async def reply(self, msg, reply_id):
        await self.sender.sendMessage(msg, reply_to_message_id=reply_id)

bot = telepot.aio.DelegatorBot(config['telegram_token'], [
    pave_event_space()(
        per_chat_id(), create_open, YouTubeBot, timeout=3600),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())

logging.info('bot started')
loop.run_forever()
