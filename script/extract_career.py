import os
import sys
sys.path.insert(0, os.getcwd())
import numpy as np
import pandas as pd
import re
from tools.cleanfucs import process_career_history


if __name__ == "__main__":
  person_info = pd.read_csv('tmp/person_info.csv')
  timepatten = re.compile("\d{1,2}\/\d\/\d{4}|\d{1,2}\/\d{1,4}|PRESENT|FORMER|UNKNOWN")
  career_history: pd.Series = person_info.career_history.apply(
      lambda s: process_career_history(s, timepatten))

  df_values = {'uid': [], 'title': [], 'company': [], 'tenure': []}
  for uid, (titles, companys, tenures) in enumerate(career_history.values):
    for title, company, tenure in zip(titles, companys, tenures):
      df_values['uid'].append(uid + 1)
      df_values['title'].append(title)
      df_values['company'].append(company)
      df_values['tenure'].append(tenure)

  dfcareer = pd.DataFrame(df_values)
  # dfcareer = dfcareer.set_index(['uid', 'title'])
  # dfcareer = dfcareer.reset_index(level=-1, drop=True)
  dfcareer.to_pickle('tmp/career_history_df.pkl')
