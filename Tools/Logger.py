import logging


class Logger:
    __instance = None

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
            self.logger = logging.getLogger("Telegram Bot Logger")


if __name__ == "__main__":
    s = Logger()
    print(s)

    a = Logger.get_instance()
    print(a)

    b = Logger.get_instance()
    print(b)

    a.logger.info("info_a")
    b.logger.info("info_b")
    s.logger.info("info_x")

