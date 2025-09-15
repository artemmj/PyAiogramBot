import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_kbs import main_kb
from settings import bot

edit_msg_router = Router()


@edit_msg_router.message(Command('test_edit_msg'))
async def cmd_edit(message: Message, state: FSMContext):
    # Бот делает отправку сообщения с сохранением объекта msg
    msg = await message.answer('Отправляю сообщение')

    # Достаем ID сообщения
    msg_id = msg.message_id

    # Имитируем набор текста 2 секунды
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await message.answer('Новое сообщение')

    # Делаем паузу ещё на 2 секунды
    await asyncio.sleep(2)

    # Изменяем текст сообщения, ID которого мы сохранили
    await bot.edit_message_text(
        message_id=msg_id,
        chat_id=message.from_user.id,
        text='<b>Я тебе отправил сообщение!!!</b>',
    )


@edit_msg_router.message(Command('test_edit_msg2'))
async def cmd_edit2(message: Message, state: FSMContext):
    new_msg = await bot.copy_message(
        chat_id=message.from_user.id,
        from_chat_id=message.from_user.id, 
        message_id=message.message_id
    )
    await message.delete()
    await bot.edit_message_text(
        text='<b>Отправляю сообщение!!!</b>',
        chat_id=message.from_user.id,
        message_id=new_msg.message_id
    )
    # await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


@edit_msg_router.message(Command('test_edit_msg3'))
async def cmd_edit3(message: Message, state: FSMContext):
    msg = await message.answer('Привет!')
    await asyncio.sleep(2)
    old_text = msg.text
    await msg.delete()
    await message.answer(
        f'''<code>{old_text}</code>
<b>Жирный</b>
<i>Курсив</i>
<u>Подчеркнутый</u>
<s>Зачеркнутый</s>
<tg-spoiler>Спойлер (скрытый текст)</tg-spoiler>
<a href="http://www.example.com/">Ссылка в тексте</a>
<code>Код с копированием текста при клике</code>
<pre>Спойлер с копированием текста</pre>''',
        reply_markup=main_kb(message.from_user.id))
