import asyncio
import logging

import sys
import telepot
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space

from bot import YouTubeBot
from config import Config

if __name__ == '__main__':
    config = Config.get_config()
    logging.basicConfig(level=logging.DEBUG)

    logging.debug('config loaded')

    bot = telepot.aio.DelegatorBot(config['telegram_token'], [
        pave_event_space()
            (per_chat_id(), create_open, YouTubeBot, timeout=sys.maxsize),
    ])

    loop = asyncio.get_event_loop()
    loop.create_task(bot.message_loop())

    logging.info('bot started')
    loop.run_forever()
