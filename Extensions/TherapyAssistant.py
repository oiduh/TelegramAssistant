from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from datetime import datetime, timedelta
import pytz
from Tools.Logger import Logger
from Tools.MedicationTools import Medicine, Therapy
from Tools.CustomCallback import custom_medication_message
from CommandManager.CommandManager import CommandType, command


logger = Logger.get_instance().logger

# default medication list -> TODO: make it customizable later if necessary
THERAPY = Therapy()
THERAPY.medication_list += [
    Medicine(name="Aprednislon 25mg", type="pill(s)",
             breakfast=3, lunch=0, dinner=0,
             start=datetime(2021, 9, 21, 0, 0, 0),
             end=  datetime(2021, 9, 27, 23, 59, 59)),
    Medicine(name="Aprednislon 25mg", type="pill(s)",
             breakfast=2.5, lunch=0, dinner=0,
             start=datetime(2021, 9, 28, 0, 0, 0),
             end=  datetime(2021, 10, 4, 23, 59, 59)),
    Medicine(name="Aprednislon 25mg", type="pill(s)",
             breakfast=2, lunch=0, dinner=0,
             start=datetime(2021, 10, 5, 0, 0, 0),
             end=  datetime(2021, 10, 11, 23, 59, 59)),
    Medicine(name="Aprednislon 25mg", type="pill(s)",
             breakfast=1.5, lunch=0, dinner=0,
             start=datetime(2021, 10, 12, 0, 0, 0),
             end=  datetime(2021, 10, 18, 23, 59, 59)),
    Medicine(name="Aprednislon 25mg", type="pill(s)",
             breakfast=1, lunch=0, dinner=0,
             start=datetime(2021, 10, 19, 0, 0, 0),
             end=  datetime(2021, 10, 25, 23, 59, 59)),
    Medicine(name="Aprednislon 5mg", type="pill(s)",
             breakfast=4, lunch=0, dinner=0,
             start=datetime(2021, 10, 26, 0, 0, 0),
             end=  datetime(2021, 11, 1, 23, 59, 59)),
    Medicine(name="Aprednislon 5mg", type="pill(s)",
             breakfast=3, lunch=0, dinner=0,
             start=datetime(2021, 11, 2, 0, 0, 0),
             end=  datetime(2021, 11, 8, 23, 59, 59)),
    Medicine(name="Aprednislon 5mg", type="pill(s)",
             breakfast=2, lunch=0, dinner=0,
             start=datetime(2021, 11, 9, 0, 0, 0),
             end=  datetime(2021, 11, 15, 23, 59, 59)),
    Medicine(name="Aprednislon 5mg", type="pill(s)",
             breakfast=1, lunch=0, dinner=0,
             start=datetime(2021, 10, 16, 0, 0, 0),
             end=  datetime(2021, 11, 22, 23, 59, 59)),
    Medicine(name="Pantoloc 40mg", type="pill(s)",
             breakfast=1, lunch=0, dinner=0,
             start=datetime(2021, 9, 21, 0, 0, 0),
             end=  datetime(2021, 11, 22, 23, 59, 59),
             delay=-1),
    Medicine(name="Pentasa 1g", type="pack",
             breakfast=1, lunch=0, dinner=1,
             start=datetime(2021, 9, 21, 0, 0, 0),
             end=  datetime(2021, 11, 22, 23, 59, 59))
]


TIME_ZONE = pytz.timezone('Europe/Vienna')
MEDICATION_LIST = THERAPY.medication_list

# default hours for meals -> change with commands if necessary
BREAKFAST_HOUR = 8
LUNCH_HOUR = 12
DINNER_HOUR = 17


@command(CommandType.COMMAND_HANDLER)
def set(update: Update, context: CallbackContext) -> None:
    def valid_usage(args):
        return len(args) == 2 and args[0].lower() in ["breakfast", "lunch", "dinner"] and args[1].isnumeric()

    args = update.message.text.split(" ")[1:]
    if not valid_usage(args):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Error: wrong command usage\n"
                                      "       correct usage examples:\n"
                                      "           /set breakfast 8\n"
                                      "           /set lunch 3\n"
                                      "           /set dinner 18"
                                 )
        return

    global BREAKFAST_HOUR, LUNCH_HOUR, DINNER_HOUR
    meal, hour = args[0].lower(), int(args[1])
    if meal == "breakfast":
        BREAKFAST_HOUR = hour
    elif meal == "lunch":
        LUNCH_HOUR = hour
    else:
        DINNER_HOUR = hour
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"Setting {meal} hour to {hour} successful")


@command(CommandType.COMMAND_HANDLER)
def get(update: Update, context: CallbackContext) -> None:
    args = update.message.text.split(" ")[1:]
    if not len(args) == 1 or not args[0].lower() in ["all", "breakfast", "lunch", "dinner"]:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Error: wrong command usage\n"
                                      "       correct usage examples:\n"
                                      "           /get all\n"
                                      "           /get breakfast\n"
                                      "           /get lunch\n"
                                      "           /get dinner"
                                 )
        return
    meal = args[0]
    responses = [
        f"breakfast hour:  {BREAKFAST_HOUR}",
        f"lunch hour:      {LUNCH_HOUR}",
        f"dinner hour:     {DINNER_HOUR}"
    ]
    if meal == "breakfast":
        response = responses[0]
    elif meal == "lunch":
        response = responses[1]
    elif meal == "dinner":
        response = responses[2]
    else:
        response = "\n".join(responses)
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


def sendMessage(context: CallbackContext, medicine: Medicine) -> None:
    context.bot.send_message(chat_id=context.job.context,
                             text=f"\n-----------------{medicine.name}-----------------------\n"
                                  f"    from:   {medicine.start}\n"
                                  f"    to:     {medicine.end}\n"
                                  f"    amount: {medicine.breakfast}"
                             )


def sendMessageTest(context: CallbackContext) -> None:
    context.bot.send_message(chat_id=context.job.context, text="test")


def startMedicationReminder(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text="startMedicationReminder")
    for it, medicine in enumerate(MEDICATION_LIST):
        start_time = TIME_ZONE.localize(medicine.start)
        end_time = TIME_ZONE.localize(medicine.end)
        amounts = [medicine.breakfast, medicine.lunch, medicine.dinner]
        hours = [BREAKFAST_HOUR, LUNCH_HOUR, DINNER_HOUR]
        for amount, hour in zip(amounts, hours):
            if amount == 0:
                continue
            custom_callback = custom_medication_message(sendMessage, medicine=medicine)
            job = context.job_queue.run_repeating(
                callback=custom_callback,
                interval=timedelta(hours=24),
                first=start_time+timedelta(hours=hour+medicine.delay),
                last=end_time,
                context=update.message.chat_id
            )

            # TODO: rework this response for debugging
            response = f"\n---------------{medicine.name}------------\n"
            response += f"    from:      {medicine.start}\n"
            response += f"    to:        {medicine.end}\n"
            if hour == BREAKFAST_HOUR:
                response += f"    breakfast: {medicine.breakfast}\n"
            elif hour == LUNCH_HOUR:
                response += f"    lunch:     {medicine.lunch}\n"
            else:
                response += f"    dinner:    {medicine.dinner}\n"
            response += f"    next:      {job.next_t}"

            logger.info(response)


@command(CommandType.COMMAND_HANDLER_JOB)
def therapyStart(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.message.chat_id, text='Starting your Medication reminder')
    startMedicationReminder(update=update, context=context)


@command(CommandType.COMMAND_HANDLER)
def getJobs(update: Update, context: CallbackContext) -> None:
    job = context.job_queue.jobs()[0]
    med = job.callback.keywords['medicine']
    response =  f"\n    {med.name}\n"
    response += f"    {job.job.next_run_time}"
    logger.info(response)


@command(CommandType.COMMAND_HANDLER)
def therapyRestart(update: Update, context: CallbackContext) -> None:
    job_list = context.job_queue.jobs()
    for job in job_list:
        job.job.remove()
    logger.info("all jobs cancelled, now restarting with new hours")
    therapyStart(update=update, context=context)
    logger.info("jobs restarted")
