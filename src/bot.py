from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CAT_API_KEY = os.getenv('CAT_API_KEY')

SCH, DONE, GIF = range(3)

async def hello(update, context):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def chooseSchool(update, context):
    keyboard = [
        [
            InlineKeyboardButton("NUS", callback_data="NUS"),
            InlineKeyboardButton("NTU", callback_data="NTU"),
            InlineKeyboardButton("SMU", callback_data="SMU")
        ],
        [
            InlineKeyboardButton("SUTD", callback_data="SUTD"),
            InlineKeyboardButton("SIT", callback_data="SIT"),
            InlineKeyboardButton("SUSS", callback_data="SUSS")
        ],
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Done", callback_data='done'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # await context.bot.send_message("Please choose a univerSITy:", reply_markup=reply_markup)
    await update.callback_query.message.edit_text("Please choose a univerSITy:", reply_markup=reply_markup)

async def selectSection(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Personal Information", callback_data="pinfo"),
            InlineKeyboardButton("School", callback_data="sch"),
        ],
        [
            InlineKeyboardButton("Current education", callback_data="curred"),
            InlineKeyboardButton("Seeking degree", callback_data="seekdeg"),
        ],
        [ 
            InlineKeyboardButton("Cancel", callback_data='done')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message != None:
        await update.message.reply_text("Please select the section to set up", reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text("Please select the section to set up", reply_markup=reply_markup)


async def saveUser(update, context):
    user = update.message.from_user

    user_info = {
        'username': user.username,
        'name': user.first_name,
        'chat_id': update.effective_chat.id,
        'sch_id': 'undecided',
        'curr_edu_id': 'unknown',
        'seek_deg_id': 'unknown'
    } 

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[user.id] = user_info

    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)

    reply_keyboard = [["Undecided", "NUS", "NTU"], 
                      ["SMU", "SUTD", "SIT"],
                      ["SUSS", "Others"]]

    await update.message.reply_text(
        "Which school are you applying for?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="School?"
        )
    )

    return SCH

async def saveSchool(update, context):
    user = update.message.from_user if update.message != None else update.callback_query.from_user

    sch = update.message.text if update.message != None else update.callback_query.data
    sch_id = ''

    if (sch == "undecided"):
        sch_id = ""
    elif (sch == "NUS"):
        sch_id = "NUS"
    elif (sch == "NTU"):
        sch_id = "NTU"
    elif (sch == "SMU"):
        sch_id = "SMU"
    elif (sch == "SUTD"):
        sch_id = "SUTD"
    elif (sch == "SIT"):
        sch_id = "SIT"
    elif (sch == "SUSS"):
        sch_id = "SUSS"
    # elif (sch == "Others"):
    #     sch_id = "others"
    else:
        return # not any of the choices

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[str(user.id)]['sch'] = sch_id

    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)


    if update.message != None:
        await update.message.reply_text(
            "School saved as " + sch + ".",
            reply_markup=ReplyKeyboardRemove())
    else:
        keyboard = [
            [ 
                InlineKeyboardButton("Back", callback_data='back'),
                InlineKeyboardButton("Done", callback_data='done')
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(
            "School saved as " + sch + ".",
            reply_markup=reply_markup
    )

    return SCH

async def done(update, context):
    await update.callback_query.message.edit_text("Stop setting up.", reply_markup=None)

    return DONE

async def cancel(update, context):
    user = update.message.from_user
    await update.message.reply_text(
        "Ok, we'll stop saving your settings", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


bot = ApplicationBuilder().token(BOT_TOKEN).build()

# a bit buggy now
settings_handler = ConversationHandler(
        entry_points=[CommandHandler("settings", saveUser)],
        states={
            SCH: [MessageHandler(filters.Regex("""^(Undecided|
                                                      NUS|
                                                      NTU|
                                                      SMU|
                                                      SUTD|
                                                      SIT|
                                                      SUSS|
                                                      Others)$"""), saveSchool)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

# callback handlers
bot.add_handler(CallbackQueryHandler(chooseSchool, pattern='^sch'))
bot.add_handler(CallbackQueryHandler(selectSection, pattern='^back'))
bot.add_handler(CallbackQueryHandler(done, pattern='^done$'))

# this callback encompasses all (no search for pattern)
# put behind every other for now
bot.add_handler(CallbackQueryHandler(saveSchool)) 

bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("register", selectSection))
bot.add_handler(settings_handler)
bot.run_polling()

