import logging
import sys


class Logger:

    def __init__(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Config has been setup")
