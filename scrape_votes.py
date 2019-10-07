from collections import defaultdict
import json
import time
import random
from tqdm import tqdm
import pandas as pd

from gazpacho import get

def get_vote(number):
    url = 'http://api.openparliament.ca/votes/ballots/'
    params = {'vote': f'/42-1/{number}', 'limit': 500}
    content = get(url, params)
    data = json.loads(content)['objects']
    return data

def parse_single_vote(vote):
    mp = vote['politician_url'].split('/')[-2]
    ballot = vote['ballot']
    return mp, ballot

def parse_votes(vote):
    votes = get_vote(vote)
    votes = [parse_single_vote(v) for v in votes]
    votes = {mp: b for mp, b in votes}
    return votes

all_votes = defaultdict(dict)
for vote in tqdm(range(1, 1379 + 1)):
    all_votes[vote] = parse_votes(vote)
    s = 0.5 + random.randint(-4, 4) / 10
    time.sleep(s)

with open('data/votes.json', 'w') as f:
    json.dump(all_votes, f, ensure_ascii=False, indent=2)
