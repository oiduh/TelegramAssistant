from Tools.Logger import Logger
from CommandManager.CommandManager import command, CommandType
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

logger = Logger.get_instance().logger


def beep(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text='BEEP')


def boop(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text='BOOP')


@command(CommandType.COMMAND_HANDLER_JOB)
def beepboop(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text='Setting a timer for 10 seconds!')
    context.job_queue.run_repeating(beep, interval=20, first=1, context=update.message.chat_id)
    context.job_queue.run_repeating(boop, interval=20, first=3, context=update.message.chat_id)


@command(CommandType.COMMAND_HANDLER_JOB)
def stop(update: Update, context: CallbackContext):
    jobs = [x for x in context.job_queue.jobs()]
    logger.info("cancelling the following jobs")
    for job in jobs:
        if job.name in ["beep", "boop"]:
            logger.info(f"cancel: {job.name}")
            job.schedule_removal()
    context.bot.send_message(chat_id=update.message.chat_id, text="beep boop jobs cancelled")
