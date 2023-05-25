import logging

from Classes import *
from Components import * 
from telegram.ext import *
from telegram import *


config = ConfigManager("dev.config")
api_key = config.get("telegram_key")
home = Home()
profile = Profile()
match = Match()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(api_key).build()

    home_handler = ConversationHandler(
        entry_points=[CommandHandler("start", home.start),
                      CallbackQueryHandler(callback=home.back_to_start,
                                           pattern="home")],
        states={
            "HOME_START": [CallbackQueryHandler(callback=home.back_to_start,
                                           pattern="home")]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), home.start)],
        name="match_conversation",
        persistent=False,
        allow_reentry=True
    )

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
                        callback=profile.edit_your_cuisine_pref,
                        pattern="food_pref"
                    ),
                    CallbackQueryHandler(
                        callback=profile.choose_buddy_age_pref,
                        pattern="buddy_pref"
                    ),
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
                    callback=profile.handle_choosing_cuisine__edit_diet,
                    pattern="1|2|3|4|5|6|7|8|Select All|Done"
                )
            ],
            "CHOOSING_DIET": [
                CallbackQueryHandler(
                    callback=profile.handle_choosing_diet__home,
                    pattern="1|2|3|Select All|Done"
                )
            ],
            "CHOOSING_BUDDY_AGE": [
                CallbackQueryHandler(
                    callback=profile.handle_buddy_age__buddy_gender,
                    pattern="1|2|3|4|5|6|Select All|Done"
                )
            ],
            "CHOOSING_BUDDY_GENDER": [
                CallbackQueryHandler(
                    callback=profile.handle_buddy_gender__home,
                    pattern="1|2|3|Select All|Done"
                )
            ]
        },
        fallbacks=[CommandHandler("start", home.start)],
        name="profile_conversation",
        persistent=False,
        allow_reentry=True
    )

    match_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(match.find_match, pattern = "match", block=False),
                      CallbackQueryHandler(match.dequeue, pattern="dequeue", block=False)],
        states={
            "MATCHED": [
                MessageHandler(filters = None, callback = match.chat),
                CommandHandler("end", match.dequeue)
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), home.start)],
        name="match_conversation",
        persistent=False,
        allow_reentry=True
    )

    application.add_handler(home_handler)
    application.add_handler(profile_handler)
    application.add_handler(match_handler)

    # application.add_handler(CallbackQueryHandler(match.find_match, pattern='match', block=False))
    application.add_handler(CallbackQueryHandler(match.dequeue, pattern='dequeue', block=False))
    application.run_polling()

if __name__ == '__main__':
    count = True
    main()
