from youtube_statistics import YTstats
import json

import config

API_KEYS = config.API_KEYS

channel_id = 'UCLVcdDuJIkpfyZnZgy5WUbQ'

yt = YTstats(API_KEYS, channel_id)
yt.extract_all()
yt.dump()

with open('cha_con_tech.json', 'w') as f:
            json.dump(yt.dump(), f, indent=4)