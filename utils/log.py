import logging


class Log:
    def __init__(self, filename):
        log_format = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s')
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(filename=filename,
                                           mode='a',
                                           encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_format)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        stream_handler.setLevel(logging.INFO)

        # 각각 다른 로거 인스턴스가 생성될 때마다 핸들러가 중복 추가될 우려가 있습니다.
        # https://stackoverflow.com/questions/6729268/python-logging-messages-appearing-twice
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)