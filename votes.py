import json
import pandas as pd
import numpy as np

with open('data/mps.json', 'r') as f:
    mps = json.load(f)

mps = pd.DataFrame(mps)
mps = mps.T.reset_index().rename(columns={'index': 'mp_id'})

with open('data/votes.json', 'r') as f:
    votes = json.load(f)

votes = pd.DataFrame(votes)
votes = votes.T.reset_index().rename(columns={'index': 'vote_id'})
votes = votes.melt(id_vars=['vote_id'], var_name='mp_id', value_name='vote')

df = pd.merge(votes, mps, how='left', on='mp_id')
df.vote_id = df.vote_id.astype('int')
# solve for leona-alleslev
df['party'] = np.where((df['mp_id'] == 'leona-alleslev') & (df['vote_id'] <= 880), 'Liberal', df['party'])

# party votes
pvotes = df[df['vote'].isin(['Yes', 'No'])]
pvotes = pvotes[pvotes['party'].isin(['Liberal', 'Conservative', 'NDP'])]
pvotes = pvotes.groupby(['vote_id', 'party', 'vote'])['mp_id'].count()
pvotes = pvotes / pvotes.groupby(['vote_id', 'party']).sum()
pvotes = pvotes.reset_index().rename(columns={'mp_id': 'party_percent'})
pvotes = pvotes[pvotes['party_percent'] > 0.5].rename(columns={'vote': 'party_line'})
pvotes = pvotes.drop('party_percent', axis=1)

df = pd.merge(df, pvotes, how='left', on=['vote_id', 'party'])

# absent
absent = df.groupby(['mp_id', 'vote'])['riding'].count()
absent = absent / absent.groupby('mp_id').sum()
absent = absent.reset_index().rename(columns={'riding': 'percent'})
absent = absent[absent['vote'] == "Didn't vote"]
absent = absent.dropna()
absent = absent.sort_values('percent', ascending=False)

# vote against party line
break_vote = df[df['vote'] != df['party_line']]
break_vote = break_vote[break_vote['vote'].isin(['Yes', 'No'])]
break_vote = break_vote[break_vote['party'].isin(['Liberal', 'Conservative', 'NDP'])]
break_vote = break_vote.reset_index(drop=True)
break_vote = break_vote.groupby('mp_id')['vote'].count().reset_index()
break_vote.sort_values('vote', ascending=False)

#
