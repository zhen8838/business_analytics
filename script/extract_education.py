import os
import sys
sys.path.insert(0, os.getcwd())
import numpy as np
import pandas as pd
import re
from tools.cleanfucs import process_education


if __name__ == "__main__":
  person_info = pd.read_csv('tmp/person_info.csv')
  edu_pattern = re.compile(r'EDUCATION\|\|--')
  education: pd.Series = person_info.education.apply(lambda s: process_education(s, edu_pattern))

  df_values = {'uid': [], 'degree': [], 'institution': []}
  for uid, (degree, institution) in enumerate(education.values):
    for degree, institution in zip(degree, institution):
      df_values['uid'].append(uid + 1)
      df_values['degree'].append(degree)
      df_values['institution'].append(institution)

  dfeducation = pd.DataFrame(df_values)
  # dfcareer = dfcareer.set_index(['uid', 'title'])
  # dfcareer = dfcareer.reset_index(level=-1, drop=True)
  dfeducation.to_pickle('tmp/education_df.pkl')
