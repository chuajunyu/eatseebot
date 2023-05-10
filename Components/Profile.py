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

        self.multi_input = {
            'Select All': 'Select All',
            'Done': 'Done'
        }

    async def single_age_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = self.keyboard_generator.generate_keyboard(self.age_choices)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_age_text, 
                                    reply_markup=markup)
    
    async def single_gender_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        markup = self.keyboard_generator.generate_keyboard(self.gender_choices)
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=bot_text.choose_gender_text, 
                                    reply_markup=markup)
        
    async def multi_age_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, edit=False):
        choices = dict(self.age_choices, **self.multi_input)
        markup = self.keyboard_generator.generate_keyboard(choices, selected)
        if edit:
            query = update.callback_query
            await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                message_id=query.message.id,
                                                text=bot_text.choose_buddy_age, 
                                                reply_markup=markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text=bot_text.choose_buddy_age, 
                                        reply_markup=markup)
    
    async def multi_gender_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, edit=False):
        choices = dict(self.gender_choices, **self.multi_input)
        markup = self.keyboard_generator.generate_keyboard(choices, selected)
        if edit:
            query = update.callback_query
            await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                message_id=query.message.id,
                                                text=bot_text.choose_buddy_gender, 
                                                reply_markup=markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text=bot_text.choose_buddy_gender, 
                                        reply_markup=markup)
            
    async def multi_cuisine_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, edit=False):
        choices = dict(self.cuisine_choices, **self.multi_input)
        markup = self.keyboard_generator.generate_keyboard(choices, selected)
        if edit:
            query = update.callback_query
            await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                message_id=query.message.id,
                                                text=bot_text.choose_cuisine_text, 
                                                reply_markup=markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text=bot_text.choose_cuisine_text, 
                                        reply_markup=markup)
    
    async def multi_diet_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, edit=False):
        choices = dict(self.diet_choices, **self.multi_input)
        markup = self.keyboard_generator.generate_keyboard(choices, selected)
        if edit:
            query = update.callback_query
            await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                message_id=query.message.id,
                                                text=bot_text.choose_diet_text, 
                                                reply_markup=markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text=bot_text.choose_diet_text, 
                                        reply_markup=markup)

    async def new_user_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.single_age_input(update, context)
        return "NEW_CHOOSING_AGE" 

    async def handle_new_user_age__new_user_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        context.user_data['age'] = query.data
        age_choice = self.age_choices[query.data]
        await context.bot.edit_message_text(text=f"You chose {age_choice} as your age range.",
                                                    chat_id=query.message.chat_id, message_id=query.message.id)
        await self.single_gender_input(update, context)
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
            [InlineKeyboardButton("Buddy Preference", callback_data="buddy_pref"),],
            [InlineKeyboardButton("Back to Home", callback_data="home"),]
        ]
        message = bot_text.profile
        
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, 
                                       reply_markup=markup, parse_mode="Markdown")
        return "PROFILE_HOME"
    
    async def edit_your_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.single_age_input(update, context)
        return "CHOOSING_AGE"

    async def handle_choosing_age__edit_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        telename = update.effective_chat.username
        self.service.change_age(telename, query.data)
        age_choice = self.age_choices[query.data]
        await context.bot.edit_message_text(text=f"You chose {age_choice} as your age range.",
                                                    chat_id=query.message.chat_id, message_id=query.message.id)
        await self.single_gender_input(update, context)
        return "CHOOSING_GENDER"

    async def handle_choosing_gender__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        telename = update.effective_chat.username
        self.service.change_gender(telename, query.data)
        gender_choice = self.gender_choices[query.data]
        await context.bot.edit_message_text(text=f"You chose {gender_choice} as your gender.",
                                            chat_id=query.message.chat_id, message_id=query.message.id)
        # EDIT USER INFORMATION
        await self.profile_home(update, context)
        return "PROFILE_HOME"
    
    async def choose_buddy_age_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Query db for users current buddy age pref
        telename = update.effective_chat.username
        selected = self.service.select_user_age_pref(telename)
        context.user_data["buddy_age"] = selected
        
        await self.multi_age_input(update, context, selected)
        return "CHOOSING_BUDDY_AGE"

    async def handle_buddy_age__buddy_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        pressed = query.data
        if pressed == "Done":
            if context.user_data["buddy_age"]:
                telename = update.effective_chat.username
                self.service.change_age_preferences(telename, context.user_data["buddy_age"])
                await context.bot.edit_message_text(text=f"Buddy Age Preferences Registered!",
                                                        chat_id=query.message.chat_id, message_id=query.message.id)
                await self.choose_buddy_gender(update, context)
                return "CHOOSING_BUDDY_GENDER"
        else:
            if pressed == "Select All":
                if context.user_data["buddy_age"] != list(self.age_choices.keys()):
                    context.user_data["buddy_age"] = list(self.age_choices.keys())
                else:
                    context.user_data["buddy_age"] = list()
            elif pressed in context.user_data['buddy_age']:
                context.user_data["buddy_age"].remove(pressed)
            else:
                context.user_data["buddy_age"].append(pressed)

        await self.multi_age_input(update, context, context.user_data["buddy_age"], edit=True)
        return "CHOOSING_BUDDY_AGE"
        
    async def choose_buddy_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):       
        telename = update.effective_chat.username
        selected = self.service.select_user_gender_pref(telename)
        context.user_data["buddy_gender"] = selected
        await self.multi_gender_input(update, context, selected)

    async def handle_buddy_gender__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        pressed = query.data
        if pressed == "Done":
            if context.user_data["buddy_gender"]:
                telename = update.effective_chat.username
                self.service.change_gender_preferences(telename, context.user_data["buddy_gender"])
                await context.bot.edit_message_text(text=f"Buddy Gender Preferences Registered!",
                                                        chat_id=query.message.chat_id, message_id=query.message.id)
                await self.profile_home(update, context)
                return "PROFILE_HOME"
        else:
            if pressed == "Select All":
                if context.user_data["buddy_gender"] != list(self.gender_choices.keys()):
                    context.user_data["buddy_gender"] = list(self.gender_choices.keys())
                else:
                    context.user_data["buddy_gender"] = list()
            elif pressed in context.user_data['buddy_gender']:
                context.user_data["buddy_gender"].remove(pressed)
            else:
                context.user_data["buddy_gender"].append(pressed)

        await self.multi_gender_input(update, context, context.user_data["buddy_gender"], edit=True)
        return "CHOOSING_BUDDY_GENDER"

    async def edit_your_cuisine_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telename = update.effective_chat.username
        selected = self.service.select_user_age_pref(telename)
        context.user_data["cuisine"] = selected
        
        await self.multi_cuisine_input(update, context, selected)
        return "CHOOSING_CUISINE"
    
    async def handle_choosing_cuisine__edit_diet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        pressed = query.data
        if pressed == "Done":
            if context.user_data["cuisine"]:
                telename = update.effective_chat.username
                self.service.change_cuisine_preferences(telename, context.user_data["cuisine"])
                await context.bot.edit_message_text(text=f"Cuisine Preferences Registered!",
                                                        chat_id=query.message.chat_id, message_id=query.message.id)
                await self.edit_your_diet_pref(update, context)
                return "CHOOSING_DIET"
        else:
            if pressed == "Select All":
                if context.user_data["cuisine"] != list(self.cuisine_choices.keys()):
                    context.user_data["cuisine"] = list(self.cuisine_choices.keys())
                else:
                    context.user_data["cuisine"] = list()
            elif pressed in context.user_data['cuisine']:
                context.user_data["cuisine"].remove(pressed)
            else:
                context.user_data["cuisine"].append(pressed)

        await self.multi_cuisine_input(update, context, context.user_data["cuisine"], edit=True)
        return "CHOOSING_CUISINE"

    async def edit_your_diet_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):    
        telename = update.effective_chat.username
        selected = self.service.select_user_age_pref(telename)
        context.user_data["diet"] = selected
        
        await self.multi_diet_input(update, context, selected)
        return "CHOOSING_DIET"
    
    async def handle_choosing_diet__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        pressed = query.data
        if pressed == "Done":
            if context.user_data["diet"]:
                telename = update.effective_chat.username
                self.service.change_diet_preferences(telename, context.user_data["diet"])
                await context.bot.edit_message_text(text=f"Diet Preferences Registered!",
                                                        chat_id=query.message.chat_id, message_id=query.message.id)
                await self.profile_home(update, context)
                return "PROFILE_HOME"
        else:
            if pressed == "Select All":
                if context.user_data["diet"] != list(self.diet_choices.keys()):
                    context.user_data["diet"] = list(self.diet_choices.keys())
                else:
                    context.user_data["diet"] = list()
            elif pressed in context.user_data['diet']:
                context.user_data["diet"].remove(pressed)
            else:
                context.user_data["diet"].append(pressed)

        await self.multi_diet_input(update, context, context.user_data["diet"], edit=True)
        return "CHOOSING_DIET"
