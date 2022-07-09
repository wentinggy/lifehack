from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters
import requests
import os
from dotenv import load_dotenv
import json
import re

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
            InlineKeyboardButton("Cancel", callback_data='done'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # await context.bot.send_message("Please choose a univerSITy:", reply_markup=reply_markup)
    await update.callback_query.message.edit_text("Please choose a university:", reply_markup=reply_markup)

async def chooseCommitment(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Full-time", callback_data="ft-T"),
            InlineKeyboardButton("Part-time", callback_data="ft-F")
        ],
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Cancel", callback_data='done'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # await context.bot.send_message("Please choose a univerSITy:", reply_markup=reply_markup)
    await update.callback_query.message.edit_text("Select accordingly:", reply_markup=reply_markup)

async def chooseSeekingDegree(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Bachelors", callback_data="bc"),
            InlineKeyboardButton("Bachelors with Honours", callback_data="bchons")
        ],
        [
            InlineKeyboardButton("Masters", callback_data="mast"),
            InlineKeyboardButton("PhD", callback_data="phd")
        ],
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Cancel", callback_data='done')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # await context.bot.send_message("Please choose a univerSITy:", reply_markup=reply_markup)
    await update.callback_query.message.edit_text("Please choose the degree you are pursuing:", reply_markup=reply_markup)

async def selectSection(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Personal Information", callback_data="pinfo")
        ],
        [
            InlineKeyboardButton("School", callback_data="sch"),
            InlineKeyboardButton("Commitment", callback_data="ft")
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
        'sch': 'undecided',
        'curr_edu_id': 'unknown',
        'seek_deg_id': 'unknown',
        'ft': 'T'
    } 

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[user.id] = user_info

    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)


async def saveSchool(update, context):
    user = update.callback_query.from_user

    sch = update.callback_query.data
    sch_id = ''

    if (sch == "Undecided"):
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

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[str(user.id)]['sch'] = sch_id

    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)

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


async def saveCommitment(update, context):
    user = update.callback_query.from_user

    is_ft_string = update.callback_query.data
    is_ft = re.sub('^ft-', '', is_ft_string)

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[str(user.id)]['ft'] = is_ft

    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)

    keyboard = [
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Done", callback_data='done')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(
        "Full time: " + is_ft + ".",
        reply_markup=reply_markup
    )
    return


async def saveSeekDeg(update, context):
    user = update.callback_query.from_user

    seek_deg = update.callback_query.data
    seek_deg_id = ''

    if (seek_deg == 'bc'):
        seek_deg_id = "Bachelors"
    elif (seek_deg == "bchons"):
        seek_deg_id = "Bachelors with Honours"
    elif (seek_deg == "masts"):
        seek_deg_id = "Masters"
    elif (seek_deg == "phd"):
        seek_deg_id = "PhD"

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[str(user.id)]['seek_deg_id'] = seek_deg_id

    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)

    keyboard = [
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Done", callback_data='done')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(
        "Seeking degree: " + seek_deg_id + ".",
        reply_markup=reply_markup
    )
    return


async def fetch(update, context):
    user = update.message.from_user

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    sch = users[str(user.id)]['sch']
    if_ft = users[str(user.id)]['ft']
    sch_web = ''

    if (sch == "undecided"):
        sch_web = "No school indicated"
    elif (sch == "NUS"):
        sch_web = "https://www.nus.edu.sg/oam/scholarships"
    elif (sch == "NTU"):
        sch_web = "https://www.ntu.edu.sg/admissions/undergraduate/scholarships"
    elif (sch == "SMU"):
        sch_web = "https://admissions.smu.edu.sg/scholarships"
    elif (sch == "SUTD"):
        sch_web = "https://www.sutd.edu.sg/Admissions/Undergraduate/Scholarship/Application-for-scholarships"
    elif (sch == "SIT"):
        sch_web = "https://www.singaporetech.edu.sg/admissions/undergraduate/scholarships"
    elif (sch == "SUSS"):
        if if_ft == 'T':
            sch_web = "https://www.suss.edu.sg/full-time-undergraduate/admissions/suss-scholarships-awards"
        else:
            sch_web = "https://www.suss.edu.sg/part-time-undergraduate/admissions/scholarships"
    # elif (sch == "Others"):
    #     sch_web = "others"
    else:
        return # not any of the choices

    await update.message.reply_text("Scholarships can be found at " + sch_web)


async def showProfile(update, context):
    user = update.message.from_user

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    msg = ''
    profile = users[str(user.id)]
    for info in profile:
        if info == "chat_id":
            continue
        msg += info + ": " + str(profile[info]) + "\n"
    
    await update.message.reply_text(msg)


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
bot.add_handler(CallbackQueryHandler(chooseCommitment, pattern='^ft$'))
bot.add_handler(CallbackQueryHandler(saveCommitment, pattern='^ft-*'))
bot.add_handler(CallbackQueryHandler(chooseSeekingDegree, pattern='^seekdeg$'))

bot.add_handler(CallbackQueryHandler(saveSchool, pattern='^(?i)(nus|ntu|smu|sutd|sit|suss)'))
bot.add_handler(CallbackQueryHandler(saveSeekDeg, pattern='^(?i)(bc|bchons|mast|phd)'))

bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("register", selectSection))
bot.add_handler(CommandHandler("fetch", fetch))
bot.add_handler(CommandHandler("show", showProfile))
bot.add_handler(settings_handler)
bot.run_polling()

