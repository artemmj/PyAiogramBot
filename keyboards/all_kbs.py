from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from decouple import config


def main_kb(user_telegram_id: int):
    """
    Функция возвращает созданную клавиатуру, которую мы привязываем к сообщению.
    """
    kb_list = [  # cоздание списка кнопок:
        [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="📚 Каталог"), KeyboardButton(text="Давай инлайн!")],
    ]

    # Создание админской кнопки, если админ
    if user_telegram_id in [int(admin_id) for admin_id in config('ADMINS').split(',')]:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])

    keyboard = ReplyKeyboardMarkup(   # cоздаем клавиатуру с переданными кнопками
        keyboard=kb_list,
        resize_keyboard=True,         # клавиатура будет автоматически изменять размер
        one_time_keyboard=False,      # клавиатура скрывается после одного использования
        # input_field_placeholder=''  # заменяет стандартную подпись на пользовательскую
    )
    return keyboard


def spec_kb():
    """
    Клавиатура с особыми кнопками: поделиться контактами, поделиться локацией, создать опрос.
    """
    kb_list = [
        # Позволяет пользователю отправить геолокацию
        [KeyboardButton(text="Отправить гео", request_location=True)],
        # Позволяет отправить номер
        [KeyboardButton(text="Поделиться номером", request_contact=True)],
        # Позволяет создать викторину или опрос. Может принимать один из параметров
        # type = «quiz» (викторина) или «regular» (опрос).
        [KeyboardButton(text="Отправить викторину/опрос", request_poll=KeyboardButtonPollType())],
        [KeyboardButton(text="Домой")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь специальной клавиатурой:",
    )
    return keyboard


def create_rat_kb():
    """
    Клавиатура со шкалой голосования, в которой результаты записаны в виде баллов от 1 до 10.
    """
    builder = ReplyKeyboardBuilder()                # используется для построения клавиатуры
    for item in [str(i) for i in range(1, 11)]:
        builder.button(text=item)                   # список строк-кнопок от '1' до '10'
    builder.button(text='Домой')                    # добавление кнопки Назад
    builder.adjust(4, 4, 2, 1)                      # настройка расположения кнопок
    return builder.as_markup(resize_keyboard=True)  # преобразуем клавиатуру в объект ReplyKeyboardMarkup
