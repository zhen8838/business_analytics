import pandas as pd
import argparse
from pathlib import Path
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-file', type=str, default='tmp/career_history_df.pkl')
  args = parser.parse_args()
  file_path = Path(args.file)
  df: pd.DataFrame = pd.read_pickle(file_path.as_posix())
  df = df.reset_index(-1)
  #  预处理
  d = {
      'Chief Executive Officer': 'CEO',
      'Co-Chief Executive Officer': 'CEO',
      'Chief Financial Officer': 'CFO',
      'Chief Operating Officer': 'COO',
      'Chief Information Officer': 'CIO',
      'Chief Accounting Officer': 'CAO',
      'Chief Acctg Ofcr': 'CAO',
      'Chief Marketing Officer': 'CMO',
      'Chief Commercial Ofcr': 'CCO',
      'Chief Commercial Officer': 'CCO',
      'Vice President': 'VP',
      'Gen Cnsl': 'General Counsel',
      'Pres': 'President',
      'Gen Counsel': 'General Counsel',
  }
  s = []
  named_title_list = ['CEO', 'CFO', 'CTO', 'Chairman', 'President', 'Founder', 'VP', ]
  named_title = dict(zip(named_title_list, range(len(named_title_list))))

  titles = []
  for t in df['title']:
    title = [False] * len(named_title)
    if t:
      for c in t.split('/'):
        c = c.strip(' ').rstrip(' ')
        c.replace('Vice President', 'VP')
        c = d.get(c, c)
        for k, v in named_title.items():
          if k in c:
            title[v] = True
    titles.append(title)

  # pd.DataFrame(s).value_counts().to_csv('tmp/titles.csv')

  df[named_title_list] = titles
  df.to_pickle(path=(file_path.parent / (file_path.stem + '_norm_title.pkl')).as_posix())
