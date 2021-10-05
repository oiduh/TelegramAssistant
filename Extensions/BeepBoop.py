from Tools.Logger import Logger
from Extensions.BaseExtension import BaseExtension
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

logger = Logger.get_instance().logger


class BeepBoop(BaseExtension):

    def __init__(self, bot):
        BaseExtension.__init__(self, bot)

    @staticmethod
    def n_beep(context: CallbackContext):
        context.bot.send_message(chat_id=context.job.context, text='BEEP')

    @staticmethod
    def n_boop(context: CallbackContext):
        context.bot.send_message(chat_id=context.job.context, text='BOOP')

    @staticmethod
    def chj_beepboop(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id, text='Setting a timer for 10 seconds!')
        context.job_queue.run_repeating(BeepBoop.n_beep, interval=20, first=1, context=update.message.chat_id)
        context.job_queue.run_repeating(BeepBoop.n_boop, interval=20, first=3, context=update.message.chat_id)

    @staticmethod
    def chj_stop(update: Update, context: CallbackContext):
        jobs = [x for x in context.job_queue.jobs()]
        logger.info("cancelling the following jobs")
        for job in jobs:
            if job.name in ["n_beep", "n_boop"]:
                logger.info(f"cancel: {job.name}")
                job.schedule_removal()
        context.bot.send_message(chat_id=update.message.chat_id, text="beep boop jobs cancelled")
