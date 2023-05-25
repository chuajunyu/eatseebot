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
    
        # Check if person has filled up their profile, if haven't prompt them to fill up their profile
        profile = self.service.show_profile(chat_id)
        print(profile)
        if not profile["age pref"] or not profile["gender pref"] or not profile["cuisine pref"]:
            inline_keyboard = [
                [InlineKeyboardButton("Back to Home", callback_data="home")]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Profile is incomplete", reply_markup=markup)
            return ConversationHandler.END
        
        # Proceed to match them
        else:
            
            inline_keyboard = [
                [InlineKeyboardButton("Stop Matching", callback_data="dequeue")]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)
            await update.callback_query.message.reply_text(text="Finding a match for you!", reply_markup=markup)

            match_result = self.service.match_user(chat_id)
            if match_result:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Congrats, you have been matched!")
                return "MATCHED"
            else:
                # Repeatedly Check if have been added into queue
                while True:
                    print(self.service.is_user_in_queue(chat_id))
                    if not self.service.is_user_in_queue(chat_id):  # THIS can mean either dequeue or has been successfully added to chatroom
                        if self.service.is_user_in_chat(chat_id):
                            # Matched successfully
                            await context.bot.send_message(chat_id=update.effective_chat.id, text="Congrats, you have been matched!")
                            return "MATCHED"
                        else:
                            # User dequeued
                            await context.bot.send_message(chat_id=update.effective_chat.id, text="You have been dequeued")
                            return ConversationHandler.END
                    await asyncio.sleep(1)


        
        # if self.service.match_user(chat_id):
        # #when match is successful
        #     return "MATCHED"
        # else:
        # #when match failed
        # #keep running _function to check if telename in queue is matched
        #     start = time.time()
        #     while(time.time() - start <20) and self.state:
                
        #         if not self.service.check_queue(chat_id):
        #             #not found in table means matched
                    
        #             return "MATCHED"
                
            
        # await self.dequeue(update, context)
        # inline_keyboard = [
        #     [InlineKeyboardButton('Return to home', callback_data='home')]
        # ]
        # markup = InlineKeyboardMarkup(inline_keyboard)
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="No matches found for u :(", reply_markup=markup)
        # return ConversationHandler.END
    

    async def dequeue(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("dequeue calllleld")
        chat_id = update.effective_chat.id
        if self.service.dequeue_user(chat_id):
            inline_keyboard = [
                [InlineKeyboardButton("Back to Home", callback_data="home")]
            ]
            markup = InlineKeyboardMarkup(inline_keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="CHAT END", reply_markup=markup)
            
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
        return "MATCHED"
        #for more than 2 ppl matching next time
        #if len(partner_id) > 1:
