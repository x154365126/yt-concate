import os
import time

from pytube import YouTube

from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for yt in data: # url
            print('downloading caption for', yt.id) # url
            if utils.caption_file_exists(yt):
                print('found existing cation file')
                continue

            try:
                source = YouTube(yt.url)
                en_caption = source.captions.get_by_language_code('a.en')
                en_caption_convert_to_srt = (en_caption.generate_srt_captions())
                # print(en_caption_convert_to_srt)

            except (KeyError, AttributeError):
                print('Error when downloading caption for', yt.url)
                continue

            # save the caption to a file named Output.txt
            text_file = open(utils.caption_filepath(url), "w", encoding='utf-8')
            text_file.write(en_caption_convert_to_srt)
            text_file.close()

        end = time.time()
        print('took', end - start, 'seconds')

        return data