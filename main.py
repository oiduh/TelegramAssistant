from dotenv import load_dotenv
import os
from MedBot import MedBot
from Extensions.TutorialMethods import TutorialMethods
from Extensions.BeepBoop import BeepBoop
from Extensions.TherapyAssistant import TherapyAssistant

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')


if __name__ == '__main__':
    med_bot = MedBot(bot_token=API_KEY)

    # add more extension to this list as needed
    extension_list = [
        TutorialMethods,
        BeepBoop,
        TherapyAssistant
    ]

    for extension in extension_list:
        med_bot.add_extension(extension)
    med_bot.run()

