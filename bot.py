from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import ContextTypes
from news_api import NewsAPI

class TelegramBot:
    def __init__(self, news_api):
        self.news_api = news_api

    def main_menu_buttons(self) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton("Последние новости", callback_data='get_general_news')],
            [InlineKeyboardButton("Спортивные новости", callback_data='get_sports_news')],
            [InlineKeyboardButton("Новости культуры", callback_data='get_culture_news')],
            [InlineKeyboardButton("Поиск новостей", callback_data='search_news')],
        ]
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        print(f"Пользователь {update.message.from_user.id} начал взаимодействие с ботом.")
        context.user_data['pages'] = {
            'general': 1,
            'sports': 1,
            'culture': 1,
        }
        await update.message.reply_text(
            'Привет! Выберите категорию новостей ниже:',
            reply_markup=self.main_menu_buttons()
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        pages = context.user_data['pages']
        print(f"Пользователь {query.from_user.id} нажал кнопку: {query.data}")

        if query.data == 'get_general_news':
            pages['general'] =  1
            news = self.news_api.get_news(category='general', page=pages['general'])
            await context.bot.send_message(chat_id=chat_id, text=f"Последние новости:\n\n{news}",
                                           reply_markup=self.show_more_buttons('general'))
        elif query.data == 'get_sports_news':
            pages['sports'] = 1
            news = self.news_api.get_news(category='sports', page=pages['sports'])
            await context.bot.send_message(chat_id=chat_id, text=f"Спортивные новости:\n\n{news}",
                                           reply_markup=self.show_more_buttons('sports'))
        elif query.data == 'get_culture_news':
            pages['culture'] = 1
            news = self.news_api.get_news(category='entertainment', page=pages['culture'])
            await context.bot.send_message(chat_id=chat_id, text=f"Новости культуры:\n\n{news}",
                                           reply_markup=self.show_more_buttons('culture'))
        elif query.data.startswith('show_more_'):
            category = query.data.split('_')[2]
            pages[category] += 1
            news = self.news_api.get_news(category=category, page=pages[category])
            await context.bot.send_message(chat_id=chat_id, text=f"Дополнительные новости:\n\n{news}",
                                           reply_markup=self.show_more_buttons(category))
        elif query.data == 'back_to_menu':
            await context.bot.send_message(chat_id=chat_id, text='Выберите категорию новостей ниже:',
                                           reply_markup=self.main_menu_buttons())
        elif query.data == 'search_news':
            await context.bot.send_message(chat_id=chat_id, text='Введите ваш запрос для поиска новостей:')
            return

    async def search_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.message.text
        print(f"Пользователь {update.message.from_user.id} выполнил поиск: {query}")
        news = self.news_api.get_news(query=query)
        await update.message.reply_text(
            f"Результаты поиска по запросу '{query}':\n\n{news}",
            reply_markup=self.main_menu_buttons()
        )

    def show_more_buttons(self, category: str) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton("Показать еще", callback_data=f'show_more_{category}')],
            [InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')],
        ]
        return InlineKeyboardMarkup(keyboard)