import asyncio
import logging
import os

import telepot

import api
import replies
from config import Config


class YouTubeBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        self.config = Config.get_config()
        self.vk_api = api.vk_auth(self.config)
        logging.debug('authenticated to vk.com')
        super(YouTubeBot, self).__init__(*args, **kwargs)

    async def message_handler(self, text, message_id):
        if not api.validate(text):
            logging.debug('invalid url received: {0}'.format(text))
            await self.reply(replies.INVALID_URL, message_id)
            return

        await self.reply(replies.UPLOAD_STARTED, message_id)
        video_vk_url = await self.test()  # await self.pipeline(text)

        logging.info("uploaded: {0} -> {1}".format(text, video_vk_url))
        await self.reply(replies.UPLOADED_VIDEO.format(video_vk_url), message_id)

    @asyncio.coroutine
    def pipeline(self, text):
        video_data = api.download(text, self.config['tmp_path'])
        video_vk_url = api.upload_video(self.vk_api, video_data.path, video_data.name)
        os.remove(video_data.path)
        return video_vk_url

    async def test(self):
        await asyncio.sleep(30)
        return 'test'

    async def on_chat_message(self, msg):
        text = msg['text']
        msg_id = msg['message_id']
        try:
            await self.message_handler(text, msg_id)
        except Exception as e:
            await self.reply("Ohh... I've got an error here! {0}".format(e.args), msg_id)

    async def reply(self, msg, reply_id):
        await self.sender.sendMessage(msg, reply_to_message_id=reply_id)