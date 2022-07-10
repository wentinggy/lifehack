from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters
import requests
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


SCH, DONE, AGE, GENDER, CITIZENSHIP = range(5)


async def hello(update, context):
    await update.message.reply_text(f"Hello {update.effective_user.first_name}! Let's discover scholarships that you never knew existed! Type /settings to get started followed by /register to start your profiling!")


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

async def chooseAge(update, context):
    keyboard = [
        [
            InlineKeyboardButton("18", callback_data="18"),
            InlineKeyboardButton("19", callback_data="19"),
            InlineKeyboardButton("20", callback_data="20")
        ],
        [
            InlineKeyboardButton("21", callback_data="21"),
            InlineKeyboardButton("22", callback_data="22"),
            InlineKeyboardButton("23", callback_data="23")
        ],
                [
            InlineKeyboardButton("24", callback_data="24"),
            InlineKeyboardButton("25", callback_data="25"),
            InlineKeyboardButton("26", callback_data="26")
        ],
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Done", callback_data='done'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("How old are you?", reply_markup=reply_markup)

async def chooseGender(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Male", callback_data="Male"),
            InlineKeyboardButton("Female", callback_data="Female"),
            InlineKeyboardButton("Others", callback_data="Others")
        ],
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Done", callback_data='done'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("What is your gender?", reply_markup=reply_markup)

async def chooseCitizenship(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Singaporean", callback_data="Singaporean"),
            InlineKeyboardButton("PR", callback_data="PR"),

        ],
       [

            InlineKeyboardButton("International Student", callback_data="International Student")
        ],
        [ 
            InlineKeyboardButton("Back", callback_data='back'),
            InlineKeyboardButton("Done", callback_data='done'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("What is your citizenship?", reply_markup=reply_markup)




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

            InlineKeyboardButton("Personal Information", callback_data="pinfo"),
            InlineKeyboardButton("Age", callback_data="age"),
            
        ],
        [
            InlineKeyboardButton("Gender", callback_data="gender"),
            InlineKeyboardButton("Citizenship", callback_data="citizenship"),
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
        'age_id': 'unknown',
        'gender_id': 'unknown',
        'citizenship_id': 'unknown',
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


async def saveAge(update, context):
    user = update.message.from_user if update.message != None else update.callback_query.from_user

    age = update.message.text if update.message != None else update.callback_query.data
    age_id = ''

    if (age == "unknown"):
        age_id = ""
    elif (age == "18"):
        age_id = "18"
    elif (age == "19"):
        age_id = "19"
    elif (age == "20"):
        age_id = "21"
    elif (age == "22"):
        age_id = "23"
    elif (age == "24"):
        age_id = "24"
    elif (age == "25"):
        age_id = "25"
    elif (age == "26"):
        age_id = "26"

    else:
        return # not any of the choices

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[str(user.id)]['age'] = age_id

    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)


    if update.message != None:
        await update.message.reply_text(
            "Age saved as " + age + ".",
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
            "Age saved as " + age + ".",
            reply_markup=reply_markup
    )

    return AGE

async def saveGender(update, context):
    user = update.message.from_user if update.message != None else update.callback_query.from_user

    gender = update.message.text if update.message != None else update.callback_query.data
    gender_id = ''

    if (gender == "unknown"):
        gender_id = ""
    elif (gender == "Male"):
        gender_id = "Male"
    elif (gender == "Female"):
        gender_id = "Female"
    elif (gender == "Others"):
        gender_id = "Others"

    else:
        return # not any of the choices

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)

    users[str(user.id)]['gender'] = gender_id


    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)

    if update.message != None:
        await update.message.reply_text(
            "Gender saved as " + gender + ".",
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
            "Gender saved as " + gender + ".",
            reply_markup=reply_markup
    )
    return GENDER

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

    

async def saveCitizen(update, context):
    user = update.message.from_user if update.message != None else update.callback_query.from_user

    citizenship = update.message.text if update.message != None else update.callback_query.data
    citizenship_id = ''

    if (citizenship == "unknown"):
        citizenship_id = ""
    elif (citizenship == "Singaporean"):
        citizenship_id = "Singaporean"
    elif (citizenship == "PR"):
        citizenship_id = "PR"
    elif (citizenship == "International Student"):
        citizenship_id = "International Student"

    else:
        return # not any of the choices

    with open('users.json', 'r') as user_db:
        users = json.load(user_db)
    users[str(user.id)]['citizenship'] = citizenship_id
    with open('users.json', 'w') as user_db:
        json.dump(users, user_db)
    if update.message != None:
        await update.message.reply_text(
            "Citizenship saved as " + citizenship + ".",
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
            "Citizenship saved as " + citizenship + ".",
            reply_markup=reply_markup
    )

    return CITIZENSHIP


async def fetch(update, context):
    user = update.message.from_user
    sch = users[str(user.id)]['sch']
    if_ft = users[str(user.id)]['ft']
    if_SG = users[str(user.id)]['citizenship']
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

    #based on citizenship
    if (if_SG == "International Student"):
        sch_web = "https://oyaop.com/opportunity/scholarships-and-fellowships/schwarzman-scholarships-for-international-students-fully-funded-apply-now/"


    

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

bot.add_handler(CallbackQueryHandler(chooseAge, pattern='^age$'))
bot.add_handler(CallbackQueryHandler(chooseGender, pattern='^gender$'))
bot.add_handler(CallbackQueryHandler(chooseCitizenship, pattern='^citizenship$'))
bot.add_handler(CallbackQueryHandler(chooseCommitment, pattern='^ft$'))
bot.add_handler(CallbackQueryHandler(saveCommitment, pattern='^ft-*'))
bot.add_handler(CallbackQueryHandler(chooseSeekingDegree, pattern='^seekdeg$'))

bot.add_handler(CallbackQueryHandler(saveSchool, pattern='^(?i)(nus|ntu|smu|sutd|sit|suss)'))
bot.add_handler(CallbackQueryHandler(saveSeekDeg, pattern='^(?i)(bc|bchons|mast|phd)'))
bot.add_handler(CallbackQueryHandler(saveAge)) 
bot.add_handler(CallbackQueryHandler(saveGender)) 
bot.add_handler(CallbackQueryHandler(saveCitizen)) 

bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("register", selectSection))
bot.add_handler(CommandHandler("fetch", fetch))
bot.add_handler(CommandHandler("show", showProfile))
bot.add_handler(settings_handler)
bot.run_polling()


