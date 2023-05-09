from telegram.ext import *
from telegram import *


class KeyboardGenerator:
    """Generates Complex Inline Keyboard Markups for the Telegram Bot"""
    def __init__(self):
        self.max_width = 2

    def generate_keyboard(self, choices, selected=[], selected_icon='\u2705'):  # ✅  
        keyboard = list()
        row = list()
        for choice in choices.items():
            callback_data, option = choice

            # If option is selected, add a tick beside it
            if option in selected:
                option_text = option + " " + selected_icon
            else:
                option_text = option

            row.append(InlineKeyboardButton(option_text, callback_data=callback_data))

            # If row has 2 buttons, create another row below
            if len(row) == self.max_width:
                keyboard.append(row)
                row = list()
        if row:
            keyboard.append(row)

        markup = InlineKeyboardMarkup(keyboard)
        return markup


