import asyncio
from aiogram import Router, F
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import CallbackQuery, Message

from settings import admins, bot
from filters.is_admin import IsAdmin
from keyboards.all_kbs import main_kb, spec_kb
from keyboards.inline_kbs import get_inline_kb, ease_link_inline_kb
from utils.gen_random_person import gen_random_person
from utils.get_msk_time import get_msc_date

# Router используется для удобного масштабирования проекта. Благодаря ему
# мы можем отказаться от необходимости импортировать Dispatcher в каждом хендлере.
start_router = Router()


@start_router.message(CommandStart())  # срабатывает на команду /start
async def cmd_start(message: Message, command: CommandObject):
    command_arg: str = command.args  # извлекаем метку-аргумент команды
    user_id = message.from_user.id

    omsg = 'Запуск сообщения по команде /start'
    if command_arg:
        await message.answer(f'{omsg} с меткой <code>{command_arg}</code>', reply_markup=main_kb(user_id))
    else:
        await message.answer(f'{omsg} без метки', reply_markup=main_kb(user_id))


@start_router.message(Command('start2'))  # активируется при любой команде, переданной аргументом
async def cmd_start_2(message: Message):
    await message.answer(
        'Запуск сообщения по команде /start2',
        reply_markup=spec_kb(),
    )

# F.text != 'Пока!'
# F.text.contains('Привет')
# F.text.lower().contains('привет')
# F.text.startswith('Привет')
# F.text.endswith('дружище')
# ~F.text
# ~F.text.startswith('spam')
# F.text.upper().in_({'ПРИВЕТ', 'ПОКА'})
# F.text.upper().in_(['ПРИВЕТ', 'ПОКА'])
# F.chat.type.in_({"group", "supergroup"})
# f.content_type.in_({'text', 'sticker', 'photo'})
# F.text.len() == 5
# F.text.regexp(r'(?i)^Привет, .+')

@start_router.message(F.text == '/start3')  # позволяет фильтровать сообщения по содержимому текста
async def cmd_start_3(message: Message):
    await message.answer(
        'Запуск сообщения по команде /start3',
        reply_markup=ease_link_inline_kb(),
    )


@start_router.callback_query(F.data == 'back_home')
async def back_home(call: CallbackQuery):
    await call.message.answer(
        'Возвращаю в главное меню',
        reply_markup=main_kb(call.message.from_user.id),
    )

@start_router.message(F.text == 'Давай инлайн!')
async def get_inline_btn_link(message: Message):
    await message.answer(
        'Вот инлайн клавиатура со ссылками:',
        reply_markup=get_inline_kb(),
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


@start_router.message(F.text.lower().contains('подписывайся'))
async def process_find_word(message: Message):
    await message.answer('В твоем сообщении было найдено слово "подписывайся", а у нас такое писать запрещено!')


@start_router.message(F.text.lower().contains('подписывайся'), IsAdmin(admins))
async def process_find_word2(message: Message):
    await message.answer('О, админ, здарова! А тебе можно писать подписывайся.')


@start_router.message(F.text.lower().contains('охотник'))
async def cmd_start(message: Message, state: FSMContext):
    # Отправка обычного сообщения
    await message.answer('Я думаю, что ты тут про радугу рассказываешь')

    # То же действие, но через объект бота
    await bot.send_message(chat_id=message.from_user.id, text='Для меня это слишком просто')

    # Ответ через цитату
    msg = await message.reply('Ну вот что за глупости!?')

    # Ответ через цитату, через объект bot
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Хотя, это забавно...',
        reply_to_message_id=msg.message_id,
    )

    await bot.forward_message(
        chat_id=message.from_user.id,
        from_chat_id=message.from_user.id,
        message_id=msg.message_id,
    )

    await message.answer('Все это шизааа...')

    data_task = {
        'user_id': message.from_user.id,
        'full_name': message.from_user.full_name,
        'username': message.from_user.username,
        'message_id': message.message_id,
        'date': get_msc_date(message.date),
    }
    print(data_task)


@start_router.message(Command('test_edit_msg'))
async def cmd_start(message: Message, state: FSMContext):
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


@start_router.message(Command('test_edit_msg2'))
async def cmd_start2(message: Message, state: FSMContext):
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


@start_router.message(Command('test_edit_msg3'))
async def cmd_start3(message: Message, state: FSMContext):
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
