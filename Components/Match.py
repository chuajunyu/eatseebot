import logging
from telegram.ext import *
from telegram import *
import time
import bot_text

from Classes import Service

class Match:
    
    def __init__(self):
        self.service = Service()
        self.state = True
        
    
    async def matching(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        
        if self.service.match_user(chat_id):
        #when match is successful
            return "MATCHED"
        else:
        #when match failed
        #keep running _function to check if telename in queue is matched
            start = time.time()
            while(time.time() - start <20) and self.state:
                
                if not self.service.check_queue(chat_id):
                    #not found in table means matched
                    
                    return "MATCHED"
                
            
        await self.dequeue(update, context)
        inline_keyboard = [
            [InlineKeyboardButton('Return to home', callback_data='home')]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No matches found for u :(", reply_markup=markup)
        return ConversationHandler.END
    

    async def dequeue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        if self.service.dequeue_user(chat_id):
            
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="CHAT END")
            
            return ConversationHandler.END
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="DEQUEUE FUNCTION ERROR")
            
            return ConversationHandler.END

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        chatroom_id = self.service.select_chatroom(chat_id)
        partner_id = self.service.select_chatroom_user(chatroom_id)[0]
        await context.bot.send_message(chat_id = partner_id, text = update.message["text"])
        return "Matched"
        #for more than 2 ppl matching next time
        #if len(partner_id) > 1:
