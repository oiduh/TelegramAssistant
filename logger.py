import logging


class _Logger:
    __instance = None

    @staticmethod
    def get_instance():
        if _Logger.__instance is None:
            _Logger()
        return _Logger.__instance

    def __init__(self):
        if _Logger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            _Logger.__instance = self
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
            self.logger = logging.getLogger("Telegram Bot Logger")


if __name__ == "__main__":
    s = _Logger()
    print(s)

    a = _Logger.get_instance()
    print(a)

    b = _Logger.get_instance()
    print(b)

    a._logger.info("info_a")
    b._logger.info("info_b")
    s._logger.info("info_x")

