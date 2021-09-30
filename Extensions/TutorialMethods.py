from logger import _Logger
from Extensions.BaseExtension import BaseExtension
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

logger = _Logger.get_instance().logger

########################
#                      #
#  Tutorial functions  #
#                      #
########################


class TutorialMethods(BaseExtension):

    def __init__(self, bot):
        BaseExtension.__init__(self, bot)

    @staticmethod
    def ch_start(update: Update, context: CallbackContext):
        """Send a message when the command /start is issued."""
        logger.info("start function")
        # METHOD 1
        update.message.reply_text('Hi!')
        # METHOD 2
        message = 'Welcome to the bot'
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    @staticmethod
    def ch_help(update: Update, context: CallbackContext):
        """Send a message when the command /help is issued."""
        logger.info("help function")
        update.message.reply_text('Help!')


    # TODO: remove this later -> problem: replies with command of other classes
    @staticmethod
    # default mh method
    def n_echo(update: Update, context: CallbackContext):
        """Echo the user message."""
        logger.info("echo function")
        update.message.reply_text(update.message.text)
