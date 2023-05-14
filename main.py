import logging

from Classes import *
from Components import * 
from Components import Match
from telegram.ext import *
from telegram import *


config = ConfigManager("dev.config")
api_key = config.get("telegram_key")
home = Home()
profile = Profile()
match = Match.Match()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(api_key).build()

    profile_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(callback=profile.profile_home,
                                           pattern="profile")],
        states={
            "PROFILE_HOME": [
                    CallbackQueryHandler(
                        callback=profile.edit_your_age,
                        pattern="personal_info"
                    ),
                    CallbackQueryHandler(
                        callback=home.not_implemented_yet,
                        pattern="food_pref"
                    ),
                    CallbackQueryHandler(
                        callback=home.not_implemented_yet,
                        pattern="buddy_pref"
                    )
            ],
            "CHOOSING_AGE": [
                CallbackQueryHandler(
                    callback=profile.handle_choosing_age__edit_gender,
                    pattern="16-19|20-24|25-29"
                )
            ],
            "CHOOSING_GENDER": [
                CallbackQueryHandler(
                    callback=profile.handle_choosing_gender__home,
                    pattern="Male|Female|Non Binary"
                )
            ],
            "CHOOSING_CUISINE": [
                CallbackQueryHandler(
                    callback=profile.edit_your_dietary_pref,
                    pattern="Chinese|Malay|Indian|Western"
                )
            ],
            "CHOOSING_DIET": [
                CallbackQueryHandler(
                    callback=profile.edit_your_age,
                    pattern="yourinfo"
                )
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), home.start)],
        name="profile_conversation",
        persistent=False,
    )


    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    home_handler = ConversationHandler(
        entry_points=[CommandHandler("start", home.start), CallbackQueryHandler(home.start, pattern = "home")],
        states={

        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), home.start)],
        name="match_conversation",
        persistent=False,
    )


    match_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(match.queue, pattern = "queue")],
        states={
            "MATCHED": [
                
                MessageHandler(filters = None, callback = match.chat),
                CommandHandler("end", match.dequeue)
            ],
            "DEQUEUE": [
                CallbackQueryHandler(match.dequeue)
            ]
            
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), home.start)],
        name="match_conversation",
        persistent=False,
    )

    application.add_handler(home_handler)
    application.add_handler(profile_handler)
    application.add_handler(match_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
