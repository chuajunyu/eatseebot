import logging
from typing import Any
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

        self.age_choices = self.service.get_age_choices()
        self.gender_choices = self.service.get_gender_choices()
        self.cuisine_choices = self.service.get_cuisine_choices()
        self.diet_choices = self.service.get_diet_choices()

    def convert_to_text(self, selected, choice_dict):
        if type(selected) == int:
            return f"_{choice_dict[str(selected)]}_"
        output = ""
        selected.sort()
        for i in selected:
            output += f"_{choice_dict[str(i)]}_, "
        output = output.strip(", ")
        return output

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE, is_redirect=True):
        # Check whether their profile exists inside the database
        telename = update.effective_chat.username

        if self.service.is_user_existing(telename):
            data = self.service.show_profile(telename)

            if not is_redirect:
                query = update.callback_query
                await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.id)

            message = bot_text.home_existing_user.format(telename,
                                              self.convert_to_text(data["age"], self.age_choices),
                                              self.convert_to_text(data["gender"], self.gender_choices),
                                              self.convert_to_text(data["age pref"], self.age_choices),
                                              self.convert_to_text(data["gender pref"], self.gender_choices),
                                              self.convert_to_text(data["cuisine pref"], self.cuisine_choices),
                                              self.convert_to_text(data["diet pref"], self.diet_choices)
                                              )

            inline_keyboard = [
                [InlineKeyboardButton('View and Edit Your Profile', callback_data="profile"),
                InlineKeyboardButton('Find A Match!', callback_data='match')]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, 
                                           reply_markup=markup, parse_mode='Markdown')
            return "HOME_START"  # state
        else:
            inline_keyboard = [
                [InlineKeyboardButton('Create a new profile!', callback_data="new_profile")]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You don't have an existing user in our db", 
                                           reply_markup=markup, parse_mode='Markdown')
            
            return "HOME_START"
        
    async def back_to_start(self, update, context):
        return await self.start(update, context, is_redirect=False)
    
    async def not_implemented_yet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="Sorry we did not implement this yet :p, go back to /start :p")
        return
    