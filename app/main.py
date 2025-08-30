import asyncio
import logging
from app.bot.create_bot import bot, dp, start_bot, stop_bot
from app.bot.handlers.user_router import user_router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    try:
        logger.info("Starting bot setup...")

        # Подключаем роутеры
        dp.include_router(user_router)

        # Отправляем уведомление о запуске
        await start_bot()

        # Запускаем поллинг
        logger.info("Bot started successfully")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise
    finally:
        # Отправляем уведомление об остановке
        await stop_bot()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
