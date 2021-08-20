import asyncio
import logging
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from language_middleware import setup_middleware


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

storage = MemoryStorage()

loop = asyncio.get_event_loop()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


# Настройка i18n middleware для многоязычности
i18n = setup_middleware(dp)
# Создаём псевдоним для метода gettext
_ = i18n.gettext
