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

    async def single_option_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, field, edit=False):
        markup = self.keyboard_generator.generate_keyboard(eval(f"self.{field}_choices"))
        message=eval(f"bot_text.choose_{field}_text")
        if edit:
            query = update.callback_query
            await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                message_id=query.message.id,
                                                text=message, 
                                                reply_markup=markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text=message, 
                                        reply_markup=markup)

    async def single_age_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, edit=False):
        await self.single_option_input(update, context, "age", edit=edit)
    
    async def single_gender_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, edit=False):
        await self.single_option_input(update, context, "gender", edit=edit)
            
    async def multi_option_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, field, selected, 
                                 edit=False, special_text=None):
        choices = dict(eval(f"self.{field}_choices"), **self.multi_input)
        markup = self.keyboard_generator.generate_keyboard(choices, selected)

        message=eval(f"bot_text.choose_multi_{field}")

        if special_text:
            message += f"\n\n{special_text}"

        if edit:
            query = update.callback_query
            await context.bot.edit_message_text(chat_id=query.message.chat_id,
                                                message_id=query.message.id,
                                                text=message, 
                                                reply_markup=markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text=message, 
                                        reply_markup=markup)
        
    async def multi_age_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, 
                              edit=False, special_text=None):
        await self.multi_option_input(update, context, "age", selected, edit=edit, special_text=special_text)
    
    async def multi_gender_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, 
                              edit=False, special_text=None):
        await self.multi_option_input(update, context, "gender", selected, edit=edit, special_text=special_text)
            
    async def multi_cuisine_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, 
                              edit=False, special_text=None):
        await self.multi_option_input(update, context, "cuisine", selected, edit=edit, special_text=special_text)
    
    async def multi_diet_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, selected, 
                              edit=False, special_text=None):
        await self.multi_option_input(update, context, "diet", selected, edit=edit, special_text=special_text)

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
        await self.profile_home(update, context, is_redirect=True)
        return "PROFILE_HOME"

    async def profile_home(self, update: Update, context: ContextTypes.DEFAULT_TYPE, is_redirect=False):
        inline_keyboard = [
            [InlineKeyboardButton("Personal Info", callback_data="personal_info")], 
            [InlineKeyboardButton("Food Preference", callback_data="food_pref")],
            [InlineKeyboardButton("Buddy Preference", callback_data="buddy_pref"),],
            [InlineKeyboardButton("Back to Home", callback_data="home"),]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        message = bot_text.profile
        if is_redirect:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, 
                                        reply_markup=markup, parse_mode="Markdown")
        else:
            query = update.callback_query
            await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, 
                                        reply_markup=markup, parse_mode="Markdown")
            
            return "PROFILE_HOME"
    
    async def edit_your_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.single_age_input(update, context, edit=True)
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
        await self.profile_home(update, context, is_redirect=True)
        return "PROFILE_HOME"
    
    async def choose_buddy_age_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Query db for users current buddy age pref
        telename = update.effective_chat.username
        selected = self.service.select_user_age_pref(telename)
        context.user_data["age"] = selected
        print(selected)
        
        await self.multi_age_input(update, context, selected, edit=True)
        return "CHOOSING_BUDDY_AGE"

    async def handle_buddy_age__buddy_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        async def done():
            await self.choose_buddy_gender(update, context)
        
        return await self.general_multi_handler(update, context, "age", "CHOOSING_BUDDY_AGE", 
                                                "CHOOSING_BUDDY_GENDER", done_function=done)
        
    async def choose_buddy_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):       
        telename = update.effective_chat.username
        selected = self.service.select_user_gender_pref(telename)
        context.user_data["gender"] = selected
        await self.multi_gender_input(update, context, selected)

    async def handle_buddy_gender__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        async def done():
            await self.profile_home(update, context, is_redirect=True)
        
        return await self.general_multi_handler(update, context, "gender", "CHOOSING_BUDDY_GENDER", 
                                                "PROFILE_HOME", done_function=done)

    async def edit_your_cuisine_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telename = update.effective_chat.username
        selected = self.service.select_user_cuisine_pref(telename)
        context.user_data["cuisine"] = selected
        
        await self.multi_cuisine_input(update, context, selected, edit=True)
        return "CHOOSING_CUISINE"
    
    async def handle_choosing_cuisine__edit_diet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        async def done():
            await self.edit_your_diet_pref(update, context)
        
        return await self.general_multi_handler(update, context, "cuisine", "CHOOSING_CUISINE", 
                                                "CHOOSING_DIET", done_function=done)

    async def edit_your_diet_pref(self, update: Update, context: ContextTypes.DEFAULT_TYPE):    
        telename = update.effective_chat.username
        selected = self.service.select_user_diet_pref(telename)
        context.user_data["diet"] = selected
        
        await self.multi_diet_input(update, context, selected)
        return "CHOOSING_DIET"
    
    async def handle_choosing_diet__home(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        async def done():
            await self.profile_home(update, context, is_redirect=True)
        
        return await self.general_multi_handler(update, context, "diet", "CHOOSING_DIET", "PROFILE_HOME", done_function=done,
                                                can_be_empty=True)

    async def general_multi_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE, field: str,
                              choosing_state, done_state, done_function, can_be_empty=False):
        query = update.callback_query
        pressed = query.data
        if pressed == "Done":
            if context.user_data[field] or can_be_empty:
                telename = update.effective_chat.username
                eval(f"self.service.change_{field}_preferences")(telename, context.user_data[field])
                await context.bot.edit_message_text(text=f"{field.capitalize()} Preferences Registered!",
                                                        chat_id=query.message.chat_id, message_id=query.message.id)
                await done_function()
                return done_state
            else:
                await eval(f"self.multi_{field}_input")(update, context, context.user_data[field], 
                                            edit=True, special_text="Please select at least 1 option.")
                return choosing_state
        else:
            if pressed == "Select All":
                if set(context.user_data[field]) != set(list(eval(f"self.{field}_choices.keys()"))):
                    context.user_data[field] = list(eval(f"self.{field}_choices.keys()"))
                else:
                    context.user_data[field] = list()
            elif pressed in context.user_data[field]:
                context.user_data[field].remove(pressed)
            else:
                context.user_data[field].append(pressed)

        await eval(f"self.multi_{field}_input")(update, context, context.user_data[field], edit=True)
        return choosing_state
