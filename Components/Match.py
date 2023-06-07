import logging
from telegram.ext import *
from telegram import *
import asyncio

from Classes import Service

class Match:
    """
    Class Handling the Matching and Chatting of users, as well as the functions within
    the chat, such as getting food recommendations
    """
    def __init__(self):
        self.service = Service()
        self.location= dict()
        self.pending_location = list()

    async def matched_state(self, update, context):
        return "MATCHED"

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

    def get_chatroom_users(self, chat_id):
        chatroom_id = self.service.select_chatroom(chat_id)
        return self.service.select_chatroom_user(chatroom_id)
        
    def get_partner_ids(self, chat_id):
        return [id for id in self.get_chatroom_users(chat_id) if id != chat_id]
        
    async def send_text(self, recipient_ids, message, context: ContextTypes.DEFAULT_TYPE):
        for recipient in recipient_ids:
            await context.bot.send_message(chat_id=recipient, text=message)

    async def send_payload_to_partners(self, partner_ids, message, context: ContextTypes.DEFAULT_TYPE):
        for partner in partner_ids:
            if message["text"]:
                await context.bot.send_message(chat_id=partner, text=message["text"])
            elif message["photo"]:
                await context.bot.send_photo(chat_id=partner, photo=message["photo"][0])
            elif message["sticker"]:
                await context.bot.send_sticker(chat_id=partner, sticker=message["sticker"])

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Check if user is in chat, else this function should not be executed
        chat_id = update.effective_chat.id
        if not self.service.is_user_in_chat(chat_id):
            return "POST_CHAT"
        
        partner_ids = self.get_partner_ids(chat_id)
        await self.send_payload_to_partners(partner_ids, update.message, context)
        return "MATCHED"
    
    async def handle_get_location_partner(self, update, context):
        chat_id = update.effective_chat.id

        if chat_id in self.pending_location:
            self.pending_location.remove(chat_id)
        else:
            return "MATCHED"
        
        message = update.message
        current_pos = (message.location.latitude, message.location.longitude)
        self.location[chat_id] = current_pos
        return "MATCHED"
            
    async def options(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Check if the user is in chat, else this function should not be allowed
        chat_id = update.effective_chat.id
        if not self.service.is_user_in_chat(chat_id):
            await context.bot.send_message(chat_id=chat_id, text="This function is only available in chat")
        
        inline_keyboard = [
            [InlineKeyboardButton("Recommend Food", callback_data="find_food")], 
            [InlineKeyboardButton("End Match", callback_data="leave_chat")],
            [InlineKeyboardButton("Cancel", callback_data="return_to_matched")],
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
        
        self.pending_location.remove(chat_id)
        self.service.delete_chatroom_user(chat_id)
        await self.post_chat(chat_id, context)
        
        # If there is only 1 other user, then remove them as well
        remaining = self.service.select_chatroom_user(chatroom_id)
        if len(remaining) == 1:
            self.service.delete_chatroom_user(remaining[0])
            self.pending_location.remove(remaining[0])
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
        query = update.callback_query
        await context.bot.edit_message_text(text="Hungry liao isit?", chat_id=query.message.chat_id, message_id=query.message.id)

        inline_keyboard = [
                [InlineKeyboardButton("Quick Recommendations", callback_data="quick_find")],
                [InlineKeyboardButton("Customized Recommendations", callback_data="custom_find")],
                [InlineKeyboardButton("Cancel", callback_data="return_to_matched")]
            ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        chat_id = update.effective_chat.id
        await context.bot.send_message(chat_id=chat_id, text="what kind of food recoomendation u want", reply_markup=markup)
        return "CHOOSING_REC_TYPE"
    
    async def quick_find(self, update, context):
        query = update.callback_query
        await context.bot.edit_message_text(text="You chose quickfind", chat_id=query.message.chat_id, message_id=query.message.id)

        chat_id = update.effective_chat.id
        inline_keyboard = [
                [InlineKeyboardButton("Enter your live locations", callback_data="location")],
                [InlineKeyboardButton("Choose a town!", callback_data="town")],
                [InlineKeyboardButton("Cancel", callback_data="return_to_matched")]
            ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=chat_id, text="choose how u want your location thingy bro", reply_markup=markup)
        return "CHOOSING_LOCATION_TYPE"

    async def get_location(self, update, context):
        query = update.callback_query
        await context.bot.edit_message_text(text="You selected live locations", chat_id=query.message.chat_id, message_id=query.message.id)
        chat_id = update.effective_chat.id
        message = "Send your gps location pls"
        chatroom_user_ids = self.get_chatroom_users(chat_id)
        self.pending_location.extend(chatroom_user_ids)
        await self.send_text(chatroom_user_ids, message, context)
        return 'WAITING_FOR_LOC'

    async def handle_get_location(self, update, context):
        chat_id = update.effective_chat.id
        message = update.message
        current_pos = (message.location.latitude, message.location.longitude)
        self.pending_location.remove(chat_id)
        self.location[chat_id] = current_pos

        chatroom_user_ids = self.get_chatroom_users(chat_id)
        
        while any([True for id in chatroom_user_ids if id in self.pending_location]):
            await asyncio.sleep(2)

        coordinates = [self.location[id] for id in chatroom_user_ids if id in self.location]
        result = self.service.get_food_recommendations(chatroom_user_ids, coordinates)
        
        for restaurant in result[:5]:
            message = self.service.format_restaurant(restaurant)
            await self.send_text(chatroom_user_ids, message, context)
        return "MATCHED"

    async def get_town(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="REPORT feature is Coming SOON!")
        return "MATCHED"

    async def custom_find(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="CUSTOM FIND is Coming SOON!")
        return "POST_CHAT"
    
    async def report(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="REPORT feature is Coming SOON!")
        return "POST_CHAT"
        