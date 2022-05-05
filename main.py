from youtube_statistics import YTstats
import json

API_KEYS = 'AIzaSyCNf3zF2ATZGD-xnnK9tZDIinda-R3pasI'
channel_id = 'UCLVcdDuJIkpfyZnZgy5WUbQ'

yt = YTstats(API_KEYS, channel_id)
yt.extract_all()
yt.dump()

with open('cha_con_tech.json', 'w') as f:
            json.dump(yt.dump(), f, indent=4)