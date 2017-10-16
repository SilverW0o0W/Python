"""
This file for controlling multi-process logging 
"""

from multiprocessing import Process, Pipe
import logging
import logging.config
# import cloghandler

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class LoggingController(object):
    """
    Wrapper logging instance.
    """

    def __init__(self, config=None, logger_name=None):
        if config:
            logging.config.dictConfig(config)
        self.pipe = Pipe(duplex=False)
        self.logger_name = logger_name
        log_process = Process(target=self._logger_process,
                              args=(self.pipe[0], self.logger_name,))
        log_process.start()

    def _logger_process(self, pipe, logger_name):
        logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%d %b %Y %H:%M:%S',
                            filemode='a',
                            filename='log.log')
        logger = logging.getLogger(
            logger_name) if logger_name else logging.getLogger()
        while True:
            message = pipe.recv()
            if not message:
                break
            logger.log(message[0], message[1])

    # def _print_log(self, logger, pipe):

    def setLevel(self, level):
        """
        Set the logging level of this logger.
        """
        pass

    def debug(self, msg, *args, **kwargs):
        """
        Debug level
        """
        self.log(DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Info level
        """
        self.log(INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Warning level
        """
        self.log(WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Error level
        """
        self.log(ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        Exception level
        """
        kwargs['exc_info'] = 1
        self.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Critical level
        """
        self.log(CRITICAL, msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """
        Logger level
        """
        msg = msg.format(args, kwargs)
        message = [level, msg]
        self.pipe[1].send(message)


if __name__ == '__main__':
    logger = LoggingController()
    logger.error('test')
    while True:
        pass
