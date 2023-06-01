from telegram.ext import *
from telegram import *


class KeyboardGenerator:
    """Generates Complex Inline Keyboard Markups for the Telegram Bot"""
    def __init__(self):
        self.max_width = 2

    def generate_keyboard(self, choices, selected=[], selected_icon='\u2705'):  # ✅  
        """Generates an inline keyboard automatically.
        Accomodates multi option inline keyboards by printing the ✅ icon (or any unicode icon) 
        beside all options specified under the selected list.
        
        Input:
            [choices]: Dictionary representing key value pairs of callback data to option text
            [selected]: List of string representing the options that have been selected by the user
            [selected_icon]: String representing the unicode code for the icon beside selected options
                             Defaulted to ✅

        """
        keyboard = list()
        row = list()
        for choice in choices.items():
            callback_data, option = choice

            # If option is selected, add a tick beside it
            if callback_data in selected:
                option_text = str(option) + " " + selected_icon
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
