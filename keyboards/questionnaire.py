from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config


def gender_kb():
    kb_list = [[KeyboardButton(text="👨‍🦱Мужчина")], [KeyboardButton(text="👩‍🦱Женщина")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери пол:",
    )
    return keyboard


def check_data():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='correct')],
        [InlineKeyboardButton(text="❌Заполнить сначала", callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def get_login_tg():
    kb_list = [[InlineKeyboardButton(text="Использовать мой логин с ТГ", callback_data='in_login')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
