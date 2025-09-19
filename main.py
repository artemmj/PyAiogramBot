import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from database import create_table_users
from handlers.start import start_router
from handlers.faq import faq_router
from handlers.edit_msg import edit_msg_router
from handlers.send import send_files_router
from handlers.questionnaire import questionnaire_router
from settings import dp, bot


async def main():
    # Добавляем задачу в планировщик, будет выполняться каждые 10 секунд, и запускаем
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    await create_table_users()

    commands = [
        BotCommand(command='start', description='Старт'),
        BotCommand(command='faq', description='Частые вопросы'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())  # объект, определяющий область действия команд

    dp.include_router(start_router)
    dp.include_router(faq_router)
    dp.include_router(edit_msg_router)
    dp.include_router(send_files_router)
    dp.include_router(questionnaire_router)
    await bot.delete_webhook(drop_pending_updates=True)


    # Запускаем бота в режиме опроса (polling). Бот начинает непрерывно
    # запрашивать обновления с сервера Telegram и обрабатывать их
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
