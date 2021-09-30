from logger import _Logger
from Extensions.BaseExtension import BaseExtension
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from Tools.MedicationTools import Medicine, Therapy
from datetime import datetime, timedelta
import pytz
from Tools.CustomCallback import custom_medication_message


logger = _Logger.get_instance().logger

# default medication list -> TODO: make it customizable later if necessary
therapy = Therapy()
therapy.medication_list += [
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


class TherapyAssistant(BaseExtension):

    time_zone = pytz.timezone('Europe/Vienna')
    medication_list = therapy.medication_list

    # default hours for meals -> change with commands if necessary
    breakfast_hour = 8
    lunch_hour = 12
    dinner_hour = 17

    def __init__(self, bot):
        BaseExtension.__init__(self, bot)

    @staticmethod
    def ch_set(update: Update, context: CallbackContext):
        def valid_usage(args):
            return len(args) == 2 and args[0].lower() in ["breakfast", "lunch", "dinner"] and args[1].isnumeric()

        args = update.message.text.split(" ")[1:]
        if valid_usage(args):
            meal, hour = args[0].lower(), int(args[1])
            if meal == "breakfast":
                TherapyAssistant.breakfast_hour = hour
            elif meal == "lunch":
                TherapyAssistant.lunch_hour = hour
            else:
                TherapyAssistant.dinner_hour = hour
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"Setting {meal} hour to {hour} successful")
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Error: wrong command usage\n"
                                          "       correct usage examples:\n"
                                          "           /set breakfast 8\n"
                                          "           /set lunch 3\n"
                                          "           /set dinner 18"
                                     )

    @staticmethod
    def ch_get(update: Update, context: CallbackContext):
        args = update.message.text.split(" ")[1:]
        if len(args) == 1 and args[0].lower() in ["all", "breakfast", "lunch", "dinner"]:
            meal = args[0]
            responses = [
                f"breakfast hour:  {TherapyAssistant.breakfast_hour}",
                f"lunch hour:      {TherapyAssistant.lunch_hour}",
                f"dinner hour:     {TherapyAssistant.dinner_hour}"
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
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Error: wrong command usage\n"
                                          "       correct usage examples:\n"
                                          "           /get all\n"
                                          "           /get breakfast\n"
                                          "           /get lunch\n"
                                          "           /get dinner")

    @staticmethod
    def n_sendMessage(context: CallbackContext, medicine: Medicine):
        context.bot.send_message(chat_id=context.job.context,
                                 text=f"\n-----------------{medicine.name}-----------------------\n"
                                      f"    from:   {medicine.start}\n"
                                      f"    to:     {medicine.end}\n"
                                      f"    amount: {medicine.breakfast}"
                                 )

    @staticmethod
    def n_sendMessageTest(context: CallbackContext):
        context.bot.send_message(chat_id=context.job.context, text="test")

    @staticmethod
    def n_startMedicationReminder(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id, text="startMedicationReminder")
        for it, medicine in enumerate(TherapyAssistant.medication_list):
            start_time = TherapyAssistant.time_zone.localize(medicine.start)
            end_time = TherapyAssistant.time_zone.localize(medicine.end)
            amounts = [medicine.breakfast, medicine.lunch, medicine.dinner]
            hours = [TherapyAssistant.breakfast_hour, TherapyAssistant.lunch_hour, TherapyAssistant.dinner_hour]
            for amount, hour in zip(amounts, hours):
                if amount == 0:
                    continue
                custom_callback = custom_medication_message(TherapyAssistant.n_sendMessage, medicine=medicine)
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
                if hour == TherapyAssistant.breakfast_hour:
                    response += f"    breakfast: {medicine.breakfast}\n"
                elif hour == TherapyAssistant.lunch_hour:
                    response += f"    lunch:     {medicine.lunch}\n"
                else:
                    response += f"    dinner:    {medicine.dinner}\n"
                response += f"    next:      {job.next_t}"

                logger.info(response)

    @staticmethod
    def chj_therapyStart(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id, text='Starting your Medication reminder')
        TherapyAssistant.n_startMedicationReminder(update=update, context=context)

    @staticmethod
    def ch_getJobs(update: Update, context: CallbackContext):
        job = context.job_queue.jobs()[0]
        med = job.callback.keywords['medicine']
        response =  f"\n    {med.name}\n"
        response += f"    {job.job.next_run_time}"
        logger.info(response)

    @staticmethod
    def ch_therapyRestart(update: Update, context: CallbackContext):
        job_list = context.job_queue.jobs()
        for job in job_list:
            job.job.remove()
        logger.info("all jobs cancelled, now restarting with new hours")
        TherapyAssistant.chj_therapyStart(update=update, context=context)
        logger.info("jobs restarted")




if __name__ == "__main__":
    t = TherapyAssistant(None)
    print(t.medication_list)