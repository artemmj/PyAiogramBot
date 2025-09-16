import asyncio
import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.state import (
    State,        # представляет собой конкретное состояние, в котором может находиться пользователь
    StatesGroup,  # позволяет объединять несколько состояний в логическую группу
)

# Хранит данные о текущем состоянии пользователя и позволяет
# изменять их, перемещая пользователя между различными состояниями
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
# from aiogram.utils.chat_action import ChatActionSender

from keyboards.questionnaire import check_data, gender_kb, get_login_tg
from settings import bot

questionnaire_router = Router()


def extract_number(text):
    """
    Функция извлекает число из текста - на случай если пользователь
    ввел "мне 20 лет" вместо "20" - функция достанет 20 конвертнет в int.
    """
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    return None


class Form(StatesGroup):
    gender = State()
    age = State()
    full_name = State()
    user_login = State()
    photo = State()
    about = State()
    check_state = State()


@questionnaire_router.message(Command('start_questionnaire'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет. Для начала выбери свой пол: ', reply_markup=gender_kb())
    await state.set_state(Form.gender)


@questionnaire_router.message((F.text.lower().contains('мужчина')) | (F.text.lower().contains('женщина')), Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(gender=message.text, user_id=message.from_user.id)
    await message.answer('Супер! А теперь напиши сколько тебе полных лет: ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.age)


@questionnaire_router.message(F.text, Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Пожалуйста, выбери вариант из тех что в клавиатуре: ', reply_markup=gender_kb())
    await state.set_state(Form.gender)


@questionnaire_router.message(F.text, Form.age)
async def start_questionnaire_process(message: Message, state: FSMContext):
    check_age = extract_number(message.text)

    if not check_age or not (1 <= int(message.text) <= 100):
        await message.reply("Пожалуйста, введите корректный возраст (число от 1 до 100).")
        return

    await state.update_data(age=check_age)
    await message.answer('Теперь укажите свое полное имя:')
    await state.set_state(Form.full_name)


@questionnaire_router.message(F.text, Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    text = 'Теперь укажите ваш логин, который будет использоваться в боте'

    if message.from_user.username:
        text += ' или нажмите на кнопку ниже и в этом случае вашим логином будет логин из вашего телеграмм: '
        await message.answer(text, reply_markup=get_login_tg())
    else:
        text += ' : '
        await message.answer(text)

    await state.set_state(Form.user_login)


# вариант когда мы берем логин из профиля телеграмм
@questionnaire_router.callback_query(F.data, Form.user_login)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Беру логин с телеграмм профиля')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(user_login=call.from_user.username)
    await call.message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


# вариант когда мы берем логин из введенного пользователем
@questionnaire_router.message(F.text, Form.user_login)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(user_login=message.from_user.username)
    await message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


@questionnaire_router.message(F.photo, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@questionnaire_router.message(F.document.mime_type.startswith('image/'), Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.document.file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@questionnaire_router.message(F.document, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте фото!')
    await state.set_state(Form.photo)


@questionnaire_router.message(F.text, Form.about)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(about=message.text)

    data = await state.get_data()

    caption = (
        f'Пожалуйста, проверьте все ли верно: \n\n' \
        f'<b>Полное имя</b>: {data.get("full_name")}\n' \
        f'<b>Пол</b>: {data.get("gender")}\n' \
        f'<b>Возраст</b>: {data.get("age")} лет\n' \
        f'<b>Логин в боте</b>: {data.get("user_login")}\n' \
        f'<b>О себе</b>: {data.get("about")}'
    )

    await message.answer_photo(photo=data.get('photo'), caption=caption, reply_markup=check_data())
    await state.set_state(Form.check_state)

# сохраняем данные
@questionnaire_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Данные сохранены')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Благодарю за регистрацию. Ваши данные успешно сохранены!')
    await state.clear()


# запускаем анкету сначала
@questionnaire_router.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Запускаем сценарий с начала')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Привет. Для начала выбери свой пол: ', reply_markup=gender_kb())
    await state.set_state(Form.gender)


############################################################################################################


# @questionnaire_router.message(Command('start_questionnaire'))
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     # async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
#     #     await asyncio.sleep(1)
#     await message.answer('Привет. Напиши как тебя зовут: ')
#     # state позволяет управлять состояниями пользователя, перемещать пользователя по состояниям и прочее.

#     # Когда пользователь дойдет до этого момента функции,
#     # он окажется в состоянии Form.name, а значит, что его отправка
#     # данных (ввод имени) отнесется к .
#     await state.set_state(Form.set_name)

    
# @questionnaire_router.message(F.text, Form.set_name)
# async def capture_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     # async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
#     #     await asyncio.sleep(2)
#     await message.answer('Супер! А теперь напиши сколько тебе полных лет: ')
#     await state.set_state(Form.set_age)


# @questionnaire_router.message(F.text, Form.set_age)
# async def capture_age(message: Message, state: FSMContext):
#     check_age = extract_number(message.text)

#     if not check_age or not (1 <= check_age <= 100):
#         await message.reply('Пожалуйста, введите корректный возраст (число от 1 до 100).')
#         return
#     await state.update_data(age=check_age)

#     data = await state.get_data()
#     msg_text = (f'Вас зовут <b>{data.get("name")}</b> и вам <b>{data.get("age")}</b> лет. '
#                 f'Спасибо за то что ответили на мои вопросы.')
#     await message.answer(msg_text)
#     await state.clear()
