import asyncio

from aiogram.types import BotCommand, BotCommandScopeDefault

from handlers.start import start_router
from settings import dp, bot


async def main():
    # Добавляем задачу в планировщик, будет выполняться каждые 10 секунд, и запускаем
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    commands = [
        # Объект, используемый для создания команд бота. Каждая команда имеет два
        # атрибута: command (имя команды) и description (описание команды).
        BotCommand(command='start', description='Старт'),
        BotCommand(command='start2', description='Старт2'),
        BotCommand(command='start3', description='Старт3'),
        BotCommand(command='faq', description='Частые вопросы'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())  # объект, определяющий область действия команд

    # Добавляем роутер start_router в диспетчер. Это позволяет диспетчеру
    # знать о всех обработчиках команд, которые определены в start_router
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем бота в режиме опроса (polling). Бот начинает непрерывно
    # запрашивать обновления с сервера Telegram и обрабатывать их
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
