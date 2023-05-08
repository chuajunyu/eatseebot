import logging
from telegram.ext import *
from telegram import *
import time
import bot_text

from Classes import Service

class Match:
    
    def __init__(self):
        self.service = Service()
        
        self.partner = None
        
    
    async def queue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telename = update.effective_chat.username
        
        if self.service.queue_user(telename):
            
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="Matching...")
            
            return "MATCH"
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="Oops something went wrong, try again?")
            return "DEQUEUE"
        
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
                self.partner = userid[1]
                return "MATCHED"
                
            
         
        inline_keyboard = [
            [InlineKeyboardButton('Return to home', callback_data='dequeue')]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No matches found for u :(", reply_markup=markup)
        return "DEQUEUE"
    

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
        await context.bot.send_message(chat_id = "@" + self.partner, text = context.bot.message(from_user = "@" + telename))
