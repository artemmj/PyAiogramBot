import asyncio

from aiogram import Router, F  # магический фильтр
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.all_kbs import main_kb, spec_kb
from keyboards.inline_kbs import create_qst_inline_kb, get_inline_kb, ease_link_inline_kb

from settings import bot, questions
from utils.gen_random_person import gen_random_person

# Router используется для удобного масштабирования проекта. Благодаря ему
# мы можем отказаться от необходимости импортировать Dispatcher в каждом хендлере.
start_router = Router()


@start_router.message(CommandStart())  # срабатывает на команду /start
async def cmd_start(message: Message, command: CommandObject):
    command_args: str = command.args  # извлекаем метку-аргумент команды
    user_id = message.from_user.id

    omsg = 'Запуск сообщения по команде /start'
    if command_args:
        await message.answer(f'{omsg} с меткой <b>{command_args}</b>', reply_markup=main_kb(user_id))
    else:
        await message.answer(f'{omsg} без метки', reply_markup=main_kb(user_id))


@start_router.message(Command('start2'))  # активируется при любой команде, переданной аргументом
async def cmd_start_2(message: Message):
    await message.answer(
        'Запуск сообщения по команде /start2',
        reply_markup=spec_kb(),
    )


@start_router.message(F.text == '/start3')  # позволяет фильтровать сообщения по содержимому текста
async def cmd_start_3(message: Message):
    await message.answer(
        'Запуск сообщения по команде /start3',
        reply_markup=ease_link_inline_kb(),
    )


@start_router.message(F.text == 'Давай инлайн!')
async def get_inline_btn_link(message: Message):
    await message.answer(
        'Вот инлайн клавиатура со ссылками:',
        reply_markup=get_inline_kb(),
    )


@start_router.callback_query(F.data == 'back_home')
async def back_home(call: CallbackQuery):
    await call.message.answer(
        'Возвращаю в главное меню',
        reply_markup=main_kb(call.message.from_user.id),
    )


@start_router.callback_query(F.data == 'get_person')
async def send_random_person(call: CallbackQuery):
    # await call.answer('Генерирую случайного пользователя', show_alert=False)
    await call.answer()
    user = gen_random_person()
    formatted_message = (
        f"👤 <b>Имя:</b> {user['name']}\n"
        f"🏠 <b>Адрес:</b> {user['address']}\n"
        f"📧 <b>Email:</b> {user['email']}\n"
        f"📞 <b>Телефон:</b> {user['phone_number']}\n"
        f"🎂 <b>Дата рождения:</b> {user['birth_date']}\n"
        f"🏢 <b>Компания:</b> {user['company']}\n"
        f"💼 <b>Должность:</b> {user['job']}\n"
    )
    await call.message.answer(formatted_message)


@start_router.message(Command('faq'))
async def cmd_faq(message: Message):
    await message.answer(
        'Сообщение с инлайн клавиатурой с вопросами',
        reply_markup=create_qst_inline_kb(questions),
    )


@start_router.callback_query(F.data.startswith('qst_'))
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
