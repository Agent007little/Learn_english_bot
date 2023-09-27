import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import commands_handlers, dictionary_handlers

from config_data.config import Config, load_config

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands_handlers.router)
    dp.include_router(dictionary_handlers.router)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())