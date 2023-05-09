import logging
from telegram.ext import *
from telegram import *

import bot_text

from Classes import Service
from Classes import KeyboardGenerator

class Profile:
    """
    Class handling the Creation, Deletion and Editting of User Profiles
    """
    def __init__(self):
        self.service = Service()
        self.keyboard_generator = KeyboardGenerator()

        self.age_choices = self.service.get_age_choices()
        self.gender_choices = self.service.get_gender_choices()
        self.cuisine_choices = self.service.get_cuisine_choices()
        self.diet_choices = self.service.get_diet_choices()

    async def new_user_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = self.keyboard_generator.generate_keyboard(self.age_choices)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_age_text, 
                                    reply_markup=markup)
        return "NEW_CHOOSING_AGE"

    async def handle_new_user_age__new_user_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        context.user_data['age'] = query.data
        age_choice = self.age_choices[query.data]
        await context.bot.edit_message_text(text=f"You chose {age_choice} as your age range.",
                                                    chat_id=query.message.chat_id, message_id=query.message.id)
        await self.edit_your_gender(update, context)
        return "NEW_CHOOSING_GENDER"

    async def new_user_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = self.keyboard_generator.generate_keyboard(self.gender_choices)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_gender_text, 
                                    reply_markup=markup)
        return "NEW_CHOOSING_GENDER"

    async def handle_new_user_gender__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        context.user_data['gender'] = query.data
        gender_choice = self.gender_choices[query.data]
        await context.bot.edit_message_text(text=f"You chose {gender_choice} as your gender.",
                                            chat_id=query.message.chat_id, message_id=query.message.id)
        
        # Push information online to DB
        telename = update.effective_chat.username
        
        if not self.service.is_user_existing(telename):
            if self.service.create_user(telename,
                                     context.user_data['age'],
                                     context.user_data['gender']):
                await context.bot.send_message(text=f"Welcome {telename}! Your profile has been successfully created!",
                                           chat_id=query.message.chat_id)

        await self.profile_home(update, context)
        return "PROFILE_HOME"

    async def profile_home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        inline_keyboard = [
            [InlineKeyboardButton("Personal Info", callback_data="personal_info")], 
            [InlineKeyboardButton("Food Preference", callback_data="food_pref")],
            [InlineKeyboardButton("Buddy Preference", callback_data="buddy_pref")]
        ]

        message = bot_text.profile
        
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, 
                                       reply_markup=markup, parse_mode="Markdown")
        return "PROFILE_HOME"
    
    async def edit_your_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = self.keyboard_generator.generate_keyboard(self.age_choices)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_age_text, 
                                    reply_markup=markup)
        return "CHOOSING_AGE"

    async def handle_choosing_age__edit_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        telename = update.effective_chat.username
        print(query.data)
        self.service.change_age(telename, query.data)
        age_choice = self.age_choices[query.data]
        await context.bot.edit_message_text(text=f"You chose {age_choice} as your age range.",
                                                    chat_id=query.message.chat_id, message_id=query.message.id)
        await self.edit_your_gender(update, context)
        return "CHOOSING_GENDER"

    async def edit_your_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = self.keyboard_generator.generate_keyboard(self.gender_choices)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_gender_text, 
                                    reply_markup=markup)
        return "CHOOSING_GENDER"

    async def handle_choosing_gender__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        telename = update.effective_chat.username
        self.service.change_gender(telename, query.data)
        gender_choice = self.gender_choices[query.data]
        await context.bot.edit_message_text(text=f"You chose {gender_choice} as your gender.",
                                            chat_id=query.message.chat_id, message_id=query.message.id)
        
        # Push information online to 
        
        # if not self.service.is_user_existing(telename):
        #     if self.service.create_user(telename,
        #                              context.user_data['age'],
        #                              context.user_data['gender']):
        #         await context.bot.send_message(text=f"New profile created",
        #                                    chat_id=query.message.chat_id)

        await self.profile_home(update, context)
        return "PROFILE_HOME"
    
    # async def edit_your_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     markup = self.keyboard_generator.generate_keyboard(self.age_choices)
    #     await context.bot.send_message(chat_id=update.effective_chat.id, 
    #                                 text=bot_text.choose_age_text, 
    #                                 reply_markup=markup)
    #     return "CHOOSING_AGE"

    # async def handle_choosing_age__edit_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     query = update.callback_query
    #     context.user_data["age"] = query.data
    #     age_choice = self.age_choices[query.data]
    #     await context.bot.edit_message_text(text=f"You chose {age_choice} as your age range.",
    #                                                 chat_id=query.message.chat_id, message_id=query.message.id)
    #     await self.edit_your_gender(update, context)
    #     return "CHOOSING_GENDER"

    # async def edit_your_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     markup = self.keyboard_generator.generate_keyboard(self.gender_choices)
    #     await context.bot.send_message(chat_id=update.effective_chat.id, 
    #                                 text=bot_text.choose_gender_text, 
    #                                 reply_markup=markup)
    #     return "CHOOSING_GENDER"

    # async def handle_choosing_gender__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     query = update.callback_query
    #     context.user_data['gender'] = query.data
    #     gender_choice = self.gender_choices[query.data]
    #     await context.bot.edit_message_text(text=f"You chose {gender_choice} as your gender.",
    #                                         chat_id=query.message.chat_id, message_id=query.message.id)
        
    #     # Push information online to 
    #     telename = update.effective_chat.username
    #     if not self.service.is_user_existing(telename):
    #         if self.service.create_user(telename,
    #                                  context.user_data['age'],
    #                                  context.user_data['gender']):
    #             await context.bot.send_message(text=f"New profile created",
    #                                        chat_id=query.message.chat_id)

    #     await self.profile_home(update, context)
    #     return "PROFILE_HOME"

    async def edit_your_cuisine_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = self.keyboard_generator.generate_keyboard(self.cuisine_choices)
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
        markup = self.keyboard_generator.generate_keyboard(self.diet_choices)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_diet_text, 
                                    reply_markup=markup)
        return "CHOOSING_DIET"
