import os
import sys
sys.path.insert(0, os.getcwd())
import numpy as np
import pandas as pd
import re
from tools.cleanfucs import process_board_memberships, process_tenure


if __name__ == "__main__":
  person_info = pd.read_csv('tmp/person_info.csv')
  board_memberships: pd.Series = person_info.board_memberships.apply(process_board_memberships)
  tenurepattern = re.compile('(\d+\/\d+\/\d{4})|(\d{1,2}\/\d{1,4})|(PRESENT)|(FORMER)|(UNKNOWN)')
  df_values = {'uid': [], 'company': [], 'title': [], 'tenure': []}
  for uid, (companys, titles, tenures) in enumerate(board_memberships.values):
    for invalidw in ['Board Member', 'institution', 'company', 'Publications', 'UNKNOWN FUTURE DATE', 'Awards']:
      if invalidw in tenures:
        e = tenures.index(invalidw)
        if e != 0:
          titles = titles[:e]
          companys = companys[:e]
          tenures = tenures[:e]
        else:
          titles = titles[e]
          companys = companys[e]
          tenures = [None]
    sorted_idx, tenures = process_tenure(tenures, tenurepattern)
    start_tenure, end_tenure = zip(*tenures)
    titles = [titles[idx] for idx in sorted_idx]
    companys = [companys[idx] for idx in sorted_idx]
    for company, title, tenure in zip(companys, titles, tenures):
      df_values['uid'].append(uid + 1)
      df_values['company'].append(company)
      df_values['title'].append(title)
      df_values['tenure'].append(tenure)

  dfboard = pd.DataFrame(df_values)
  dfboard.to_pickle('tmp/board_memberships_df.pkl')
