from Tools.Logger import Logger
from CommandManager.CommandManager import command, CommandType
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.callbackcontext import CallbackContext

logger = Logger.get_instance().logger


########################
#                      #
#  Tutorial functions  #
#                      #
########################
@command(CommandType.COMMAND_HANDLER)
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    logger.info("start function")
    # METHOD 1
    update.message.reply_text('Hi!')
    # METHOD 2
    message = 'Welcome to the bot'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


@command(CommandType.COMMAND_HANDLER)
def helper(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    logger.info("help function")
    update.message.reply_text('Help!')


#@command(CommandType.MESSAGE_HANDLER)
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    logger.info("echo function")
    update.message.reply_text(update.message.text)


@command(CommandType.COMMAND_HANDLER)
def button(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    #update.message.reply_text('Please choose:', reply_markup=reply_markup)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="choose button",
                             reply_markup=reply_markup)


@command(CommandType.CALLBACK_QUERY_HANDLER)
def btn(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")
