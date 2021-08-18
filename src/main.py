import logging
import os
import time
from database import add_entry
from user import User
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

GENDER, NAME, STAR, AGE, OCCUPATION, SCORE = range(6)
users = dict()


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender.
    type /restart to restart"""
    reply_keyboard = [['巴打', '絲打']]
    user = User(update.message.from_user.id)
    users[user.tg_id] = user
    user.info["tg_name"] = update.message.from_user.username
    user.info["tg_id"] = update.message.from_user.id

    update.message.reply_text('你好！歡迎嚟到TG星座分析！首先我需要一啲關於你嘅背景資料，再用深度學習結合呢啲數據'
                              '就可以分析出最準嘅人格！')
    time.sleep(5)
    update.message.reply_text(
        '首先我想知你係巴定絲？',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='巴定絲？'
        ),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a nickname."""
    user = users.get(update.message.from_user.id)
    user.info["gender"] = update.message.text
    logger.info("Gender of %s: %s", user.info["tg_name"], user.info["gender"])

    update.message.reply_text(
        "原來係咁！人改名嘅時候會不經意透露佢嘅人格，所以請輸入你嘅連登名或者花名。",
        reply_markup=ReplyKeyboardRemove()
    )

    return NAME


def name(update: Update, context: CallbackContext) -> int:
    """ask for star."""
    nickname = update.message.text
    user = users.get(update.message.from_user.id)
    user.info["nickname"] = nickname
    logger.info("Name of %s: %s", user.info["tg_name"], nickname)
    reply_keyboard = [['牡羊座', '金牛座', "雙子座"],
                      ["巨蟹座", "獅子座", "處女座"],
                      ["天秤座", "天蠍座", "射手座"],
                      ["魔羯座", "水瓶座", "雙魚座"]]

    update.message.reply_text(
        f"{user.info['nickname']}你咩星座？",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='揀一個星座：'
        ),
    )
    return STAR


def star(update: Update, context: CallbackContext) -> int:
    """ask for age"""
    star_info = update.message.text
    user = users.get(update.message.from_user.id)
    user.info["star"] = star_info
    nickname = user.info["nickname"]
    logger.info("Star of %s: %s", user.info["tg_name"], star_info)
    update.message.reply_text(f"{star_info}嘅你幾歲呢？")
    return AGE


def age(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    age_info = update.message.text
    user = users.get(update.message.from_user.id)
    if not (age_info.isnumeric() and 0 < int(age_info) < 100):
        update.message.reply_text("零分重作")
        logger.info("Asked user %s to retype the age.", user.info["tg_name"])
        return AGE

    user.info["age"] = age_info
    logger.info("Age of %s: %s", user.info["tg_name"], age_info)

    num = int(age_info)
    if num < 20:
        update.message.reply_text("哇你好後生喎！")
    elif num < 40:
        update.message.reply_text("都唔算太老，哈哈！")
    else:
        update.message.reply_text("步入中年喇喎！")

    reply_keyboard = [['小學', '中學', '大專'],
                      ["碩士或以上", "做緊野"]]
    time.sleep(3)
    update.message.reply_text(
        "咁而家有無讀書？由於你嘅人生階段都會影響人格，所以請認真回答！",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='讀緊咩'
        ),
    )

    return OCCUPATION


def occupation(update: Update, context: CallbackContext) -> int:
    occupation_info = update.message.text
    user = users.get(update.message.from_user.id)
    user.info["occupation"] = occupation_info
    logger.info("occupation of %s: %s", user.info["tg_name"], occupation_info)
    if occupation_info != "做緊野":
        update.message.reply_text(f"讀{occupation_info}加油啊！")
    else:
        update.message.reply_text("原來你返緊工。")
    time.sleep(3)

    update.message.reply_text("搞掂！請等十秒左右，我用緊深度學習技術分析你嘅人格！")
    for i in range(3):
        time.sleep(3)
        update.message.reply_text("...")

    time.sleep(2)
    update.message.reply_text(f'{user.info["nickname"]}！作為{user.info["star"]}...')
    time.sleep(4)
    update.message.reply_text(f'覺得以上分析準唔準？請俾0至10分！')

    return SCORE


def score(update: Update, context: CallbackContext) -> int:
    user = users.get(update.message.from_user.id)
    score_info = update.message.text
    if not (score_info.isnumeric() and 0 <= int(score_info) <= 10):
        update.message.reply_text("零分重作")
        logger.info("Asked user %s to retype the score.", user.info["tg_name"])
        return SCORE

    user.info["score"] = score_info
    logger.info("Score of %s: %s", user.info["tg_name"], score_info)
    update.message.reply_text(f'如果覺得準嘅歡迎share俾朋友！再見。')
    logger.info("Info of %s is: %s", user.info["tg_name"], user.info)
    add_entry(user.info)
    logger.info("Info of %s stored in database", user.info["tg_name"])

    users.pop(update.message.from_user.id)

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.

    TOKEN = os.environ["TEL_TOKEN"]
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(Filters.regex('^(巴打|絲打)$'), gender)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            STAR: [MessageHandler(Filters.regex("^(牡羊座|金牛座|雙子座|巨蟹座|獅子座|處女座|天秤座|"
                                                "天蠍座|射手座|魔羯座|水瓶座|雙魚座)$"), star)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            OCCUPATION: [MessageHandler(Filters.regex("^(小學|中學|大專|碩士或以上|做緊野)$"), occupation)],
            SCORE: [MessageHandler(Filters.text & ~Filters.command, score)]
        },
        fallbacks=[CommandHandler('restart', start)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
