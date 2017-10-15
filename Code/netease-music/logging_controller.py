"""
This file for controlling multi-process logging 
"""

from multiprocessing import Process, Pipe
import logging
import logging.config
import cloghandler


class LoggingController(object):
    """
    Wrapper logging instance.
    """

    def __init__(self, type, config_value, logger_name=None):
        self.type = type
        logging.config.dictConfig(config_value)
        self.pipe = Pipe(duplex=False)
        self.logger_name = logger_name
        self.dispose = False
        log_process = Process(target=self.logger_process,
                              args=(self.pipe[0], self.logger_name,))
        log_process.start()

    def logger_process(self, pipe, logger_name):
        logger = logging.getLogger(
            logger_name) if logger_name else logging.getLogger()
        self.print_log(logger, pipe)

    def print_log(self, logger, pipe):
        while True:
            if self.dispose:
                break