import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from decouple import config

bot = Bot(
    token=config('TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),  # чтобы бот мог воспринимать html разметку
)
# Основной объект, отвечающий за обработку входящих сообщений и других
# обновлений, поступающих от Telegram. Именно через диспетчер проходят
# все сообщения и команды, отправляемые пользователями бота.
dp = Dispatcher(storage=MemoryStorage())  # для хранения состояния конечных автоматов FSM используется RAM

admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')

questions = {
    1: {'qst': 'Столица Италии?', 'answer': 'Рим'},
    2: {'qst': 'Сколько континентов на Земле?', 'answer': 'Семь'},
    3: {'qst': 'Самая длинная река в мире?', 'answer': 'Нил'},
    4: {'qst': 'Какой элемент обозначается символом "O"?', 'answer': 'Кислород'},
    5: {'qst': 'Как зовут главного героя книги "Гарри Поттер"?', 'answer': 'Гарри Поттер'},
    6: {'qst': 'Сколько цветов в радуге?', 'answer': 'Семь'},
    7: {'qst': 'Какая планета третья от Солнца?', 'answer': 'Земля'},
    8: {'qst': 'Кто написал "Войну и мир"?', 'answer': 'Лев Толстой'},
    9: {'qst': 'Что такое H2O?', 'answer': 'Вода'},
    10: {'qst': 'Какой океан самый большой?', 'answer': 'Тихий океан'},
}
