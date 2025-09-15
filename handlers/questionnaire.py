import asyncio
import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from settings import bot

questionnaire_router = Router()


def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    return None


class Form(StatesGroup): 
    name = State()
    age = State()


@questionnaire_router.message(Command('start_questionnaire'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Привет. Напиши как тебя зовут: ')
    await state.set_state(Form.name)

    
@questionnaire_router.message(F.text, Form.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Супер! А теперь напиши сколько тебе полных лет: ')
    await state.set_state(Form.age)

    
@questionnaire_router.message(F.text, Form.age)
async def capture_age(message: Message, state: FSMContext):
    check_age = extract_number(message.text)

    if not check_age or not (1 <= check_age <= 100):
        await message.reply('Пожалуйста, введите корректный возраст (число от 1 до 100).')
        return
    await state.update_data(age=check_age)

    data = await state.get_data()
    msg_text = (f'Вас зовут <b>{data.get("name")}</b> и вам <b>{data.get("age")}</b> лет. '
                f'Спасибо за то что ответили на мои вопросы.')
    await message.answer(msg_text)
    await state.clear()
