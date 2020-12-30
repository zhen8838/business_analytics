import os
import sys
sys.path.insert(0, os.getcwd())
import numpy as np
import pandas as pd
import re
from tools.cleanfucs import process_board_memberships


if __name__ == "__main__":
  person_info = pd.read_csv('tmp/person_info.csv')
  board_memberships: pd.Series = person_info.board_memberships.apply(process_board_memberships)

  df_values = {'uid': [], 'company': [], 'title': [], 'tenure': []}
  for uid, (company, title, tenure) in enumerate(board_memberships.values):
    for company, title, tenure in zip(company, title, tenure):
      df_values['uid'].append(uid)
      df_values['company'].append(company)
      df_values['title'].append(title)
      df_values['tenure'].append(tenure)

  dfboard = pd.DataFrame(df_values)
  # dfcareer = dfcareer.set_index(['uid', 'title'])
  # dfcareer = dfcareer.reset_index(level=-1, drop=True)
  dfboard.to_pickle('tmp/board_memberships_df.pkl')