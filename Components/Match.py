import logging
from telegram.ext import *
from telegram import *
import asyncio

from Classes import Service

class Match:
    def __init__(self):
        self.service = Service()

    async def find_match(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        query = update.callback_query

        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.id)
    
        # Check if person has filled up their profile, if haven't prompt them to fill up their profile
        profile = self.service.show_profile(chat_id)
        if not profile["age pref"] or not profile["gender pref"] or not profile["cuisine pref"]:
            inline_keyboard = [
                [InlineKeyboardButton("Back to Home", callback_data="home")]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Profile is incomplete", reply_markup=markup)
            return ConversationHandler.END
        
        # Proceed to match them
        inline_keyboard = [
            [InlineKeyboardButton("Stop Matching", callback_data="dequeue")]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        message = await context.bot.send_message(chat_id=chat_id, text="Finding a match for you!", reply_markup=markup)

        match_result = self.service.match_user(chat_id)
        if match_result:
            partner_id, _ = match_result[0]
            self.service.dequeue_user(partner_id)  # Also dequeue the partner who was in the queue
            await context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Congrats, you have been matched!")
            return "MATCHED"
        else:
            # Repeatedly Check if have been added into queue
            while True:
                if not self.service.is_user_in_queue(chat_id):  # THIS can mean either dequeue or has been successfully added to chatroom
                    if self.service.is_user_in_chat(chat_id):
                        # Matched successfully
                        await context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id)
                        await context.bot.send_message(chat_id=update.effective_chat.id, text="Congrats, you have been matched!")
                        return "MATCHED"
                    else:
                        # User dequeued
                        return ConversationHandler.END
                await asyncio.sleep(1)

    async def dequeue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        query = update.callback_query

        if self.service.dequeue_user(chat_id):
            await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.id)
            inline_keyboard = [
                [InlineKeyboardButton("Back to Home", callback_data="home")]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="You stopped matching", reply_markup=markup)
            return ConversationHandler.END

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Check if user is in chat, else this function should not be executed
        chat_id = update.effective_chat.id
        if not self.service.is_user_in_chat(chat_id):
            return "POST_CHAT"

        chatroom_id = self.service.select_chatroom(chat_id)

        partner_ids = [id for id in self.service.select_chatroom_user(chatroom_id) if id != chat_id]
        for partner in partner_ids:
            if update.message["text"]:
                await context.bot.send_message(chat_id = partner, text = update.message["text"])
            elif update.message["photo"]:
                await context.bot.send_photo(chat_id = partner, photo = update.message["photo"][0])
            elif update.message["sticker"]:
                await context.bot.send_sticker(chat_id = partner, sticker = update.message["sticker"])
            return "MATCHED"
        
        
    async def options(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Check if the user is in chat, else this function should not be allowed
        chat_id = update.effective_chat.id
        if not self.service.is_user_in_chat(chat_id):
            await context.bot.send_message(chat_id=chat_id, text="This function is only available in chat")
        
        inline_keyboard = [
            [InlineKeyboardButton("Recommend Food", callback_data="find_food")], 
            [InlineKeyboardButton("End Match", callback_data="leave_chat")],
            [InlineKeyboardButton("Close Options", callback_data="return_to_matched")],
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=chat_id, text="HEre are y our options grrr meowm", reply_markup=markup)
        return "OPTIONS"

    async def leave_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.id)
        
        # remove user from chat
        chat_id = update.effective_chat.id
        chatroom_id = self.service.select_chatroom(chat_id)

        self.service.delete_chatroom_user(chat_id)
        await self.post_chat(chat_id, context)
        
        # If there is only 1 other user, then remove them as well
        remaining = self.service.select_chatroom_user(chatroom_id)
        if len(remaining) == 1:
            self.service.delete_chatroom_user(remaining[0])
            await self.post_chat(remaining[0], context)
        return "POST_CHAT"
        
    async def post_chat(self, chat_id, context):
        """Handles the post chat buttons
        """
        inline_keyboard = [
                [InlineKeyboardButton("Report Previous User", callback_data="report")],
                [InlineKeyboardButton("Find another Match", callback_data="find_match")],
                [InlineKeyboardButton("Back to Home", callback_data="home")]
            ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=chat_id, text="Your chat has ended", reply_markup=markup)
        return

    async def find_food(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Food Recommendations are Coming SOON!")
        return "MATCHED"
    
    async def report(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="REPORT feature is Coming SOON!")
        return "POST_CHAT"
        