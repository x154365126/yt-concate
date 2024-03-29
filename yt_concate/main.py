import getopt
import sys

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.postflight import Postflight

from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'


def usarg():
    print("python3 main.py -c <channel_id> -s <search_word> -l <limit>")
    print("python3 main.py --channel_id <channel_id> --search_word <search_word> --limit <limit>"
          "--cleanup <cleanup>")

    print('python3 main.py OPTIONS')
    print("OPTIONS:")
    print("{:>6} {:<20}{}".format('-c', '--channel_id', "Channel id of the Youtube Channel_id"))
    print("{:>6} {:<20}{}".format('-s', '--search_word', "search_word of the captions"))
    print("{:>6} {:<20}{}".format('-l', '--limit', "Number of clips"))
    print("{:>6} {:<20}{}".format('--cleanup', "True or False to delete the videos and captions"))

def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'incredible',
        'limit': 20,
        'cleanup':False
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:s:l:", ["channel_id=", "search_word=", "limit=", "cleanup"])
    except getopt.GetoptError:
        usarg()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usarg()
            sys.exit(0)
        elif opt in ("-c", "--channel_id"):
            inputs['channel_id'] = arg
        elif opt in ("-s", "--search_word"):
            inputs['search_word'] = arg
        elif opt in ("-l", "limit"):
            inputs["limit"] = arg
        elif opt in "cleanup":
            inputs['cleanup'] = arg

    if not inputs['channel_id'] or not inputs['search_word']:
        usarg()
        sys.exit(2)

    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
