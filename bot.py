import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
loggers = logger.setLevel(logging.INFO)

print(logger)
print(loggers)

loggert = logger.setLevel(logging.DEBUG)
print(loggert)

#TOKEN = ""

import telegram
bot = telegram.Bot(token= str(TOKEN))
print(bot.get_me())

from telegram.ext import Updater
updater = Updater(token= str(TOKEN))
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me! or /help /me")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def me(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="me ooonnggg")

from telegram.ext import CommandHandler
me_handler = CommandHandler('me', me)
dispatcher.add_handler(me_handler)

def echo(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)
caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram import InlineQueryResultArticle, ParseMode,InputTextMessageContent
def inline_caps(bot, update):
    query = update.inline_query.query
    #if not query:
        #return
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper()),
            description="Upper_case"),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN),            
            #reply_markup={"inline_keyboard":[[{"text":"Click","url":"https://www.google.com"}]]},
            description="Bold_case"),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN),
            #reply_markup={"inline_keyboard":[[{"text":"Click","url":"https://www.google.com"}]]},
            description="Italic_case")]
    '''
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper()),
            reply_markup={"inline_keyboard":[[{"text":"Click","url":"https://www.google.com"}]]},
            url="https://www.google.com",
            hide_url=True,
            description="Test description",
            thumb_url="https://pbs.twimg.com/profile_images/830697812773842944/aADdsDXj_400x400.jpg",
            thumb_width=64,
            thumb_height=64,
        )
    )
    '''
    bot.answer_inline_query(update.inline_query.id, results)
from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)
'''
from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_test(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.lower(),
            title='Test',
            input_message_content=InputTextMessageContent(query.lower()),
            reply_markup={"inline_keyboard":[[{"text":"Click","url":"https://www.google.com"}]]},
            url="https://www.google.com",
            hide_url=True,
            description="Test description",
            thumb_url="https://pbs.twimg.com/profile_images/830697812773842944/aADdsDXj_400x400.jpg",
            thumb_width=64,
            thumb_height=64,
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)
from telegram.ext import InlineQueryHandler
inline_test_handler = InlineQueryHandler(inline_test)
dispatcher.add_handler(inline_test_handler)
'''

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
def inline(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    
from telegram.ext import CommandHandler
inline_handler = CommandHandler('in', inline)
dispatcher.add_handler(inline_handler)



def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

from telegram.ext import Updater, CallbackQueryHandler
updater.dispatcher.add_handler(CallbackQueryHandler(button))

#====set timer====

def alarm(bot, job):
    """Send the alarm message."""
    #bot.send_message(job.context, text='Beep!')
    bot.send_message(job.context, text='⏰ Kriiiiiii...ng!')


def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            #update.message.reply_text('Sorry we can not go back to future!')
            update.message.reply_text('Sorry gk bisa ke masa depan bro!')
            return

        # Add job to queue
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job

        #update.message.reply_text('Timer successfully set!')
        update.message.reply_text('Timer sukses diset!')

    except (IndexError, ValueError):
        #update.message.reply_text('Usage: /set <seconds>')
        update.message.reply_text('Gunakan: /set <Detik>')


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        #update.message.reply_text('You have no active timer')
        update.message.reply_text('kamu belum mengeset timer : /set <Detik>')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    #update.message.reply_text('Timer successfully unset!')
    update.message.reply_text('Set timer sukses dicancel!')

from telegram.ext import CommandHandler
dp = updater.dispatcher
dp.add_handler(CommandHandler("set", set_timer,
                               pass_args=True,
                               pass_job_queue=True,
                               pass_chat_data=True))
dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

#=================
    
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()



'''
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        "remove update.message.chat_id from conversation list"
    except BadRequest:
        "handle malformed requests - read more below!"
    except TimedOut:
        "handle slow connection problems"
    except NetworkError:
        "handle other connection problems"
    except ChatMigrated as e:
        "the chat_id of a group has changed, use e.new_chat_id instead"
    except TelegramError:
        "handle all other telegram related errors"

dispatcher.add_error_handler(error_callback)

bot.leave_chat(chat_id=<invalid chat id>)
telegram.error.BadRequest: Chat not found

bot.answer_callback_query(<invalid query id>)
telegram.error.BadRequest: Query_id_invalid

bot.get_file(<invalid file id>)
telegram.error.BadRequest: Invalid file id

bot.edit_message_text(chat_id, "sample old message")
telegram.error.BadRequest: Message is not modified

bot.send_message(chat_id, 'a'*40960)
telegram.error.BadRequest: Message is too long

r = telegram.constants.MAX_MESSAGE_LENGTH
print(r) 
s = telegram.constants.MAX_CAPTION_LENGTH
print(s)

print("Example code to set up the logging module:")
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
'''
#===========================
'''
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
'''

