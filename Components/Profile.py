import logging
from telegram.ext import *
from telegram import *

import bot_text

from Classes import Service

class Profile:
    """
    Class handling the Creation, Deletion and Editting of User Profiles
    """
    def __init__(self):
        self.service = Service()

    async def profile_home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        inline_keyboard = [
            [InlineKeyboardButton("Personal Info", callback_data="personal_info")], 
            [InlineKeyboardButton("Food Preference", callback_data="food_pref")],
            [InlineKeyboardButton("Buddy Preference", callback_data="buddy_pref")]
        ]

        telename = update.effective_chat.username

        if self.service.is_user_existing(telename):
            data = self.service.show_profile(telename)
            print(data["age"])

            message = bot_text.profile.format(telename,
                                              data["age"],
                                              data["gender"],
                                              data["age pref"],
                                              data["gender pref"],
                                              data["cuisine pref"],
                                              data["diet pref"]
                                              )
        else:
            message = "you don't exist in our system yet pls go fill it up"
        
        # retrieve the users info and let them know what is filled up and what is missing
        
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=message, 
                                    reply_markup=markup)
        return "PROFILE_HOME"
    
    async def edit_your_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # call api to get list of ages
        inline_keyboard = [
            [InlineKeyboardButton('16-19', callback_data='16-19'), 
             InlineKeyboardButton('20-24', callback_data='20-24')],
            [InlineKeyboardButton('25-29', callback_data='25-29'), 
             InlineKeyboardButton('30-39', callback_data='30-39')],
            [InlineKeyboardButton('50 & Above', callback_data='50 & Above')]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_age_text, 
                                    reply_markup=markup)
        return "CHOOSING_AGE"

    async def handle_choosing_age__edit_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        context.user_data["age"] = 1
        await context.bot.edit_message_text(text=f"You chose {query.data} as your age range.",
                                                    chat_id=query.message.chat_id, message_id=query.message.id)
        await self.edit_your_gender(update, context)
        return "CHOOSING_GENDER"

    async def edit_your_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        inline_keyboard = [
            [InlineKeyboardButton('Male', callback_data='Male'), 
             InlineKeyboardButton('Female', callback_data="50")],
            [InlineKeyboardButton('Non Binary', callback_data='Non Binary')]
        ]
        print(update.callback_query.inline_message_id)
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_gender_text, 
                                    reply_markup=markup)
        return "CHOOSING_GENDER"

    async def handle_choosing_gender__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        context.user_data['gender'] = 1
        await context.bot.edit_message_text(text=f"You chose {query.data} as your gender.",
                                            chat_id=query.message.chat_id, message_id=query.message.id)
        
        # Push  information online to 
        telename = update.effective_chat.username
        if not self.service.is_user_existing(telename):
            if self.service.create_user(telename,
                                     context.user_data['age'],
                                     context.user_data['gender']):
                await context.bot.send_message(text=f"New profile created",
                                           chat_id=query.message.chat_id)

        await self.profile_home(update, context)
        return "PROFILE_HOME"

    async def edit_your_cuisine_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        inline_keyboard = [
            [InlineKeyboardButton('Chinese', callback_data='Chinese'), 
             InlineKeyboardButton('Malay', callback_data='Malay')],
            [InlineKeyboardButton('Indian', callback_data='Indian'), 
             InlineKeyboardButton('Western', callback_data='Western')],
            [InlineKeyboardButton('Korean', callback_data='Korean'), 
             InlineKeyboardButton('Japanese', callback_data='Japanese')],
            [InlineKeyboardButton('Indonesian', callback_data='Indonesian'), 
             InlineKeyboardButton('Vietnamese', callback_data='Vietnamese')]
        ]
        print(update.callback_query.inline_message_id)
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_cuisine_text, 
                                    reply_markup=markup)
        return "CHOOSING_CUISINE"
    
    async def handle_choosing_cuisine(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        context.user_data["age"] = 1
        await context.bot.edit_message_text(text=f"You chose {query.data} as your age range.",
                                                    chat_id=query.message.chat_id, message_id=query.message.id)
        await self.edit_your_gender(update, context)
        return "CHOOSING_CHOOSING"

    async def edit_your_dietary_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        inline_keyboard = [
            [InlineKeyboardButton('Halal', callback_data='Halal'), 
             InlineKeyboardButton('Vegetarian', callback_data='Vegetarian')],
            [InlineKeyboardButton('Vegan', callback_data='Vegan')]
        ]
        print(update.callback_query.inline_message_id)
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_diet_text, 
                                    reply_markup=markup)
        return "CHOOSING_DIET"
