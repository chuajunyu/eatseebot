import logging
from telegram.ext import *
from telegram import *
import time
import bot_text

from Classes import Service

class Match:
    
    def __init__(self):
        self.service = Service()
        
        
        
        
    
    async def queue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telename = update.effective_chat.username
        
        if self.service.queue_user(telename):
            
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="Matching...")
            await self.matching(update, context)
            
            return None
        else:
            await self.dequeue(update, context)
            inline_keyboard = [
            [InlineKeyboardButton('Try again', callback_data='queue')]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Oops something went wrong, try again?", reply_markup=markup)
            
            
            return None
    
    
    
    async def matching(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telename = update.effective_chat.username
        start = time.time()
        while(time.time() - start <20):
            userid = self.service.match_user(telename) #userid of match
            
            if userid:
                data = self.service.show_profile(userid[1])  #telename
                message = bot_text.profile.format(data["telename"],
                                                data["age"],
                                                data["gender"],
                                                )
                await context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text= message )
                
                return "MATCHED"
                
            
        await self.dequeue(update, context)
        inline_keyboard = [
            [InlineKeyboardButton('Return to home', callback_data='home')]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No matches found for u :(", reply_markup=markup)
        return ConversationHandler.END
    

    async def dequeue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telename = update.effective_chat.username
        if self.service.dequeue_user(telename):
            
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="DEQUEUED")
            
            return ConversationHandler.END
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="sum happened")
            
            return ConversationHandler.END

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telename = update.effective_chat.username
        user_id = self.service.get_user_id(telename)
        partner_id = self.service.select_chatroom_user(user_id)
        if partner_id == None:
            partner_id = self.service.select_chatroom(user_id)
        partner_telename = self.service.show_profile(partner_id)["telename"]
        await context.bot.send_message(chat_id = "@" + partner_telename, text = context.bot.message(from_user = "@" + telename))