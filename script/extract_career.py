import os
import sys
sys.path.insert(0, os.getcwd())
import numpy as np
import pandas as pd
import re
from tools.cleanfucs import process_career_history, process_tenure


if __name__ == "__main__":
  person_info = pd.read_csv('tmp/person_info.csv')
  timepatten = re.compile("\d{1,2}\/\d\/\d{4}|\d{1,2}\/\d{1,4}|PRESENT|FORMER|UNKNOWN")
  career_history: pd.Series = person_info.career_history.apply(
      lambda s: process_career_history(s, timepatten))

  tenurepattern = re.compile('(\d+\/\d+\/\d{4})|(\d{1,2}\/\d{1,4})|(PRESENT)|(FORMER)|(UNKNOWN)')
  df_values = {'uid': [], 'title': [], 'company': [], 'start_tenure': [], 'end_tenure': []}
  for uid, (titles, companys, tenures) in enumerate(career_history.values):
    for invalidw in ['Publications', 'UNKNOWN FUTURE DATE', 'Awards']:
      if invalidw in tenures:
        e = tenures.index(invalidw)
        titles = titles[:e]
        companys = companys[:e]
        tenures = tenures[:e]
    sorted_idx, tenures = process_tenure(tenures, tenurepattern)
    start_tenures, end_tenures = zip(*tenures)
    titles = [titles[idx] for idx in sorted_idx]
    companys = [companys[idx] for idx in sorted_idx]
    for title, company, start_tenure, end_tenure in zip(titles, companys, start_tenures, end_tenures):
      df_values['uid'].append(uid + 1)
      df_values['title'].append(title)
      df_values['company'].append(company)
      df_values['start_tenure'].append(start_tenure)
      df_values['end_tenure'].append(end_tenure)

  dfcareer = pd.DataFrame(df_values)
  dfcareer.to_pickle('tmp/career_history_df.pkl')
