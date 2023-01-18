from .log import config_logger
from .step import Step

class Postflight(Step):
    def process(self, data, inputs, utils):
        logging = config_logger()
        logging.info('in Postflight')
        # print('in Postflight')
