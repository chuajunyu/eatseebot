import logging
from telegram.ext import *
from telegram import *

import bot_text

from Classes import Service

class Home:
    """
    Class handling the Home Page
    """
    def __init__(self):
        self.service = Service()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        inline_keyboard = [
            [InlineKeyboardButton('View and Edit Your Profile', callback_data="profile"),
             InlineKeyboardButton('Find A Match!', callback_data='match')]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_text.start_text, reply_markup=markup)
        return "HOME_START"
    
    async def not_implemented_yet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="Sorry we did not implement this yet :p, go back to /start :p")
        return