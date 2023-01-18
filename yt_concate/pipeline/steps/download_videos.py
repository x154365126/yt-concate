import time
from .step import Step

import pytube

from pytube import YouTube
from yt_concate.settings import VIDEOS_DIR
from .log import config_logger
from multiprocessing import Process
from threading import Thread



class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logging = config_logger()
        start = time.time()

        Threads = []

        for i in range(4):
            Threads.append(Thread(target=self.downloadvideos(data, utils)))

        for thread in Threads:
            thread.start()

        for thread in Threads:
            thread.join()

        # # print(len(data))
        # yt_set = set([found.yt for found in data])
        # # print(len(yt_set))
        # print('videos to download=', len(yt_set))
        # for yt in yt_set:
        #     # yt = found.yt
        #     url = yt.url
        #
        #     if utils.video_file_exists(yt):
        #         print(f'found existing video file for {url}, skipping')
        #         continue
        #
        #     print('downloading', url)
        #     YouTube(url).streams.get_by_resolution('360p').download(output_path=VIDEOS_DIR, filename=yt.id + '.mp4')

        end = time.time()
        logging.debug(f'總共費時{end - start}')

        return data

    @staticmethod
    def downloadvideos(data, utils):
        logging = config_logger()
        yt_set = set([found.yt for found in data])
        logging.info('videos to download={}'.format(len(yt_set)))

        for yt in yt_set:
            url = yt.url

            if utils.video_file_exists(yt):
                logging.info(f'found existing video file for {url}, skipping')
                continue
            try:
                logging.info('downloading', url)
                YouTube(url).streams.first().download(output_path=VIDEOS_DIR, filename=yt.id)
            except pytube.exceptions.RegexMatchError:
                logging.warning('downloading error {}'.format(url))
