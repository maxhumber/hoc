from collections import defaultdict
import json
import time
import random
from tqdm import tqdm
import pandas as pd

from gazpacho import get

url = 'http://api.openparliament.ca/politicians/'
params = {'limit': 500}
content = get(url, params)
data = json.loads(content)['objects']

mps = {}
for mp in data:
    key = mp['url'].split('/')[2]
    value = {
        'province': mp['current_riding']['province'],
        'riding': mp['current_riding']['name']['en'],
        'party': mp['current_party']['short_name']['en']
    }
    mps[key] = value

with open('data/mps.json', 'w') as f:
    json.dump(mps, f, ensure_ascii=False, indent=2)
