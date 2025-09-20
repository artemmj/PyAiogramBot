import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from database import create_table_users, get_all_users
from handlers.start import start_router
from handlers.faq import faq_router
from handlers.edit_msg import edit_msg_router
from handlers.send import send_files_router
from handlers.user import user_router
from handlers.questionnaire import questionnaire_router
from settings import admins, dp, bot


async def set_commands():
    """Функция настраивает командное меню."""
    commands = [
        BotCommand(command='start', description='Старт'),
        BotCommand(command='profile', description='Мой профиль'),
        BotCommand(command='faq', description='Частые вопросы'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    """Функция, которая выполнится когда бот запустится."""
    await set_commands()
    count_users = await get_all_users(count=True)
    try:
        [
            await bot.send_message(admin_id, f'Я запущен🥳. Сейчас в базе <b>{count_users}</b> пользователей.')
            for admin_id in admins
        ]
    except:
        pass


async def stop_bot():
    """Функция, которая выполнится когда бот завершит свою работу."""
    try:
        [await bot.send_message(admin_id, 'Бот остановлен. За что?😔') for admin_id in admins]
    except:
        pass


async def main():
    await create_table_users()

    dp.include_router(start_router)
    dp.include_router(faq_router)
    dp.include_router(edit_msg_router)
    dp.include_router(send_files_router)
    dp.include_router(user_router)
    dp.include_router(questionnaire_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Запуск бота в режиме long polling - при запуске бот
    # очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
