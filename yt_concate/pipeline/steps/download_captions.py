import os
import time

from pytube import YouTube

from .log import config_logger
from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logging = config_logger()
        start = time.time()
        for yt in data: # url
            logging.info('downloading caption for {}'.format(yt.id))
            # print('downloading caption for', yt.id) # url
            if utils.caption_file_exists(yt):
                logging.info('found existing cation file')
                # print('found existing cation file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
                # print(en_caption_convert_to_srt)

            except (KeyError, AttributeError):
                logging.warning('Error when downloading caption for {}'.format(yt.url))
                # print('Error when downloading caption for', yt.url)
                continue

            # save the caption to a file named Output.txt
            text_file = open(yt.caption_filepath, "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

        end = time.time()
        # logging.debug('took {}-{}'.format(end, start))
        logging.debug(f'took{end - start}s')
        # print('took', end - start, 'seconds')

        return data
