import logging

from Classes import *
from Components import *

from telegram.ext import *
from telegram import *


config = ConfigManager("dev.config")
api_key = config.get("telegram_key")

home = Home()
profile = Profile()

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
                                           pattern="profile"),
                      CallbackQueryHandler(callback=profile.new_user_age,
                                           pattern="new_profile")                    
                                           ],
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
            "NEW_CHOOSING_AGE": [
                CallbackQueryHandler(
                    callback=profile.handle_new_user_age__new_user_gender,
                    pattern="1|2|3|4|5|6"
                )
            ],
            "NEW_CHOOSING_GENDER": [
                CallbackQueryHandler(
                    callback=profile.handle_new_user_gender__home,
                    pattern="1|2|3"
                )
            ],
            "CHOOSING_AGE": [
                CallbackQueryHandler(
                    callback=profile.handle_choosing_age__edit_gender,
                    pattern="1|2|3|4|5|6"
                )
            ],
            "CHOOSING_GENDER": [
                CallbackQueryHandler(
                    callback=profile.handle_choosing_gender__home,
                    pattern="1|2|3"
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
            ],
        },
        fallbacks=[CommandHandler("start", home.start)],
        name="profile_conversation",
        persistent=False,
    )


    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    home_handler = ConversationHandler(
        entry_points=[CommandHandler("start", home.start)],
        states={
            "HOME_START": [
                CallbackQueryHandler(
                    callback=home.not_implemented_yet,
                    pattern="match"
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), home.start)],
        name="home_conversation",
        persistent=False,
    )

    application.add_handler(home_handler)
    application.add_handler(profile_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
