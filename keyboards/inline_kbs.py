from aiogram.types import (
    InlineKeyboardMarkup,  # используется для создания разметки инлайн клавиатуры
    InlineKeyboardButton,  # отдельная кнопка на инлайн клавиатуре (текст и действие, например, отправку CallBack)
    WebAppInfo,            # класс используется для создания кнопок, которые открывают веб-приложения
)
from aiogram.utils.keyboard import InlineKeyboardBuilder  # инструмент для построения инлайн клавиатур


def ease_link_inline_kb():
    """Инлайн клавиатура со ссылками."""
    inline_kb_list = [
        # Содержит вложенные списки с объектами InlineKeyboardButton. Каждая вложенная
        # структура представляет собой отдельную строку кнопок на инлайн клавиатуре.
        [InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/anonerror/')],
        [InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=artemmj')],
        [InlineKeyboardButton(text="Сайт", web_app=WebAppInfo(url="https://ya.ru"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def get_inline_kb():
    """Инлайн клавиатура с кнопками с callback-data."""
    inline_kb_list = [
        [InlineKeyboardButton(text="Генерировать пользователя", callback_data='get_person')],
        [InlineKeyboardButton(text="Домой", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def create_qst_inline_kb(questions: dict) -> InlineKeyboardMarkup:
    """Инлайн клавиатура со списком вопросов."""
    builder = InlineKeyboardBuilder()

    for question_id, question_data in questions.items():
        builder.row(InlineKeyboardButton(text=question_data.get('qst'), callback_data=f'qst_{question_id}'))

    builder.row(InlineKeyboardButton(text='Домой', callback_data='back_home'))

    # Настраиваем размер клавиатуры
    builder.adjust(1)
    return builder.as_markup()
