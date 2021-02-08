import pandas as pd
import statsmodels.api as sm


def calc_ols(data_name='sample_CEO'):
  data = pd.read_pickle(f'tmp/{data_name}.pkl')
  data = data.dropna(axis=0, subset=['promote_time'])
  x = sm.add_constant(data.iloc[:, [12, 13, 14, 16, 17]])
  y = data.iloc[:, 15]
  model = sm.OLS(y, x)
  result = model.fit()
  summary = result.summary()
  param_tab = pd.DataFrame(summary.tables[0].data)
  stat_tab = pd.DataFrame(summary.tables[1].data)
  t = stat_tab[1:][3].tolist()

  def get_mdiff(keyw):
    return (data['promote_time'][data[keyw] ==
                                 1].mean() -
            data['promote_time'][data[keyw] == 0].mean())
  title = ['Doctor', 'Master', 'bachelor', 'work_before', 'top_sch']
  mean_diff = list(map(get_mdiff, title))
  mean_diff.insert(0, 0)
  title.insert(0, 'const')

  result = pd.DataFrame(list(zip(title, t, mean_diff)), columns=['title', 't', 'mean_diff']).set_index('title')

  print(data_name)
  print(param_tab[2][1], param_tab[3][1])
  print(result)
  print()
