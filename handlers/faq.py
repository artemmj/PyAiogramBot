import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.inline_kbs import create_qst_inline_kb

from settings import bot, questions

faq_router = Router()

@faq_router.message(Command('faq'))
async def cmd_faq(message: Message):
    await message.answer(
        'Сообщение с инлайн клавиатурой с вопросами',
        reply_markup=create_qst_inline_kb(questions),
    )


@faq_router.callback_query(F.data.startswith('qst_'))
async def cmd_faq_answer(call: CallbackQuery):
    await call.answer()  # даем понять серверу телеграмм что все у нас хорошо
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = questions[qst_id]
    msg_text = (
        f'Ответ на вопрос {qst_data.get("qst")}\n\n'
        f'<b>{qst_data.get("answer")}</b>\n\n'
        f'Выбери другой вопрос:'
    )
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        # Имитация набора ботом сообщения
        await asyncio.sleep(.5)
        await call.message.answer(msg_text, reply_markup=create_qst_inline_kb(questions))
