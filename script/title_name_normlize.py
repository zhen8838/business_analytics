import pandas as pd
df: pd.DataFrame = pd.read_pickle('dev/career_history_df.pkl')

df = df.reset_index(-1)
s: pd.Series = df['title'].str.split('/')
hist = []

jobtitles = []
for v in s.values:
  if isinstance(v,list):
    for m in v:
      jobtitles.append(m)
