import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, PollAnswerHandler
from config import Config
from news_api import NewsAPI
from bot import TelegramBot
import nest_asyncio
nest_asyncio.apply()

async def main():
    config = Config()
    news_api = NewsAPI(config.news_api_key)
    bot = TelegramBot(news_api)

    print("Запуск бота...")
    application = Application.builder().token(config.telegram_token).build()

    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CallbackQueryHandler(bot.button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.search_handler))  # Обработка текстовых сообщений

    print("Бот готов к работе.")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())  # Используйте asyncio.run() для запуска основной функции